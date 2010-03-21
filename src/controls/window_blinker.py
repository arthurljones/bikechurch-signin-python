import wx

class WindowBlinker(wx.EvtHandler):
	def __init__(self, target, color = "pink", times = 4, period = 750):
		wx.EvtHandler.__init__(self)
		
		self.times = times * 2
		self.target = target
		self.origColor = target.GetClassDefaultAttributes().colBg
		self.blinkColor = color
		self.period = period / 2
		
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.OnTimer)
		self.timer.Start(period)
		
		self.target.SetBackgroundColour(self.blinkColor)

	def OnTimer(self, event):
		currColor = self.target.GetBackgroundColour()
		if currColor == self.origColor:
			self.target.SetBackgroundColour(self.blinkColor)
		else:
			self.target.SetBackgroundColour(self.origColor)
		
		self.times -= 1
		if self.times <= 0:
			self.Stop()
		self.target.Refresh()
	
	def Done(self):
		return self.times <= 0
		
	def Stop(self):
		self.target.SetBackgroundColour(self.origColor)
		self.timer.Stop()
