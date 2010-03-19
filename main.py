#!/usr/bin/python

import wx, sys	
import src.csvImport as csvImport, src.db as db, src.ui as ui
from src.controller import Controller

#python -u main.py 2>&1 | grep -Ev 'Gtk-WARNING'

def main(createDB = False):
	#sys.stderr = sys.stdout


	if createDB:				 
		db.CreateTablesFromScratch()
		csvImport.ReadMembersFromCSV("members.csv", "succeeded.csv", "failed.csv")
	
	connection = db.Connection()
	controller = Controller(connection)
	app = wx.App()
	form = ui.MainWindow(controller)
	app.MainLoop()
	
if __name__ == "__main__":
	#cProfile.run("main()", "mainprof")
	#stats = pstats.Stats("mainprof")
	#stats.sort_stats('cumulative').print_stats(15)
	main()

