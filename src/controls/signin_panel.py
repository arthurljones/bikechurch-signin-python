import wx
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
		
		bigFont = wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTWEIGHT_BOLD, wx.NORMAL)
		medFont = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
		self.AddLabel(sizer, bigFont, u"Sign In Here", wx.ALIGN_CENTER)
		self.AddLabel(sizer, medFont, u"Hi! What's your name?")
		
		self.nameEntryDefaultText = u"Type your name here."
		self.nameEntry = wx.TextCtrl(self, wx.ID_ANY, self.nameEntryDefaultText)
		self.nameEntry.Bind(wx.EVT_TEXT, self.OnNameEntryChange)
		self.nameEntry.Bind(wx.EVT_SET_FOCUS, self.OnNameEntryFocus)
		sizer.Add(self.nameEntry, 0, wx.EXPAND)
		
		self.AddLabel(sizer, medFont, u"If you've been here before,\nclick your name in the list:")
		
		self.nameListBox = wx.ListBox(self, wx.ID_ANY)
		self.nameListBox.Bind(wx.EVT_LISTBOX, self.OnListClick)
		self.nameListBox.Bind(wx.EVT_LISTBOX_DCLICK, self.OnListClick)
		sizer.Add(self.nameListBox, 0, wx.EXPAND)
		sizer.SetItemMinSize(self.nameListBox, wx.Size(-1, 150))
		
		self.shoptimeChoice = ShoptimeChoice(self, self.OnSigninClick)
		sizer.Add(self.shoptimeChoice, 0, wx.EXPAND)
		sizer.SetMinSize((200, 0))
	
	def AddLabel(self, sizer, font, string, flags = 0):
		text = wx.StaticText(self, wx.ID_ANY, string)
		if font is not None:
			text.SetFont(font)
		sizer.Add(text, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL | flags, 5)
		return text
		
	def OnNameEntryChange(self, event):
		if self.suppressNextListChange:
			self.suppressNextListChange = False
			event.Skip()
			return
			
		self.nameListBox.Clear()
		partialName = self.nameEntry.GetValue()
		partialNameLen = len(partialName)

		if partialNameLen > 1:
			self.nameList = self.controller.FindPeopleByPartialName(partialName)
			if len(self.nameList) > 0:
				names = ["{0} {1}".format(n["firstName"], n["lastName"])
					for n in self.nameList]
				self.nameListBox.SetItems(names)

				self.nameListBox.SetSelection(-1)
				for i in range(len(names)):
					if partialName.lower() == names[i].lower():
						self.nameListBox.SetSelection(i)
					break
	
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
		selection = self.nameListBox.GetSelection()
		nameEntered = self.nameEntry.GetValue()
		if not nameEntered or nameEntered == self.nameEntryDefaultText:
			#TODO: Flash name box
			pass
		elif self.nameListBox.GetCount() == 0 or selection < 0:
			self.controller.ShowNewPersonScreen(self.nameEntry.GetValue(), type)
		else:
			self.controller.SignPersonIn(self.nameList[selection]["id"], type)
			
	def ResetValues(self):
		print "reset values on signin panel"
		self.nameEntry.SetValue(self.nameEntryDefaultText)
		self.nameListBox.Clear()
		self.nameList = []
