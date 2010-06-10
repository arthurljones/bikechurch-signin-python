 # -*- coding: utf-8 -*-
 
import wx
from ..controller import GetController
from ..ui import AddLabel, MakeInfoEntrySizer, MedFont
from ..controls.autowrapped_static_text import AutowrappedStaticText
from ..strings import trans

def FormatFeedbackDate(feedback):
	return feedback.date.strftime("%a %b %d at %I%p")

class ViewFeedbackPanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)
		
		sizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(sizer)

		AddLabel(self, sizer, MedFont(), u"Select feedback to view.")
		self._feedbackListBox = wx.ListBox(self, wx.ID_ANY)
		self._feedbackListBox.Bind(wx.EVT_LISTBOX, self._OnListClick)
		self._feedbackListBox.Bind(wx.EVT_LISTBOX_DCLICK, self._OnListClick)
		sizer.Add(self._feedbackListBox, 1, wx.EXPAND)
		
		def FeedbackString(item):
			name = item.name
			if len(name) > 16:
				name = name[:7] + "..."
			
			feedback = item.feedback
			if len(feedback) > 10:
				feedback = feedback[:7] + "..."
				
			return "{0}: \"{1}\" said \"{2}\"".format(
				FormatFeedbackDate(item), name, feedback)
		
		self._feedback = GetController().GetFeedback()
		self._feedbackListBox.SetItems([FeedbackString(item) for item in self._feedback])
		
		displaySizer = MakeInfoEntrySizer()
		sizer.Add(displaySizer, 1, wx.EXPAND)
		
		def AddFeedbackField(label, multiline = False):
			text = wx.StaticText(self, label = label)
			text.SetFont(MedFont())
			displaySizer.Add(text, 0,
				wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 5)
			
			style = wx.TE_READONLY
			if multiline:
				style |= wx.TE_MULTILINE
			field = wx.TextCtrl(self, style = style)
			field.SetFont(MedFont())
			displaySizer.Add(field, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
			return field
		
		self._currentDate = AddFeedbackField("Date:")
		self._currentName = AddFeedbackField("Name:")
		self._currentFeedback = AddFeedbackField("Feedback:", multiline = True)
		
	def _OnListClick(self, event):
		feedback = self._feedback[event.GetSelection()]
		self._currentDate.SetValue(FormatFeedbackDate(feedback))
		self._currentName.SetValue(feedback.name)
		self._currentFeedback.SetValue(feedback.feedback)

class MechanicToolboxDialog(wx.Dialog):
	def __init__(self, firstName = "", lastName = ""):
		wx.Dialog.__init__(self, None, title = "Mechanic Toolbox")
		
		outerSizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(outerSizer)
		
		self._feedbackPanel = ViewFeedbackPanel(self)
		outerSizer.Add(self._feedbackPanel, 1, wx.EXPAND)		
		
		buttonSizer = self.CreateButtonSizer(wx.OK)
		outerSizer.Add(buttonSizer, 0, wx.ALIGN_RIGHT)
		
		ok = self.FindWindowById(wx.ID_OK)
		ok.Bind(wx.EVT_BUTTON, self.OnOK)
	
	def OnOK(self, event):
		self.EndModal(wx.ID_OK)


