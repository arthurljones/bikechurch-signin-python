 # -*- coding: utf-8 -*-
 
import db, wx, MySQLdb, os
from datetime import datetime
from sqlalchemy import func, or_
from sqlalchemy.exc import IntegrityError, OperationalError, InvalidRequestError
from db import Person, Member, Shoptime, ShopOccupant, Bike

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
		
		print("{4}{0}({1}) in {2}: \"{3}\"".format(file, lineNumber, function, text, prefix))

def PrintDBAPIError(error):
	print("Error on commit ({0}): {1}".format(error.orig[0], error.orig[1]))
	print("\tStatement: {0}".format(error.statement))
	print("\tParams: {0}".format(error.params))
	print("\tStacktrace follows:")	
	PrintShortStack(limit = 4, start = 2)
	
	print("")
	
def PrintSQLAlchemyError(error):
	print("Error on commit ({0}): {1}".format(error.message, error.args))
	print("\tStacktrace follows:")	
	PrintShortStack(limit = 4, start = 2)
	
	print("")	

class Controller:
	def __init__(self):
		self._lastPersonCreated = None
		
	def SetUI(self, ui):
		self._ui = ui
		
	def Commit(self):
		try:
			db.session.commit()
		except (IntegrityError, OperationalError), error:					
			PrintDBAPIError(error)
			
		except (InvalidRequestError), error:
			PrintSQLAlchemyError(error)
			
		else:
			return True
			
		if error.connection_invalidated:
			print("\tConnection to database invalidate - reconnecting")
			db.Connect()
		else:
			db.session.rollback()

			
	def Rollback(self):
		db.session.rollback()

	def GetPersonByFullName(self, firstName, lastName):
		return db.session.query(Person) \
			.filter(Person.firstName == firstName) \
			.filter(Person.lastName == lastName).first()

	def GetPersonByID(self, personID):
		return db.session.query(Person) \
			.filter(Person.id == personID).first()
		
	def FindPeopleByPartialName(self, partialName):
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

	def AuthenticateMechanic(self, activity):
		return self._ui.AuthenticateMechanic(activity)

	def ShowNewPersonDialog(self, firstName = u"", lastName = u""):
		return self._ui.ShowNewPersonDialog(firstName, lastName)

	def SignPersonIn(self, person, type):
		if person is None:
			person = self._lastPersonCreated
			
		if person.occupantInfo is not None:
			if person.occupantInfo.type == type:
				self._ui.FlashError(
					"{0} is already signed in to do {1}".format(
					person.Name(), type))
				return
			else:
				self.SignPersonOut(person)
		
		occupant = ShopOccupant()
		occupant.personID = person.id
		occupant.start = datetime.now()
		occupant.type = type
		person.occupantInfo = occupant
		
		if self.Commit():
			self._ui.AddOccupant(person, datetime.now(), type)
			return occupant
		else:
			return None

	def SignPersonOut(self, person):		
		if person.occupantInfo:
			shoptime = Shoptime()
			shoptime.personID = person.id
			shoptime.start = person.occupantInfo.start
			shoptime.end = datetime.now()
			shoptime.type = person.occupantInfo.type
			shoptime.notes = u""
			
			person.shoptimes.append(shoptime)
			db.session.delete(person.occupantInfo)
			
			self.Commit()
		else:
			raise RuntimeError("Trying to sign {0} out, "\
				"but they aren't in the occupants table.".format(person))
				
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
			bike.personID = person.id
		else:
			bike.personID = None
		db.session.add(bike)
		if self.Commit():
			return bike
		else:
			return None
		
	def GetLastPersonCreated(self):
		return self._lastPersonCreateds	
		
	def FlashError(self, *argv, **argd):
		self._ui.FlashError(*argv, **argd)
		
	def StopFlashing(self):
		self._ui.ResetError()
		
	def ViewPersonInfo(self, person):
		if 1: #self.AuthenticateMechanic("view info for {0}".format(person.Name())):
			self._ui.ShowViewPersonDialog(person)

def GetController(): 
	global _controller
	if not _controller:
		_controller = Controller()
		
	return _controller
	
def ResetController():
	global _controller
	_controller = Controller()
	return _controller
