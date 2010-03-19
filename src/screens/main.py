import wx
from screen import Screen

from ..controls.occupants_list import OccupantsList
from ..controls.signin_panel import SignInPanel

class MainScreen(Screen):
	def __init__(self, parent, controller):
		Screen.__init__(self, parent)
		
		self.occupantsList = OccupantsList(self, controller)
		self.signinPanel = SignInPanel(self, controller)
		
		self.GetSizer().Add(self.signinPanel, 0, wx.ALL, 8)
		self.GetSizer().Add(self.occupantsList, 1, wx.EXPAND | wx.ALL, 8)
		
		self.AddElement(self.occupantsList)
		self.AddElement(self.signinPanel)
