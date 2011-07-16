# -*- coding: utf-8 -*-

import wx
from datetime import datetime
import db

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

_sHugeFont = None
def HugeFont():
	global _sHugeFont
	if not _sHugeFont:
		_sHugeFont = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
		
	return _sHugeFont

def GetShoptimeTypeDescription(type):
	if type in db.shoptimeChoices:
		return db.shoptimeChoices[type]
	else:
		return "\"{0}\"".format(type)

def MakeInfoEntrySizer():
	sizer = wx.FlexGridSizer(0, 2)
	sizer.AddGrowableCol(1)
	return sizer
	
def MakeStaticBoxSizer(parent, label = "", style = wx.HORIZONTAL):
	staticBox = wx.StaticBox(parent, label = label)
	staticBox.SetFont(MedFont())
	return wx.StaticBoxSizer(staticBox, style)	

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

def FormatTimedelta(timedelta):
	hours = timedelta.days * 24
	hours += timedelta.seconds / (3600)
	minutes = (timedelta.seconds % 3600) / 60
	return "{0}h {1}m".format(hours, minutes)

def DatetimeWxToPy(wxdt):
	return datetime(
		wxdt.GetYear(),
		wxdt.GetMonth() + 1,
		wxdt.GetDay(),
		wxdt.GetHour(),
		wxdt.GetMinute(),
		wxdt.GetSecond(),
		wxdt.GetMillisecond() * 1000)

def DatetimePyToWx(pydt):
	wxdt = wx.DateTime().Now()
	
	if hasattr(pydt, "year"):
		wxdt.SetYear(pydt.year)
		wxdt.SetMonth(pydt.month - 1)
		wxdt.SetDay(pydt.day)
		
	if hasattr(pydt, "hour"):
		wxdt.SetHour(pydt.hour)
		wxdt.SetMinute(pydt.minute)
		wxdt.SetSecond(pydt.second)
		wxdt.SetMillisecond(pydt.microsecond / 1000)
		
	return wxdt

def GetTextSize(text, font, parent):
	dc = wx.ClientDC(parent);
	dc.SetFont(font)
	return dc.GetTextExtent(text)

class Delegator(object):
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
		if attr in self.__dict__:
			return self.__dict__[attr]
			
		for delegate in self._delegates:
			if hasattr(delegate, attr):
				return getattr(delegate, attr)
					
		raise AttributeError("No attribute \'{0}\' in {1} or delegates".format(
			attr, self.__class__.__name__))
			
class WindowSizes:
	pass

winSizes = WindowSizes()

winSizes.mainWindow = (1000, 550)
winSizes.authenticateMechanic = (300, 140)
winSizes.newPerson = (350, 450)
winSizes.viewPerson = (950, 470)
winSizes.shoptimeDialog = (300, 200)
winSizes.bikeDialog = (330, 200)
winSizes.feedbackDialog = (340, 160)
winSizes.mechanicToolbox = (250, 150)
winSizes.findBike = (450, 370)
