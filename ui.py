import db
import wx, datetime

class ShopOccupantsArea():
	def __init__(self, parent):
		if not isinstance(parent, wx.Window):
			raise TypeError("Parent must be a wx.Window")
			
		self.parent = parent

		titleFont = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
		self.titleText = wx.StaticText(parent, wx.ID_ANY, u"Who's in the Shop:")
		self.titleText.SetFont(titleFont)
		self.dateText = wx.StaticText(parent, wx.ID_ANY, u"")
		self.dateText.SetFont(titleFont)
		
		titleSizer = wx.BoxSizer()
		titleSizer.Add(self.titleText, 0, wx.ALL, 5)
		titleSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)
		titleSizer.Add(self.dateText, 0, wx.ALL, 5)
		
		self.listSizer = wx.FlexGridSizer(rows = 0, cols = 4)
		self.listSizer.SetFlexibleDirection(wx.VERTICAL)
		self.listSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_ALL)
		for i in range(4 * 10):
			button = wx.StaticText(parent, wx.ID_ANY, u"blah blah blah")
			button.Wrap(-1)
			self.listSizer.Add(button, 1, wx.ALL | wx.EXPAND, 5)
		
		self.gridSizer = wx.FlexGridSizer(2, 1)
		self.gridSizer.AddGrowableCol(0)
		self.gridSizer.AddGrowableCol(1)
		self.gridSizer.Add(titleSizer, 1, wx.EXPAND)
		self.gridSizer.Add(self.listSizer, 1, wx.EXPAND)
		
		self.UpdateTimes()
	
	def GetOuterSizer(self):
		return self.gridSizer
	
	def AddOccupantLine(self):
		pass
	
	def RemoveOccupantLine(self):
		pass
		
	def UpdateTimes(self):
		self.dateText.SetLabel(datetime.datetime.now().strftime("%A %b %d  %I:%M %p"))
		
		
class SignInArea():
	def __init__(self, parent):
		if not isinstance(parent, wx.Window):
			raise TypeError("Parent must be a wx.Window")
		
		self.parent = parent
		
		bigFont = wx.Font(18, wx.FONTFAMILY_SWISS, wx.FONTWEIGHT_BOLD, wx.NORMAL)
		mediumFont = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
		
		startHereText = wx.StaticText(parent, wx.ID_ANY, u"Sign In Here")
		startHereText.SetFont(bigFont)
		enterNameText = wx.StaticText(parent, wx.ID_ANY, u"Hi! What's your name?")
		startHereText.SetFont(mediumFont)
		selectNameText = wx.StaticText(parent, wx.ID_ANY, u"Click your name if it's in the list:")
		startHereText.SetFont(mediumFont)
		whatToDoText = wx.StaticText(parent, wx.ID_ANY, u"What did you want to do in the shop today?")
		startHereText.SetFont(mediumFont)
		
		self.nameEntryDefaultText = u"Type your name here."
		self.nameEntry = wx.TextCtrl(parent, wx.ID_ANY, self.nameEntryDefaultText)
		self.nameList = wx.ListBox(parent, wx.ID_ANY)
		self.workButton = wx.Button(parent, wx.ID_ANY, u"Work on my bike!")
		self.partsButton = wx.Button(parent, wx.ID_ANY, u"Look for parts!")
		self.worktradeButton = wx.Button(parent, wx.ID_ANY, u"Do work trade!")
		self.volunteerButton = wx.Button(parent, wx.ID_ANY, u"Volunteer!")
		
		staticBox = wx.StaticBox(parent)
		self.boxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
		self.boxSizer.Add(startHereText, 0, wx.ALL | wx.ALIGN_CENTER, 5)
		self.boxSizer.Add(enterNameText, 0, wx.ALL, 5)
		self.boxSizer.Add(self.nameEntry, 0, wx.EXPAND)
		self.boxSizer.Add(selectNameText, 0, wx.EXPAND | wx.ALL, 5)
		self.boxSizer.Add(self.nameList, 0, wx.EXPAND)
		self.boxSizer.SetItemMinSize(self.nameList, wx.Size(-1, 150))
		self.boxSizer.Add(whatToDoText, 0, wx.ALL, 5)
		self.boxSizer.Add(self.workButton, 0, wx.EXPAND)
		self.boxSizer.Add(self.partsButton, 0, wx.EXPAND)
		self.boxSizer.Add(self.worktradeButton, 0, wx.EXPAND)
		self.boxSizer.Add(self.volunteerButton, 0, wx.EXPAND)
		
		self.nameEntry.Bind(wx.EVT_TEXT, self.OnNameEntryChange)
		self.nameEntry.Bind(wx.EVT_SET_FOCUS, self.OnNameEntryFocus)
		
	def OnNameEntryChange(self, event):
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
	
	def GetOuterSizer(self):
		return self.boxSizer
	
class MainWindow(wx.Frame):
	def __init__(self, parent, dbConnection):
		wx.Frame.__init__(self, parent, id = wx.ID_ANY, title = u"Welcome To The Bike Church!",
			pos = wx.DefaultPosition, size = wx.Size(800, 450),
			style = wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL, name = "MainWindow")
		
		self.dbConnection = dbConnection
		
		self.occupantsPanel = ShopOccupantsArea(self)
		self.signInPanel = SignInArea(self)
		
		self.sizer = wx.BoxSizer(wx.HORIZONTAL)		
		self.sizer.Add(self.signInPanel.GetOuterSizer(), 0)
		self.sizer.Add(self.occupantsPanel.GetOuterSizer(), 1, wx.EXPAND)
		
		self.SetSizer(self.sizer)
		self.Layout()
		self.Centre(wx.BOTH)
		
		self.updateTimer = wx.Timer(self)
		self.updateTimer.Start(1000 * 20)

		self.Bind(wx.EVT_SIZE, self.OnResize)
		self.Bind(wx.EVT_TIMER, self.OnTimer)

	# Frame resize event method
	def OnResize(self, event):
		self.Layout()
	
	def OnTimer(self, event):
		self.occupantsPanel.UpdateTimes()
		
	def GetDBConnection(self):
		return self.dbConnection
		
