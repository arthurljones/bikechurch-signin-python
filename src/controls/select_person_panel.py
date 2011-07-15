 # -*- coding: utf-8 -*-
 
import wx
from src.ui import MedFont, AddLabel
from src.controller import GetController

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

class ReturnHitEvent(wx.PyCommandEvent):
	eventType = wx.NewEventType()
	def __init__(self, sender, name):
		wx.PyCommandEvent.__init__(self)
		self.SetEventType(ReturnHitEvent.eventType)
		self.SetEventObject(sender)
		self._name = name

	def GetName(self):
		return self._name
	
	def SetName(self, name):
		self._name = name	
wx.EVT_RETURN_HIT = wx.PyEventBinder(ReturnHitEvent.eventType)

class EmptyListClickedEvent(wx.PyCommandEvent):
	eventType = wx.NewEventType()
	def __init__(self, sender):
		wx.PyCommandEvent.__init__(self)
		self.SetEventType(EmptyListClickedEvent.eventType)
		self.SetEventObject(sender)
wx.EVT_EMPTY_LIST_CLICKED = wx.PyEventBinder(EmptyListClickedEvent.eventType)

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
		self._nameEntry = wx.TextCtrl(self, wx.ID_ANY, self._nameEntryDefaultText,
			style = wx.TE_PROCESS_ENTER)
		self._nameEntry.Bind(wx.EVT_TEXT, self._OnNameEntryChange)
		self._nameEntry.Bind(wx.EVT_SET_FOCUS, self._OnNameEntryFocus)
		self._nameEntry.Bind(wx.EVT_TEXT_ENTER, self._OnReturnHit)
		sizer.Add(self._nameEntry, 1, wx.EXPAND)

		AddLabel(self, sizer, MedFont(), listLabel)
		
		self._nameListBox = wx.ListBox(self, wx.ID_ANY)
		self._nameListBox.Bind(wx.EVT_LISTBOX, self._OnListClick)
		self._nameListBox.Bind(wx.EVT_LISTBOX_DCLICK, self._OnListClick)
		self._nameListBox.Bind(wx.EVT_KEY_DOWN, self._OnListKeydown)
		for event in [wx.EVT_LEFT_UP, wx.EVT_MIDDLE_DOWN, wx.EVT_RIGHT_DOWN,
			wx.EVT_LEFT_DCLICK, wx.EVT_MIDDLE_DCLICK, wx.EVT_RIGHT_DCLICK]:
			self._nameListBox.Bind(event, self._OnListDeadSpaceClick)

		sizer.Add(self._nameListBox, 1, wx.EXPAND)
		self._nameListBox.SetSizeHints(200, 80)
	
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
		
	def SetFocus(self):
		self._nameEntry.SetFocus()
	
	def _PopulateList(self, partialName):	
		self._nameListBox.Clear()
		event = PersonSelectedEvent(self, None)
		
		if partialName:
			self._people = GetController().FindPeopleByPartialName(partialName)
			names = [person.Name() for person in self._people]
			
			self._nameListBox.SetItems(names)
			self._nameListBox.SetSelection(-1)
			
			for i in range(len(names)):
				enteredName = partialName.lower().split()
				listName = names[i].lower().split()
				if enteredName == listName:
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
			
	def _OnListDeadSpaceClick(self, event):
		if self._nameListBox.GetCount() == 0:
			self._SendEvent(EmptyListClickedEvent(self))
			
	def _OnReturnHit(self, event):
		selection = self._nameEntry.GetValue()
		self._SendEvent(ReturnHitEvent(self, selection))
		
	def _OnListKeydown(self, event):
		if event.GetKeyCode() == wx.WXK_RETURN:
			selection = self._nameEntry.GetValue()
			self._SendEvent(ReturnHitEvent(self, self.GetNameEntered()))
		else:
			event.Pass()
		
	def GetNameEntryWidget(self):
		return self._nameEntry
		
	def GetNameListWidget(self):
		return self._nameListBox
			
