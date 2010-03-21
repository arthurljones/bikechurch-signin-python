 # -*- coding: utf-8 -*-
 
import wx

def MakeInfoEntrySizer():
	sizer = wx.FlexGridSizer(0, 2)
	sizer.AddGrowableCol(1)
	return sizer

def AddField(parent, sizer, font, label, entryKind = wx.TextCtrl, style = 0):
	text = wx.StaticText(parent, wx.ID_ANY, label)
	if font:
		text.SetFont(font)
	sizer.Add(text, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 5)
	field = entryKind(parent, wx.ID_ANY, style = style)
	sizer.Add(field, 0, wx.EXPAND)
	return field
	
def AddLabel(parent, sizer, font, string, flags = 0, type = wx.StaticText):
	label = type(parent, wx.ID_ANY, string)
	label.SetFont(font)
	sizer.Add(label, 0, flags | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
	return label

_sMedFont = None
def MedFont():
	global _sMedFont
	if not _sMedFont:
		_sMedFont = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
		
	return _sMedFont

_sBigFont = None
def BigFont():
	global _sBigFont
	if not _sBigFont:
		_sBigFont = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
		
	return _sBigFont

class Delegator():
	def __init__(self):
		self._delegates = []
		
	def AppendDelegate(self, delegate):
		self._delegates.append(delegate)
		
	def PushDelegate(self, delegate):
		self._delegates.insert(0, delegate)
		
	def RemoveDelegate(self, delegate):
		try:
			self._delegates.remove(delegate)
		except ValueError:
			pass
	
	def __getattr__(self, attr):
		if self.__dict__.has_key(attr):
			return self.__dict__[attr]
			
		for delegate in self._delegates:
			if hasattr(delegate, attr):
				return getattr(delegate, attr)
					
		raise AttributeError("No attribute \'{0}\' in {1} or delegates".format(
			attr, self.__class__.__name__))
			
