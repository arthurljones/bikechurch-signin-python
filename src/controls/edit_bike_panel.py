import wx
from ..src.ui_utils import AddField, MakeInfoEntrySizer

class EditBikePanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)
		
		bikes = ["Mountain Bike", "Road Bike", "Hybrid", 
			"Cruiser", "Three Speed", "Recumbent", "Chopper",
			"Mixte", "Tallbike", "Town Bike"]
		bikes.sort()
		bikes.append("Other")
		
		sizer = MakeInfoEntrySizer()
		self.SetSizer(sizer)
		medFont = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
		AddBikeField = lambda *args: AddField(self, sizer, medFont, *args)
		self.color = AddBikeField("Color:")
		self.type = AddBikeField("Type:", wx.Choice)
		self.type.SetItems(bikes)
		self.maker = AddBikeField("Maker:")
		self.model = AddBikeField("Model:")
		self.serial = AddBikeField("Serial #:")
		
	def Validate(self):
		pass
		
	def GetValues(self):
		return {
			"color":	self.color.GetValue(),
			"type":		self.type.GetValue(),
			"maker":	self.maker.GetValue(),
			"model":	self.model.GetValue(),
			"serial":	self.serial.GetValue(),
			}
