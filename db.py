import MySQLdb, sys
from datetime import date, timedelta

def CreateTablesFromScratch():
	print("Creating database tables from scratch...")
	sys.stdout.flush()
	
	conn = MySQLdb.connect(
		host = "localhost",
		user = "signin_creator",
		passwd = "signin_creator",
		db = "signin_db")
		
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

	conn.commit()
	cursor.close()
	conn.close()
	
	print("\tSuccess")

class SigninDBConnection:
	def __init__(self):
		self.connection = MySQLdb.connect(
			host = "localhost", user = "signin", passwd = "signin", db = "signin_db")
		self.cursor = self.connection.cursor()		

	def __del__(self):
		self.cursor.close()
		self.connection.close()
	
	def Commit(self):
		self.connection.commit()
		
	def Rollback(self):
		self.connection.rollback()

	def FormatDate(self, date):
		if date is None: return None
		else: return MySQLdb.Date(date.year, date.month, date.day)

	def GetLastInsertID(self):
		self.cursor.execute("SELECT LAST_INSERT_ID();")
		return int(self.cursor.fetchone()[0])

	def FindPersonIDByFullName(self, firstName, lastName):
		self.cursor.execute("SELECT id FROM persons WHERE first_name = %s AND last_name = %s;",
			(firstName, lastName))
		if self.cursor.rowcount == 0:
			return None
		else:
			return int(self.cursor.fetchone()[0])

	def PersonIsAMember(self, personID):
		self.cursor.execute("SELECT id FROM members WHERE person_id = %s;", (personID,))
		return self.cursor.rowcount > 0

	def CreatePerson(self, firstName, lastName):
		self.cursor.execute("INSERT INTO persons (first_name, last_name) VALUES (%s, %s);", (firstName, lastName))
		return self.GetLastInsertID();
		
	def CreateMember(self, personID, startDate, endDate, streetAddress, emailAddress, phoneNumber, donation, notes):
		startDate = self.FormatDate(startDate)
		endDate = self.FormatDate(endDate)
		self.cursor.execute("INSERT INTO members \
					(person_id, start_date, end_date, street_address, email_address, phone_number, donation, notes) \
					VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
					(personID, startDate, endDate, streetAddress, emailAddress, phoneNumber, donation, notes))
		return self.GetLastInsertID();
		
	def FindPersonsByPartialName(self, partialName):
		partialLen = len(partialName)
		self.cursor.execute("SELECT CONCAT(persons.first_name, \" \", persons.last_name), persons.id \
				FROM persons \
				WHERE LEFT(persons.first_name, %s) = %s or LEFT(persons.last_name, %s) = %s\
				ORDER BY persons.first_name;",
				(partialLen, partialName, partialLen, partialName))
				
		class NameResult:
			def __init__(self, name, id):
				self.name = name
				self.id = id

		return (NameResult(row[0], row[1]) for row in self.cursor.fetchall())
