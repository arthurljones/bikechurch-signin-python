import wx
from ..ui_utils import AddLabel

class ShoptimeChoice(wx.Panel):
	def __init__(self, parent, onClick, sizer = wx.BoxSizer(wx.VERTICAL)):
		wx.Panel.__init__(self, parent)
		
		self.SetSizer(sizer)
		medFont = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
		buttonFont = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)

		def AddButton(string, type):
			button = wx.Button(self, wx.ID_ANY, string)
			button.SetFont(buttonFont)
			sizer.Add(button, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
			button.Bind(wx.EVT_BUTTON, lambda e: onClick(e, type))
		
		AddLabel(self, sizer, medFont, u"What do you want to do?")
		sizer.AddSpacer((0, 0), 0, wx.EXPAND)
		AddButton(u"Work on my bike!", "shoptime")
		AddButton(u"Look for parts!", "parts")
		AddButton(u"Do work trade!", "worktrade")
		AddButton(u"Volunteer!", "volunteer")
