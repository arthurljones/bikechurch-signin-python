import wx
from ..ui_utils import MakeInfoEntrySizer, AddField
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
		password = AddField(self, entrySizer, None, "Password:",
			style = wx.TE_PASSWORD)
		sizer.Add(entrySizer, 1, wx.EXPAND | wx.ALL, 5)
		password.Bind(wx.EVT_TEXT, self.OnPasswordChange)
		
		buttons = self.CreateButtonSizer(wx.OK | wx.CANCEL)
		sizer.Add(buttons, 0, wx.EXPAND)
		ok = self.FindWindowById(wx.ID_OK)
		ok.Disable()

		password.SetFocus()

		self.Layout()
	
	def OnPasswordChange(self, event):
		password = event.GetEventObject().GetValue()
		hash = hashlib.sha1(password).hexdigest()
		ok = self.FindWindowById(wx.ID_OK)
		ok.Enable(hash == MechanicPasswordDialog.passHash)
