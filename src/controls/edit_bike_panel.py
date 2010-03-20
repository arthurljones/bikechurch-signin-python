 # -*- coding: utf-8 -*-
 
import wx
from ..ui_utils import AddField, MakeInfoEntrySizer

class EditBikePanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)
		
		bikes = ["Mountain", "Road", "Hybrid", 
			"Cruiser", "Three Speed", "Recumbent", "Chopper",
			"Mixte", "Tallbike", "Town Bike", "Touring"]
		bikes.sort()
		bikes.append("Other")
		
		sizer = MakeInfoEntrySizer()
		self.SetSizer(sizer)
		medFont = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
		AddBikeField = lambda *args: AddField(self, sizer, medFont, *args)
		self.color = AddBikeField("Color:")
		self.type = AddBikeField("Type:", wx.Choice)
		self.type.SetItems(bikes)
		self.brand = AddBikeField("Brand:")
		self.model = AddBikeField("Model:")
		self.serial = AddBikeField("Serial #:")
		
	def Validate(self):
		#TODO
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
		self.type.SetSelection(-1)
		self.brand.SetValue("")
		self.model.SetValue("")
		self.serial.SetValue("")
