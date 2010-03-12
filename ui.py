import db
import wx
from datetime import datetime, timedelta
import random

class ShopOccupantLine():
	timeTypeStrings = {
		"shoptime":	"Working on a Bike",
		"parts":	"Looking for Parts",
		"worktrade":	"Doing Worktrade",
		"volunteer":	"Volunteering"
		}
	
	def __init__(self, parent, sizer, firstName, lastName, startTime, type):
		self.parent = parent
		self.firstName = firstName
		self.lastName = lastName
		self.startTime = startTime
		self.type = type
		
		possesiveChar = "s"
		if firstName[-1] == "s":
			possesiveChar = ""

		def AddText(parent, sizer, string, flags = 0):
			text = wx.StaticText(parent, wx.ID_ANY, string)
			text.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.NORMAL, wx.NORMAL))
			sizer.Add(text, 0, wx.ALIGN_CENTER_VERTICAL | flags)
			return text
			 
		def AddButton(parent, sizer, string, onClick):
			button = wx.Button(parent, wx.ID_ANY, string)
			button.SetMaxSize(wx.Size(-1, 25))
			sizer.Add(button, 1, wx.ALIGN_CENTER_VERTICAL)
			button.Bind(wx.EVT_BUTTON, onClick)
		 
		AddText(parent, sizer, u"{0} {1}".format(firstName, lastName))
		AddText(parent, sizer, u"{0}".format(ShopOccupantLine.timeTypeStrings[type]))
		self.timeText = AddText(parent, sizer, u"", wx.ALIGN_RIGHT)
		 
		buttonSizer = wx.BoxSizer()
		AddButton(parent, buttonSizer, u"View Info", self.OnViewInfoClicked)
		AddButton(parent, buttonSizer, u"Sign Out", self.OnSignOutClicked)
		sizer.Add(buttonSizer, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
		
		self.UpdateTime()
		
	def OnViewInfoClicked(self, event):
		print("View info for {0} {1}".format(self.firstName, self.lastName))
		
	def OnSignOutClicked(self, event):
		print("Sign out {0} {1}".format(self.firstName, self.lastName))
		
	def UpdateTime(self):
		timediff = datetime.now() - self.startTime
		seconds = timediff.seconds
		hours = int(timediff.seconds / (60 * 60))
		seconds -= hours * (60 * 60)
		hours += timediff.days * 24
		minutes = seconds / 60
		
		if hours == 0 and minutes == 0:
			minutes = 1
	
		timeString = ""
		if (hours > 0):
			timeString += " {0} hrs".format(hours)
		if (minutes > 0):
			timeString += " {0} min".format(minutes)
			
		self.timeText.SetLabel(timeString)
		
class ShopOccupantsArea():
	def __init__(self, parent):
		if not isinstance(parent, wx.Window):
			raise TypeError("Parent must be a wx.Window")
			
		self.parent = parent
		self.occupants = []

		titleFont = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
		self.titleText = wx.StaticText(parent, wx.ID_ANY, u"Who's in the Shop:")
		self.titleText.SetFont(titleFont)
		self.dateText = wx.StaticText(parent, wx.ID_ANY, u"")
		self.dateText.SetFont(titleFont)
		
		titleSizer = wx.BoxSizer()
		titleSizer.Add(self.titleText, 0, wx.ALL, 5)
		titleSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)
		titleSizer.Add(self.dateText, 0, wx.ALL, 5)
		
		self.scrollbox = wx.ScrolledWindow(parent, style = wx.VSCROLL)

		self.listSizer = wx.FlexGridSizer(rows = 0, cols = 4, hgap = 10, vgap = 0)
		self.listSizer.SetFlexibleDirection(wx.BOTH)
		self.listSizer.AddGrowableCol(1, 1)
		self.listSizer.AddGrowableCol(2, 1)
		
		def AddColumnHeader(parent, sizer, name):
			label = wx.StaticText(parent, wx.ID_ANY, name)
			label.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.NORMAL, wx.NORMAL))
			localSizer = wx.BoxSizer(wx.VERTICAL)
			localSizer.Add(label)
			localSizer.Add(wx.StaticLine(parent), 0, wx.EXPAND)
			sizer.Add(localSizer, 0, wx.ALIGN_CENTER | wx.EXPAND)
		
		AddColumnHeader(self.scrollbox, self.listSizer, u"Name")
		AddColumnHeader(self.scrollbox, self.listSizer, u"Activity")
		AddColumnHeader(self.scrollbox, self.listSizer, u"Time In Shop")
		AddColumnHeader(self.scrollbox, self.listSizer, u"")
		
		personsInShop = self.parent.GetDBConnection().GetPersonsInShop()
		if personsInShop is not None:
			for person in self.parent.GetDBConnection().GetPersonsInShop():
				self.occupants.append(ShopOccupantLine(self.scrollbox, self.listSizer,
					person["firstName"], person["lastName"],
					person["start"], person["type"]))
		
		self.scrollbox.SetSizer(self.listSizer)
		self.scrollbox.SetScrollRate(0, 5)
				
		self.gridSizer = wx.FlexGridSizer(2, 1)
		self.gridSizer.SetFlexibleDirection(wx.BOTH)
		self.gridSizer.AddGrowableCol(0)
		self.gridSizer.AddGrowableRow(1)
		self.gridSizer.Add(titleSizer, 1, wx.EXPAND)
		self.gridSizer.Add(self.scrollbox, 1, wx.EXPAND)
		
		self.UpdateTimes()
	
	def GetOuterSizer(self):
		return self.gridSizer
	
	def AddOccupantLine(self, firstName, lastName, startTime, type):
		occupant = ShopOccupantLine(self.scrollbox, self.listSizer,
			firstName, lastName, startTime, type)
		self.occupants.append(occupant)
		self.listSizer.Layout()
		self.gridSizer.Layout()
	
	def RemoveOccupantLine(self, name):
		pass
		
	def UpdateTimes(self):
		self.dateText.SetLabel(datetime.now().strftime("%A %b %d  %I:%M %p"))
		for occupant in self.occupants:
			occupant.UpdateTime()
		self.gridSizer.Layout()
		
