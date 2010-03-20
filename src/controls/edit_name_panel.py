import wx
from ..ui_utils import AddField, MakeInfoEntrySizer

class EditNamePanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)
		
		sizer = MakeInfoEntrySizer()
		self.SetSizer(sizer)
		medFont = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
		AddNameField = lambda *args: AddField(self, sizer, medFont, *args)
		self.firstName = AddNameField("First name:")
		self.lastName = AddNameField("Last name:")
		
	def Validate(self):
		#TODO
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
