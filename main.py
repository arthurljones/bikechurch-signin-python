#!/usr/bin/python
 # -*- coding: utf-8 -*-
 
import wx, sys	
from src.csvImport import ReadMembersFromCSV
from src.db import CreateTablesFromScratch
from src.main_window import MainWindow
from src.controller import ResetController

from warnings import warn

version = (0, 1, 0)

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
	print("Starting bikechurch-signin v{0}".format(".".join([str(x) for x in version])))

	CheckVersion("wx", "2.8")
	CheckVersion("MySQLdb", "1.2.2")
	CheckVersion("sqlalchemy", "0.6")

	if createDB:				 
		CreateTablesFromScratch()
		ReadMembersFromCSV("members.csv", "succeeded.csv", "failed.csv")

	ResetController()
	app = wx.App()
	form = MainWindow()
	app.MainLoop()
	
if __name__ == "__main__":
	#cProfile.run("main()", "mainprof")
	#stats = pstats.Stats("mainprof")
	#stats.sort_stats('cumulative').print_stats(15)
	main()

