
#MySQLdb uses ImmutableSet, which is deprecated, so python complains by default
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)
    import MySQLdb

import sys, re
from datetime import date, timedelta

def SearchAndExtract(regex, string, group = 0):
	result = regex.search(string, re.IGNORECASE)
	if result is None:
		return (string, None)
	else:
		newString = string[:result.start()] + string[result.end():]
		string = newString
		return (newString, result.group(group))

class ColumnDef:
	reUnsigned = re.compile("\s*unsigned\s*")
	reZerofill = re.compile("\s*zerofill\s*")
	reParens = re.compile("\s*\((.*)\)\s*")
	reCharset = re.compile("\s*character set (\w+)\s*")
	reCollation = re.compile("\s*collation (\w+)\s*")
	
	def __init__(self, row):
		
		self.name = row[0]
		typeLine = row[1].lower()
		
		typeLine, self.unsigned  = SearchAndExtract(ColumnDef.reUnsigned, typeLine)
		typeLine, self.zerofill  = SearchAndExtract(ColumnDef.reZerofill, typeLine)
		typeLine, parensPart     = SearchAndExtract(ColumnDef.reParens, typeLine, 1)
		typeLine, self.charset   = SearchAndExtract(ColumnDef.reCharset, typeLine, 1)
		typeLine, self.collation = SearchAndExtract(ColumnDef.reCollation, typeLine, 1)
		
		self.type = typeLine
		
		self.unsigned = self.unsigned is None
		self.zerofill = self.zerofill is None
		
		self.enumValues = None
		self.precision = None
		self.length = None
		
		if parensPart is not None:
			if self.type == "enum" or self.type == "set":
				self.enumValues = [word.strip() for word in parensPart.split(",")]
			elif self.type == "float" or self.type == "double":
				values = parensPart.split(",")
				self.length = int(values[0])
				self.precision = int(values[1])
			else:
				self.length = int(parensPart)
			
		self.nullAllowed = row[2]
		self.key = row[3]
		self.default = row[4]
		self.extra = row[5]	

class RowObject:
	#TODO: Create methods to validate params
	def __init__(self, tableName, columnDefs):
		self.columns = columnDefs
		self.table = tableName
		self.values = dict((col.name, col.default) for col in self.columns)
		
	def __getitem__(self, itemName):
		return self.values[itemName]
		
	def __setitem__(self, itemName, value):
		if itemName in self.values:
			self.values[itemName] = value
		else:
			raise KeyError("{0}".format(itemName))
							
	def FromQuery(self, query):
		for column in self.columns:
			self[column.name] = query[0]
			query = query[1:]
		if len(query) != 0:
			print("RowObject.FromQuery discarded excess column values: {0}".format(query))
			raise ValueError("Excess column values")
		return self

class SigninDBConnection:
	def __init__(self):
		self.connection = MySQLdb.connect(
			host = "localhost", user = "signin", passwd = "signin", db = "signin_db")
		self.cursor = self.connection.cursor()
		
		self.cursor.execute("SHOW TABLES;")
		tables = [table[0] for table in self.cursor.fetchall()]
		
		self.tables = {}
		for table in tables:
			self.cursor.execute("SHOW COLUMNS FROM {0}".format(table))
			self.tables[table] = []
			for columnDefs in self.cursor.fetchall():
				self.tables[table].append(ColumnDef(columnDefs))
			
	def __del__(self):
		self.cursor.close()
		self.connection.close()

	def Commit(self):
		self.connection.commit()
		
	def Rollback(self):
		self.connection.rollback()

	def Insert(self, rowObject):
		'''Inserts values in rowObject into the the table specified by rowObject'''
		valueNames = "("
		valuesSubs = "("
		valuesList = []
		for value in rowObject.values.keys():
			#Don't insert a value in the 'id' column, since it autoincrements
			if value == "id":
				continue
			valueNames += "{0}, ".format(value)
			valuesSubs += "%s, "
			valuesList.append(rowObject.values[value])
		valueNames = valueNames[:-2] + ")"
		valuesSubs = valuesSubs[:-2] + ")"
		valuesList = tuple(valuesList)
		self.cursor.execute("INSERT INTO {0} {1} VALUES {2};"
			.format(rowObject.table, valueNames, valuesSubs), valuesList)
			
		rowObject["id"] = self.connection.insert_id()
			
	def Update(self, rowObject):
		'''Updates values of the object rowObject in the table specified by rowObject'''
		setString = ""
		valuesList = []
		for value in rowObject.values.keys():
			#id shouldn't change when updating
			if value == "id":
				continue
			setString += "{0} = %s, ".format(value)
			valuesList.append(rowObject.values[value])
		setString = setString[:-2]
		valuesList.append(rowObject["id"])
		valuesList = tuple(valuesList)
		self.cursor.execute("UPDATE {0} SET {1} WHERE id = %s;"
			.format(rowObject.table, setString), valuesList)
	
	def EmptyRow(self, table):
		return RowObject(table, self.tables[table])

	def GetPersonByFullName(self, firstName, lastName):
		self.cursor.execute("SELECT * FROM persons WHERE firstName = %s AND lastName = %s;",
			(firstName, lastName))
		if self.cursor.rowcount == 0: return None
		else: return self.EmptyRow("persons").FromQuery(self.cursor.fetchone())

	def GetMemberByPersonID(self, personID):
		self.cursor.execute("SELECT * FROM members WHERE personId = %s;", (personID,))
		if self.cursor.rowcount == 0: return None
		else: return self.EmptyRow("members").FromQuery(self.cursor.fetchone())
		
	def FindPersonsByPartialName(self, partialName):
		partialLen = len(partialName)
		self.cursor.execute("SELECT CONCAT(persons.firstName, \" \", persons.lastName) \
				FROM persons \
				WHERE LEFT(persons.firstName, %s) = %s \
					OR LEFT(persons.lastName, %s) = %s \
					OR LEFT(CONCAT(persons.firstname, \" \", persons.lastname), %s) = %s \
				ORDER BY persons.firstName;",
				(partialLen, partialName, partialLen, partialName, partialLen, partialName))

		return [row[0] for row in self.cursor.fetchall()]
		
	def GetHoursInProgress(self):
		self.cursor.execute("SELECT persons.firstName, persons.lastName, hours.start, hours.type \
				FROM hours INNER JOIN persons \
				ON hours.personID = persons.id \
				WHERE hours.duration == 0 \
				ORDER BY persons.firstName;")
				
		return self.cursor.fetchall()


