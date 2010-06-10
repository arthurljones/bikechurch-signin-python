# -*- coding: utf-8 -*-

import wx, datetime
from ..ui import MedFont
from window_blinker import WindowBlinker
from ..dialogs.edit_dialog import FeedbackDialog
from ..dialogs.mechanic_toolbox import MechanicToolboxDialog
from ..controller import GetController
from ..strings import trans
		
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

		self._textBG = wx.Panel(self)		
		innerSizer.Add(self._textBG, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 3)
		textBGSizer = wx.BoxSizer(wx.VERTICAL)
		self._textBG.SetSizer(textBGSizer)
		self._text = wx.StaticText(self._textBG, wx.ID_ANY, "")
		self._text.SetFont(MedFont())
		textBGSizer.Add(self._text, 1, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.TOP, 5)
		
		buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
		innerSizer.Add(buttonSizer, 0, wx.ALIGN_RIGHT | wx.EXPAND)
		
		def AddButton(label, onClick, flags = 0, height = 26):
			button = wx.Button(self, wx.ID_ANY, label)
			buttonSizer.Add(button, 1, wx.ALIGN_CENTER_VERTICAL | flags)
			button.SetMaxSize((-1, height))
			button.SetMinSize((button.GetMinSize()[0], height))
			button.Bind(wx.EVT_BUTTON, onClick)
			return button
			
		self._feedback = AddButton(trans.statusButtonFeedback, self._OnFeedback)
		self._toolbox = AddButton(trans.statusButtonToolbox, self._OnToolbox)
				
	def _OnToolbox(self, event):
		if GetController().AuthenticateMechanic(self, trans.authenticateToolbox):
			dialog = MechanicToolboxDialog(self)
			dialog.ShowModal()
		
	def _OnFeedback(self, event):
		dialog = FeedbackDialog(self)
		if dialog.ShowModal() == wx.ID_OK:
			feedback = dialog.Get()
			feedback.date = datetime.datetime.now()
			GetController().AddFeedback(feedback)
				
	def FlashError(self, error, targets = []):
		self.StopAllFlashing()
		
		try:
			iter(targets)
		except TypeError:
			targets = [targets]
		targets.append(self._textBG)
		
		self._text.SetLabel(error)
		
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
		self._text.SetLabel("")
		self.Layout()
				
