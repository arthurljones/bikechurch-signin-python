 # -*- coding: utf-8 -*-
 
import wx
from ..ui_utils import AddField, MakeInfoEntrySizer, MedFont
from ..db import Bike

_values = ["color", "type", "brand", "model", "serial"]

class Value(object):
	def __init__(self, parent, name, control, getter = "GetValue", setter = "SetValue", zero = ""):
		self.control = control
		self.name = name
		self.getter = lambda: getattr(control, getter)()
		self.setter = lambda x: getattr(control, setter)(x)
		self.zero = zero
		
	def Get(self):
		return self.getter()
		
	def Set(self, value):
		return self.setter(value)
		
	def Reset(self):
		return self.setter(self.zero)

class EditBikePanel(wx.Panel):
	
	def __init__(self, parent, controller):
		wx.Panel.__init__(self, parent)
		self._controller = controller
		
		types = sorted(Bike.__table__.c.type.type.enums)
		
		self.values = []
		
		sizer = MakeInfoEntrySizer()
		self.SetSizer(sizer)
		
		AddValue = lambda *args : self.values.append(Value(self, *args))
		AddBikeField = lambda *args: AddField(self, sizer, MedFont(), *args)
		AddValue("color", AddBikeField("Color:"))
		type = AddBikeField("Type:", wx.Choice)
		type.SetItems(types)
		AddValue("type", type, "GetStringSelection", "SetSelection", 0)
		AddValue("brand", AddBikeField("Brand:"))
		AddValue("model", AddBikeField("Model:"))
		AddValue("serial", AddBikeField("Serial #:"))
	
	def Validate(self):
		errors = []
		requiredValues = ["color", "type", "serial"]
		for value in self.values:
			if value.name in requiredValues and not value.Get():
				errors.append(value.control)
				
		if errors:
			self._controller.FlashError(
			"You need at least the color, type, and serial# for your bike",
			errors)
			return False
			
		return True
		
	def IsEmpty(self):
		for value in self.values:
			if value.Get():
				return False
		return True
		
	def GetBike(self):
		bike = Bike()
		for value in self.values:
			setattr(bike, value.name, value.Get())
		return bike

	def ResetValues(self):
		for value in self.values:
			value.Reset()