class SignInArea():
	def __init__(self, parent):
		if not isinstance(parent, wx.Window):
			raise TypeError("Parent must be a wx.Window")
		
		self.parent = parent
		self.suppressNextListChange = False
		
		def AddText(parent, sizer, font, string, flags = 0):
			text = wx.StaticText(parent, wx.ID_ANY, string)
			if font is not None:
				text.SetFont(font)
			sizer.Add(text, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL | flags, 5)
			return text
			 
		def AddButton(parent, sizer, string, onClick):
			button = wx.Button(parent, wx.ID_ANY, string)
			button.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL))
			sizer.Add(button, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
			button.Bind(wx.EVT_BUTTON, onClick)
			return button
		
		staticBox = wx.StaticBox(parent)
		self.sizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
		
		bigFont = wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTWEIGHT_BOLD, wx.NORMAL)
		medFont = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
		AddText(parent, self.sizer, bigFont, u"Sign In Here", wx.ALIGN_CENTER)
		AddText(parent, self.sizer, medFont, u"Hi! What's your name?")
		
		self.nameEntryDefaultText = u"Type your name here."
		self.nameEntry = wx.TextCtrl(parent, wx.ID_ANY, self.nameEntryDefaultText)
		self.nameEntry.Bind(wx.EVT_TEXT, self.OnNameEntryChange)
		self.nameEntry.Bind(wx.EVT_SET_FOCUS, self.OnNameEntryFocus)
		self.sizer.Add(self.nameEntry, 0, wx.EXPAND)
		
		AddText(parent, self.sizer, medFont, u"If you've been here before,\nclick your name in the list:")
		
		self.nameList = wx.ListBox(parent, wx.ID_ANY)
		self.nameList.Bind(wx.EVT_LISTBOX, self.OnListClick)
		self.nameList.Bind(wx.EVT_LISTBOX_DCLICK, self.OnListClick)
		self.sizer.Add(self.nameList, 0, wx.EXPAND)
		self.sizer.SetItemMinSize(self.nameList, wx.Size(-1, 150))
		
		AddText(parent, self.sizer, medFont, u"What do you want to do?")
		AddButton(parent, self.sizer, u"Work on my bike!", lambda e: self.OnSigninClick(e, "shoptime"))
		AddButton(parent, self.sizer, u"Look for parts!", lambda e: self.OnSigninClick(e, "parts"))
		AddButton(parent, self.sizer, u"Do work trade!", lambda e: self.OnSigninClick(e, "worktrade"))
		AddButton(parent, self.sizer, u"Volunteer!", lambda e: self.OnSigninClick(e, "volunteer"))
		
	def OnNameEntryChange(self, event):
		if self.suppressNextListChange:
			self.suppressNextListChange = False
			event.Skip()
			return
			
		self.nameList.Clear()
		partialName = self.nameEntry.GetValue()
		partialNameLen = len(partialName)
					
		if partialNameLen > 1:
			conn = self.parent.GetDBConnection()
			matchingNames = conn.FindPersonsByPartialName(partialName)
			self.nameList.SetItems(matchingNames)
	
	def OnNameEntryFocus(self, event):
		if self.nameEntry.GetValue() == self.nameEntryDefaultText:
			self.nameEntry.SetValue("")
	
	def OnListClick(self, event):
		selection = self.nameList.GetStringSelection()
		if selection != "":
			self.suppressNextListChange = True
			self.nameEntry.SetValue(selection)
	
	def OnSigninClick(self, event, type):
		name = self.nameEntry.GetValue()
		if name == "" or name == self.nameEntryDefaultText:
			#Flash the name box
			pass
		else:
			conn = self.parent.GetDBConnection()
			person = conn.GetPersonByCombinedName(name)
			if person is None:
				print("Signin: new person doing {0}".format(type))
			else:
				personInShop = conn.EmptyRow("personsInShop")
				personInShop["personID"] = person["id"]
				personInShop["start"] = datetime.now()
				personInShop["type"] = type
				conn.Insert(personInShop)
				conn.Commit()
				
				self.parent.occupantsArea.AddOccupantLine(
					person["firstName"], person["lastName"], datetime.now(), type)
			
			self.nameEntry.SetValue(self.nameEntryDefaultText)
			self.nameList.Clear()
	
	def GetOuterSizer(self):
		return self.sizer
	
