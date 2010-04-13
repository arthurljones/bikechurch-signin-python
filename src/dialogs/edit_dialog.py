# -*- coding: utf-8 -*-

import wx
from ..controller import GetController
from ..controls.edit_panel import EditShoptimePanel, EditBikePanel, EditFeedbackPanel

class EditDialog(wx.Dialog):	
	def __init__(self, parent, EditPanelType, typeName, size, object = None):
		self._object = object
		title = "{0} {1}".format("Edit" if object else "Add", typeName)
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
		EditDialog.__init__(self, parent, EditShoptimePanel, "Shoptime", (300, 200), object)
		
class BikeDialog(EditDialog):
	def __init__(self, parent, object = None):
		EditDialog.__init__(self, parent, EditBikePanel, "Bike", (250, 200), object)
		
class FeedbackDialog(EditDialog):
	def __init__(self, parent, object = None):
		EditDialog.__init__(self, parent, EditFeedbackPanel, "", (340, 160), object)
		self.SetTitle("Leave Feedback")
	
	
	
