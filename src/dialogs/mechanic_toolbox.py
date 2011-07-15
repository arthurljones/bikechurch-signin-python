# -*- coding: utf-8 -*-

import wx
from src.controller import GetController
from src.ui import winSizes
from src.dialogs.find_bike import FindBikeDialog
from src.dialogs.view_feedback import ViewFeedbackDialog

class MechanicToolboxDialog(wx.Dialog):
	def __init__(self):
		wx.Dialog.__init__(self, None, title = "Mechanic Toolbox",
					size = winSizes.mechanicToolbox)
		
		outerSizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(outerSizer)
		
		optionsSizer = wx.BoxSizer(wx.VERTICAL)
		outerSizer.Add(optionsSizer, 0, wx.EXPAND)
		
		def AddButton(text, function):
			button = wx.Button(self, wx.ID_ANY, text)
			button.Bind(wx.EVT_BUTTON, function)
			optionsSizer.Add(button, 0, wx.EXPAND)
		
		AddButton("View Feedback", self.OnFeedback)
		AddButton("Find a Bike", self.OnFind)
		AddButton("Sign Everybody Out", self.OnSignout)

		outerSizer.AddStretchSpacer()
		
		buttonSizer = self.CreateButtonSizer(wx.OK)
		outerSizer.Add(buttonSizer, 0, wx.ALIGN_RIGHT + wx.ALIGN_BOTTOM)
		
		ok = self.FindWindowById(wx.ID_OK)
		ok.Bind(wx.EVT_BUTTON, self.OnOK)
	
	def OnFeedback(self, event):
		dialog = ViewFeedbackDialog()
		dialog.ShowModal()
		
	def OnFind(self, event):
		dialog = FindBikeDialog()
		dialog.ShowModal()
		
	def OnSignout(self, event):
		people = GetController().GetPeopleInShop()
		for person in people:
			GetController().SignPersonOut(person)
				
	def OnOK(self, event):
		self.EndModal(wx.ID_OK)


