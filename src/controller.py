 # -*- coding: utf-8 -*-
 
import db, wx, MySQLdb, os, csv
from strings import trans
from datetime import datetime, timedelta
from sqlalchemy import func, or_, and_
from sqlalchemy.exc import IntegrityError, OperationalError, InvalidRequestError
from db import Person, Member, Shoptime, ShopOccupant, Bike, Feedback
from ui import GetShoptimeTypeDescription, FormatTimedelta
from difflib import SequenceMatcher

_controller = None

def PrintShortStack(start = 0, limit = None, prefix = ""):
	import traceback
	trace = traceback.extract_stack()
	end = -start - 1
	start = 0
	if limit is not None:
		start = end - limit
	
	for line in trace[start : end]:
		filename = line[0]
		lineNumber = line[1]
		function = line[2]
		text = line[3]
		
		file = os.path.sep.join(filename.split(os.path.sep)[-2:])
		
		print("{4}{0}({1}) in {2}:\n{4}\t\"{3}\"".format(
			file, lineNumber, function, text, prefix))

def HandleDBAPIError(error):
	print("***Error on commit ({0}): {1}".format(error.orig[0], error.orig[1]))
	print("\tStatement: {0}".format(error.statement))
	print("\tParams: {0}".format(error.params))
	print("\tStacktrace follows:")	
	PrintShortStack(limit = 4, start = 2, prefix = "\t")
	
	if error.connection_invalidated:
		print("\tConnection to database invalidate - reconnecting")
		db.Connect()
	else:
		db.session.rollback()
		
	print("")
	
def HandleSQLAlchemyError(error):
	print("*** Error on commit: {0}".format("; ".join(error.args)))
	print("\tStacktrace follows:")	
	PrintShortStack(limit = 4, start = 2, prefix = "\t")
	print("")
	
	db.session.rollback()

def FuzzyStringSearch(searchString,
					sequence,
					key = lambda x : x,
					sanitizer = lambda x: x.lower().replace('0', 'o'),
					resultCount = 10,
					isJunk = None):

	matcher = SequenceMatcher(isJunk)
	matcher.set_seq2(sanitizer(searchString))
	
	matches = []
	
	for item in sequence:
		matcher.set_seq1(sanitizer(key(item)))
		if matcher.quick_ratio() >= 0.5:
			ratio = matcher.ratio()
			if (ratio >= 0.5):
				matches.append((item, ratio))
				
	matches.sort(key = lambda x: -x[1])
	return matches[:resultCount]


