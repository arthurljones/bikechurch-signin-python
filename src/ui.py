import wx

from screens.main import MainScreen
from screens.new_person import NewPersonScreen

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
		
	def Layout(self):
		for screen in self.screens:
			screen.Layout()
		self.frame.Layout()
		
	def OnResize(self, event):
		self.Layout()
	
	def OnTimer(self, event):
		self.mainScreen.occupantsArea.UpdateTimes()
		
	def HideAllScreens(self):
		for screen in self.screens:
			screen.Hide()
		self.currentScreen = None

	############

	def ShowMainScreen(self):
		self.HideAllScreens()
		self.mainScreen.Show()
		self.frame.Layout()
		self.currentScreen = self.mainScreen
		
	def ShowAddPersonScreen(self):
		self.HideAllScreens()
		self.newPersonScreen.Show()
		self.frame.Layout()
		self.currentScreen = self.newPersonScreen
	
	def GetCurrentScreen(self):
		return self.currentScreen
		
		
	def ResetSignin(self):
		self.mainScreen.signinPanel.Reset()
		
	def AddPersonToShopList(self, personID, start, type):
		self.mainScreen.signinPanel.AddOccupantLine(personID, start, type)
		
	def RemovePersonFromShopList(self, personID):
		self.mainScreen.signinPanel.RemoveOccupantLine(personID)
