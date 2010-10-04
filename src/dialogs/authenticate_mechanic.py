# -*- coding: utf-8 -*-

import wx
from ..ui import MakeInfoEntrySizer, AddField, MedFont, winSizes
import hashlib
from copy import copy
from ..strings import trans

class AuthenticateMechanicDialog(wx.Dialog):
	passHash = "e82b4263a7d8618a5b458dda8658f35bdef7e14b" #sha1
	
	def __init__(self, parent, actionDescription = trans.authenticateGeneric):
		wx.Dialog.__init__(self, parent, title = trans.enterPassword,
			size = winSizes.authenticateMechanic, style = wx.FRAME_FLOAT_ON_PARENT)

		sizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(sizer)

		text = wx.StaticText(self, wx.ID_ANY, 
			trans.mechanicPermission.format(actionDescription))
		sizer.Add(text, 0, wx.EXPAND | wx.ALL, 8)
		text.SetFont(MedFont())
				
		entrySizer = MakeInfoEntrySizer()
		self.password = AddField(self, entrySizer, None, trans.passwordLabel,
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
