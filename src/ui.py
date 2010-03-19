import wx

from controls.occupants_list import OccupantsList
from controls.signin_panel import SignInPanel
from controls.new_person_panel import NewPersonPanel
from controls.bc_statement_panel import BCStatementPanel

class TextValidator(wx.PyValidator):
	def __init__(self, onError):
		wx.PyValidator.__init__(self)

	def Clone(self):
		return TextValidator()

	def TransferToWindow(self):
		return True

	def TransferFromWindow(self):
		return True

	def Validate(self, win):
		textCtrl = self.GetWindow()
		text = textCtrl.GetValue()

class Screen(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)

		self.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
		self.elements = []
		
		self.Hide()

	def AddElement(self, element):
		self.elements.append(element)

	def Show(self):
		sizer = self.GetParent().GetSizer()
		sizer.Add(self, 1, wx.EXPAND)
		wx.Panel.Show(self)
		self.Layout()
		
	def Hide(self):
		wx.Panel.Hide(self)
		sizer = self.GetContainingSizer()
		if sizer:
			sizer.Detach(self)
			
	def Layout(self):
		for element in self.elements:
			element.Layout()
		wx.Panel.Layout(self)
			
class NewPersonScreen(Screen):
	def __init__(self, parent, controller):
		Screen.__init__(self, parent)
		
		sizer = wx.FlexGridSizer(0, 2)
		sizer.SetFlexibleDirection(wx.HORIZONTAL)
		sizer.AddGrowableCol(1)
		self.SetSizer(sizer)
		
		self.newPersonPanel = NewPersonPanel(self, controller)
		self.bcStatement = BCStatementPanel(self)
		
		self.GetSizer().Add(self.newPersonPanel, 1, wx.ALL | wx.EXPAND, 3)
		self.GetSizer().Add(self.bcStatement, 1, wx.EXPAND | wx.ALL, 3)
		
		self.AddElement(self.newPersonPanel)
		self.AddElement(self.bcStatement)

class MainScreen(Screen):
	def __init__(self, parent, controller):
		Screen.__init__(self, parent)
		
		self.occupantsList = OccupantsList(self, controller)
		self.signinPanel = SignInPanel(self, controller)
		
		self.GetSizer().Add(self.signinPanel, 0, wx.ALL, 8)
		self.GetSizer().Add(self.occupantsList, 1, wx.EXPAND | wx.ALL, 8)
		
		self.AddElement(self.occupantsList)
		self.AddElement(self.signinPanel)

class MainWindow():
	def __init__(self, controller):
				
		self.controller = controller
		controller.SetUI(self)
		
		self.frame = wx.Frame(None, id = wx.ID_ANY, title = u"Welcome To The Bike Church!",
			size = wx.Size(900, 480), style = wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
		
		self.screens = []
		
		self.mainScreen = MainScreen(self.frame, controller)
		self.screens.append(self.mainScreen)
		self.newPersonScreen = NewPersonScreen(self.frame, controller)
		self.screens.append(self.newPersonScreen)
		
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.frame.SetSizer(sizer)
		self.frame.Centre(wx.BOTH)
		self.frame.Show()
	
		self.ShowMainScreen()
		
		self.updateTimer = wx.Timer(self.frame)
		self.updateTimer.Start(1000 * 60)

		self.frame.Bind(wx.EVT_SIZE, self.OnResize)
		self.frame.Bind(wx.EVT_TIMER, self.OnTimer)

	def HideAllScreens(self):
		for screen in self.screens:
			screen.Hide()

	def ShowMainScreen(self):
		self.HideAllScreens()
		self.mainScreen.Show()
		self.frame.Layout()
		
	def ShowAddPersonScreen(self):
		self.HideAllScreens()
		self.newPersonScreen.Show()
		self.frame.Layout()
		
	def Layout(self):
		for screen in self.screens:
			screen.Layout()
		self.frame.Layout()
		
	def OnResize(self, event):
		self.Layout()
	
	def OnTimer(self, event):
		self.mainScreen.occupantsArea.UpdateTimes()
		
	def ResetSignin(self):
		self.mainScreen.signinPanel.Reset()
		
	def AddPersonToShopList(self, personID, start, type):
		self.mainScreen.signinPanel.AddOccupantLine(personID, start, type)
		
	def RemovePersonFromShopList(self, personID):
		self.mainScreen.signinPanel.RemoveOccupantLine(personID)
