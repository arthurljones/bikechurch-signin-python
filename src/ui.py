import wx

from screens.main import MainScreen
from screens.new_person import NewPersonScreen
from controls.status_bar import StatusBar

class ErrorDisplay(wx.StaticText):
	def __init__(self, parent, controller, label):
		pass
		
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
			size = wx.Size(900, 500), style = wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
		
		self.screens = []
		self.currentScreen = None
		
		self.mainScreen = MainScreen(self.frame, controller)
		self.screens.append(self.mainScreen)
		self.newPersonScreen = NewPersonScreen(self.frame, controller)
		self.screens.append(self.newPersonScreen)
		
		sizer = wx.FlexGridSizer(2, 1)
		sizer.AddGrowableRow(0)
		sizer.AddGrowableCol(0)
		self.frame.SetSizer(sizer)
		self.frame.Centre(wx.BOTH)
		self.frame.Show()
		
		self.screenSizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(self.screenSizer, 1, wx.EXPAND)
		self.statusBar = StatusBar(self.frame, self.controller)
		sizer.Add(self.statusBar, 0, wx.EXPAND)
	
		self.ShowMainScreen()
		#self.ShowNewPersonScreen()
		
		self.frame.Bind(wx.EVT_SIZE, self.OnResize)
		
	def Layout(self):
		for screen in self.screens:
			screen.Layout()
		self.frame.Layout()
		
	def OnResize(self, event):
		self.Layout()
	
	def HideAllScreens(self):
		for screen in self.screens:
			screen.Hide()
		self.currentScreen = None

	############
	
	def __getattr__(self, attr):
		
		if self.__dict__.has_key(attr):
			return self.__dict__[attr]
		
		if self.__dict__.has_key("currentScreen"):
			if self.currentScreen and hasattr(self.currentScreen, attr):
				return getattr(self.currentScreen, attr)
		
		if self.__dict__.has_key("screens"):
			for screen in self.screens:
				if hasattr(screen, attr):
					return getattr(screen, attr)
					
		raise AttributeError("No attribute {0} in {1} or children".format(
			attr, self.__class__.__name__))
			

	def ShowMainScreen(self):
		self.HideAllScreens()
		self.mainScreen.Show(self.screenSizer)
		self.frame.Layout()
		self.currentScreen = self.mainScreen
		
	def ShowNewPersonScreen(self):
		self.HideAllScreens()
		self.newPersonScreen.Show(self.screenSizer)
		self.frame.Layout()
		self.currentScreen = self.newPersonScreen
	
	def GetCurrentScreen(self):
		return self.currentScreen
