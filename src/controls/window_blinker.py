# -*- coding: utf-8 -*-

import wx

class WindowBlinker(wx.EvtHandler):
	def __init__(self, target, color = "pink", times = 4, period = 750):
		wx.EvtHandler.__init__(self)
		
		self._times = times * 2
		self._target = target			
		self._origColor = target.GetClassDefaultAttributes().colBg
		self._blinkColor = color
		self._period = period / 2
		
		self._timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self._OnTimer)
		self._timer.Start(period)
		
		self._target.SetBackgroundColour(self._blinkColor)
		
	def __del__(self):
		self.Stop()
		wx.EvtHandler.__del__(self)

	def _OnTimer(self, event):
		currColor = self._target.GetBackgroundColour()
		if currColor == self._origColor:
			self._target.SetBackgroundColour(self._blinkColor)
		else:
			self._target.SetBackgroundColour(self._origColor)
		
		self._times -= 1
		if self._times <= 0:
			self.Stop()
		self._target.Refresh()
	
	def Done(self):
		return self._times <= 0
		
	def Stop(self):
		self._target.SetBackgroundColour(self._origColor)
		if hasattr(self, "_timer"):
			self._timer.Destroy()
			del self._timer
