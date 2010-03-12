import db
import sys, csv
from datetime import date, timedelta

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
	
	print("Loading existing membership data...")
	sys.stdout.flush()
	
	conn = db.SigninDBConnection()
	
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
			
		lastName = row[1].strip()
		firstName = row[2].strip()

		#TODO: Do more validation before we get to this point
		person = conn.GetPersonByFullName(firstName, lastName)
		if person is None:
			person = conn.EmptyRow("persons")
			person["firstName"] = firstName
			person["lastName"] = lastName
			conn.Insert(person)

		member = conn.GetMemberByPersonID(person["id"])
		if member is None:
			member = conn.EmptyRow("members")
			member["personId"] = person["id"]
			member["streetAddress"] = row[3].strip()
			member["phoneNumber"] = row[4].strip()
			member["emailAddress"] = row[5].strip()
			member["donation"] =  money
			member["notes"] = row[8].strip()
			member["startDate"] = startDate
			member["endDate"] = endDate
					
			conn.Insert(member)
		else:
			alreadyLifer = member["endDate"] is None
			nowLifer = endDate is None
			if nowLifer and not alreadyLifer or \
				(not alreadyLifer and not nowLifer and member["endDate"] < endDate):

				member["endDate"] = endDate
				member["streetAddress"] = row[3].strip()
				member["phoneNumber"] = row[4].strip()
				member["emailAddress"] = row[5].strip()
				member["donation"] =  money
				member["notes"] = row[8].strip()
				member["startDate"] = startDate
				member["endDate"] = endDate
				
			conn.Update(member)
					
		succeeded.writerow(row)
		numSucceeded += 1
		
	conn.Commit()
	
	print("\t{0} rows successfuly parsed, {1} rows failed to parse".format(numSucceeded, numFailed))

	conn.cursor.execute("SELECT COUNT(id) FROM persons")
	memberCount = conn.cursor.fetchone()[0]
	print("{0} people in database".format(memberCount))

	conn.cursor.execute("SELECT COUNT(id) FROM members")
	memberCount = conn.cursor.fetchone()[0]
	print("{0} members in database".format(memberCount))
