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

	def Show(self, sizer):
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
		if self.__dict__.has_key(attr):
			return self.__dict__[attr]
		
		if self.__dict__.has_key("elements"):
			for element in self.elements:
				if hasattr(element, attr):
					return getattr(element, attr)
					
		raise AttributeError("No attribute {0} in {1} or children".format(
			attr, self.__class__.__name__))
			
