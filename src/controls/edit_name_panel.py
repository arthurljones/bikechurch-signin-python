 # -*- coding: utf-8 -*-
 
import wx
from ..ui_utils import AddField, MakeInfoEntrySizer, MedFont

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
		values = self.GetValues()
		if not values.firstName:
			self.controller.FlashError(
				"You must enter at least your first name.",
				self.firstName)
		elif len(values.firstName) + len(values.lastName) < 3:
			self.controller.FlashError(
				"Your name must have at least three letters.",
				[self.firstName, self.lastName])
			return False
			
		return True
		
	def GetValues(self):
		class Name: pass
		name = Name()
		name.firstName = self.firstName.GetValue()
		name.lastName = self.lastName.GetValue()
		return name
	
	def SetValues(self, firstName, lastName):
		self.firstName.SetValue(firstName)
		self.lastName.SetValue(lastName)

	def ResetValues(self):
		self.firstName.SetValue("")
		self.lastName.SetValue("")
