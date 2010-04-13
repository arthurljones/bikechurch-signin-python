 # -*- coding: utf-8 -*-
 
import wx

from ui import Delegator
from controller import GetController
from controls.status_bar import StatusBar
from controls.occupants_list import OccupantsList
from controls.signin_panel import SignInPanel

from dialogs.new_person import NewPersonDialog
from dialogs.authenticate_mechanic import AuthenticateMechanicDialog
from dialogs.view_person import ViewPersonDialog

class MainWindow(wx.Frame, Delegator):
	def __init__(self):
		size = (900, 520)
		wx.Frame.__init__(self, None, id = wx.ID_ANY,
			title = u"Welcome To The Bike Church!", size = size,
			style = (wx.RESIZE_BORDER | wx.SYSTEM_MENU# | wx.STAY_ON_TOP
				| wx.CAPTION | wx.CLOSE_BOX | wx.TAB_TRAVERSAL))
			
		self.Maximize(True)
		Delegator.__init__(self)
		self.SetMinSize(size)
		
		wx.Font.SetDefaultEncoding(wx.FONTENCODING_UTF8)
		
		GetController().SetUI(self)
		
		sizer = wx.FlexGridSizer(2, 1)
		sizer.AddGrowableRow(0)
		sizer.AddGrowableCol(0)
		self.SetSizer(sizer)
		self.Centre(wx.BOTH)
		
		screenSizer = wx.FlexGridSizer(1, 2)
		screenSizer.AddGrowableCol(1)
		screenSizer.AddGrowableRow(0)
		
		self._statusBar = StatusBar(self)
		self.PushDelegate(self._statusBar)
		
		sizer.Add(screenSizer, 1, wx.EXPAND)
		sizer.Add(self._statusBar, 0, wx.EXPAND)
				
		self._occupantsList = OccupantsList(self)
		self._signinPanel = SignInPanel(self)
		
		screenSizer.Add(self._signinPanel, 0, wx.EXPAND | wx.ALL, 8)
		screenSizer.Add(self._occupantsList, 1, wx.EXPAND | wx.ALL, 8)
		
		self.PushDelegate(self._occupantsList)
		self.PushDelegate(self._signinPanel)
				
		self.Bind(wx.EVT_SIZE, self._OnResize)
		self.Bind(wx.EVT_CLOSE, self._OnClose)
		self.Bind(wx.EVT_QUERY_END_SESSION, self._OnQueryEndSession)
		self.Bind(wx.EVT_END_SESSION, self._OnEndSession)
		self.Layout()
		self._occupantsList.Layout()
		self._signinPanel.Layout()
		
		self.Show()
		
	def _OnResize(self, event):
		self.Layout()
		
	def ShowNewPersonDialog(self, parent, firstName = "", lastName = ""):
		dialog = NewPersonDialog(parent, firstName, lastName)
		return dialog.ShowModal() == wx.ID_OK
		
	def ShowViewPersonDialog(self, parent, person):
		dialog = ViewPersonDialog(parent, person)
		return dialog.ShowModal() == wx.ID_OK

	def AuthenticateMechanic(self, parent, activity):
		return True
		
		dialog = AuthenticateMechanicDialog(parent, activity)
		return dialog.ShowModal() == wx.ID_OK

	def Reset(self, screen):
		self._signinPanel.ResetValues()
		self._statusBar.ResetError()
	
	def _OnQueryEndSession(self, event):
		pass
		
	def _OnClose(self, event):
		if not event.CanVeto():
			self.Destroy()
		elif self.AuthenticateMechanic(self, "close the signin program"):
			self.Destroy()
		else:
			event.Veto()
		
	def _OnEndSession(self, event):
		pass
