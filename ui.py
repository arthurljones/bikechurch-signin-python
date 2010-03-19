import db
import wx
from datetime import datetime, timedelta
from copy import copy

sWhitespace = ' \t\n'

sTypeDescriptions = {
	"shoptime":	"Working on a Bike",
	"parts":	"Looking for Parts",
	"worktrade":	"Doing Worktrade",
	"volunteer":	"Volunteering"
	}


sBikeChurchStatement = \
	u"About the Bike Church:\n\n\tLorem ipsum dolor sit amet, consectetur adipiscing elit." \
	u" Nunc vulputate nibh id nisl luctus vel volutpat nisl euismod. Quisque sit amet odio " \
	u"enim, ut porttitor felis. Maecenas in lectus orci. In adipiscing, tellus a pretium " \
	u"convallis, erat ante posuere augue, sit amet blandit tellus dui eu nunc. Donec " \
	u"vehicula condimentum nulla sit amet posuere. Donec ac arcu a leo iaculis faucibus. " \
	u"Aenean vestibulum turpis mattis neque aliquet in mattis lectus sollicitudin. " \
	u"Phasellus neque odio, lacinia sit amet sodales vel, gravida a ligula. Cras ut velit " \
	u"arcu, non aliquam urna. Praesent vitae quam vel neque commodo pretium ut in ipsum. " \
	u"Curabitur. "


def SplitAndKeep(string, splitchars = " \t\n"):
	substrs = []
	
	i = 0
	while len(string) > 0:
		if string[i] in splitchars:
			substrs.append(string[:i])
			substrs.append(string[i])
			string = string[i+1:]
			i = 0
		else:
			i += 1
			if i >= len(string):	
				substrs.append(string)
				break
		
	return substrs

class AutowrappedStaticText(wx.StaticText):
	"""A StaticText-like widget which implements word wrapping."""
	def __init__(self, *args, **kwargs):
		wx.StaticText.__init__(self, *args, **kwargs)
		self.label = super(AutowrappedStaticText, self).GetLabel()
		self.pieces = SplitAndKeep(self.label, sWhitespace)
		self.Bind(wx.EVT_SIZE, self.OnSize)
		self.lastWrap = None
		self.Wrap()

	def SetLabel(self, newLabel):
		"""Store the new label and recalculate the wrapped version."""
		self.label = newLabel
		self.pieces = SplitAndKeep(self.label, sWhitespace)
		self.Wrap()

	def GetLabel(self):
		"""Returns the label (unwrapped)."""
		return self.label
	
	def Wrap(self):		
		"""Wraps the words in label."""
		maxWidth = self.GetParent().GetVirtualSizeTuple()[0] - 10

		#TODO: Fix this so that we're not wasting cycles, but so that it actually works
		#if self.lastWrap and self.lastWrap == maxWidth:
		#	return
			
		self.lastWrap = maxWidth	

		pieces = copy(self.pieces)
		lines = []
		currentLine = []
		currentString = ""

		while len(pieces) > 0:			
			nextPiece = pieces.pop(0)
			newString = currentString + nextPiece
			newWidth = self.GetTextExtent(newString)[0]
			currentPieceCount = len(currentLine)
			
			if (currentPieceCount > 0 and newWidth > maxWidth) or nextPiece == '\n':
				if currentPieceCount > 0 and currentLine[-1] in sWhitespace:
					currentLine = currentLine[:-1]
				if nextPiece in sWhitespace:
					pieces = pieces[1:]
						
				currentLine.append('\n')
				
				lines.extend(currentLine)
				currentLine = [nextPiece]
				currentString = nextPiece
			else:
				currentString += nextPiece
				currentLine.append(nextPiece)

		lines.extend(currentLine)
		line = "".join(lines)
		super(AutowrappedStaticText, self).SetLabel(line)
		self.Refresh()

	def OnSize(self, event):
		self.Wrap()

def MakeInfoEntrySizer():
	sizer = wx.FlexGridSizer(0, 2)
	sizer.AddGrowableCol(1)
	return sizer

def AddField(parent, sizer, font, label, entryKind = wx.TextCtrl):
	text = wx.StaticText(parent, wx.ID_ANY, label)
	text.SetFont(font)
	parent.GetSizer().Add(text, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 5)
	field = entryKind(parent, wx.ID_ANY)
	parent.GetSizer().Add(field, 0, wx.EXPAND)
	return field
	
