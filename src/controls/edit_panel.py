# -*- coding: utf-8 -*-

import wx, datetime
from strings import trans
from sqlalchemy import (Integer, Unicode, Date, DateTime, Time)
from sqlalchemy.dialects.mysql.base import MSEnum 
from src.db import Person, Member, Bike, Shoptime, Feedback
from src.ui import MedFont, MakeInfoEntrySizer
from field import TextField, ChoiceField, DateField, TimeField, DateTimeField
from src.controller import GetController

def SetFieldType(ColumnType, FieldType):
	ColumnType.FieldType = FieldType
	
SetFieldType(Integer,	TextField)
SetFieldType(Unicode,	TextField)
SetFieldType(MSEnum,	ChoiceField)
SetFieldType(Date,		DateField)
SetFieldType(Time,		TimeField)
SetFieldType(DateTime,	DateTimeField)

class EditPanel(wx.Panel):
	def __init__(self, parent, tableType):
		wx.Panel.__init__(self, parent)
		self._tableType = tableType
				
		sizer = MakeInfoEntrySizer()
		self.SetSizer(sizer)
		
		self._fields = {}
		for tableField in tableType.fields:
			name = tableField[0]
			label = tableField[1]
			column = getattr(tableType.__table__.c, name)
			fieldEditor = None
			if len(tableField) >= 3:
				fieldEditor = tableField[2]
			else:
				fieldEditor = column.type.FieldType()
			
			fieldEditor.Setup(self, sizer, column, label)
			self._fields[name] = fieldEditor
		
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
			GetController().FlashError(trans.editPersonFirstName,
				[self["firstName"].Widget()])
		elif len(person.firstName) + len(person.lastName) < 3:
			GetController().FlashError(trans.editPersonThreeLetters,
				[self["firstName"].Widget(), self["lastName"].Widget()])
		elif not namesMatch and GetController().GetPersonByFullName(
			person.firstName, person.lastName):
			GetController().FlashError(trans.editPersonAlreadyExists,
				[self["firstName"].Widget(), self["lastName"].Widget()])
		else:
			return True
			
		return False
		
class EditBikePanel(EditPanel):
	def __init__(self, parent):
		EditPanel.__init__(self, parent, Bike)
		
		bikeTypes = [
		'Mountain',
		'Road',
		'Hybrid', 
		'Cruiser',
		'Three Speed',
		'Recumbent',
		'Chopper',
		'Mixte',
		'Tallbike',
		'Town Bike',
		'Touring',
		'Track',
		'Other',
		]
				
	
	def Validate(self):
		errors = []
		for value in ["color", "type", "serial"]:
			if not self[value].Get():
				errors.append(self[value].Widget())		
		if errors:
			GetController().FlashError(trans.editBikeNotEnoughInfo, errors)
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
		self["start"].Set(datetime.datetime.now() - datetime.timedelta(hours = 1))
	
	def Validate(self):
		shoptime = self.Get()		
				
		if shoptime.start > datetime.datetime.now():
			GetController().FlashError(trans.editShoptimeNoFuture,
				self["start"].Widget())
		elif shoptime.end < shoptime.start:
			GetController().FlashError(trans.editShoptimeNoTimeTravel,
				self["end"].Widget())
		elif not shoptime.type:
			GetController().FlashError(trans.editShoptimeNeedType,
				self["type"].Widget())
		else:
			return True	
		
		return False

class EditFeedbackPanel(EditPanel):
	def __init__(self, parent):
		EditPanel.__init__(self, parent, Feedback)
	
	def Validate(self):
		feedback = self.Get()
		
		if not feedback.feedback:
			GetController().FlashError(trans.editFeedbackNeedFeedback,
				[self["feedback"].Widget()])
		else:
			return True	
		
		return False
