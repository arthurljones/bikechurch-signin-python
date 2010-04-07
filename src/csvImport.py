 # -*- coding: utf-8 -*-
 
import db
import sys, csv
from datetime import date, timedelta
from controller import ResetController

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
		
def ReadMembersFromCSV(filename, succeededFilename, failedFilename):
	reader = csv.reader(open(filename, "rb"))
	succeeded = csv.writer(open(succeededFilename, "wb"))
	failed = csv.writer(open(failedFilename, "wb"))
	
	numFailed = 0
	numSucceeded = 0
	print("Loading membership data...")
	print("\tParsing membership data file")
	sys.stdout.flush()
	
	controller = ResetController()
	
	FullName = lambda firstName, lastName: " ".join([firstName, lastName]).lower()
	
	people = {}
	for person in db.session.query(db.Person).all():
		people[FullName(person.firstName, person.lastName)] = person
	
	for row in reader:		
		startDate = ParseCSVDate(row[0])
		type, duration, money = ParseCSVMembershipTypeDurationAndDonation(row[6], row[7])
		if startDate is None or type is None:
			failed.writerow(row)
			numFailed += 1
			continue
			
		endDate = None
		if duration != None:
			endDate = startDate + duration
			
		lastName = unicode(row[1].strip())
		firstName = unicode(row[2].strip())

		fullName = FullName(firstName, lastName)

		#TODO: Do more validation before we get to this point
		person = None
		if fullName in people:
			person = people[fullName]
		else:
			person = db.Person()
			person.firstName = firstName
			person.lastName = lastName
			people[fullName] = person

		if person.memberInfo is None:
			person.memberInfo = db.Member()
		else:
			memberEndDate = person.memberInfo.endDate
			alreadyLifer = memberEndDate is None
			nowLifer = endDate is None
			if alreadyLifer or (not nowLifer and memberEndDate < endDate):
				continue

		person.memberInfo.endDate = endDate
		person.memberInfo.mailingAddress = unicode(row[3].strip())
		person.memberInfo.phoneNumber = unicode(row[4].strip())
		person.memberInfo.emailAddress = unicode(row[5].strip())
		person.memberInfo.donation =  money
		person.memberInfo.notes = unicode(row[8].strip())
		person.memberInfo.startDate = startDate
		person.memberInfo.endDate = endDate		
					
		succeeded.writerow(row)
		numSucceeded += 1
		
	print("\t\t{0} rows successfuly parsed".format(numSucceeded))
	print("\t\t{0} rows failed to parse".format(numFailed))

	print("\tCommiting data to database")
	db.session.add_all(people.values())
	db.session.commit()

	numPeople = db.session.query(db.Person).count() 
	print("\t{0} people in database".format(numPeople))
	print("...Success")
