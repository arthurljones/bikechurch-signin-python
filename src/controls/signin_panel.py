 # -*- coding: utf-8 -*-
 
import wx
from math import ceil
from ..ui_utils import MedFont, MakeStaticBoxSizer
from shoptime_choice import ShoptimeChoice

class SignInPanel(wx.Panel):
	def __init__(self, parent, controller):
		wx.Window.__init__(self, parent)	
		self._controller = controller
		self._suppressNextListChange = False
		
		sizer = MakeStaticBoxSizer(self, style = wx.VERTICAL)
		self.SetSizer(sizer)
		
		hugeFont = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTWEIGHT_BOLD, wx.NORMAL)
		self._AddLabel(sizer, hugeFont, u"Sign In Here", wx.ALIGN_CENTER)
		self._AddLabel(sizer, MedFont(), u"Hi! What's your name?")
		
		self._nameEntryDefaultText = u"Type your name here."
		self._nameEntry = wx.TextCtrl(self, wx.ID_ANY, self._nameEntryDefaultText)
		self._nameEntry.Bind(wx.EVT_TEXT, self._OnNameEntryChange)
		self._nameEntry.Bind(wx.EVT_SET_FOCUS, self._OnNameEntryFocus)
		sizer.Add(self._nameEntry, 0, wx.EXPAND)
		
		self._AddLabel(sizer, MedFont(),
			u"If you've been here before,\nclick your name in the list:")
		
		self._nameListBox = wx.ListBox(self, wx.ID_ANY)
		self._nameListBox.Bind(wx.EVT_LISTBOX, self._OnListClick)
		self._nameListBox.Bind(wx.EVT_LISTBOX_DCLICK, self._OnListClick)
		sizer.Add(self._nameListBox, 1, wx.EXPAND)
		
		self._shoptimeChoice = ShoptimeChoice(self, self._OnSigninClick)
		sizer.Add(self._shoptimeChoice, 0, wx.EXPAND)
		
		self._shoptimeChoice.Disable()
	
	def _AddLabel(self, sizer, font, string, flags = 0):
		text = wx.StaticText(self, wx.ID_ANY, string)
		if font is not None:
			text.SetFont(font)
		sizer.Add(text, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL | flags, 5)
		return text
		
	def _PopulateList(self, partialName):	
		self._nameListBox.Clear()
		if partialName:
			self._people = self._controller.FindPeopleByPartialName(partialName)
			names = [person.Name() for person in self._people]
			
			self._nameListBox.SetItems(names)
			self._nameListBox.SetSelection(-1)
			
			for i in range(len(names)):
				if partialName.lower() == names[i].lower():
					self._nameListBox.SetSelection(i)
					break
							
	def _OnNameEntryChange(self, event):
		partialName = self._nameEntry.GetValue().strip()
		nameEntered = partialName != "" and partialName != self._nameEntryDefaultText
		self._shoptimeChoice.Enable(nameEntered)
		
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
			self._suppressNextListChange = True
			self._nameEntry.SetValue(selection)
	
	def _OnSigninClick(self, event, type):
		if type == "worktrade":
			if not self._controller.AuthenticateMechanic("do worktrade"):
				return
				
		elif type == "volunteer":
			if not self._controller.AuthenticateMechanic("volunteer"):
				return
			
		selection = self._nameListBox.GetSelection()
		if self._nameListBox.GetCount() == 0 or selection < 0:
			name = self._nameEntry.GetValue()
			nameWords = name.split()
			numWords = len(nameWords)
			halfWords = int(ceil(numWords / 2.0))
			firstName = " ".join(nameWords[:halfWords])
			lastName = " ".join(nameWords[halfWords:])
			
			if self._controller.ShowNewPersonDialog(firstName, lastName):
				self._controller.SignPersonIn(None, type)
				self.ResetValues()
		else:
			if self._controller.SignPersonIn(self._people[selection], type):
				self.ResetValues()
			
	def ResetValues(self):
		self._nameEntry.SetValue(self._nameEntryDefaultText)
		self._nameListBox.Clear()
		self.nameList = []
