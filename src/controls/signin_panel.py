 # -*- coding: utf-8 -*-
 
import wx
from math import ceil
from ..ui import MedFont, HugeFont, MakeStaticBoxSizer, AddLabel
from shoptime_choice import ShoptimeChoicePanel
from select_person_panel import SelectPersonPanel
from ..controller import GetController
from ..strings import trans

class SignInPanel(wx.Panel):
	def __init__(self, parent):
		wx.Window.__init__(self, parent)
		self._suppressNextListChange = False
		
		sizer = MakeStaticBoxSizer(self, style = wx.VERTICAL)
		self.SetSizer(sizer)

		AddLabel(self, sizer, HugeFont(), trans.signinIntro, wx.ALIGN_CENTER)
		AddLabel(self, sizer, MedFont(), trans.signinGreeting)
		
		self._selectPerson = SelectPersonPanel(self, u"", trans.signinClickName)
		sizer.Add(self._selectPerson, 0, wx.EXPAND)
		
		self._shoptimeChoice = ShoptimeChoicePanel(self)
		sizer.Add(self._shoptimeChoice, 0, wx.EXPAND)
		
		self.Bind(wx.EVT_NAME_ENTERED, self._OnNameEntered)
		self.Bind(wx.EVT_RETURN_HIT, self._OnNameReturn)
		self.Bind(wx.EVT_PERSON_SELECTED, lambda e: "{0} selected".format(e.GetPerson()))
		self.Bind(wx.EVT_SHOPTIME_CHOICE, self._OnShoptimeChoice)
		self.Bind(wx.EVT_EMPTY_LIST_CLICKED, self._OnEmptyListClicked)
		
		self._shoptimeChoice.Disable()
		self.ResetValues()
			
	def _OnNameEntered(self, event):
		name = event.GetName()
		nameEntered = name != "" and name != self._selectPerson.GetDefaultName()
		self._shoptimeChoice.Enable(nameEntered)
	
	def _OnShoptimeChoice(self, event):
		GetController().StopFlashing()
		
		type = event.GetType()

		if type == "worktrade":
			if not GetController().AuthenticateMechanic(self,
				trans.authenticateWorktrade):
				return
				
		elif type == "volunteer":
			if not GetController().AuthenticateMechanic(self,
				trans.authenticateVolunteer):
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

	def _FlashTasks(self):
		widgets = self._shoptimeChoice.GetWidgets()
		GetController().FlashError(trans.signin.selectTask, widgets)
		
	def _FlashName(self):
		widgets = [self._selectPerson.GetNameEntryWidget()]
		GetController().FlashError(trans.signin.enterName, widgets)
				
	def _OnNameReturn(self, event):
		if event.GetName():
			self._FlashTasks()
		else:
			self._FlashName()
			
	def _OnEmptyListClicked(self, event):
		if self._selectPerson.GetNameEntered():
			self._FlashTasks()
		else:
			self._FlashName()		
			
	def ResetValues(self):
		self._selectPerson.ResetValues()
		self._selectPerson.SetFocus()
