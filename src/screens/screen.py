import wx

class Screen(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)

		self.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
		self.elements = []
		
		self.Hide()

	def __del__(self):
		wx.Panel.__del__(self)

	def AddElement(self, child):
		self.elements.append(child)

	def Show(self):
		sizer = self.GetParent().GetSizer()
		sizer.Add(self, 1, wx.EXPAND)
		wx.Panel.Show(self)
		self.Layout()
		
	def Hide(self):
		wx.Panel.Hide(self)
		sizer = self.GetContainingSizer()
		if sizer:
			sizer.Detach(self)
			
	def Layout(self):
		for child in self.elements:
			child.Layout()
		wx.Panel.Layout(self)
		
	def __getattr__(self, attr):
		for child in self.elements:
			if hasattr(child, attr):
				return getattr(child, attr)
				
		raise AttributeError("Cannot delegate \"{0}\"".format(attr))
			
