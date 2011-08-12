#!/usr/bin/python
# -*- coding: utf-8 -*-
import wx, datetime
from src.csvImport import ReadMembersFromCSV
from src.db import CreateTablesFromScratch
from src.main_window import MainWindow
from src.controller import GetController, ResetController

from warnings import warn

version = (0, 1, 0)

#TODO: Fix shoptime editor to allow unspecified end time
#BUG: Names list fails to bring up names after program is running for days
#TODO: Reset horizontal name listbox position to origin when changing names
#TODO: BMX should be an option for type of bike!
#TODO: Be able to search by patron, past date, or bike
#TODO: Edit current shoptime
#TODO: Notes on patrons

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
	CheckVersion("sqlalchemy", "0.6")

	if createDB:				 
		CreateTablesFromScratch()
		ReadMembersFromCSV("members.csv", "succeeded.csv", "failed.csv")

	ResetController()
	
	app = wx.App()
	MainWindow()
	app.MainLoop()
	
if __name__ == "__main__":
	main(0)

