import csvImport, db, ui, ui_forms
from copy import copy
import wx

def DebugStuff(conn):
	#Get all current lifetime members we know about
	conn.cursor.execute("SELECT members.endDate \
				FROM persons JOIN members \
				ON persons.id = members.personId \
				WHERE members.endDate IS NULL;")
				
	print("{0} lifetime members".format(conn.cursor.rowcount))
				 
#db.CreateTablesFromScratch()
#csvImport.ReadMembersFromCSV("members.csv", "succeeded.csv", "failed.csv")		

conn = db.SigninDBConnection()
app = wx.App()
form = ui.MainWindow(None, conn)
form.Show()
app.MainLoop()