class MainWindow(wx.Frame):
	def __init__(self, parent, dbConnection):
		wx.Frame.__init__(self, parent, id = wx.ID_ANY, title = u"Welcome To The Bike Church!",
			pos = wx.DefaultPosition, size = wx.Size(900, 480),
			style = wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL, name = "MainWindow")
		
		self.dbConnection = dbConnection
		
		self.occupantsArea = ShopOccupantsArea(self)
		self.signInArea = SignInArea(self)
		
		self.sizer = wx.BoxSizer(wx.HORIZONTAL)		
		self.sizer.Add(self.signInArea.GetOuterSizer(), 0, wx.ALL, 8)
		self.sizer.Add(self.occupantsArea.GetOuterSizer(), 1, wx.EXPAND | wx.ALL, 8)
		
		self.SetSizer(self.sizer)
		self.Layout()
		self.Centre(wx.BOTH)
		
		self.updateTimer = wx.Timer(self)
		self.updateTimer.Start(1000 * 60)

		self.Bind(wx.EVT_SIZE, self.OnResize)
		self.Bind(wx.EVT_TIMER, self.OnTimer)

	# Frame resize event method
	def OnResize(self, event):
		self.Layout()
	
	def OnTimer(self, event):
		self.occupantsArea.UpdateTimes()
		
	def GetDBConnection(self):
		return self.dbConnection
		
