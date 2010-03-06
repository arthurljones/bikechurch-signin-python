import csvImport, db, ui
from copy import copy

def DebugStuff():	
	name = "jac"
	conn = db.SigninDBConnection()
	persons = conn.FindPersonsByPartialName(name)
	print("\nPeople matching {0}:".format(name))
	for person in persons:
		print("\t{0} ({1})".format(person.name, person.id))
	
	#Get all current lifetime members we know about
	conn.cursor.execute("SELECT members.endDate \
				FROM persons JOIN members \
				ON persons.id = members.personId \
				WHERE members.endDate IS NULL;")
				
	print("{0} lifetime members".format(conn.cursor.rowcount))
				 
db.CreateTablesFromScratch()
csvImport.ReadMembersFromCSV("members.csv", "succeeded.csv", "failed.csv")
DebugStuff()
