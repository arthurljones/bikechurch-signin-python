 # -*- coding: utf-8 -*-
 
import wx

from ui_utils import Delegator
from controls.status_bar import StatusBar
from controls.occupants_list import OccupantsList
from controls.signin_panel import SignInPanel

from dialogs.new_person import NewPersonDialog
from dialogs.authenticate_mechanic import AuthenticateMechanicDialog
from dialogs.view_person import ViewPersonDialog

class MainWindow(wx.Frame, Delegator):
	def __init__(self, controller):
		size = (900, 520)
		wx.Frame.__init__(self, None, id = wx.ID_ANY,
			title = u"Welcome To The Bike Church!", size = size,
			style = wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
		Delegator.__init__(self)
		self.SetMinSize(size)
		
		wx.Font.SetDefaultEncoding(wx.FONTENCODING_UTF8)
		
		self._controller = controller
		controller.SetUI(self)
		
		self.screens = []
		self.currentScreen = None
		
		sizer = wx.FlexGridSizer(2, 1)
		sizer.AddGrowableRow(0)
		sizer.AddGrowableCol(0)
		self.SetSizer(sizer)
		self.Centre(wx.BOTH)
		
		screenSizer = wx.FlexGridSizer(1, 2)
		screenSizer.AddGrowableCol(1)
		screenSizer.AddGrowableRow(0)
		
		self.statusBar = StatusBar(self, self._controller)
		self.PushDelegate(self.statusBar)
		
		sizer.Add(screenSizer, 1, wx.EXPAND)
		sizer.Add(self.statusBar, 0, wx.EXPAND)
				
		self.occupantsList = OccupantsList(self, controller)
		self.signinPanel = SignInPanel(self, controller)
		
		screenSizer.Add(self.signinPanel, 0, wx.EXPAND | wx.ALL, 8)
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
		dialog = NewPersonDialog(self._controller, firstName, lastName)
		return dialog.ShowModal() == wx.ID_OK
		
	def ShowViewPersonDialog(self, person):
		dialog = ViewPersonDialog(self._controller, person)
		return dialog.ShowModal() == wx.ID_OK

	def AuthenticateMechanic(self, activity):
		dialog = AuthenticateMechanicDialog(activity)
		return dialog.ShowModal() == wx.ID_OK

	def Reset(self, screen):
		self.signinPanel.ResetValues()
		self.statusBar.ResetError()


