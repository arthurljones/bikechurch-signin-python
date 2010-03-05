import csvImport, db, ui

def DebugStuff():
	name = "ro"
	conn = db.SigninDBConnection()
	persons = conn.FindPersonsByPartialName(name)
	print("\nPeople matching {0}:".format(name))
	for person in persons:
		print("\t{0} ({1})".format(person.name, person.id))
	
	#Get all current lifetime members we know about
	#cursor.execute("SELECT CONCAT(persons.first_name, %s, persons.last_name), members.end_date \
	#			FROM persons JOIN members \
	#			ON persons.id = members.person_id \
	#			WHERE members.end_date IS NULL \
	#			ORDER BY persons.last_name;", (" ", ))

				 
db.CreateTablesFromScratch()
csvImport.ReadMembersFromCSV("members.csv", "succeeded.csv", "failed.csv")
DebugStuff()

