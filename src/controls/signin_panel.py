 # -*- coding: utf-8 -*-
 
import wx
from math import ceil
from ..ui import MedFont, HugeFont, MakeStaticBoxSizer, AddLabel
from shoptime_choice import ShoptimeChoicePanel
from select_person_panel import SelectPersonPanel
from ..controller import GetController

class SignInPanel(wx.Panel):
	def __init__(self, parent):
		wx.Window.__init__(self, parent)
		self._suppressNextListChange = False
		
		sizer = MakeStaticBoxSizer(self, style = wx.VERTICAL)
		self.SetSizer(sizer)
		
		AddLabel(self, sizer, HugeFont(), u"Sign In Here", wx.ALIGN_CENTER)
		AddLabel(self, sizer, MedFont(), u"Hi! What's your name?")
		
		self._selectPerson = SelectPersonPanel(self, u"Type your name here.",
			u"If you've been here before,\nclick your name in the list:")
		sizer.Add(self._selectPerson, 1, wx.EXPAND)
		
		self._shoptimeChoice = ShoptimeChoicePanel(self)
		sizer.Add(self._shoptimeChoice, 0, wx.EXPAND)
		
		self.Bind(wx.EVT_NAME_ENTERED, self._OnNameEntered)
		self.Bind(wx.EVT_PERSON_SELECTED, lambda e: "{0} selected".format(e.GetPerson()))
		self.Bind(wx.EVT_SHOPTIME_CHOICE, self._OnShoptimeChoice)
		
		self._shoptimeChoice.Disable()
			
	def _OnNameEntered(self, event):
		name = event.GetName()
		nameEntered = name != "" and name != self._selectPerson.GetDefaultName()
		self._shoptimeChoice.Enable(nameEntered)
	
	def _OnShoptimeChoice(self, event):
		type = event.GetType()
		
		if type == "worktrade":
			if not GetController().AuthenticateMechanic(self, "do worktrade"):
				return
				
		elif type == "volunteer":
			if not GetController().AuthenticateMechanic(self, "volunteer"):
				return
			
		person = self._selectPerson.GetPerson()
		if person:
			if GetController().SignPersonIn(person, type):
				self.ResetValues()
		else:
			name = self._selectPerson.GetNameEntered()
			nameWords = name.split()
			numWords = len(nameWords)
			halfWords = int(ceil(numWords / 2.0))
			firstName = " ".join(nameWords[:halfWords])
			lastName = " ".join(nameWords[halfWords:])
			
			if GetController().ShowNewPersonDialog(self, firstName, lastName):
				GetController().SignPersonIn(None, type)
				self.ResetValues()
			
	def ResetValues(self):
		self._selectPerson.ResetValues()
