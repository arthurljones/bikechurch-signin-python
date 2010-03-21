 # -*- coding: utf-8 -*-
 
import wx
from ..ui_utils import MedFont
from shoptime_choice import ShoptimeChoice

class SignInPanel(wx.Panel):
	def __init__(self, parent, controller):
		wx.Window.__init__(self, parent)	
		self.controller = controller
		self.nameList = []
		self.suppressNextListChange = False
		
		staticBox = wx.StaticBox(self)
		sizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
		self.SetSizer(sizer)
		
		hugeFont = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTWEIGHT_BOLD, wx.NORMAL)
		self.AddLabel(sizer, hugeFont, u"Sign In Here", wx.ALIGN_CENTER)
		self.AddLabel(sizer, MedFont(), u"Hi! What's your name?")
		
		self.nameEntryDefaultText = u"Type your name here."
		self.nameEntry = wx.TextCtrl(self, wx.ID_ANY, self.nameEntryDefaultText)
		self.nameEntry.Bind(wx.EVT_TEXT, self.OnNameEntryChange)
		self.nameEntry.Bind(wx.EVT_SET_FOCUS, self.OnNameEntryFocus)
		sizer.Add(self.nameEntry, 0, wx.EXPAND)
		
		self.AddLabel(sizer, MedFont(),
			u"If you've been here before,\nclick your name in the list:")
		
		self.nameListBox = wx.ListBox(self, wx.ID_ANY)
		self.nameListBox.Bind(wx.EVT_LISTBOX, self.OnListClick)
		self.nameListBox.Bind(wx.EVT_LISTBOX_DCLICK, self.OnListClick)
		sizer.Add(self.nameListBox, 0, wx.EXPAND)
		sizer.SetItemMinSize(self.nameListBox, wx.Size(-1, 125))
		
		self.shoptimeChoice = ShoptimeChoice(self, self.OnSigninClick)
		sizer.Add(self.shoptimeChoice, 0, wx.EXPAND)
		sizer.SetMinSize((200, 0))
		
		self.shoptimeChoice.Disable()
	
	def AddLabel(self, sizer, font, string, flags = 0):
		text = wx.StaticText(self, wx.ID_ANY, string)
		if font is not None:
			text.SetFont(font)
		sizer.Add(text, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL | flags, 5)
		return text
		
	def _PopulateList(self, partialName):	
		self.nameListBox.Clear()
		partialNameLen = len(partialName)

		if partialNameLen > 0:
			self.nameList = self.controller.FindPeopleByPartialName(partialName)
			if len(self.nameList) > 0:
				names = ["{0} {1}".format(n["firstName"], n["lastName"]).strip()
					for n in self.nameList]
				self.nameListBox.SetItems(names)

				self.nameListBox.SetSelection(-1)
				for i in range(len(names)):
					if partialName.lower() == names[i].lower():
						self.nameListBox.SetSelection(i)
						break
							
	def OnNameEntryChange(self, event):
		partialName = self.nameEntry.GetValue().strip()
		nameEntered = partialName != "" and partialName != self.nameEntryDefaultText
		self.shoptimeChoice.Enable(nameEntered)
		
		if self.suppressNextListChange:
			self.suppressNextListChange = False
		else:
			self._PopulateList(partialName)
			
	def OnNameEntryFocus(self, event):
		name = self.nameEntry.GetValue()
		if name == self.nameEntryDefaultText:
			self.nameEntry.SetValue("")
		elif name.lower() != self.nameListBox.GetStringSelection().lower():
			self.nameListBox.SetSelection(-1)
	
	def OnListClick(self, event):
		selection = self.nameListBox.GetStringSelection()
		if selection != "":
			self.suppressNextListChange = True
			self.nameEntry.SetValue(selection)
	
	def OnSigninClick(self, event, type):
		if type == "worktrade":
			if not self.controller.AuthenticateMechanic("do worktrade"):
				return
				
		elif type == "volunteer":
			if not self.controller.AuthenticateMechanic("volunteer"):
				return
			
		
		selection = self.nameListBox.GetSelection()
		if self.nameListBox.GetCount() == 0 or selection < 0:
			self.controller.ShowNewPersonDialog(self.nameEntry.GetValue(), type)
		else:
			self.controller.SignPersonIn(self.nameList[selection]["id"], type)
			
	def ResetValues(self):
		self.nameEntry.SetValue(self.nameEntryDefaultText)
		self.nameListBox.Clear()
		self.nameList = []
