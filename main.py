import MySQLdb, csv, sys
from datetime import date, timedelta

gDBLocation = "localhost"
gDBName = "signin_db"

gDBLimitedAccessUser = "signin"
gDBRLimitedAccessPass = "signin"

gDBFullAccessUser = "signin_creator"
gDBFullAccessPass = "signin_creator"

import MySQLdb

def DBCreateTables():
	print("Creating database tables...")
	sys.stdout.flush()
	
	conn = MySQLdb.connect(
		host = gDBLocation,
		user = gDBFullAccessUser,
		passwd = gDBFullAccessPass,
		db = gDBName)
		
	cursor = conn.cursor()
	cursor.execute("""drop table if exists bikes, hours, members, persons;""")
	
	cursor.execute("""CREATE TABLE persons
			(	id INT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
				first_name VARCHAR(64) NOT NULL,
				last_name VARCHAR(64),			
			PRIMARY KEY(id),
			UNIQUE INDEX(first_name, last_name),
			INDEX(last_name) )
			CHARSET=utf8 ENGINE=InnoDB;""")
			
	cursor.execute("""CREATE TABLE members
			(	id INT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
				person_id INT UNSIGNED NOT NULL UNIQUE,
				start_date DATE NOT NULL,
				end_date DATE,
				street_address VARCHAR(128),
				email_address VARCHAR(64),
				phone_number VARCHAR(32),
				donation SMALLINT UNSIGNED,
				notes VARCHAR(200),	
			PRIMARY KEY(id),
			INDEX(person_id),
			FOREIGN KEY(person_id) REFERENCES persons(id)
				ON DELETE NO ACTION 
				ON UPDATE CASCADE )
			CHARSET=utf8 ENGINE=InnoDB;""")
						
	cursor.execute("""CREATE TABLE hours
			(	id INT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
				person_id INT UNSIGNED NOT NULL UNIQUE,
				start_date DATE NOT NULL,
				start_time TIME,
				duration TIME NOT NULL,
				type ENUM(
					'shoptime',
					'worktrade',
					'volunteer',
					'mechanic',
					'accounting',
					'extra_shift',
					'facilities',
					'outreach',
					'ordering',
					'tools',
					'other'),
				notes VARCHAR(200),	
			PRIMARY KEY(id),
			INDEX(person_id),
			INDEX(type),
			FOREIGN KEY(person_id) REFERENCES persons(id)
				ON DELETE NO ACTION
				ON UPDATE CASCADE )
			CHARSET=utf8 ENGINE=InnoDB;""")
			
	cursor.execute("""CREATE TABLE bikes
			(	id INT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
				person_id INT UNSIGNED NOT NULL UNIQUE,
				color VARCHAR(64) NOT NULL,
				brand VARCHAR(64),
				model VARCHAR(64),
				serial VARCHAR(64),
			PRIMARY KEY(id),
			INDEX(person_id),
			INDEX(serial(10)),
			FOREIGN KEY(person_id) REFERENCES persons(id)
				ON DELETE NO ACTION
				ON UPDATE CASCADE )
			CHARSET=utf8 ENGINE=InnoDB;""")
			
	cursor.execute("""show tables""")
	raw_tables = cursor.fetchall()
	tables = (table[0] for table in raw_tables)
	for table in tables:
		#Disabled for now
		continue
		
		print("Table \'{0}\':".format(table))
		
		cursor.execute(format("show columns from {0}".format(table)))
		for column in cursor.fetchall():
			width = 16 - len(column[0]) + len (str(column[1:]))
			print("  {0}:{1: >{2}}".format(column[0], str(column[1:]), width))
		print("")
	conn.commit()
	cursor.close()
	conn.close()
	
	print("\tSuccess")

def ParseCSVDate(rawDate):
	try:
		month, day, year = rawDate.split('/')
		return date(int(year) + 2000, int(month), int(day))
	except Exception:
		print("Bad date format")
		return None

def ParseCSVMembershipTypeDurationAndDonation(rawType, rawMoney):
	rawMoney = rawMoney.strip().lower()
	rawMoney = rawMoney.replace("$", "")
	memberType = rawType.strip().lower()
	
	money = None
	if rawMoney == '': rawMoney = "20"
		
	try: money = float(rawMoney)
	except Exception:
		print("Couldn't convert money to float")
		return (None, None, None)
		
	lifeTypes = ["life", "life!", "life!!!", "lifetime", "infinity", "forever", "death", "lifer", "eternal"]
	yearTypes = ["year", "yearly", "year!", "year upgrade", "a year", "1 year"]
	monthTypes = ["month", "monthly", "mo", "m", "1 month", "month paid", "moth", "mothy", "monthy"]

	if memberType in lifeTypes or money >= 100.0:
		return ("life", None, money)
	elif memberType in yearTypes or money >= 50.0:
		return ("year", timedelta(days = 365), money)
	elif memberType in monthTypes or money >= 20.0:
		return ("month", timedelta(days = 31), money)
	else:
		print("Couldn't deduce member type: {0}, {1}".format(memberType, money))
		return (None, None, None)

