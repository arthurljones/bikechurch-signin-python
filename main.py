import MySQLdb
import csv

gDBLocation = "localhost"
gDBName = "signin_db"

gDBLimitedAccessUser = "signin"
gDBRLimitedAccessPass = "signin"

gDBFullAccessUser = "signin_creator"
gDBFullAccessPass = "signin_creator"

import MySQLdb

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
				street_address VARCHAR(128),
				email_address VARCHAR(64),
				phone_number VARCHAR(32),			
			PRIMARY KEY(id),
			INDEX(last_name, first_name) )
			CHARSET=utf8 ENGINE=InnoDB;""")
			
	cursor.execute("""CREATE TABLE members
			(	id INT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
				person_id INT UNSIGNED NOT NULL UNIQUE,
				start DATE NOT NULL,
				end DATE NOT NULL,
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
	reader = csv.Reader(filename)
	

CreateTables()
