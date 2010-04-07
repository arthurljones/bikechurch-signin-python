import wx
from ..controls.edit_panel import EditShoptimePanel
from ..controls.edit_panel import EditBikePanel

class EditDialog(wx.Dialog):	
	def __init__(self, EditPanelType, typeName, size, object = None):
		self._object = object
		title = "{0} {1}".format("Edit" if object else "Add", typeName)
		wx.Dialog.__init__(self, None, title = title, size = size, style = wx.STAY_ON_TOP)

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
	
	
	def _OnOK(self, event):
		if self.Validate():
			self.Get()
			self.EndModal(wx.ID_OK)
		
	def Validate(self):
		return self._edit.Validate()	
		
	def Get(self):
		if self._object is None:
			self._object = self._edit.Get()
		else:
			self._edit.Update(self._object)
			
		return self._object
		
class ShoptimeDialog(EditDialog):
	def __init__(self, object = None):
		EditDialog.__init__(self, EditShoptimePanel, "Shoptime", (300, 200), object)
		
class BikeDialog(EditDialog):
	def __init__(self, object = None):
		EditDialog.__init__(self, EditBikePanel, "Bike", (250, 200), object)
	
	
	