def CreateTablesFromScratch():
	print("Creating database tables from scratch...")
	sys.stdout.flush()
	
	conn = MySQLdb.connect(
		host = "localhost",
		user = "signin_creator",
		passwd = "signin_creator",
		db = "signin_db")
		
	cursor = conn.cursor()
	cursor.execute("""SHOW TABLES""")
	for table in cursor.fetchall():
		cursor.execute("DROP TABLE {0}".format(table[0]))
	
	cursor.execute("""CREATE TABLE persons
			(	id INT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
				firstName VARCHAR(64) NOT NULL,
				lastName VARCHAR(64),			
			PRIMARY KEY(id),
			UNIQUE INDEX(firstName, lastName),
			INDEX(lastName) )
			CHARSET=utf8 ENGINE=InnoDB;""")
			
	cursor.execute("""CREATE TABLE members
			(	id INT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
				personId INT UNSIGNED NOT NULL UNIQUE,
				startDate DATE NOT NULL,
				endDate DATE,
				streetAddress VARCHAR(128),
				emailAddress VARCHAR(64),
				phoneNumber VARCHAR(32),
				donation SMALLINT UNSIGNED,
				notes VARCHAR(200),	
			PRIMARY KEY(id),
			INDEX(personId),
			FOREIGN KEY(personId) REFERENCES persons(id)
				ON DELETE NO ACTION 
				ON UPDATE CASCADE )
			CHARSET=utf8 ENGINE=InnoDB;""")
						
	cursor.execute("""CREATE TABLE hours
			(	id INT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
				personID INT UNSIGNED NOT NULL UNIQUE,
				start DATETIME NOT NULL,
				duration TIME NOT NULL,
				type ENUM(
					'shoptime',
					'parts',
					'worktrade',
					'volunteer',
					'mechanic',
					'accounting',
					'extra_shift',
					'facilities',
					'outreach',
					'ordering',
					'tools',
					'other') NOT NULL,
				notes VARCHAR(200),
			PRIMARY KEY(id),
			INDEX(personId),
			INDEX(type),
			FOREIGN KEY(personId) REFERENCES persons(id)
				ON DELETE NO ACTION
				ON UPDATE CASCADE )
			CHARSET=utf8 ENGINE=InnoDB;""")
			
	cursor.execute("""CREATE TABLE hoursInProgress LIKE hours""")
	cursor.execute("""ALTER TABLE hoursInProgress
				DROP COLUMN duration,
				DROP COLUMN notes""")
			
	cursor.execute("""CREATE TABLE bikes
			(	id INT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
				personId INT UNSIGNED NOT NULL UNIQUE,
				color VARCHAR(64) NOT NULL,
				brand VARCHAR(64),
				model VARCHAR(64),
				serialNumber VARCHAR(64) NOT NULL,
			PRIMARY KEY(id),
			INDEX(personId),
			INDEX(serialNumber(10)),
			FOREIGN KEY(personId) REFERENCES persons(id)
				ON DELETE NO ACTION
				ON UPDATE CASCADE )
			CHARSET=utf8 ENGINE=InnoDB;""")

	conn.commit()
	cursor.close()
	conn.close()
	
	print("\tSuccess")
