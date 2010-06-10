 # -*- coding: utf-8 -*-
 
import wx
from ..ui import AddLabel, MedFont, BigFont
from ..strings import trans

class ShoptimeChoiceEvent(wx.PyCommandEvent):
	eventType = wx.NewEventType()
	def __init__(self, sender, type):
		wx.PyCommandEvent.__init__(self)
		self.SetEventType(ShoptimeChoiceEvent.eventType)
		self.SetEventObject(sender)
		self._type = type

	def GetType(self):
		return self._type
wx.EVT_SHOPTIME_CHOICE = wx.PyEventBinder(ShoptimeChoiceEvent.eventType)

class ShoptimeChoicePanel(wx.Panel):
	def __init__(self, parent, sizer = wx.BoxSizer(wx.VERTICAL)):
		wx.Panel.__init__(self, parent)
		
		self.SetSizer(sizer)
	
		self._buttonMap = {}
		def AddButton(string, type):
			button = wx.Button(self, wx.ID_ANY, string)
			button.SetFont(BigFont())
			sizer.Add(button, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
			self._buttonMap[button.GetId()] = type
			return button
		
		AddLabel(self, sizer, MedFont(), trans.signinIntro)
		sizer.AddSpacer((0, 0), 0, wx.EXPAND)
		self._buttons = []
		self._buttons.append(AddButton(trans.signinShoptime, "shoptime"))
		self._buttons.append(AddButton(trans.signinParts, "parts"))
		self._buttons.append(AddButton(trans.signinWorktrade, "worktrade"))
		self._buttons.append(AddButton(trans.signinVolunteer, "volunteer"))
		
		self.Bind(wx.EVT_BUTTON, self._OnButton)
		
	def _OnButton(self, event):
		event = ShoptimeChoiceEvent(self, self._buttonMap[event.GetEventObject().GetId()])
		self.GetEventHandler().AddPendingEvent(event)
		
	def GetWidgets(self):
		return self._buttons
