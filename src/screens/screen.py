 # -*- coding: utf-8 -*-
 
 #TODO: delete
 
import wx
from ..ui_utils import Delegator

class Screen(wx.Panel, Delegator):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)
		Delegator.__init__(self)

		self.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
		self.windows = []
		
		self.Hide()

	def __del__(self):
		wx.Panel.__del__(self)

	def AddChildWindow(self, window):
		self.windows.append(window)
		self.PushDelegate(window)
		
	def Show(self, sizer):
		sizer.Add(self, 1, wx.EXPAND)
		wx.Panel.Show(self)
		
	def Hide(self):
		wx.Panel.Hide(self)
		sizer = self.GetContainingSizer()
		if sizer:
			sizer.Detach(self)
			
	def Layout(self):
		for window in self.windows:
			window.Layout()
		wx.Panel.Layout(self)
		