def MySQLDate(date):
	return MySQLdb.Date(date.year, date.month, date.day)

def DBGetLastInsertID(cursor):
	cursor.execute("SELECT LAST_INSERT_ID();")
	return int(cursor.fetchone()[0])

def DBFindPersonIDByFullName(cursor, firstName, lastName):
	cursor.execute("SELECT id FROM persons WHERE first_name = %s AND last_name = %s;", (firstName, lastName))
	existingPerson = cursor.fetchall()
	if len(existingPerson) == 0:
		return None
	else:
		return int(existingPerson[0][0])

def DBPersonIsAMember(cursor, personID):
	cursor.execute("SELECT id FROM members WHERE person_id = %s;", (personID,))
	member = cursor.fetchone()
	if member is None:
		return False
	else:
		return True

def DBCreatePerson(cursor, firstName, lastName):
	cursor.execute("INSERT INTO persons (first_name, last_name) VALUES (%s, %s);", (firstName, lastName))
	return DBGetLastInsertID(cursor);
	
def DBCreateMember(cursor, personID, startDate, endDate, streetAddress, emailAddress, phoneNumber, donation, notes):	
	cursor.execute("INSERT INTO members \
				(person_id, start_date, end_date, street_address, email_address, phone_number, donation, notes) \
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
				(personID, startDate, endDate, streetAddress, emailAddress, phoneNumber, donation, notes))
	return DBGetLastInsertID(cursor);

def ReadMembersFromCSV(filename, succeededFilename, failedFilename):
	conn = MySQLdb.connect(
		host = gDBLocation,
		user = gDBLimitedAccessUser,
		passwd = gDBRLimitedAccessPass,
		db = gDBName)
		
	cursor = conn.cursor()
	
	reader = csv.reader(open(filename, "rb"))
	succeeded = csv.writer(open(succeededFilename, "wb"))
	failed = csv.writer(open(failedFilename, "wb"))
	
	numFailed = 0
	numSucceeded = 0
	
	print("Loading existing membership data...")
	sys.stdout.flush()
	
	for row in reader:
		
		startDate = ParseCSVDate(row[0])
		type, duration, money = ParseCSVMembershipTypeDurationAndDonation(row[6], row[7])
		if startDate is None or type is None:
			failed.writerow(row)
			numFailed += 1
			continue
			
		#TODO: do some input validation here, and toss broken membership lines somwhere to be manually fixed
		lastName = EscapeString(row[1].strip())
		firstName = EscapeString(row[2].strip())
		
		personID = DBFindPersonIDByFullName(cursor, firstName, lastName)
		if personID is None:
			personID = DBCreatePerson(cursor, firstName, lastName)

		if DBPersonIsAMember(cursor, personID):
			#update member
			pass
		else:
			address = EscapeString(row[3].strip())
			phone = EscapeString(row[4].strip())
			email = EscapeString(row[5].strip())
			notes = EscapeString(row[8].strip())
			endDate = None
			if duration != None:
				endDate = MySQLDate(startDate + duration)
			startDate = MySQLDate(startDate)
			
			DBCreateMember(cursor, personID, startDate, endDate,
					address, email, phone, money, notes)	
					
		succeeded.writerow(row)
		numSucceeded += 1

	cursor.execute("SELECT first_name, last_name FROM persons")
	#for person in cursor.fetchall():
		#print person
		
	conn.commit()
	
	print("\t{0} rows successfuly parsed, {1} rows failed to parse".format(numSucceeded, numFailed))

def DBFindPersonsByPartialName(cursor, partialName):
	partialLen = len(partialName)
	cursor.execute("SELECT CONCAT(persons.first_name, \" \", persons.last_name), persons.id \
			FROM persons \
			WHERE LEFT(persons.first_name, %s) = %s or LEFT(persons.last_name, %s) = %s\
			ORDER BY persons.first_name;",
			(partialLen, partialName, partialLen, partialName))
	class NameResult:
		def __init__(self, name, id):
			self.name = name
			self.id = id

	return (NameResult(row[0], row[1]) for row in cursor.fetchall())

def DebugStuff():
	conn = MySQLdb.connect(
		host = gDBLocation,
		user = gDBLimitedAccessUser,
		passwd = gDBRLimitedAccessPass,
		db = gDBName)
		
	cursor = conn.cursor()
	
	persons = DBFindPersonsByPartialName(cursor, "ry")
	for person in persons:
		print("{0} ({1})".format(person.name, person.id))
	
	#Get all current lifetime members we know about
	#cursor.execute("SELECT CONCAT(persons.first_name, %s, persons.last_name), members.end_date \
	#			FROM persons JOIN members \
	#			ON persons.id = members.person_id \
	#			WHERE members.end_date IS NULL \
	#			ORDER BY persons.last_name;", (" ", ))
				 

#ReadMembersFromCSV("members.csv", "succeeded.csv", "failed.csv")
#DBCreateTables()
DebugStuff()