def AddLabel(parent, sizer, font, string, flags = 0, type = wx.StaticText):
	label = type(parent, wx.ID_ANY, string)
	label.SetFont(font)
	sizer.Add(label, 0, flags | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
	return label

def GetShoptimeTypeDescription(type):
	if type in sTypeDescriptions:
		return sTypeDescriptions[type]
	else:
		return "\"{0}\"".format(type)

class ShoptimeChoiceArea(wx.Panel):
	def __init__(self, parent, onClick, sizer = wx.BoxSizer(wx.VERTICAL)):
		wx.Panel.__init__(self, parent)
		
		self.SetSizer(sizer)
		medFont = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
		buttonFont = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)

		def AddButton(string, type):
			button = wx.Button(self, wx.ID_ANY, string)
			button.SetFont(buttonFont)
			sizer.Add(button, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
			button.Bind(wx.EVT_BUTTON, lambda e: onClick(e, type))
		
		AddLabel(self, sizer, medFont, u"What do you want to do?")
		sizer.AddSpacer((0, 0), 0, wx.EXPAND)
		AddButton(u"Work on my bike!", "shoptime")
		AddButton(u"Look for parts!", "parts")
		AddButton(u"Do work trade!", "worktrade")
		AddButton(u"Volunteer!", "volunteer")
		

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
		
class ShopOccupantsArea(wx.Panel):
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
				self.AddOccupantLine(person["personID"], person["start"], person["type"])
		
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
		
		self.UpdateTimes()
	
	def AddColumnHeader(self, sizer, name):
		label = wx.StaticText(self.scrollbox, wx.ID_ANY, name)
		label.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.NORMAL, wx.NORMAL))
		localSizer = wx.BoxSizer(wx.VERTICAL)
		localSizer.Add(label)
		localSizer.Add(wx.StaticLine(self.scrollbox), 0, wx.EXPAND)
		sizer.Add(localSizer, 0, wx.ALIGN_CENTER | wx.EXPAND)	
	
	def AddOccupantLine(self, personID, startTime, type):
		occupant = ShopOccupantLine(self.scrollbox, self.listSizer,
			self.controller, personID, startTime, type)
		self.occupants.append(occupant)
		
		if hasattr(self, "listSizer"):
			self.listSizer.Layout()
		if hasattr(self, "gridSizer"):
			gridSizer.Layout()
	
	def RemoveOccupantLine(self, personID):
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
		
	def UpdateTimes(self):
		self.dateText.SetLabel(datetime.now().strftime("%A %b %d  %I:%M %p"))
		for occupant in self.occupants:
			occupant.UpdateTime()
		self.listSizer.Layout()
		
class SignInArea(wx.Panel):
	def __init__(self, parent, controller):
		wx.Window.__init__(self, parent)	
		self.controller = controller
		self.nameList = []
		self.suppressNextListChange = False
		
		staticBox = wx.StaticBox(self)
		sizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
		self.SetSizer(sizer)
		
		bigFont = wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTWEIGHT_BOLD, wx.NORMAL)
		medFont = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
		self.AddLabel(sizer, bigFont, u"Sign In Here", wx.ALIGN_CENTER)
		self.AddLabel(sizer, medFont, u"Hi! What's your name?")
		
		self.nameEntryDefaultText = u"Type your name here."
		self.nameEntry = wx.TextCtrl(self, wx.ID_ANY, self.nameEntryDefaultText)
		self.nameEntry.Bind(wx.EVT_TEXT, self.OnNameEntryChange)
		self.nameEntry.Bind(wx.EVT_SET_FOCUS, self.OnNameEntryFocus)
		sizer.Add(self.nameEntry, 0, wx.EXPAND)
		
		self.AddLabel(sizer, medFont, u"If you've been here before,\nclick your name in the list:")
		
		self.nameListBox = wx.ListBox(self, wx.ID_ANY)
		self.nameListBox.Bind(wx.EVT_LISTBOX, self.OnListClick)
		self.nameListBox.Bind(wx.EVT_LISTBOX_DCLICK, self.OnListClick)
		sizer.Add(self.nameListBox, 0, wx.EXPAND)
		sizer.SetItemMinSize(self.nameListBox, wx.Size(-1, 150))
		
		self.shoptimeChoice = ShoptimeChoiceArea(self, self.OnSigninClick)
		sizer.Add(self.shoptimeChoice, 0, wx.EXPAND)
		sizer.SetMinSize((200, 0))
	
	def AddLabel(self, sizer, font, string, flags = 0):
		text = wx.StaticText(self, wx.ID_ANY, string)
		if font is not None:
			text.SetFont(font)
		sizer.Add(text, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL | flags, 5)
		return text
		
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
		if self.nameListBox.GetCount() > 0 or selection < 0:
			enteredName = self.nameListBox.GetStringSelection()
			self.controller.ShowNewPersonScreen(enteredName, type)
		else:
			self.controller.SignPersonIn(self.nameList[selection]["id"], type)
			
	def Reset(self):
		self.nameEntry.SetValue(self.nameEntryDefaultText)
		self.nameListBox.Clear()
		self.nameList = []


