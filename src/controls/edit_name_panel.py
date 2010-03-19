import wx
from ..ui_utils import AddField, MakeInfoEntrySizer

class EditNamePanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)
		
		sizer = MakeInfoEntrySizer()
		self.SetSizer(sizer)
		medFont = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
		AddBikeField = lambda *args: AddField(self, sizer, medFont, *args)
		self.color = AddBikeField("First name:")
		self.maker = AddBikeField("Last name:")
		
	def Validate(self):
		pass
		
	def GetValues(self):
		pass
