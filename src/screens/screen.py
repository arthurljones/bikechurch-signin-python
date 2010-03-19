import wx

class Screen(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)

		self.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
		self.elements = []
		
		self.Hide()

	def AddElement(self, element):
		self.elements.append(element)

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
		for element in self.elements:
			element.Layout()
		wx.Panel.Layout(self)
			
