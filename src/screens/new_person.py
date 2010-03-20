 # -*- coding: utf-8 -*-
 
import wx
from screen import Screen

from ..controls.new_person_panel import NewPersonPanel
from ..controls.bc_statement_panel import BCStatementPanel

class NewPersonScreen(Screen):
	def __init__(self, parent, controller):
		Screen.__init__(self, parent)
		
		sizer = wx.FlexGridSizer(0, 2)
		sizer.SetFlexibleDirection(wx.HORIZONTAL)
		sizer.AddGrowableCol(1)
		self.SetSizer(sizer)
		
		self.newPersonPanel = NewPersonPanel(self, controller)
		self.bcStatement = BCStatementPanel(self)
		
		self.GetSizer().Add(self.newPersonPanel, 1, wx.ALL | wx.EXPAND, 3)
		self.GetSizer().Add(self.bcStatement, 1, wx.EXPAND | wx.ALL, 3)
		
		self.AddElement(self.newPersonPanel)
		self.AddElement(self.bcStatement)
