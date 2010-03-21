 # -*- coding: utf-8 -*-
 
import wx
from ..ui_utils import AddField, MakeInfoEntrySizer, MedFont

class EditBikePanel(wx.Panel):
	def __init__(self, parent, controller):
		wx.Panel.__init__(self, parent)
		self.controller = controller
		
		bikes = ["", "Mountain", "Road", "Hybrid", 
			"Cruiser", "Three Speed", "Recumbent", "Chopper",
			"Mixte", "Tallbike", "Town Bike", "Touring"]
		bikes.sort()
		bikes.append("Other")
		
		sizer = MakeInfoEntrySizer()
		self.SetSizer(sizer)
		AddBikeField = lambda *args: AddField(self, sizer, MedFont(), *args)
		self.color = AddBikeField("Color:")
		self.type = AddBikeField("Type:", wx.Choice)
		self.type.SetItems(bikes)
		self.brand = AddBikeField("Brand:")
		self.model = AddBikeField("Model:")
		self.serial = AddBikeField("Serial #:")
		
	def Validate(self):
		values = self.GetValues()
		errors = []
		if not values.color:
			errors.append(self.color)
		if not values.type:
			errors.append(self.type)
		if not values.brand:
			errors.append(self.brand)
		if not values.model:
			errors.append(self.model)
		if not values.serial:
			errors.append(self.serial)
			
		if errors:
			self.controller.FlashError(
			"You must fill out all the bike information, or leave it blank",
			errors)
			return False
			
		return True
		
	def IsEmpty(self):
		values = self.GetValues()
		for key in values.__dict__:
			if values.__dict__[key]:
				return False
				
		return True
		
	def GetValues(self):
		class BikeDescription: pass
		bike = BikeDescription()
		bike.color = self.color.GetValue()
		bike.type = self.type.GetStringSelection()
		bike.brand = self.brand.GetValue()
		bike.model = self.model.GetValue()
		bike.serial = self.serial.GetValue()
		return bike

	def ResetValues(self):
		self.color.SetValue("")
		self.type.SetSelection(0)
		self.brand.SetValue("")
		self.model.SetValue("")
		self.serial.SetValue("")
