import db
from datetime import datetime

class Controller:
	def __init__(self, dbConnection):
		self.connection = dbConnection
		
		self.connection.cursor.execute("select * from hours;")
		for line in self.connection.cursor.fetchall():
			print line
		
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
			fields = ("peopleInShop.personID", "peopleInShop.start", "peopleInShop.type"),
			tables = ("peopleInShop",),
			order = "peopleInShop.start")	

	def ShowNewPersonScreen(self, personName, type):
		pass

	def SignPersonIn(self, personID, type):
		new = self.connection.EmptyRow("peopleInShop")
		new["personID"] = personID
		new["start"] = datetime.now()
		new["type"] = type
		self.connection.Insert(new)
		self.connection.Commit()
		
		self.ui.AddPersonToShopList(personID, datetime.now(), type)
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
			print hours["type"]
			
			self.connection.cursor.execute(
				"DELETE FROM peopleInShop WHERE id = %s", (person["peopleInShop.id"]))
			self.connection.Commit()
				
		self.ui.RemovePersonFromShopList(personID)
			
		
