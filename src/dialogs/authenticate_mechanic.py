import wx
from ..ui import MakeInfoEntrySizer, AddField
import hashlib
from copy import copy

class AuthenticateMechanicDialog(wx.Dialog):
	passHash = "e82b4263a7d8618a5b458dda8658f35bdef7e14b" #sha1
	
	def __init__(self, actionDescription = "do that"):
		wx.Dialog.__init__(self, None, title = "Enter Mechanic Password",
			size = (300, 110))

		sizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(sizer)

		text = wx.StaticText(self, wx.ID_ANY,
			"You need a mechanic's permission to {0}.".format(
				actionDescription))
		sizer.Add(text, 0, wx.EXPAND | wx.ALL, 8)
				
		entrySizer = MakeInfoEntrySizer()
		self.password = AddField(self, entrySizer, None, "Password:",
			style = wx.TE_PASSWORD | wx.TE_PROCESS_ENTER)
		sizer.Add(entrySizer, 1, wx.EXPAND | wx.ALL, 5)
		self.password.Bind(wx.EVT_TEXT, self.OnPasswordChange)
		self.password.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
		self.password.SetFocus()
		
		buttons = self.CreateButtonSizer(wx.OK | wx.CANCEL)
		sizer.Add(buttons, 0, wx.EXPAND)
		ok = self.FindWindowById(wx.ID_OK)
		ok.Disable()

		self.Layout()
	
	def CheckPassword(self):
		password = self.password.GetValue()
		hash = hashlib.sha1(password).hexdigest()
		return hash == AuthenticateMechanicDialog.passHash
		
	def OnPasswordChange(self, event):
		ok = self.FindWindowById(wx.ID_OK)
		ok.Enable(self.CheckPassword())
		
	def OnEnter(self, event):
		if self.CheckPassword():
			event.Skip()
