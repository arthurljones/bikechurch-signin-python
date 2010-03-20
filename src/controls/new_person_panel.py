import wx
from ..ui_utils import AddLabel
from autowrapped_static_text import AutowrappedStaticText
from edit_name_panel import EditNamePanel
from edit_bike_panel import EditBikePanel
from shoptime_choice import ShoptimeChoice

class NewPersonPanel(wx.Panel):
	def __init__(self, parent, controller):
		wx.Panel.__init__(self, parent)	
		self.controller = controller
		
		staticBox = wx.StaticBox(self, wx.ID_ANY, "")
		outerSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
		self.SetSizer(outerSizer)
		
		medFont = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)

		AddLabel(self, outerSizer, medFont, \
			u"It looks like you haven't used this "
			u"sign-in computer before. "
			u"Please tell us about yourself and your bike.", type = AutowrappedStaticText)
		
		staticBox = wx.StaticBox(self, wx.ID_ANY, u"Your Name")
		nameEntrySizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
		AddLabel(self, nameEntrySizer, medFont, u"Type Your Name:")
		self.editNamePanel = EditNamePanel(self)
		nameEntrySizer.Add(self.editNamePanel, 0, wx.EXPAND)
		outerSizer.Add(nameEntrySizer, 0, wx.EXPAND)
		
		staticBox = wx.StaticBox(self, wx.ID_ANY, "Your Bike")
		bikeEntrySizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
		AddLabel(self, bikeEntrySizer, medFont, "Describe Your Bike (if you have one):")			
		self.editBikePanel = EditBikePanel(self)
		bikeEntrySizer.Add(self.editBikePanel, 0, wx.EXPAND)
		outerSizer.Add(bikeEntrySizer, 0, wx.EXPAND)
		
		shoptimeSizer = wx.FlexGridSizer(0, 2)
		shoptimeSizer.SetFlexibleDirection(wx.VERTICAL)
		self.shoptimeChoice = ShoptimeChoice(self, self.OnSigninClick, shoptimeSizer)
		outerSizer.Add(self.shoptimeChoice, 0, wx.EXPAND)

		self.GetSizer().SetMinSize((200, 0))
	
	def OnSigninClick(self, event, type):
		print "signin"
		if self.editNamePanel.Validate():
			print "name validated"
			personID = self.controller.CreatePerson(
				self.editNamePanel.GetValues())
			
			if not self.editBikePanel.IsEmpty():
				print "bikepanel filled"
				if self.editBikePanel.Validate():
					print "bikepanel validated"
					self.controller.CreateBike(
						self.editBikePanel.GetValues(),
						personID)
				
			self.controller.SignPersonIn(personID, type)
		
	def SetPersonName(self, firstName, lastName):
		self.editNamePanel.SetValues(firstName, lastName)

	def ResetValues(self):
		self.editNamePanel.ResetValues()
		self.editBikePanel.ResetValues()
