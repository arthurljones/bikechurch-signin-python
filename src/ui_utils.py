import wx

sTypeDescriptions = {
	"shoptime":	"Working on a Bike",
	"parts":	"Looking for Parts",
	"worktrade":	"Doing Worktrade",
	"volunteer":	"Volunteering"
	}

def MakeInfoEntrySizer():
	sizer = wx.FlexGridSizer(0, 2)
	sizer.AddGrowableCol(1)
	return sizer

def AddField(parent, sizer, font, label, entryKind = wx.TextCtrl):
	text = wx.StaticText(parent, wx.ID_ANY, label)
	text.SetFont(font)
	parent.GetSizer().Add(text, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 5)
	field = entryKind(parent, wx.ID_ANY)
	parent.GetSizer().Add(field, 0, wx.EXPAND)
	return field
	
def AddLabel(parent, sizer, font, string, flags = 0, type = wx.StaticText):
	label = type(parent, wx.ID_ANY, string)
	label.SetFont(font)
	sizer.Add(label, 0, flags | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
	return label

def GetShoptimeTypeDescription(type):
	if type in sTypeDescriptions:
		return sTypeDescriptions[type]
	else:
		return "\"{0}\"".format(type)
