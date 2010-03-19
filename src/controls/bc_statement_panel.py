import wx
from autowrapped_static_text import AutowrappedStaticText

sBikeChurchStatement = \
	u"About the Bike Church:\n\n\tLorem ipsum dolor sit amet, consectetur adipiscing elit." \
	u" Nunc vulputate nibh id nisl luctus vel volutpat nisl euismod. Quisque sit amet odio " \
	u"enim, ut porttitor felis. Maecenas in lectus orci. In adipiscing, tellus a pretium " \
	u"convallis, erat ante posuere augue, sit amet blandit tellus dui eu nunc. Donec " \
	u"vehicula condimentum nulla sit amet posuere. Donec ac arcu a leo iaculis faucibus. " \
	u"Aenean vestibulum turpis mattis neque aliquet in mattis lectus sollicitudin. " \
	u"Phasellus neque odio, lacinia sit amet sodales vel, gravida a ligula. Cras ut velit " \
	u"arcu, non aliquam urna. Praesent vitae quam vel neque commodo pretium ut in ipsum. " \
	u"Curabitur. "

class BCStatementPanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)
        
		self.staticBox = wx.StaticBox(self, wx.ID_ANY, u"About The Bike Church")
		sizer = wx.StaticBoxSizer(self.staticBox, wx.HORIZONTAL)
		self.SetSizer(sizer)
		
		medFont = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
		text = AutowrappedStaticText(self, wx.ID_ANY, sBikeChurchStatement)
		text.SetFont(medFont)
		sizer.Add(text, 1, wx.EXPAND)
