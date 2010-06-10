 # -*- coding: utf-8 -*-
 
import wx
from ..db import Person
from ..ui import AddLabel, MedFont, MakeStaticBoxSizer
from ..controls.edit_panel import EditPersonPanel, EditBikePanel
from ..controls.autowrapped_static_text import AutowrappedStaticText
from ..controller import GetController
from ..strings import trans

class NewPersonDialog(wx.Dialog):
	def __init__(self, parent, firstName = "", lastName = ""):
		wx.Dialog.__init__(self, parent, title = trans.newPersonTitle,
			style = wx.FRAME_FLOAT_ON_PARENT, size = (280, 400))
		
		outerSizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(outerSizer)

		AddLabel(self, outerSizer, MedFont(), \
			trans.newPersonInfo, type = AutowrappedStaticText)
		
		person = Person()
		person.firstName = firstName
		person.lastName = lastName
		
		nameEntrySizer = MakeStaticBoxSizer(self, trans.newPersonNameTitle, wx.VERTICAL)
		AddLabel(self, nameEntrySizer, MedFont(), trans.newPersonNameIntro)
		self.editNamePanel = EditPersonPanel(self)
		self.editNamePanel.Set(person)
		nameEntrySizer.Add(self.editNamePanel, 0, wx.EXPAND)
		outerSizer.Add(nameEntrySizer, 0, wx.EXPAND)
		
		bikeEntrySizer = MakeStaticBoxSizer(self, trans.newPersonBikeTitle, wx.VERTICAL)
		AddLabel(self, bikeEntrySizer, MedFont(), trans.newPersonBikeIntro)			
		self.editBikePanel = EditBikePanel(self)
		bikeEntrySizer.Add(self.editBikePanel, 0, wx.EXPAND)
		outerSizer.Add(bikeEntrySizer, 0, wx.EXPAND)
		
		buttonSizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)
		outerSizer.Add(buttonSizer, 1, wx.ALIGN_RIGHT)
		
		ok = self.FindWindowById(wx.ID_OK)
		cancel = self.FindWindowById(wx.ID_CANCEL)
		
		ok.Bind(wx.EVT_BUTTON, self.OnOK)
		cancel.Bind(wx.EVT_BUTTON, self.OnCancel)
		
		self.GetSizer().SetMinSize((200, 400))
	
	def OnOK(self, event):
		if self.editNamePanel.Validate():
			createBike = False
			if not self.editBikePanel.IsEmpty():
				createBike = True
				if not self.editBikePanel.Validate():
					return
			
			person = GetController().CreatePerson(self.editNamePanel.Get())
			
			if createBike:
				GetController().CreateBike(self.editBikePanel.Get(), person)

			self.EndModal(event.GetEventObject().GetId())
		
	def OnCancel(self, event):
		self.Close()
		
	def SetPersonName(self, firstName, lastName):
		self.editNamePanel.SetValues(firstName, lastName)

	def ResetValues(self):
		self.editNamePanel.ResetValues()
		self.editBikePanel.ResetValues()
