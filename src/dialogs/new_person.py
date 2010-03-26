 # -*- coding: utf-8 -*-
 
import wx

from ..ui_utils import AddLabel, MedFont
from ..controls.autowrapped_static_text import AutowrappedStaticText
from ..controls.edit_name_panel import EditNamePanel
from ..controls.edit_bike_panel import EditBikePanel

class NewPersonDialog(wx.Dialog):
	def __init__(self, controller,  firstName = "", lastName = ""):
		wx.Dialog.__init__(self, None, title = "New Person Information")
		self.controller = controller
		
		outerSizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(outerSizer)

		AddLabel(self, outerSizer, MedFont(), \
			"Since you haven't used this system before, "
			"please tell us your name and bike innformation.",
			type = AutowrappedStaticText)
		
		staticBox = wx.StaticBox(self, wx.ID_ANY, u"Your Name")
		nameEntrySizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
		AddLabel(self, nameEntrySizer, MedFont(), u"Type Your Name:")
		self.editNamePanel = EditNamePanel(self, controller)
		self.editNamePanel.SetValues(firstName, lastName)
		nameEntrySizer.Add(self.editNamePanel, 0, wx.EXPAND)
		outerSizer.Add(nameEntrySizer, 0, wx.EXPAND)
		
		staticBox = wx.StaticBox(self, wx.ID_ANY, "Your Bike")
		bikeEntrySizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
		AddLabel(self, bikeEntrySizer, MedFont(), "Describe Your Bike (if you have one):")			
		self.editBikePanel = EditBikePanel(self, controller)
		bikeEntrySizer.Add(self.editBikePanel, 0, wx.EXPAND)
		outerSizer.Add(bikeEntrySizer, 0, wx.EXPAND)
		
		buttonSizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)
		outerSizer.Add(buttonSizer, 1, wx.ALIGN_RIGHT)
		
		ok = self.FindWindowById(wx.ID_OK)
		cancel = self.FindWindowById(wx.ID_CANCEL)
		
		ok.Bind(wx.EVT_BUTTON, self.OnOK)
		cancel.Bind(wx.EVT_BUTTON, self.OnCancel)
		
		self.GetSizer().SetMinSize((200, 0))
	
	def OnOK(self, event):
		if self.editNamePanel.Validate():
			createBike = False
			if not self.editBikePanel.IsEmpty():
				createBike = True
				if not self.editBikePanel.Validate():
					return
			
			person = self.controller.CreatePerson(
				self.editNamePanel.GetPerson())
			
			if createBike:
				self.controller.CreateBike(
					self.editBikePanel.GetBike(), person)

			self.EndModal(event.GetEventObject().GetId())
		
	def OnCancel(self, event):
		self.Close()
		
	def SetPersonName(self, firstName, lastName):
		self.editNamePanel.SetValues(firstName, lastName)

	def ResetValues(self):
		self.editNamePanel.ResetValues()
		self.editBikePanel.ResetValues()
