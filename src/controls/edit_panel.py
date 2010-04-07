import wx
from sqlalchemy import (Integer, Unicode, Date, DateTime, Time)
from sqlalchemy.dialects.mysql.base import MSEnum 
from ..db import Person, Member, Bike, Shoptime
from ..ui import MedFont, MakeInfoEntrySizer
from field import TextField, ChoiceField, DateField, TimeField, DateTimeField
from ..controller import GetController

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
	def __init__(self, parent, tableType):
		wx.Panel.__init__(self, parent)
		self._tableType = tableType
				
		sizer = MakeInfoEntrySizer()
		self.SetSizer(sizer)
		
		self._fields = {}
		for field in tableType.fields:
			name = field[0]
			label = field[1]
			column = getattr(tableType.__table__.c, name)
			Type = column.type.FieldType
			if len(field) >= 3:
				Type = field[2]
			field = Type(self, sizer, column, label)
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
			
	def Update(self, object):
		for fieldName in self._fields.keys():
			setattr(object, fieldName, self[fieldName].Get())

	def ResetValues(self):
		for field in self._fields:
			field.Reset()

class EditPersonPanel(EditPanel):
	def __init__(self, parent):
		EditPanel.__init__(self, parent, Person)
	
	def Validate(self, updating = None):
		person = self.Get()
		
		namesMatch = (updating
			and updating.firstName == person.firstName
			and updating.lastName == person.lastName)
		
		if not person.firstName:
			GetController().FlashError(
				"You must enter at least your first name.",
				[self["firstName"].Widget()])
		elif len(person.firstName) + len(person.lastName) < 3:
			GetController().FlashError(
				"Your name must have at least three letters.",
				[self["firstName"].Widget(), self["lastName"].Widget()])
		elif not namesMatch and GetController().GetPersonByFullName(
			person.firstName, person.lastName):
			GetController().FlashError(
				"There's already somebody with that name in the database.",
				[self["firstName"].Widget(), self["lastName"].Widget()])
		else:
			return True
			
		return False
		
class EditBikePanel(EditPanel):
	def __init__(self, parent):
		EditPanel.__init__(self, parent, Bike)
	
	def Validate(self):
		errors = []
		for value in ["color", "type", "serial"]:
			if not self[value].Get():
				errors.append(self[value].Widget())		
		if errors:
			GetController().FlashError(
			"You need at least the color, type, and serial # for your bike",
			errors)
			return False
			
		return True
		
class EditMemberPanel(EditPanel):
	def __init__(self, parent):
		EditPanel.__init__(self, parent, Member)
		self.GetSizer().SetMinSize((200, 0))
	
	def Set(self, value):
		if value is None:
			self.Disable()
		else:
			self.Enable()
			EditPanel.Set(self, value)

	def Get(self):
		if self.IsEnabled():
			return EditPanel.Get(self)
		else:
			return None
			
	def Update(self, object):
		if self.IsEnabled():
			EditPanel.Update(self, object)
	
	def Validate(self):
		#TODO: Validate
			
		return True
		
class EditShoptimePanel(EditPanel):
	def __init__(self, parent):
		EditPanel.__init__(self, parent, Shoptime)
	
	def Validate(self):
		#TODO: Validate
			
		return True
