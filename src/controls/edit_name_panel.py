 # -*- coding: utf-8 -*-
 
import wx
from ..ui_utils import AddField, MakeInfoEntrySizer, MedFont
from ..db import Person

class EditNamePanel(wx.Panel):
	def __init__(self, parent, controller):
		wx.Panel.__init__(self, parent)
		self.controller = controller
		
		sizer = MakeInfoEntrySizer()
		self.SetSizer(sizer)
		AddNameField = lambda *args: AddField(self, sizer, MedFont(), *args)
		self.firstName = AddNameField("First name:")
		self.lastName = AddNameField("Last name:")
		
	def Validate(self):
		person = self.GetPerson()
		if not person.firstName:
			self.controller.FlashError(
				"You must enter at least your first name.",
				self.firstName)
		elif len(person.firstName) + len(person.lastName) < 3:
			self.controller.FlashError(
				"Your name must have at least three letters.",
				[self.firstName, self.lastName])
		elif self.controller.GetPersonByFullName(person.firstName, person.lastName):
			self.controller.FlashError(
				"There's already somebody with that name in the database.",
				[self.firstName, self.lastName])
		else:
			return True	
			
		return False
		
	def GetPerson(self):
		person = Person()
		person.firstName = self.firstName.GetValue()
		person.lastName = self.lastName.GetValue()
		return person
	
	def SetValues(self, firstName, lastName):
		self.firstName.SetValue(firstName)
		self.lastName.SetValue(lastName)

	def ResetValues(self):
		self.firstName.SetValue("")
		self.lastName.SetValue("")
