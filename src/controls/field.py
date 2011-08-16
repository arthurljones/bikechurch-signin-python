# -*- coding: utf-8 -*-

import wx.lib.masked.timectrl
from datetime import datetime
from src.ui import MedFont, DatetimeWxToPy, DatetimePyToWx

class Field(object):
	def __init__(self, default):
		self._setup = False
		self._Default = default
		
	def Setup(self, parent, sizer, column, label, entryWidget):
		self._entryWidget = entryWidget
		
		labelCtrl = wx.StaticText(parent, label = label)
		labelCtrl.SetFont(MedFont())
		
		sizer.Add(labelCtrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 5)
		sizer.Add(entryWidget, 1, wx.EXPAND)
		
		self.Reset()
		self._setup = True
				
	def Default(self):
		return self._Default()
		
	def Reset(self):
		return self.Set(self.Default())
		
	def Widget(self):
		return self._entryWidget
	
	def IsStarted(self):
		return self._setup
		
class TextField(Field):
	def __init__(self, default = lambda: ""):
		Field.__init__(self, default)
		
	def Setup(self, parent, sizer, column, label):	
		style = 0
		if hasattr(column.type, "length") and column.type.length >= 200:
			style = wx.TE_MULTILINE
			
		text = wx.TextCtrl(parent, style = style)
		Field.Setup(self, parent, sizer, column, label, text)
			
	def Get(self):
		return unicode(self.Widget().GetValue())
		
	def Set(self, value):
		return self.Widget().SetValue(unicode(value))
		
class ChoiceField(Field):
	def __init__(self, default = lambda: "", choiceDict = None):
		Field.__init__(self, default)
		self._choiceDict = choiceDict
		
	def Setup(self, parent, sizer, column, label):
		self._choice = wx.Choice(parent)
		if self._choiceDict is None:
			self._choiceDict = {}
			for enum in column.type.enums:
				self._choiceDict[enum] = enum
				
		self._inverseChoiceDict = dict((v,k) for k, v in self._choiceDict.iteritems())
		choices = self._choiceDict.values()
		choices.insert(0, self._Default())
		self._choice.SetItems(choices)
		Field.Setup(self, parent, sizer, column, label, self._choice)
		
	def Get(self):
		selection = self.Widget().GetStringSelection()
		
		if selection == self._Default():
			return None
		else:
			return self._choiceDict[selection]
		
	def Set(self, value):
		if value in self._inverseChoiceDict:
			return self.Widget().SetStringSelection(self._inverseChoiceDict[value])
		else:
			return self.Widget().SetStringSelection(value)
		
class DateField(Field):
	def __init__(self, default = datetime.now):
		Field.__init__(self, default)
		
	def Setup(self, parent, sizer, column, label):
		self._date = wx.DatePickerCtrl(parent)
		Field.Setup(self, parent, sizer, column, label, self._date)		
		
	def Get(self):
		return DatetimeWxToPy(self.Widget().GetValue()).date()

	def Set(self, value):
		return self.Widget().SetValue(DatetimePyToWx(value))
		
class ForeverDateField(Field):
	def __init__(self, default = datetime.now):
		Field.__init__(self, default)
		
	def Setup(self, parent, sizer, column, label):
		innerSizer = wx.BoxSizer(wx.HORIZONTAL)
		self._date = wx.DatePickerCtrl(parent)
		self._forever = wx.CheckBox(parent, label = "Never")
		
		innerSizer.Add(self._date, 1, wx.EXPAND)
		innerSizer.Add(self._forever, 0, wx.EXPAND)
		
		Field.Setup(self, parent, sizer, column, label, innerSizer)
		
		self._forever.Bind(wx.EVT_CHECKBOX, self._OnCheckbox)
		
	def _SyncCheckboxAndDate(self):
		if self._forever.GetValue() == True:
			self._date.Disable()
		else:
			self._date.Enable()
	
	def _OnCheckbox(self, event):
		self._SyncCheckboxAndDate()
		
	def Get(self):
		if self._forever.GetValue() == True:
			return DatetimeWxToPy(self._date.GetValue())
		else:
			return False

	def Set(self, value):
		retval = None		
		if value is None:
			self._forever.SetValue(True)
			retval = True
		else:
			self._forever.SetValue(False)
			retval = self._date.SetValue(DatetimePyToWx(value))
			
		self._SyncCheckboxAndDate()
		return retval
		
	def Widget(self):
		return self._date, self._forever
		
class TimeField(Field):
	def __init__(self, default = datetime.now):
		Field.__init__(self, default)
		
	def Setup(self, parent, sizer, column, label):
		self._time = wx.lib.masked.timectrl.TimeCtrl(parent, format = "HHMM")
		Field.Setup(self, parent, sizer, column, label, self._time)
		
	def Get(self):
		return DatetimeWxToPy(self.Widget().GetWxDateTime()).time()

	def Set(self, value):
		return self.Widget().SetValue(DatetimePyToWx(value))
		
class DateTimeField(Field):
	def __init__(self, default = datetime.now):
		Field.__init__(self, default)
		
	def Setup(self, parent, sizer, column, label):
		innerSizer = wx.BoxSizer(wx.HORIZONTAL)
		self._date = wx.DatePickerCtrl(parent)
		self._time = wx.lib.masked.timectrl.TimeCtrl(parent, format = "HHMM")
		
		innerSizer.Add(self._date, 1, wx.EXPAND)
		innerSizer.Add(self._time, 1, wx.EXPAND)
		
		Field.Setup(self, parent, sizer, column, label, innerSizer)
		
	def Get(self):
		date = self._date.GetValue()
		time = self._time.GetWxDateTime()
		result = datetime(date.GetYear(), date.GetMonth() + 1, date.GetDay(),
			hour = time.GetHour(), minute = time.GetMinute())
		return result 

	def Set(self, value):
		wxDatetime = DatetimePyToWx(value)
		self._date.SetValue(wxDatetime)
		self._time.SetValue(wxDatetime)
		return True
		
	def Widget(self):
		return [self._date, self._time]
