 # -*- coding: utf-8 -*-
 
import wx, datetime
from ..ui import (AddLabel, MedFont, FormatTimedelta, GetShoptimeTypeDescription, 
	MakeStaticBoxSizer)
from ..db import Shoptime, Bike
from ..controls.edit_panel import EditPersonPanel, EditMemberPanel
from ..controls.autowrapped_static_text import AutowrappedStaticText
from ..controls.add_edit_remove_list import AddEditRemoveList
from edit_dialog import ShoptimeDialog, BikeDialog
from ..controller import GetController
from ..strings import trans
		
def _AddDialogFunc(parent, EditorType):
	def AddDialog():
		dialog = EditorType(parent)
		if dialog.ShowModal() == wx.ID_OK:
			return dialog.Get()
		else:
			return None
			
	return AddDialog
	
def _EditDialogFunc(parent, EditorType):
	def EditDialog(object):
		dialog = EditorType(parent, object)
		return dialog.ShowModal() == wx.ID_OK
		
	return EditDialog

def _ShoptimeListString(shoptime):
	duration =  shoptime.end - shoptime.start		
	return "{0}: {1} of {2}".format(shoptime.start.strftime("%a %b %d %Y %I:%m%p"),
		FormatTimedelta(duration), GetShoptimeTypeDescription(shoptime.type))
						
def _BikeListString(bike):
	string = []
	string.append(bike.color)
	if bike.brand:
		string.append(bike.brand)
	if bike.model:
		string.append(bike.model)
	
	string.append("{0} bike:".format(bike.type))
	string.append("S/N {0}".format(bike.serial))
	
	return " ".join(string)
		
class ViewPersonDialog(wx.Dialog):
	def __init__(self, parent, person):
		wx.Dialog.__init__(self, parent, title = "Viewing Info For {0}".format(person.Name()),
			size = (740, 470), style = wx.FRAME_FLOAT_ON_PARENT)
		self._person = person
		
		outerSizer = wx.FlexGridSizer(2, 1)
		outerSizer.AddGrowableRow(0)
		outerSizer.AddGrowableCol(0)
		self.SetSizer(outerSizer)

		panelsSizer = wx.FlexGridSizer(1, 2)
		panelsSizer.AddGrowableCol(0)
		panelsSizer.AddGrowableRow(0)
		outerSizer.Add(panelsSizer, 1, wx.EXPAND)
		
		buttonSizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)
		outerSizer.Add(buttonSizer, 1, wx.ALIGN_RIGHT)

		listsSizer = wx.BoxSizer(wx.VERTICAL)
		infoSizer = wx.FlexGridSizer(1, 1)
		infoSizer.AddGrowableCol(0)
		
		panelsSizer.Add(infoSizer, 1, wx.EXPAND)
		panelsSizer.Add(listsSizer, 1, wx.EXPAND)
				
		posessive = person.PosessiveFirstName()	
			
		shoptimes = AddEditRemoveList(self, "{0} Shop Usage".format(posessive), 
			"Hours", person.shoptimes, _AddDialogFunc(self, ShoptimeDialog),
			_EditDialogFunc(self, ShoptimeDialog), lambda x: True,
			_ShoptimeListString, lambda shoptime: shoptime.start)
				
		bikes = AddEditRemoveList(self, "{0} Bikes".format(posessive),
			"Bike", person.bikes, _AddDialogFunc(self, BikeDialog),
			_EditDialogFunc(self, BikeDialog), lambda x: True,
			_BikeListString, lambda bike: bike.color)
			
		listsSizer.Add(shoptimes, 2, wx.EXPAND | wx.ALL, 8)
		listsSizer.Add(bikes, 1, wx.EXPAND | wx.ALL, 8)
		listsSizer.SetMinSize((400, 0))
				
		ok = self.FindWindowById(wx.ID_OK)
		cancel = self.FindWindowById(wx.ID_CANCEL)
		
		ok.Bind(wx.EVT_BUTTON, self._OnOK)
		cancel.Bind(wx.EVT_BUTTON, self._OnCancel)
		
		def AddEditPanel(label, PanelType, value, extra = None):
			editSizer = MakeStaticBoxSizer(self, "{0} {1}".format(posessive, label),
				wx.VERTICAL)
			panel = PanelType(self)
			panel.Set(value)
			editSizer.Add(panel, 1, wx.EXPAND | wx.ALL, 5)
			infoSizer.Add(editSizer, 1, wx.EXPAND | wx.ALL, 5)
			return panel
		
		self._personEditPanel = AddEditPanel("Name", EditPersonPanel, person)
		self._memberEditPanel = AddEditPanel("Member Info (Read-only)",
			EditMemberPanel, person.memberInfo)
		
		#TODO - reenable once functionality is implemented
		self._memberEditPanel.Disable()
		
		self.Layout()
		self.CenterOnScreen()
	
	def _OnOK(self, event):
		GetController().StopFlashing()
		if self._personEditPanel.Validate(self._person):
			self._personEditPanel.Update(self._person)
			GetController().Commit()
			self.EndModal(wx.ID_OK)
		
	def _OnCancel(self, event):
		GetController().StopFlashing()
		GetController().Rollback()
		self.EndModal(wx.ID_CANCEL)


