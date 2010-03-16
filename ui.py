import db
import wx
from datetime import datetime, timedelta
import random

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

class ShopOccupantLine():	
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

		def AddText(parent, sizer, string, flags = 0):
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
		 
		 
		AddText(parent, sizer, u"{0} {1}".format(firstName, lastName))
		AddText(parent, sizer, u"{0}".format(GetShoptimeTypeDescription(type)))
		self.timeText = AddText(parent, sizer, u"", wx.ALIGN_RIGHT)
		
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
		
class ShopOccupantsArea():
	def __init__(self, parent, controller):
		if not isinstance(parent, wx.Window):
			raise TypeError("Parent must be a wx.Window")
			
		self.parent = parent
		self.controller = controller
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
		
		peopleInShop = self.controller.GetPeopleInShop()
		if peopleInShop is not None:
			for person in self.controller.GetPeopleInShop():
				self.AddOccupantLine(person["personID"], person["start"], person["type"])
		
		self.scrollbox.SetSizer(self.listSizer)
		self.scrollbox.SetScrollRate(0, 20)
		self.scrollbox.Bind(wx.EVT_SCROLLWIN_THUMBTRACK, self.OnThumbTrack)
				
		self.gridSizer = wx.FlexGridSizer(2, 1)
		self.gridSizer.SetFlexibleDirection(wx.BOTH)
		self.gridSizer.AddGrowableCol(0)
		self.gridSizer.AddGrowableRow(1)
		self.gridSizer.Add(titleSizer, 1, wx.EXPAND)
		self.gridSizer.Add(self.scrollbox, 1, wx.EXPAND)
		
		self.UpdateTimes()
	
	def GetOuterSizer(self):
		return self.gridSizer
	
	def AddOccupantLine(self, personID, startTime, type):
		occupant = ShopOccupantLine(self.scrollbox, self.listSizer,
			self.controller, personID, startTime, type)
		self.occupants.append(occupant)
		
		if hasattr(self, "listSizer"):
			self.listSizer.Layout()
		if hasattr(self, "gridSizer"):
			self.gridSizer.Layout()
	
	def RemoveOccupantLine(self, personID):
		for occupant in self.occupants:
			if occupant.personID == personID:
				for element in occupant.GetElements():
					self.listSizer.Detach(element)
					element.Destroy()
				self.occupants.remove(occupant)
				break
											
		self.gridSizer.Layout()
				
	def OnThumbTrack(self, event):
		pass
		#event.Skip()
		
	def UpdateTimes(self):
		self.dateText.SetLabel(datetime.now().strftime("%A %b %d  %I:%M %p"))
		for occupant in self.occupants:
			occupant.UpdateTime()
		self.gridSizer.Layout()
		
class SignInArea():
	def __init__(self, parent, controller):
		if not isinstance(parent, wx.Window):
			raise TypeError("Parent must be a wx.Window")
		
		self.parent = parent
		self.controller = controller
		self.nameList = []
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
		
		self.nameListBox = wx.ListBox(parent, wx.ID_ANY)
		self.nameListBox.Bind(wx.EVT_LISTBOX, self.OnListClick)
		self.nameListBox.Bind(wx.EVT_LISTBOX_DCLICK, self.OnListClick)
		self.sizer.Add(self.nameListBox, 0, wx.EXPAND)
		self.sizer.SetItemMinSize(self.nameListBox, wx.Size(-1, 150))
		
		AddText(parent, self.sizer, medFont, u"What do you want to do?")
		AddButton(parent, self.sizer, u"Work on my bike!", lambda e: self.OnSigninClick(e, "shoptime"))
		AddButton(parent, self.sizer, u"Look for parts!", lambda e: self.OnSigninClick(e, "parts"))
		AddButton(parent, self.sizer, u"Do work trade!", lambda e: self.OnSigninClick(e, "worktrade"))
		AddButton(parent, self.sizer, u"Volunteer!", lambda e: self.OnSigninClick(e, "volunteer"))
		
	def OnNameEntryChange(self, event):
		"Name Entry Change"
		if self.suppressNextListChange:
			self.suppressNextListChange = False
			event.Skip()
			return
			
		self.nameListBox.Clear()
		partialName = self.nameEntry.GetValue()
		partialNameLen = len(partialName)
					
		if partialNameLen > 1:
			self.nameList = self.controller.FindPeopleByPartialName(partialName)
			if len(self.nameList) > 0:
				names = ["{0} {1}".format(n["firstName"], n["lastName"])
					for n in self.nameList]
				self.nameListBox.SetItems(names)

				self.nameListBox.SetSelection(-1)
				for i in range(len(names)):
					if partialName.lower() == names[i].lower():
						self.nameListBox.SetSelection(i)
					break
	
	def OnNameEntryFocus(self, event):
		name = self.nameEntry.GetValue()
		if name == self.nameEntryDefaultText:
			self.nameEntry.SetValue("")
		elif name.lower() != self.nameListBox.GetStringSelection().lower():
			self.nameListBox.SetSelection(-1)
	
	def OnListClick(self, event):
		selection = self.nameListBox.GetStringSelection()
		if selection != "":
			self.suppressNextListChange = True
			self.nameEntry.SetValue(selection)
	
	def OnSigninClick(self, event, type):
		selection = self.nameListBox.GetSelection()
		if selection < 0:
			enteredName = self.nameListBox.GetStringSelection()
			self.controller.ShowNewPersonScreen(enteredName, type)
		else:
			self.controller.SignPersonIn(self.nameList[selection]["id"], type)
			
	def Reset(self):
		self.nameEntry.SetValue(self.nameEntryDefaultText)
		self.nameListBox.Clear()
		self.nameList = []
	
	def GetOuterSizer(self):
		return self.sizer
	
		
