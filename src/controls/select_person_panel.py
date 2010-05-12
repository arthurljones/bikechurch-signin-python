 # -*- coding: utf-8 -*-
 
import wx
from ..ui import MedFont, AddLabel
from ..controller import GetController

class NameEnteredEvent(wx.PyCommandEvent):
	eventType = wx.NewEventType()
	def __init__(self, sender, name):
		wx.PyCommandEvent.__init__(self)
		self.SetEventType(NameEnteredEvent.eventType)
		self.SetEventObject(sender)
		self._name = name

	def GetName(self):
		return self._name
	
	def SetName(self, name):
		self._name = name
		
wx.EVT_NAME_ENTERED = wx.PyEventBinder(NameEnteredEvent.eventType)

class PersonSelectedEvent(wx.PyCommandEvent):
	eventType = wx.NewEventType()
	def __init__(self, sender, person):
		wx.PyCommandEvent.__init__(self)
		self.SetEventType(PersonSelectedEvent.eventType)
		self.SetEventObject(sender)
		self._person = person

	def GetPerson(self):
		return self._person
	
	def SetPerson(self, person):
		self._person = person
		
wx.EVT_PERSON_SELECTED = wx.PyEventBinder(PersonSelectedEvent.eventType)

class SelectPersonPanel(wx.Panel):
	def __init__(self, parent, defaultEntry = "", listLabel = ""):
		wx.Panel.__init__(self, parent)
		self._suppressNextListChange = False
		
		sizer = wx.FlexGridSizer(3, 1)
		sizer.AddGrowableRow(2)
		self.SetSizer(sizer)
		
		self._nameEntryDefaultText = defaultEntry
		self._nameEntry = wx.TextCtrl(self, wx.ID_ANY, self._nameEntryDefaultText)
		self._nameEntry.Bind(wx.EVT_TEXT, self._OnNameEntryChange)
		self._nameEntry.Bind(wx.EVT_SET_FOCUS, self._OnNameEntryFocus)
		sizer.Add(self._nameEntry, 1, wx.EXPAND)

		AddLabel(self, sizer, MedFont(), listLabel)
		
		self._nameListBox = wx.ListBox(self, wx.ID_ANY)
		self._nameListBox.Bind(wx.EVT_LISTBOX, self._OnListClick)
		self._nameListBox.Bind(wx.EVT_LISTBOX_DCLICK, self._OnListClick)
		sizer.Add(self._nameListBox, 1, wx.EXPAND)
	
	def GetDefaultName(self):
		return self._nameEntryDefaultText
		
	def GetPerson(self):
		selection = self._nameListBox.GetSelection()
		if self._nameListBox.GetCount() > 0 and selection >= 0:
			return self._people[selection]
		else:
			return None
		
	def GetNameEntered(self):
		return self._nameEntry.GetValue()
		
	def ResetValues(self):
		self._nameEntry.SetValue(self._nameEntryDefaultText)
		self._nameListBox.Clear()
	
	def _PopulateList(self, partialName):	
		self._nameListBox.Clear()
		event = PersonSelectedEvent(self, None)
		
		if partialName:
			self._people = GetController().FindPeopleByPartialName(partialName)
			names = [person.Name() for person in self._people]
			
			self._nameListBox.SetItems(names)
			self._nameListBox.SetSelection(-1)
			
			for i in range(len(names)):
				if partialName.lower() == names[i].lower():
					self._nameListBox.SetSelection(i)
					event.SetPerson(self._people[i])
					break
	
		self._SendEvent(event)
	
	def _SendEvent(self, event):
		self.GetEventHandler().AddPendingEvent(event)
	
	def _OnNameEntryChange(self, event):
		partialName = self._nameEntry.GetValue().strip()
		self._SendEvent(NameEnteredEvent(self, partialName))
		
		if self._suppressNextListChange:
			self._suppressNextListChange = False
		else:
			self._PopulateList(partialName)
			
	def _OnNameEntryFocus(self, event):
		name = self._nameEntry.GetValue()
		if name == self._nameEntryDefaultText:
			self._nameEntry.SetValue("")
		elif name.lower() != self._nameListBox.GetStringSelection().lower():
			self._nameListBox.SetSelection(-1)
	
	def _OnListClick(self, event):
		selection = self._nameListBox.GetStringSelection()
		if selection != "":
			person = self._people[self._nameListBox.GetSelection()]
			self._SendEvent(PersonSelectedEvent(self, person))
			self._suppressNextListChange = True
			self._nameEntry.SetValue(selection)
			
