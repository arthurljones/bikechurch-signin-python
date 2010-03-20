 # -*- coding: utf-8 -*-

import wx

class StatusBar(wx.Panel):
	def __init__(self, parent, controller):
		wx.Panel.__init__(self, parent, 0)
		
		outerSizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(outerSizer)
		outerSizer.Add(wx.StaticLine(self), 0, wx.EXPAND)
		innerSizer = wx.BoxSizer(wx.HORIZONTAL)
		outerSizer.Add(innerSizer, 1, wx.EXPAND)

		text = wx.StaticText(self, wx.ID_ANY, "Placeholder text.")
		innerSizer.Add(text, 1, wx.ALIGN_CENTER_VERTICAL)
		
		buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
		innerSizer.Add(buttonSizer, 0, wx.ALIGN_RIGHT)
		self.language = wx.Button(self, wx.ID_ANY, u"En Español")
		self.toolbox = wx.Button(self, wx.ID_ANY, u"Mechanic's Toolbox")
		self.language.SetMaxSize((-1, 25))
		self.toolbox.SetMaxSize((-1, 25))
		buttonSizer.Add(self.language, 1)
		buttonSizer.Add(self.toolbox, 1)
