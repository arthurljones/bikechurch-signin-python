 # -*- coding: utf-8 -*-
 
import wx
from datetime import datetime
from ..ui import FormatTimedelta, GetShoptimeTypeDescription
from ..controller import GetController

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

		def AddOccupantLabel(string, flags = 0):
			text = wx.StaticText(parent, wx.ID_ANY, string)
			text.SetFont(wx.Font(9, wx.FONTFAMILY_SWISS, wx.NORMAL, wx.NORMAL))
			sizer.Add(text, 0, wx.ALIGN_CENTER_VERTICAL | flags)
			self._elements.append(text)
			return text

		AddOccupantLabel(person.Name())
		AddOccupantLabel(u"{0}".format(GetShoptimeTypeDescription(type)))
		self.timeText = AddOccupantLabel(u"", wx.ALIGN_RIGHT)
		
		buttonSizer = wx.BoxSizer()
		self._elements.append(buttonSizer)
		sizer.Add(buttonSizer, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
		
		def AddOccupantButton(string, onClick):
			button = wx.Button(parent, wx.ID_ANY, string)
			button.SetMaxSize(wx.Size(-1, 25))
			buttonSizer.Add(button, 1, wx.ALIGN_CENTER_VERTICAL)
			button.Bind(wx.EVT_BUTTON, onClick)
			self._elements.append(button)
			
		AddOccupantButton(u"View Info", self.OnViewInfoClicked)
		AddOccupantButton(u"Sign Out", self.OnSignOutClicked)
		
		self.UpdateTime()
		 
	def GetPerson(self):
		return self._person
	
	def GetElements(self):
		return self._elements
		
	def OnViewInfoClicked(self, event):
		GetController().ViewPersonInfo(self._parent, self._person)
		
	def OnSignOutClicked(self, event):
		GetController().SignPersonOut(self._person)
		
	def UpdateTime(self):
		self.timeText.SetLabel(FormatTimedelta(datetime.now() - self._startTime))
		
class OccupantsList(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)
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
		
		self._scrollbox = wx.ScrolledWindow(self)

		self._listSizer = wx.FlexGridSizer(rows = 0, cols = 4, hgap = 10, vgap = 0)
		self._listSizer.SetFlexibleDirection(wx.BOTH)
		self._listSizer.AddGrowableCol(1, 1)
		self._listSizer.AddGrowableCol(2, 1)
		self._scrollbox.SetSizer(self._listSizer)
		self._scrollbox.SetScrollRate(0, 20)
		self._scrollbox.Bind(wx.EVT_SCROLLWIN_THUMBTRACK, self.OnThumbTrack)
		
		def AddColumnHeader(name, flags = 0):
			label = wx.StaticText(self._scrollbox, wx.ID_ANY, name)
			label.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.NORMAL, wx.NORMAL))
			localSizer = wx.BoxSizer(wx.VERTICAL)
			localSizer.Add(label, flag = flags)
			localSizer.Add(wx.StaticLine(self._scrollbox), 0, wx.EXPAND)
			self._listSizer.Add(localSizer, 0, wx.ALIGN_CENTER | wx.EXPAND)	

		AddColumnHeader(u"Name")
		AddColumnHeader(u"Activity")
		AddColumnHeader(u"Time In Shop", wx.ALIGN_RIGHT)
		AddColumnHeader(u"")
		
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
	
	def AddOccupant(self, person, startTime, type):
		occupant = OccupantLine(self._scrollbox, self._listSizer, person, startTime, type)
		self.occupants.append(occupant)
		self._listSizer.Layout()
	
	def RemoveOccupant(self, person):
		for occupant in self.occupants:
			if occupant.GetPerson() is person:
				for element in occupant.GetElements():
					self._listSizer.Detach(element)
					element.Destroy()
				self.occupants.remove(occupant)
				break
											
		self._listSizer.Layout()
				
	def OnThumbTrack(self, event):
		pass
			
	def OnTimer(self, event):
		self.UpdateTimes()
		
	def UpdateTimes(self):
		self.dateText.SetLabel(datetime.now().strftime("%A %b %d  %I:%M %p"))
		for occupant in self.occupants:
			occupant.UpdateTime()
		self._listSizer.Layout()
