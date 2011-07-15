#!/usr/bin/python
# -*- coding: utf-8 -*-
import wx, datetime
from src.csvImport import ReadMembersFromCSV
from src.db import CreateTablesFromScratch
from src.main_window import MainWindow
from src.controller import GetController, ResetController

from warnings import warn

version = (0, 1, 0)

#FIXED: If you type in your name again, but do not click on it in the option box, it thinks you are a brand new person
#FIXED: Typed-in name results in "duplicate name" error in new person screen, where it shouldn't be anyway
#DONE: Run inside a python script so that we can capture output to a log.

#TODO: Fix long login times for people signed in overnight or longer
#BUG: Names list fails to bring up names after program is running for days
#TODO: Reset horizontal name listbox position to origin when changing names
#TODO: BMX should be an option for type of bike!
#TODO: Be able to search by patron, past date, or bike
#TODO: Arrow down from text box selects entries in list
#TODO: Edit current shoptime

def CheckVersion(packageName, minimumVersion):
	package = __import__(packageName)
	curVersion = [x for x in package.__version__.split(".")]
	minVersion = [x for x in minimumVersion.split(".")]

	for pair in zip(curVersion, minVersion):
		if pair[0] < pair[1]:
			message = "Module {0} v{1} is older than minimum v{2}".format(
				package.__name__, package.__version__, minimumVersion)
			warn(message, UserWarning, 2)
			return False
			
	return True

def main(createDB = False):
	print("{1} Starting bikechurch-signin v{0}".format(".".join([str(x) for x in version]),
		datetime.datetime.now()))

	CheckVersion("wx", "2.8")
	CheckVersion("MySQLdb", "1.2.2")
	CheckVersion("sqlalchemy", "0.7")

	if createDB:				 
		CreateTablesFromScratch()
		ReadMembersFromCSV("members.csv", "succeeded.csv", "failed.csv")

	ResetController()
	app = wx.App()
	MainWindow()
	app.MainLoop()
	
if __name__ == "__main__":
	main(0)