class BikeInfoEntryArea(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)
		
		bikes = ["Mountain Bike", "Road Bike", "Hybrid", 
			"Cruiser", "Three Speed", "Recumbent", "Chopper",
			"Mixte", "Tallbike", "Town Bike"]
		bikes.sort()
		bikes.append("Other")
		
		sizer = MakeInfoEntrySizer()
		self.SetSizer(sizer)
		medFont = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
		AddBikeField = lambda *args: AddField(self, sizer, medFont, *args)
		self.color = AddBikeField("Color:")
		self.type = AddBikeField("Type:", wx.Choice)
		self.type.SetItems(bikes)
		self.maker = AddBikeField("Maker:")
		self.model = AddBikeField("Model:")
		self.serial = AddBikeField("Serial #:")
		
	def Validate(self):
		pass
		
	def GetValues(self):
		return {
			"color":	self.color.GetValue(),
			"type":		self.type.GetValue(),
			"maker":	self.maker.GetValue(),
			"model":	self.model.GetValue(),
			"serial":	self.serial.GetValue(),
			}
		
class NameInfoEntryArea(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)
		
		sizer = MakeInfoEntrySizer()
		self.SetSizer(sizer)
		medFont = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
		AddBikeField = lambda *args: AddField(self, sizer, medFont, *args)
		self.color = AddBikeField("First name:")
		self.maker = AddBikeField("Last name:")
		
	def Validate(self):
		pass
		
	def GetValues(self):
		pass
		
class AddPersonArea(wx.Panel):
	def __init__(self, parent, controller):
		wx.Panel.__init__(self, parent)	
		self.controller = controller
		
		staticBox = wx.StaticBox(self, wx.ID_ANY, "")
		outerSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
		self.SetSizer(outerSizer)
		
		medFont = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)

		AddLabel(self, outerSizer, medFont, \
			u"It looks like you haven't used this "
			u"sign-in computer before. "
			u"Please tell us about yourself and your bike.", type = AutowrappedStaticText)
		
		staticBox = wx.StaticBox(self, wx.ID_ANY, u"Your Name")
		nameEntrySizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
		AddLabel(self, nameEntrySizer, medFont, u"Type your name:")
		self.nameInfoEntry = NameInfoEntryArea(self)
		nameEntrySizer.Add(self.nameInfoEntry, 0, wx.EXPAND)
		outerSizer.Add(nameEntrySizer, 0, wx.EXPAND)
		
		staticBox = wx.StaticBox(self, wx.ID_ANY, "Your Bike")
		bikeEntrySizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
		AddLabel(self, bikeEntrySizer, medFont, "If you have a bike, describe it:")			
		self.bikeInfoEntry = BikeInfoEntryArea(self)
		bikeEntrySizer.Add(self.bikeInfoEntry, 0, wx.EXPAND)
		outerSizer.Add(bikeEntrySizer, 0, wx.EXPAND)
		
		shoptimeSizer = wx.FlexGridSizer(0, 2)
		shoptimeSizer.SetFlexibleDirection(wx.VERTICAL)
		self.shoptimeChoice = ShoptimeChoiceArea(self, self.OnSigninClick, shoptimeSizer)
		outerSizer.Add(self.shoptimeChoice, 0, wx.EXPAND)

		self.GetSizer().SetMinSize((200, 0))
	
	def OnSigninClick(self, event, type):
		pass
		
