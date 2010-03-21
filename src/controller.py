 # -*- coding: utf-8 -*-
 
import db, wx, MySQLdb
from datetime import datetime
from math import ceil

def PrintableName(name):
	return "{0} {1}".format(name[0], name[1])

class Controller:
	def __init__(self, dbConnection):
		self.connection = dbConnection
		self.lastPersonCreated = None
		
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

	def AuthenticateMechanic(self, activity):
		return self.ui.AuthenticateMechanic(activity)

	def ShowNewPersonDialog(self, personName, type):
		nameWords = personName.split()
		numWords = len(nameWords)
		halfWords = int(ceil(numWords / 2.0))
		firstName = " ".join(nameWords[:halfWords])
		lastName = " ".join(nameWords[halfWords:])
		
		print "Showing new person dialog"
		if self.ui.ShowNewPersonDialog(firstName, lastName):
			print "Signing person in"
			self.SignPersonIn(self.lastPersonCreated, type)

	def SignPersonIn(self, personID, type):
		person = self.GetPersonInShopByPersonID(personID)
		if person is not None:
			if person["type"] == type:
				self.ui.FlashError(
					"{0} is already signed in to do {1}".format(
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
			
	def CreatePerson(self, name):
		person = self.connection.EmptyRow("people")
		person["firstName"] = name.firstName
		person["lastName"] = name.lastName
		self.connection.Insert(person)
		self.lastPersonCreated = person["id"]
		return person["id"]
		
	def CreateBike(self, bikeDesc, personID = None):
		bike = self.connection.EmptyRow("bikes")
		bike["color"] = bikeDesc.color
		bike["type"] = bikeDesc.type
		bike["brand"] = bikeDesc.brand
		bike["model"] = bikeDesc.model
		bike["serial"] = bikeDesc.serial
		bike["personID"] = personID
		self.connection.Insert(bike)
		return bike["id"]
		
	def FlashError(self, *argv, **argd):
		self.ui.FlashError(*argv, **argd)
		
	def StopFlashing(self):
		self.ui.ResetError()
		
	def ViewPersonInfo(self, personID):
		personName = PrintableName(self.GetPersonNameByID(personID))
		if self.AuthenticateMechanic("view info for {0}".format(personName)):
			#TODO: Show view person screen here
			print "TODO: View person not implemented yet."

