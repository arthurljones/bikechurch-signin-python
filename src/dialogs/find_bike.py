# -*- coding: utf-8 -*-

import wx
from src.ui import winSizes
from src.controls.edit_panel import EditBikePanel

class FindBikeDialog(wx.Dialog):
	def __init__(self):
		wx.Dialog.__init__(self, None, title = "Find Bike", size = winSizes.findBike)
		
		self._editBikeWidth = 350
		
		outerSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.SetSizer(outerSizer)
		
		sizer = wx.FlexGridSizer(4, 1)
		sizer.AddGrowableRow(1)
		outerSizer.Add(sizer, 1, wx.EXPAND)
		
		searchInfoSizer = wx.FlexGridSizer(1, 2)
		searchInfoSizer.AddGrowableCol(0)
		sizer.Add(searchInfoSizer, 1, wx.EXPAND)
	  
		self._bikeInfo = EditBikePanel(self)
		self._bikeInfo.SetMinSize((self._editBikeWidth, -1))
		searchInfoSizer.Add(self._bikeInfo, 1, wx.EXPAND)
		
		self._searchButton = wx.Button(self, wx.ID_ANY, "Search")
		self._searchButton.SetMinSize((winSizes.findBike[0] - self._editBikeWidth, -1))
		searchInfoSizer.Add(self._searchButton, 1, wx.ALIGN_BOTTOM + wx.ALIGN_RIGHT)
		
		self._resultList = wx.ListBox(self, wx.ID_ANY)
		sizer.Add(self._resultList, 1, wx.EXPAND)
		
		optionSizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(optionSizer, 1, wx.EXPAND)
		
		def AddButton(text, function):
			button = wx.Button(self, wx.ID_ANY, text)
			button.Bind(wx.EVT_BUTTON, function)
			optionSizer.Add(button, 0, wx.EXPAND)
			
		AddButton("View Bike", self.OnView)
		AddButton("Edit Bike", self.OnEdit)
		AddButton("View Patron", self.OnPatron)
		
		buttonSizer = self.CreateButtonSizer(wx.OK)
		sizer.Add(buttonSizer, 1, wx.ALIGN_RIGHT)
		
		ok = self.FindWindowById(wx.ID_OK)
		ok.Bind(wx.EVT_BUTTON, self.OnOK)
	
	def OnView(self, event):
		pass
	
	def OnEdit(self, event):
		pass
	
	def OnPatron(self, event):
		pass
	
	def OnOK(self, event):
		self.EndModal(wx.ID_OK)

			
