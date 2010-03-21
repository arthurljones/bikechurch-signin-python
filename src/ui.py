 # -*- coding: utf-8 -*-
 
import wx

from ui_utils import Delegator
from screens.main import MainScreen
from controls.status_bar import StatusBar
from controls.occupants_list import OccupantsList
from controls.signin_panel import SignInPanel

from screens.new_person import NewPersonDialog
from dialogs.authenticate_mechanic import AuthenticateMechanicDialog

class MainWindow(wx.Frame, Delegator):
	def __init__(self, controller):
		size = (900, 520)
		wx.Frame.__init__(self, None, id = wx.ID_ANY,
			title = u"Welcome To The Bike Church!", size = size,
			style = wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
		Delegator.__init__(self)
		self.SetMinSize(size)
		
		wx.Font.SetDefaultEncoding(wx.FONTENCODING_UTF8)
		
		self.controller = controller
		controller.SetUI(self)
		
		self.screens = []
		self.currentScreen = None
		
		sizer = wx.FlexGridSizer(2, 1)
		sizer.SetFlexibleDirection(wx.VERTICAL)
		sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
		sizer.AddGrowableRow(0)
		sizer.AddGrowableCol(0)
		self.SetSizer(sizer)
		self.Centre(wx.BOTH)
		
		screenSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.statusBar = StatusBar(self, self.controller)
		self.PushDelegate(self.statusBar)
		
		sizer.Add(screenSizer, 1, wx.EXPAND)
		sizer.Add(self.statusBar, 0, wx.EXPAND)
				
		self.occupantsList = OccupantsList(self, controller)
		self.signinPanel = SignInPanel(self, controller)
		
		screenSizer.Add(self.signinPanel, 0, wx.ALL, 8)
		screenSizer.Add(self.occupantsList, 1, wx.EXPAND | wx.ALL, 8)
		
		self.PushDelegate(self.occupantsList)
		self.PushDelegate(self.signinPanel)
				
		self.Bind(wx.EVT_SIZE, self.OnResize)
		self.Layout()
		self.occupantsList.Layout()
		self.signinPanel.Layout()
		
		self.Show()
		
	def Layout(self):
		for screen in self.screens:
			screen.Layout()
		wx.Frame.Layout(self)
		
	def OnResize(self, event):
		self.Layout()
		
	def ShowNewPersonDialog(self, firstName = "", lastName = ""):
		dialog = NewPersonDialog(self.controller, firstName, lastName)
		result = dialog.ShowModal()
		print result
		return result == wx.ID_OK

	def AuthenticateMechanic(self, activity):
		dialog = AuthenticateMechanicDialog(activity)
		return dialog.ShowModal() == wx.ID_OK

	def Reset(self, screen):
		self.signinPanel.ResetValues()
		self.statusBar.ResetError()


