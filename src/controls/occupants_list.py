import wx
from datetime import datetime

sTypeDescriptions = {
	"shoptime":	"Working on a Bike",
	"parts":	"Looking for Parts",
	"worktrade":	"Doing Worktrade",
	"volunteer":	"Volunteering"
	}

def GetShoptimeTypeDescription(type):
	if type in sTypeDescriptions:
		return sTypeDescriptions[type]
	else:
		return "\"{0}\"".format(type)


class OccupantLine():	
	def __init__(self, parent, sizer, controller, personID, startTime, type):
		self.parent = parent
		self.controller = controller
		self.personID = personID
		name = controller.GetPersonNameByID(personID)
		firstName = name[0]
		lastName = name[1]
		self.startTime = startTime
		type = type
		self.elements = []
		
		possesiveChar = "s"
		if firstName[-1] == "s":
			possesiveChar = ""

		def AddLabel(parent, sizer, string, flags = 0):
			text = wx.StaticText(parent, wx.ID_ANY, string)
			text.SetFont(wx.Font(9, wx.FONTFAMILY_SWISS, wx.NORMAL, wx.NORMAL))
			sizer.Add(text, 0, wx.ALIGN_CENTER_VERTICAL | flags)
			self.elements.append(text)
			return text
			 
		def AddButton(parent, sizer, string, onClick):
			button = wx.Button(parent, wx.ID_ANY, string)
			button.SetMaxSize(wx.Size(-1, 25))
			sizer.Add(button, 1, wx.ALIGN_CENTER_VERTICAL)
			button.Bind(wx.EVT_BUTTON, onClick)
			self.elements.append(button)
		 
		 
		AddLabel(parent, sizer, u"{0} {1}".format(firstName, lastName))
		AddLabel(parent, sizer, u"{0}".format(GetShoptimeTypeDescription(type)))
		self.timeText = AddLabel(parent, sizer, u"", wx.ALIGN_RIGHT)
		
		buttonSizer = wx.BoxSizer()
		self.elements.append(buttonSizer)
		AddButton(parent, buttonSizer, u"View Info", self.OnViewInfoClicked)
		AddButton(parent, buttonSizer, u"Sign Out", self.OnSignOutClicked)
		sizer.Add(buttonSizer, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
		
		self.UpdateTime()
		
	def GetElements(self):
		return self.elements
		
	def OnViewInfoClicked(self, event):
		print("View info for {0}".format(self.personID))
		
	def OnSignOutClicked(self, event):
		self.controller.SignPersonOut(self.personID)
		
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
		
class OccupantsList(wx.Panel):
	def __init__(self, parent, controller):
		wx.Panel.__init__(self, parent)
		self.controller = controller
		self.occupants = []

		titleFont = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
		self.titleText = wx.StaticText(self, wx.ID_ANY, u"Who's in the Shop:")
		self.titleText.SetFont(titleFont)
		self.dateText = wx.StaticText(self, wx.ID_ANY, u"")
		self.dateText.SetFont(titleFont)
		
		titleSizer = wx.BoxSizer()
		titleSizer.Add(self.titleText, 0, wx.ALL, 5)
		titleSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)
		titleSizer.Add(self.dateText, 0, wx.ALL, 5)
		
		self.scrollbox = wx.ScrolledWindow(self, style = wx.VSCROLL)

		self.listSizer = wx.FlexGridSizer(rows = 0, cols = 4, hgap = 10, vgap = 0)
		self.listSizer.SetFlexibleDirection(wx.BOTH)
		self.listSizer.AddGrowableCol(1, 1)
		self.listSizer.AddGrowableCol(2, 1)

		self.AddColumnHeader(self.listSizer, u"Name")
		self.AddColumnHeader(self.listSizer, u"Activity")
		self.AddColumnHeader(self.listSizer, u"Time In Shop")
		self.AddColumnHeader(self.listSizer, u"")
		
		peopleInShop = self.controller.GetPeopleInShop()
		if peopleInShop is not None:
			for person in self.controller.GetPeopleInShop():
				self.AddOccupant(person["personID"],
					person["start"], person["type"])
		
		self.scrollbox.SetSizer(self.listSizer)
		self.scrollbox.SetScrollRate(0, 20)
		self.scrollbox.Bind(wx.EVT_SCROLLWIN_THUMBTRACK, self.OnThumbTrack)
				
		gridSizer = wx.FlexGridSizer(2, 1)
		gridSizer.SetFlexibleDirection(wx.BOTH)
		gridSizer.AddGrowableCol(0)
		gridSizer.AddGrowableRow(1)
		gridSizer.Add(titleSizer, 1, wx.EXPAND)
		gridSizer.Add(self.scrollbox, 1, wx.EXPAND)
		self.SetSizer(gridSizer)
		
		self.Bind(wx.EVT_TIMER, self.OnTimer)
		self.updateTimer = wx.Timer(self)
		self.updateTimer.Start(1000)# * 60)
		
		self.UpdateTimes()
	
	def AddColumnHeader(self, sizer, name):
		label = wx.StaticText(self.scrollbox, wx.ID_ANY, name)
		label.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.NORMAL, wx.NORMAL))
		localSizer = wx.BoxSizer(wx.VERTICAL)
		localSizer.Add(label)
		localSizer.Add(wx.StaticLine(self.scrollbox), 0, wx.EXPAND)
		sizer.Add(localSizer, 0, wx.ALIGN_CENTER | wx.EXPAND)	
	
	def AddOccupant(self, personID, startTime, type):
		occupant = OccupantLine(self.scrollbox, self.listSizer,
			self.controller, personID, startTime, type)
		self.occupants.append(occupant)
		
		if hasattr(self, "listSizer"):
			self.listSizer.Layout()
		if hasattr(self, "gridSizer"):
			gridSizer.Layout()
	
	def RemoveOccupant(self, personID):
		for occupant in self.occupants:
			if occupant.personID == personID:
				for element in occupant.GetElements():
					self.listSizer.Detach(element)
					element.Destroy()
				self.occupants.remove(occupant)
				break
											
		self.listSizer.Layout()
				
	def OnThumbTrack(self, event):
		pass
			
	def OnTimer(self, event):
		self.UpdateTimes()
		
	def UpdateTimes(self):
		self.dateText.SetLabel(datetime.now().strftime("%A %b %d  %I:%M %p"))
		for occupant in self.occupants:
			occupant.UpdateTime()
		self.listSizer.Layout()
