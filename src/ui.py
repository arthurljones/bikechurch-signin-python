 # -*- coding: utf-8 -*-
 
import wx, time
from datetime import datetime, MAXYEAR
from sqlalchemy import (Integer, Unicode, Date, DateTime, Time)
from sqlalchemy.dialects.mysql.base import MSEnum 
from db import Person, Member, Bike

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

_typeDescriptions = {
	"shoptime":	"Working on a Bike",
	"parts":	"Looking for Parts",
	"worktrade":	"Doing Worktrade",
	"volunteer":	"Volunteering"
	}

def GetShoptimeTypeDescription(type):
	if type in _typeDescriptions:
		return _typeDescriptions[type]
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

def FormatTimediff(timediff):
	seconds = timediff.seconds
	hours = int(timediff.seconds / (60 * 60))
	seconds -= hours * (60 * 60)
	hours += timediff.days * 24
	minutes = seconds / 60

	timeString = []
	if hours > 0:
		timeString.append("{0}hr".format(hours))
	if minutes > 0 or hours == 0:
		timeString.append("{0}min".format(minutes))
		
	return " ".join(timeString)

def wxDatetimeToPy(wxDatetime):
	return datetime.fromtimestamp(wxDatetime.GetTicks())
	
def pyDatetimeToWx(pyDatetime):
	return wx.DateTimeFromTimeT(time.mktime(pyDatetime.timetuple()))

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
		if self.__dict__.has_key(attr):
			return self.__dict__[attr]
			
		for delegate in self._delegates:
			if hasattr(delegate, attr):
				return getattr(delegate, attr)
					
		raise AttributeError("No attribute \'{0}\' in {1} or delegates".format(
			attr, self.__class__.__name__))

class Field(object):
	def __init__(self, parent, sizer, column, label, entry, default):
		self._default = default
		self._entry = entry
		
		labelCtrl = wx.StaticText(parent, label = label)
		labelCtrl.SetFont(MedFont())
		
		sizer.Add(labelCtrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 5)
		sizer.Add(entry, 0, wx.EXPAND)
		
		self.Reset()
		
	def Default(self):
		return self._default()
		
	def Reset(self):
		return self.Set(self.Default())
		
	def Widget(self):
		return self._entry
		
class TextField(Field):
	def __init__(self, parent, sizer, column, label, default = lambda: ""):
		style = 0
		if hasattr(column.type, "length") and column.type.length >= 200:
			style = wx.TE_MULTILINE
			
		text = wx.TextCtrl(parent, style = style)
		Field.__init__(self, parent, sizer, column, label, text, default)
		
	def Get(self):
		return unicode(self.Widget().GetValue())
		
	def Set(self, value):
		return self.Widget().SetValue(unicode(value))
		
class ChoiceField(Field):
	def __init__(self, parent, sizer, column, label, default = lambda: ""):
		self._choice = wx.Choice(parent)
		self._choice.SetItems(column.type.enums)
		Field.__init__(self, parent, sizer, column, label, self._choice, default)
		
	def Get(self):
		return self.Widget().GetStringSelection()
		
	def Set(self, value):
		return self.Widget().SetStringSelection(value)
		
class DateField(Field):
	def __init__(self, parent, sizer, column, label, default = datetime.now):
		self._date = wx.DatePickerCtrl(parent)
		Field.__init__(self, parent, sizer, column, label, self._date, default)
		
	def Get(self):
		return wxDatetimeToPy(self.Widget().GetValue())

	def Set(self, value):
		if value is None:
			value = datetime(2032, 12, 31)
		return self.Widget().SetValue(pyDatetimeToWx(value))
		
class TimeField(Field):
	def __init__(self, parent, sizer, column, label, default = datetime.now):
		self._time = wx.lib.masked.TimeCtrl
		Field.__init__(self, parent, sizer, column, label, self._time, default)	\
		
	def Get(self):
		return wxDatetimeToPy(self.Widget().GetValue())

	def Set(self, value):
		return self.Widget().SetValue(pyDatetimeToWx(value))
		
class DateTimeField(Field):
	pass 
	
def SetFieldType(ColumnType, FieldType):
	ColumnType.FieldType = FieldType
	
#Set up field type information in sqlalchemy column types
SetFieldType(Integer,	TextField)
SetFieldType(Unicode,	TextField)
SetFieldType(MSEnum,	ChoiceField)
SetFieldType(Date,	DateField)
SetFieldType(Time,	TimeField)
SetFieldType(DateTime,	DateTimeField)

class EditPanel(wx.Panel):
	def __init__(self, parent, controller, tableType):
		wx.Panel.__init__(self, parent)
		self._controller = controller
		self._tableType = tableType
				
		sizer = MakeInfoEntrySizer()
		self.SetSizer(sizer)
		
		self._fields = {}
		for field in tableType.fields:
			name = field[0]
			label = field[1]
			column = getattr(tableType.__table__.c, name)
			field = column.type.FieldType(self, sizer, column, label)
			self._fields[name] = field
		
	def __getitem__(self, field):
		return self._fields[field]
		
	def IsEmpty(self):
		for field in self._fields.keys():
			if self[field].Get():
				return False
		return True
		
	def Get(self):
		object = self._tableType()
		for fieldName in self._fields.keys():
			setattr(object, fieldName, self[fieldName].Get())
		return object
			
	def Set(self, object):
		for fieldName in self._fields.keys():
			self[fieldName].Set(getattr(object, fieldName))

	def ResetValues(self):
		for field in self._fields:
			field.Reset()

class EditPersonPanel(EditPanel):
	def __init__(self, parent, controller):
		EditPanel.__init__(self, parent, controller, Person)
	
	def Validate(self):
		person = self.Get()
		
		if not person.firstName:
			self._controller.FlashError(
				"You must enter at least your first name.",
				[self["firstName"].Widget()])
		elif len(person.firstName) + len(person.lastName) < 3:
			self._controller.FlashError(
				"Your name must have at least three letters.",
				[self["firstName"].Widget(), self["lastName"].Widget()])
		elif self._controller.GetPersonByFullName(person.firstName, person.lastName):
			self._controller.FlashError(
				"There's already somebody with that name in the database.",
				[self["firstName"].Widget(), self["lastName"].Widget()])
		else:
			return True
			
		return False
		
class EditBikePanel(EditPanel):
	def __init__(self, parent, controller):
		EditPanel.__init__(self, parent, controller, Bike)
	
	def Validate(self):
		errors = []
		for value in ["color", "type", "serial"]:
			if not self[value].Get():
				errors.append(self[value].Widget())		
		if errors:
			self._controller.FlashError(
			"You need at least the color, type, and serial # for your bike",
			errors)
			return False
			
		return True
		
class EditMemberPanel(EditPanel):
	def __init__(self, parent, controller):
		EditPanel.__init__(self, parent, controller, Member)
		self.GetSizer().SetMinSize((200, 0))
	
	def Validate(self):		
		#TODO: Validate
			
		return True
		

