 # -*- coding: utf-8 -*-
 
import wx
from ..ui import AddLabel, MedFont, BigFont

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
		
		AddLabel(self, sizer, MedFont(), u"What do you want to do?")
		sizer.AddSpacer((0, 0), 0, wx.EXPAND)
		AddButton(u"Work on my bike!", "shoptime")
		AddButton(u"Look for parts!", "parts")
		AddButton(u"Do work trade!", "worktrade")
		AddButton(u"Volunteer!", "volunteer")
		
		self.Bind(wx.EVT_BUTTON, self._OnButton)
		
	def _OnButton(self, event):
		event = ShoptimeChoiceEvent(self, self._buttonMap[event.GetEventObject().GetId()])
		self.GetEventHandler().AddPendingEvent(event)
