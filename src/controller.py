import db
import MySQLdb
from datetime import datetime
from math import ceil

def PrintableName(name):
	return "{0} {1}".format(name[0], name[1])

class Controller:
	def __init__(self, dbConnection):
		self.connection = dbConnection
		
	def SetUI(self, ui):
		self.ui = ui

	def GetPersonByFullName(self, firstName, lastName):
		return self.connection.SimpleQuery(
			"people", "firstName = %s AND lastName = %s", "", (firstName, lastName), False)

	def GetPersonNameByID(self, personID):
		name = self.connection.ComplexQuery(
			fields = ("firstName", "lastName"),
			tables = ("people",),
			where = "id = %s",
			args = (personID, ))
		
		if len(name) == 0:
			return None
		else:
			return (name[0]["firstName"], name[0]["lastName"])

	def GetMemberByPersonID(self, personID):
		return self.connection.SimpleQuery(
			"members", "personID = %s", "", (personID,), False)
		
	def FindPeopleByPartialName(self, partialName):
		return self.connection.SimpleQuery("people",
			where = "LEFT(people.firstName, %s) = %s \
				OR LEFT(people.lastName, %s) = %s \
				OR LEFT(CONCAT(people.firstname, \" \", people.lastname), %s) = %s",
			order = "people.firstName",
			args = (len(partialName), partialName) * 3)
		
	def GetPeopleInShop(self):	
		return self.connection.ComplexQuery(
			fields = ("personID", "start", "type"),
			tables = ("peopleInShop",),
			order = "start")	
			
	def GetPersonInShopByPersonID(self, personID):
		person = self.connection.ComplexQuery(
			fields = ("personID", "start", "type"),
			tables = ("peopleInShop",),
			where = "personID = %s",
			args = (personID, ),
			order = "start")
			
		if len(person) == 0:
			return None
		else:
			return person[0]

	def ShowNewPersonScreen(self, personName, type):
		self.ui.ShowAddPersonScreen()
		
		nameWords = personName.split()
		numWords = len(nameWords)
		halfWords = int(ceil(numWords / 2.0))
		firstName = " ".join(nameWords[:halfWords])
		lastName = " ".join(nameWords[halfWords:])
			
		self.ui.SetPersonName(firstName, lastName)

	def SignPersonIn(self, personID, type):
		person = self.GetPersonInShopByPersonID(personID)
		if person is not None:
			if person["type"] == type:
				#TODO: Flash existing entry in people list
				print("{0} is already signed in to do {1}".format(
					PrintableName(self.GetPersonNameByID(personID)), type))
				return
			else:
				self.SignPersonOut(personID)
		
		new = self.connection.EmptyRow("peopleInShop")
		new["personID"] = personID
		new["start"] = datetime.now()
		new["type"] = type
		self.connection.Insert(new)
		self.connection.Commit()
		#TODO: Flash new entry in people list
		self.ui.AddOccupant(personID, datetime.now(), type)
		self.ui.ResetSignin()

	def SignPersonOut(self, personID):	
		persons = self.connection.ComplexQuery(
			fields = ("people.id", "peopleInShop.id", "peopleInShop.start", "peopleInShop.type"),
			tables = ("peopleInShop", "people"),
			join = "INNER JOIN",
			on = "people.id = peopleInShop.personID",
			where = "people.id = %s",
			order = "peopleInShop.start",
			args = (personID,),
			stripPrefixes = False)
		
		if len(persons) > 0:
			person = persons[0]
			
			hours = self.connection.EmptyRow("hours")
			hours["personID"] = person["people.id"]
			hours["start"] = person["peopleInShop.start"]
			hours["duration"] = datetime.now() - hours["start"]
			hours["type"] = person["peopleInShop.type"]
			hours["notes"] = ""
			self.connection.Insert(hours)
			
			self.connection.cursor.execute(
				"DELETE FROM peopleInShop WHERE id = %s", (person["peopleInShop.id"]))
			self.connection.Commit()
				
		self.ui.RemoveOccupant(personID)
			
		