class Controller:
	def __init__(self):
		self._lastPersonCreated = None
		self._signoutTimeout = 5 #hours
		self._ui = None
		self.PeriodicUpdate(None)
		#results = FuzzyStringSearch(searchString = "DM039",
		#						sequence = db.session.query(Bike).all(),
		#						key = lambda bike: bike.serial)
		
		#results = FuzzyStringSearch(searchString = "Jimmy James",
		#							sequence = db.session.query(Person).all(),
		#							key = lambda x: "{0} {1}".format(x.firstName, x.lastName),
		#							isJunk = lambda x: x in " \t")
		
		#for item in results:
		#	print item
		
	def SetUI(self, ui):
		self._ui = ui
		
	def Commit(self):
		try:
			db.session.commit()
		except (IntegrityError, OperationalError), error:					
			HandleDBAPIError(error)
			
		except (InvalidRequestError), error:
			HandleSQLAlchemyError(error)
			
		else:
			return True
			
		return False
					
	def Rollback(self):
		db.session.rollback()

	def GetPersonByFullName(self, firstName, lastName):
		return db.session.query(Person) \
			.filter(Person.firstName == firstName) \
			.filter(Person.lastName == lastName).first()

	def GetPersonByID(self, personID):
		return db.session.query(Person) \
			.filter(Person.id == personID).first()
		
	def GetCurrentMembers(self):
		return db.session.query(Person) \
			.join(Member) \
			.filter(or_(
				Member.endDate >= func.current_timestamp(),
				Member.endDate == None)).all()
	
	def WriteCurrentMemberEmails(self, filename):
		output = csv.writer(open(filename, "wb"))
		for person in self.GetCurrentMembers():
			if  person.memberInfo.emailAddress:
				output.writerow((person.firstName, person.lastName,
					person.memberInfo.emailAddress,	person.memberInfo.endDate))
		
		
	def FindPeopleByPartialName(self, partialName):
		partialName = ' '.join(partialName.split()) #strip out extra spaces
		namelen = len(partialName)
		return db.session.query(Person).filter(
			or_(
				or_(
					func.left(Person.firstName, namelen) == partialName,
					func.left(Person.lastName, namelen) == partialName,
				),
				func.left(Person.firstName + u" " + Person.lastName, namelen) == partialName
			)
		).all()
	
		
	def GetPeopleInShop(self):
		return db.session.query(Person) \
			.join(ShopOccupant) \
			.filter(ShopOccupant.personID == Person.id) \
			.order_by(ShopOccupant.start).all()

	def FindPeopleBySerialNumber(self, serial):
		return db.session.query(Person) \
			.join(Bike) \
			.filter(and_( \
				Bike.personID == Person.id, \
				func.instr(Bike.serial, serial) > 0)).all()

	def AuthenticateMechanic(self, parent, activity):
		if self._ui is not None:
			return self._ui.AuthenticateMechanic(parent, activity)

	def ShowNewPersonDialog(self, parent, firstName = u"", lastName = u""):
		if self._ui is not None:
			return self._ui.ShowNewPersonDialog(parent, firstName, lastName)
		else:
			return None

	def SignPersonIn(self, person, type):
		if person is None:
			person = self._lastPersonCreated
			
		if self._ui is not None and person.occupantInfo is not None:
			if person.occupantInfo.type == type:
				widget = self._ui.GetOccupantNameWidget(person)
				error = trans.sigininAlreadySignedIn
				typeDesc = GetShoptimeTypeDescription(type)
				self._ui.FlashError(
					error.format(person.Name(), typeDesc), [widget])
				return
			else:
				self.SignPersonOut(person)
		
		occupant = ShopOccupant()
		occupant.personID = person.id
		occupant.start = datetime.now()
		occupant.type = type
		person.occupantInfo = occupant
		
		if self.Commit():
			if self._ui is not None:
				self._ui.AddOccupant(person, datetime.now(), type)
			return occupant
		else:
			return None

	def SignPersonOut(self, person):
		if person.occupantInfo:
			shoptime = Shoptime()
			shoptime.start = person.occupantInfo.start
			if datetime.now() - shoptime.start > timedelta(hours = self._signoutTimeout):
				shoptime.end = None
			else:
				shoptime.end = datetime.now()
			shoptime.type = person.occupantInfo.type
			shoptime.notes = u""
		
			person.shoptimes.append(shoptime)
			db.session.delete(person.occupantInfo)
			
			self.Commit()
		else:
			raise RuntimeError("Trying to sign {0} out, "\
				"but they aren't in the occupants table.".format(person))
		
		if self._ui is not None:		
			self._ui.RemoveOccupant(person)
			
	def CreatePerson(self, person):
		db.session.add(person)
		if self.Commit():
			self._lastPersonCreated = person
			return person
		else:
			return None
		
	def CreateBike(self, bike, person = None):
		if person:
			person.bikes.append(bike)
		else:
			bike.personID = None
			db.session.add(bike)
			
		if self.Commit():
			return bike
		else:
			return None
			
	def AddFeedback(self, feedback):
		db.session.add(feedback)
		if self.Commit():
			return feedback
		else:
			return None
			
	def GetFeedback(self):
		return db.session.query(Feedback).all()
		
	def GetLastPersonCreated(self):
		return self._lastPersonCreated
		
	def FlashError(self, *argv, **argd):
		if self._ui is not None:
			self._ui.FlashError(*argv, **argd)
		
	def StopFlashing(self):
		if self._ui is not None:
			self._ui.ResetError()
		
	def ViewPersonInfo(self, parent, person):
		if self.AuthenticateMechanic(parent, trans.authenticateView.format(person.Name())):
			if self._ui is not None:
				self._ui.ShowViewPersonDialog(parent, person)
			
	def PeriodicUpdate(self, event):
		people = self.GetPeopleInShop()
		timeout = 8
		for person in people:
			if datetime.now() - person.occupantInfo.start > timedelta(hours = self._signoutTimeout):
				print("{0} has been signed in for more than {1} hours and has been removed." \
					.format(person.Name(), self._signoutTimeout))
				self.SignPersonOut(person)
			
	def DebugSignRandomPeopleIn(self, howmany):
		for person in self.GetPeopleInShop():
			self.SignPersonOut(person)
		
		people = db.session.query(Person) \
			.order_by(func.rand()) \
			.limit(howmany).all()
			
		for person in people:
			self.SignPersonIn(person, "shoptime")
			
	def FixLongShoptimes(self):
		shoptimes = db.session.query(Shoptime).all()
		
		maxTime = timedelta(hours = self._signoutTimeout)
		for shoptime in shoptimes:
			if shoptime.end is not None:
				duration = shoptime.end - shoptime.start
				if duration > maxTime:
					shoptime.end = None
					print("{0}: {1} of {2} marked indefinite.".format(
						shoptime.person.Name(),
						FormatTimedelta(duration),
						shoptime.type))

		self.Commit()

def GetController():
	global _controller
	if not _controller:
		_controller = Controller()
		
	return _controller
	
def ResetController():
	global _controller
	_controller = Controller()
	return _controller
