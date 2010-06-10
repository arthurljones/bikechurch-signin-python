 # -*- coding: utf-8 -*-
 
import wx
from datetime import datetime
from ..ui import FormatTimedelta, GetShoptimeTypeDescription
from ..controller import GetController
from ..strings import trans

class OccupantLine():	
	def __init__(self, parent, sizer, person, startTime, type):
		self._parent = parent
		self._person = person
		self._startTime = startTime
		type = type
		self._elements = []
		
		possesiveChar = "s"
		if self._person.firstName and self._person.firstName[-1] == "s":
			possesiveChar = ""

		buttonSizer = wx.BoxSizer()
		self._elements.append(buttonSizer)
		sizer.Add(buttonSizer, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
		
		def AddOccupantButton(string, onClick):
			button = wx.Button(parent, wx.ID_ANY, string)
			button.SetMaxSize(wx.Size(-1, 25))
			buttonSizer.Add(button, 1, wx.ALIGN_CENTER_VERTICAL)
			button.Bind(wx.EVT_BUTTON, onClick)
			self._elements.append(button)
			
		AddOccupantButton(trans.occupantViewButton, self.OnViewInfoClicked)
		AddOccupantButton(trans.occupantSignoutButton, self.OnSignOutClicked)

		def AddOccupantLabel(string, flags = 0):
			text = wx.StaticText(parent, wx.ID_ANY, string)
			text.SetFont(wx.Font(9, wx.FONTFAMILY_SWISS, wx.NORMAL, wx.NORMAL))
			sizer.Add(text, 0, wx.ALIGN_CENTER_VERTICAL | flags)
			self._elements.append(text)
			return text

		self._name = AddOccupantLabel(person.Name())
		self._type = AddOccupantLabel(u"{0}".format(GetShoptimeTypeDescription(type)))
		self._timeText = AddOccupantLabel(u"", wx.ALIGN_RIGHT)
		
		self.UpdateTime()
		 
	def GetPerson(self):
		return self._person
	
	def GetElements(self):
		return self._elements
		
	def GetVerticalPos(self):
		return self._timeText.GetPosition()[1]
		
	def GetNameWidget(self):
		return self._name
		
	def OnViewInfoClicked(self, event):
		GetController().ViewPersonInfo(self._parent, self._person)
		
	def OnSignOutClicked(self, event):
		GetController().SignPersonOut(self._person)
		
	def UpdateTime(self):
		self._timeText.SetLabel(FormatTimedelta(datetime.now() - self._startTime))
		
class OccupantsList(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)
		self.occupants = []

		titleFont = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
		self.titleText = wx.StaticText(self, wx.ID_ANY, trans.occupantListHeader)
		self.titleText.SetFont(titleFont)
		self.dateText = wx.StaticText(self, wx.ID_ANY, u"")
		self.dateText.SetFont(titleFont)
		
		titleSizer = wx.BoxSizer()
		titleSizer.Add(self.titleText, 0, wx.ALL, 5)
		titleSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)
		titleSizer.Add(self.dateText, 0, wx.ALL, 5)
		
		self._scrollRate = 20
		self._scrollbox = wx.ScrolledWindow(self)
		self._scrollbox.SetScrollRate(0, self._scrollRate)
		self._scrollSizer = wx.BoxSizer()
		self._scrollbox.SetSizer(self._scrollSizer)
		
		self._gridContainer = wx.Panel(self._scrollbox)
		self._scrollSizer.Add(self._gridContainer, 1, wx.EXPAND)

		self._listSizer = wx.FlexGridSizer(rows = 0, cols = 4, hgap = 10, vgap = 0)
		self._listSizer.SetFlexibleDirection(wx.BOTH)
		self._listSizer.AddGrowableCol(1, 1)
		self._listSizer.AddGrowableCol(2, 1)
		self._gridContainer.SetSizer(self._listSizer)
			
		def AddColumnHeader(name, flags = 0):
			label = wx.StaticText(self._gridContainer, wx.ID_ANY, name)
			label.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.NORMAL, wx.NORMAL))
			localSizer = wx.BoxSizer(wx.VERTICAL)
			localSizer.Add(label, flag = flags)
			localSizer.Add(wx.StaticLine(self._gridContainer), 0, wx.EXPAND)
			self._listSizer.Add(localSizer, 0, wx.ALIGN_CENTER | wx.EXPAND)	
		
		AddColumnHeader(u"")
		AddColumnHeader(trans.occupantColumnName)
		AddColumnHeader(trans.occupantColumnActivity)
		AddColumnHeader(trans.occupantColumnTime, wx.ALIGN_RIGHT)

		peopleInShop = GetController().GetPeopleInShop()
		if peopleInShop is not None:
			for person in peopleInShop:
				self.AddOccupant(person,
					person.occupantInfo.start, person.occupantInfo.type)

		gridSizer = wx.FlexGridSizer(2, 1)
		gridSizer.SetFlexibleDirection(wx.BOTH)
		gridSizer.AddGrowableCol(0)
		gridSizer.AddGrowableRow(1)
		gridSizer.Add(titleSizer, 1, wx.EXPAND)
		gridSizer.Add(self._scrollbox, 1, wx.EXPAND)
		self.SetSizer(gridSizer)
		
		self.Bind(wx.EVT_TIMER, self.OnTimer)
		self.updateTimer = wx.Timer(self)
		self.updateTimer.Start(1000)
		
		self.UpdateTimes()
	
	def _GetOccupant(self, person):
		for occupant in self.occupants:
			if occupant.GetPerson() is person:
				return occupant
	
	def AddOccupant(self, person, startTime, type):
		occupant = OccupantLine(self._gridContainer , self._listSizer, person, startTime, type)
		self.occupants.append(occupant)					
		self._scrollbox.FitInside()
		self._scrollbox.Scroll(-1, occupant.GetVerticalPos() / self._scrollRate)
	
	def RemoveOccupant(self, person):
		occupant = self._GetOccupant(person)
		if occupant:
			for element in occupant.GetElements():
				self._listSizer.Detach(element)
				element.Destroy()
			self.occupants.remove(occupant)
											
		self._scrollbox.FitInside()

	def GetOccupantNameWidget(self, person):
		occupant = self._GetOccupant(person)
		if occupant:
			return occupant.GetNameWidget()
		else:
			return None

	def OnTimer(self, event):
		self.UpdateTimes()
		
	def UpdateTimes(self):
		self.dateText.SetLabel(datetime.now().strftime("%A %b %d  %I:%M %p"))
		for occupant in self.occupants:
			occupant.UpdateTime()
		self._listSizer.Layout()
