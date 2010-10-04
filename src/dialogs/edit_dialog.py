# -*- coding: utf-8 -*-

import wx
from ..ui import winSizes
from ..controller import GetController
from ..controls.edit_panel import EditShoptimePanel, EditBikePanel, EditFeedbackPanel
from ..strings import trans

class EditDialog(wx.Dialog):	
	def __init__(self, parent, EditPanelType, typeName, size, object = None):
		self._object = object
		title = ""
		if object:
			title = trans.editEditTitle.format(typeName)
		else:
			title = trans.editAddTitle.format(typeName)
		wx.Dialog.__init__(self, parent, title = title, size = size,
			style = wx.FRAME_FLOAT_ON_PARENT)

		sizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(sizer)
				
		self._edit = EditPanelType(self)
		if object:
			self._edit.Set(object)
		sizer.Add(self._edit, 1, wx.EXPAND | wx.ALL, 5)
		
		buttons = self.CreateButtonSizer(wx.OK | wx.CANCEL)
		sizer.Add(buttons, 0, wx.EXPAND)
		
		ok = self.FindWindowById(wx.ID_OK)
		ok.Bind(wx.EVT_BUTTON, self._OnOK)
		
		cancel = self.FindWindowById(wx.ID_CANCEL)
		cancel.Bind(wx.EVT_BUTTON, self._OnCancel)
	
	def _OnOK(self, event):
		GetController().StopFlashing()
		if self.Validate():
			self.Get()
			self.EndModal(wx.ID_OK)
			
	def _OnCancel(self, event):
		GetController().StopFlashing()
		self.EndModal(wx.ID_CANCEL)
		
	def Validate(self):
		return self._edit.Validate()	
		
	def Get(self):
		if self._object is None:
			self._object = self._edit.Get()
		else:
			self._edit.Update(self._object)
			
		return self._object
		
class ShoptimeDialog(EditDialog):
	def __init__(self, parent, object = None):
		EditDialog.__init__(self, parent, EditShoptimePanel, trans.editShoptime,
			winSizes.shoptimeDialog, object)
		
class BikeDialog(EditDialog):
	def __init__(self, parent, object = None):
		EditDialog.__init__(self, parent, EditBikePanel, trans.editBike,
			winSizes.bikeDialog, object)
		
class FeedbackDialog(EditDialog):
	def __init__(self, parent, object = None):
		EditDialog.__init__(self, parent, EditFeedbackPanel, "", 
			winSizes.feedbackDialog, object)
		self.SetTitle(trans.feedbackTitle)
	
