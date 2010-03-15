#!/usr/bin/python

import csvImport, db, ui, control
import wx, sys

import cProfile, pstats
	
def main(createDB = False):
	if createDB:				 
		db.CreateTablesFromScratch()
		csvImport.ReadMembersFromCSV("members.csv", "succeeded.csv", "failed.csv")
	
	connection = db.Connection()
	controller = control.Controller(connection)
	app = wx.App()
	form = ui.MainWindow(controller)
	app.MainLoop()
	
	
if __name__ == "__main__":
	#cProfile.run("main()", "mainprof")
	#stats = pstats.Stats("mainprof")
	#stats.sort_stats('cumulative').print_stats(15)
	main()

