import MySQLdb
import csv
from datetime import date, timedelta

gDBLocation = "localhost"
gDBName = "signin_db"

gDBLimitedAccessUser = "signin"
gDBRLimitedAccessPass = "signin"

gDBFullAccessUser = "signin_creator"
gDBFullAccessPass = "signin_creator"

import MySQLdb

def EscapeString(string):
	string = string.replace("\'", "\\\'")
	string = string.replace("\"", "\\\"")
	string = string.replace("`", "\\`")
	return string

def CreateTables():
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
			INDEX(last_name, first_name) )
			CHARSET=utf8 ENGINE=InnoDB;""")
			
	cursor.execute("""CREATE TABLE members
			(	id INT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
				person_id INT UNSIGNED NOT NULL UNIQUE,
				start DATE NOT NULL,
				end DATE,
				street_address VARCHAR(128),
				email_address VARCHAR(64),
				phone_number VARCHAR(32),
				donation SMALLINT UNSIGNED,			
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
				notes CHAR(128),	
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
		print("Table \'{0}\':".format(table))
		
		cursor.execute(format("show columns from {0}".format(table)))
		for column in cursor.fetchall():
			width = 16 - len(column[0]) + len (str(column[1:]))
			print("  {0}:{1: >{2}}".format(column[0], str(column[1:]), width))
		print("")
	conn.commit()
	cursor.close()
	conn.close()

def ReadMembersFromCSV(filename):
	conn = MySQLdb.connect(
		host = gDBLocation,
		user = gDBLimitedAccessUser,
		passwd = gDBRLimitedAccessPass,
		db = gDBName)
		
	cursor = conn.cursor()
	
	reader = csv.reader(filename)
	for row in reader:
		start_date = row[0]
		last_name = EscapeString(row[1].strip())
		first_name = EscapeString(row[2].strip())
		address = EscapeString(row[3].strip())
		phone = EscapeString(row[4].strip())
		email = EscapeString(row[5].strip())
		type = row[6].lower().strip()
		money = row[7].strip()
		notes = EscapeString(row[8].strip())
		
		try:
			number_money = float(money)
			money = number_money
		except Exception:
			money = None
		
		year, month, day = start_date.split('/')
		start_date = date(int(year), int(month), int(day))
		
		life_names = ["life", "life!", "life!!!", "lifetime", "infinity", "forever", "death", "lifer", "eternal", "upgrade to lifetime--$50"]
		year_names = ["year", "yearly", "year!", "year upgrade", "a year", "1 year", "year , expires 9/1/2010", "youth membership"]
		month_names = ["month", "monthly", "mo", "m", "1 month", "month paid", "moth", "mothy", "monthy", "6month"]

		end_date = start_date
		if type in life_names or (isinstance(money, (float,)) and money >= 100.0):
			end_date = None
		elif type in year_names or (isinstance(money, (float,)) and money >= 50.0):
			end_date = start_date + timedelta(days = 365)
		elif type in month_names or (isinstance(money, (float,)) and money >= 20.0) or type == "" and money is None:
			end_date = start_date + timedelta(days = 31)
		else:
			print("{0}: {1} ({2})".format(type, money, notes))
			continue
			
		print("{0} -> {1}".format(start_date, end_date))
			
			
		#TODO: do some input validation here, and toss broken membership lines somwhere to be manually fixed
		cursor.execute("""INSERT INTO persons (first_name, last_name)
					VALUES (\'{0}\', \'{1}\');""".format(first_name, last_name))
		cursor.execute("SELECT LAST_INSERT_ID();")
		last_insert_id = cursor.fetchall()[0][0]
		#cursor.execute("""INSERT INTO members (person_id, start, end, street_address, email_address, phone_number, donation)
		#			VALUES (%s, \'%s\', \'%s\');""".format(first_name, last_name))

	cursor.execute("SELECT first_name, last_name FROM persons")
	#for person in cursor.fetchall():
		#print person

CreateTables()
ReadMembersFromCSV(open("members.csv", "r"))