class BikeChurchStatementArea(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)
        
		self.staticBox = wx.StaticBox(self, wx.ID_ANY, u"About The Bike Church")
		sizer = wx.StaticBoxSizer(self.staticBox, wx.HORIZONTAL)
		self.SetSizer(sizer)
		
		medFont = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
		text = AutowrappedStaticText(self, wx.ID_ANY, sBikeChurchStatement)
		text.SetFont(medFont)
		sizer.Add(text, 1, wx.EXPAND)

class Screen(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)

		self.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
		self.elements = []
		
		self.Hide()

	def AddElement(self, element):
		self.elements.append(element)

	def Show(self):
		sizer = self.GetParent().GetSizer()
		sizer.Add(self, 1, wx.EXPAND)
		wx.Panel.Show(self)
		self.Layout()
		
	def Hide(self):
		wx.Panel.Hide(self)
		sizer = self.GetContainingSizer()
		if sizer:
			sizer.Detach(self)
			
	def Layout(self):
		for element in self.elements:
			element.Layout()
		wx.Panel.Layout(self)
			
class AddPersonScreen(Screen):
	def __init__(self, parent, controller):
		Screen.__init__(self, parent)
		
		sizer = wx.FlexGridSizer(0, 2)
		sizer.SetFlexibleDirection(wx.HORIZONTAL)
		sizer.AddGrowableCol(1)
		self.SetSizer(sizer)
		
		self.addPersonArea = AddPersonArea(self, controller)
		self.bikeChurchStatement = BikeChurchStatementArea(self)
		
		self.GetSizer().Add(self.addPersonArea, 1, wx.ALL | wx.EXPAND, 3)
		self.GetSizer().Add(self.bikeChurchStatement, 1, wx.EXPAND | wx.ALL, 3)
		
		self.AddElement(self.addPersonArea)
		self.AddElement(self.bikeChurchStatement)

class MainScreen(Screen):
	def __init__(self, parent, controller):
		Screen.__init__(self, parent)
		
		self.occupantsArea = ShopOccupantsArea(self, controller)
		self.signinArea = SignInArea(self, controller)
		
		self.GetSizer().Add(self.signinArea, 0, wx.ALL, 8)
		self.GetSizer().Add(self.occupantsArea, 1, wx.EXPAND | wx.ALL, 8)
		
		self.AddElement(self.occupantsArea)
		self.AddElement(self.signinArea)

class MainWindow():
	def __init__(self, controller):
				
		self.controller = controller
		controller.SetUI(self)
		
		self.frame = wx.Frame(None, id = wx.ID_ANY, title = u"Welcome To The Bike Church!",
			size = wx.Size(900, 480), style = wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
		
		self.screens = []
		
		self.mainScreen = MainScreen(self.frame, controller)
		self.screens.append(self.mainScreen)
		self.addPersonScreen = AddPersonScreen(self.frame, controller)
		self.screens.append(self.addPersonScreen)
		
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.frame.SetSizer(sizer)
		self.frame.Centre(wx.BOTH)
		self.frame.Show()
		
		#self.ShowAddPersonScreen()
		self.ShowMainScreen()
		
		self.updateTimer = wx.Timer(self.frame)
		self.updateTimer.Start(1000 * 60)

		self.frame.Bind(wx.EVT_SIZE, self.OnResize)
		self.frame.Bind(wx.EVT_TIMER, self.OnTimer)

	def HideAllScreens(self):
		for screen in self.screens:
			screen.Hide()

	def ShowMainScreen(self):
		self.HideAllScreens()
		self.mainScreen.Show()
		self.frame.Layout()
		
	def ShowAddPersonScreen(self):
		self.HideAllScreens()
		self.addPersonScreen.Show()
		self.frame.Layout()
		
	def Layout(self):
		for screen in self.screens:
			screen.Layout()
		self.frame.Layout()
		
	def OnResize(self, event):
		self.Layout()
	
	def OnTimer(self, event):
		self.occupantsArea.UpdateTimes()
		
	def ResetSignin(self):
		self.signinArea.Reset()
		
	def AddPersonToShopList(self, personID, start, type):
		self.occupantsArea.AddOccupantLine(personID, start, type)
		
	def RemovePersonFromShopList(self, personID):
		self.occupantsArea.RemoveOccupantLine(personID)