class AddPersonArea():
	def __init__(self, parent, controller):
		if not isinstance(parent, wx.Window):
			raise TypeError("Parent must be a wx.Window")
		
		self.parent = parent
		self.controller = controller
		self.nameList = []
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
		
		self.nameListBox = wx.ListBox(parent, wx.ID_ANY)
		self.nameListBox.Bind(wx.EVT_LISTBOX, self.OnListClick)
		self.nameListBox.Bind(wx.EVT_LISTBOX_DCLICK, self.OnListClick)
		self.sizer.Add(self.nameListBox, 0, wx.EXPAND)
		self.sizer.SetItemMinSize(self.nameListBox, wx.Size(-1, 150))
		
		AddText(parent, self.sizer, medFont, u"What do you want to do?")
		AddButton(parent, self.sizer, u"Work on my bike!", lambda e: self.OnSigninClick(e, "shoptime"))
		AddButton(parent, self.sizer, u"Look for parts!", lambda e: self.OnSigninClick(e, "parts"))
		AddButton(parent, self.sizer, u"Do work trade!", lambda e: self.OnSigninClick(e, "worktrade"))
		AddButton(parent, self.sizer, u"Volunteer!", lambda e: self.OnSigninClick(e, "volunteer"))
		
	def OnNameEntryChange(self, event):
		"Name Entry Change"
		if self.suppressNextListChange:
			self.suppressNextListChange = False
			event.Skip()
			return
			
		self.nameListBox.Clear()
		partialName = self.nameEntry.GetValue()
		partialNameLen = len(partialName)
					
		if partialNameLen > 1:
			self.nameList = self.controller.FindPeopleByPartialName(partialName)
			if len(self.nameList) > 0:
				names = ["{0} {1}".format(n["firstName"], n["lastName"])
					for n in self.nameList]
				self.nameListBox.SetItems(names)

				self.nameListBox.SetSelection(-1)
				for i in range(len(names)):
					if partialName.lower() == names[i].lower():
						self.nameListBox.SetSelection(i)
					break
	
	def OnNameEntryFocus(self, event):
		name = self.nameEntry.GetValue()
		if name == self.nameEntryDefaultText:
			self.nameEntry.SetValue("")
		elif name.lower() != self.nameListBox.GetStringSelection().lower():
			self.nameListBox.SetSelection(-1)
	
	def OnListClick(self, event):
		selection = self.nameListBox.GetStringSelection()
		if selection != "":
			self.suppressNextListChange = True
			self.nameEntry.SetValue(selection)
	
	def OnSigninClick(self, event, type):
		selection = self.nameListBox.GetSelection()
		if selection < 0:
			enteredName = self.nameListBox.GetStringSelection()
			self.controller.ShowNewPersonScreen(enteredName, type)
		else:
			self.controller.SignPersonIn(self.nameList[selection]["id"], type)
			
	def Reset(self):
		self.nameEntry.SetValue(self.nameEntryDefaultText)
		self.nameListBox.Clear()
		self.nameList = []
	
	def GetOuterSizer(self):
		return self.sizer	
	
class MainWindow():
	def __init__(self, controller):
				
		self.controller = controller
		controller.SetUI(self)
		
		self.frame = wx.Frame(None, id = wx.ID_ANY, title = u"Welcome To The Bike Church!",
			size = wx.Size(900, 480), style = wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
		
		self.occupantsArea = ShopOccupantsArea(self.frame, controller)
		self.signinArea = SignInArea(self.frame, controller)
		#self.addPersonArea = AddPersonArea(self.frame, controller)
		
		sizer = wx.BoxSizer(wx.HORIZONTAL)		
		sizer.Add(self.signinArea.GetOuterSizer(), 0, wx.ALL, 8)
		sizer.Add(self.occupantsArea.GetOuterSizer(), 1, wx.EXPAND | wx.ALL, 8)
		
		self.frame.SetSizer(sizer)
		self.frame.Layout()
		self.frame.Centre(wx.BOTH)
		self.frame.Show()
		
		self.updateTimer = wx.Timer(self.frame)
		self.updateTimer.Start(1000 * 60)

		self.frame.Bind(wx.EVT_SIZE, self.OnResize)
		self.frame.Bind(wx.EVT_TIMER, self.OnTimer)

	# Frame resize event method
	def OnResize(self, event):
		self.frame.Layout()
	
	def OnTimer(self, event):
		self.occupantsArea.UpdateTimes()
		
	def ResetSignin(self):
		self.signinArea.Reset()
		
	def AddPersonToShopList(self, personID, start, type):
		self.occupantsArea.AddOccupantLine(personID, start, type)
		
	def RemovePersonFromShopList(self, personID):
		self.occupantsArea.RemoveOccupantLine(personID)
