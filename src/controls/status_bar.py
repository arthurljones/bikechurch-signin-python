 # -*- coding: utf-8 -*-

import wx
from ..ui import MedFont
from window_blinker import WindowBlinker
		
class StatusBar(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, 0)
		
		self.blinkers = []
				
		outerSizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(outerSizer)
		outerSizer.Add(wx.StaticLine(self), 0, wx.EXPAND)
		innerSizer = wx.FlexGridSizer(1, 2)
		innerSizer.AddGrowableCol(0)
		outerSizer.Add(innerSizer, 0, wx.EXPAND)

		self.textBG = wx.Panel(self)		
		innerSizer.Add(self.textBG, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 3)
		textBGSizer = wx.BoxSizer(wx.VERTICAL)
		self.textBG.SetSizer(textBGSizer)
		self.text = wx.StaticText(self.textBG, wx.ID_ANY, "")
		self.text.SetFont(MedFont())
		textBGSizer.Add(self.text, 1, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.TOP, 5)
		
		buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
		innerSizer.Add(buttonSizer, 0, wx.ALIGN_RIGHT | wx.EXPAND)
		
		def AddButton(label, flags = 0, height = 26):
			button = wx.Button(self, wx.ID_ANY, label)
			buttonSizer.Add(button, 1, wx.ALIGN_CENTER_VERTICAL | flags)
			button.SetMaxSize((-1, height))
			button.SetMinSize((button.GetMinSize()[0], height))
		self.language = AddButton(u"En Español")
		self.toolbox = AddButton(u"Mechanic's Toolbox")
		
	def FlashError(self, error, targets = []):
		self.StopAllFlashing()
		
		try:
			iter(targets)
		except TypeError:
			targets = [targets]
		targets.append(self.textBG)
		
		self.text.SetLabel(error)
		
		for target in targets:				
			blinker = WindowBlinker(target)
			self.blinkers.append(blinker)
			
		self.Layout()
	
	def StopAllFlashing(self):
		for blinker in self.blinkers:
			blinker.Stop()
			blinker.Destroy()
			
		self.blinkers = []		
	
	def Hide(self):
		pass
		
	def ResetError(self):
		self.StopAllFlashing()
		self.text.SetLabel("Placeholder Text.")
		self.Layout()
				
