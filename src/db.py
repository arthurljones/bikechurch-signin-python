 # -*- coding: utf-8 -*-
 
import sys, time
from .strings import trans
from sqlalchemy import (create_engine, MetaData, Column, Table, Integer, Unicode,
	Index, ForeignKeyConstraint, Date, DateTime, Time)
from sqlalchemy.dialects.mysql.base import MSEnum 
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#hack?
from controls.field import ForeverDateField

Base = declarative_base()

class Person(Base):
	__tablename__ = 'people'
	__table_args__ = { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8' }
	
	id		= Column(Integer, primary_key = True, unique = True, nullable = False)
	firstName	= Column(Unicode(64), nullable = False)
	lastName 	= Column(Unicode(64))
	
	memberInfo	= relationship('Member', backref = 'person', uselist = False,
		cascade = "all, delete, delete-orphan")
	shoptimes	= relationship('Shoptime', backref = 'person',
		cascade = "all, delete, delete-orphan")
	occupantInfo	= relationship('ShopOccupant', backref = 'person', uselist = False,
		cascade = "all, delete")
	bikes		= relationship('Bike', backref = 'owner',
		cascade = "all, delete, delete-orphan")
	
	fields = [
		("firstName", trans.patronFirstName),
		("lastName", trans.patronLastName),
	]
	
	def Name(self):
		return "{0}  {1}".format(self.firstName, self.lastName)
		
	def PosessiveFirstName(self):
		return "{0}'{1}".format(self.firstName, "s" if self.firstName[-1] != 's' else "")
		
	def __repr__(self):
		return "<{0}> {1}".format(self.__class__.__name__, self.Name())

Index('idx_fullName', Person.__table__.c.firstName, Person.__table__.c.lastName, unique = True)

class Member(Base):
	__tablename__ = 'members'
	__table_args__ = (
		ForeignKeyConstraint(['personID'], ['people.id'],
			ondelete = 'CASCADE', onupdate = 'CASCADE'), 
		{ 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8' }
	)
		
	id		= Column(Integer, primary_key = True, unique = True, nullable = False)
	personID	= Column(Integer, nullable = False, unique = True, index = True)
	startDate	= Column(Date, nullable = False)
	endDate		= Column(Date)
	mailingAddress	= Column(Unicode(200))
	emailAddress	= Column(Unicode(64))
	phoneNumber	= Column(Unicode(32))
	donation	= Column(Integer, nullable = False)
	notes		= Column(Unicode(200))
	
	fields = [
		("startDate", trans.memberStart),
		("endDate", trans.memberEnd, ForeverDateField),
		("donation", trans.memberDonation),
		("phoneNumber", trans.memberPhone),
		("emailAddress", trans.memberEmail),
		("mailingAddress", trans.memberSnailmail),
		("notes", trans.memberNotes),
	]
	
shoptimeChoices = {
	'shoptime' : trans.shoptimeTypeWorking,
	'parts' : trans.shoptimeTypeParts,
	'worktrade' : trans.shoptimeTypeWorktrade,
	'volunteer' : trans.shoptimeTypeVolunteer,
	#'clerkship' : "Doing a clerkship",
}

class Shoptime(Base):
	__tablename__ = 'shoptime'
	__table_args__ = (
		ForeignKeyConstraint(['personID'], ['people.id'],
			ondelete = 'CASCADE', onupdate = 'CASCADE'), 
		{ 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8' }
	)
		
	id		= Column(Integer, primary_key = True, unique = True, nullable = False)
	personID	= Column(Integer, nullable = False, index = True)
	start		= Column(DateTime, nullable = False)
	end		= Column(DateTime, nullable = False)
	notes 		= Column(Unicode(200))
	type 		= Column(MSEnum(*shoptimeChoices.keys(), strict = True),
				nullable = False, index = True)
	
	fields = [
		("start", trans.shoptimeStart),
		("end", trans.shoptimeEnd),
		("type", trans.shoptimeType),
		("notes", trans.shoptimeNotes),
	]
	
	def __repr__(self):
		return "<{0}> {1} From {2} Until {3}".format(
			self.__class__.__name__, self.type, self.start, self.end)		
	
Shoptime.__table__.c.type.type.choiceDict = shoptimeChoices
	
class ShopOccupant(Base):
	__tablename__ = 'shopOccupants'
	__table_args__ = (
		ForeignKeyConstraint(['personID'], ['people.id'],
			ondelete = 'CASCADE', onupdate = 'CASCADE'), 
		{ 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8' }
	)
		
	id		= Column(Integer, primary_key = True, unique = True, nullable = False)
	personID	= Column(Integer, nullable = False, index = True, unique = True)
	start		= Column(DateTime, nullable = False)
	type 		= Column(MSEnum(*shoptimeChoices, strict = True),
				nullable = False, index = True)
	
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
				
class Bike(Base):
	__tablename__ = 'bikes'
	__table_args__ = (
		ForeignKeyConstraint(['personID'], ['people.id'],
			ondelete = 'CASCADE', onupdate = 'CASCADE'), 
		{ 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8' }
	)
		
	id		= Column(Integer, primary_key = True, unique = True, nullable = False)
	personID	= Column(Integer, index = True)
	type		= Column(MSEnum(*bikeTypes, strict = True), nullable = False)
	color		= Column(Unicode(64), nullable = False)
	brand		= Column(Unicode(64))
	model		= Column(Unicode(64))
	serial		= Column(Unicode(64), nullable = False, index = True)

	fields = [
		("type", trans.bikeType),
		("color", trans.bikeColor),
		("brand", trans.bikeBrand),
		("model", trans.bikeModel),
		("serial", trans.bikeSerial),
	]
	
	def __repr__(self):
		return "<{0}> {1} {2} {3} {4} {5}".format(
			self.__class__.__name__, self.color, self.type, self.brand,
			self.model, self.serial)
			
class Feedback(Base):
	__tablename__ = 'feedback'
	__table_args__ = (
		{ 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8' }
	)
		
	id		= Column(Integer, primary_key = True, unique = True, nullable = False)
	date		= Column(DateTime, default = None, index = True, nullable = False)
	name		= Column(Unicode(64))
	feedback	= Column(Unicode(500), nullable = False)
				
	fields = [
		("name", trans.feedbackName),
		("feedback", trans.feedbackFeedback),
	]
	
	def __repr__(self):
		return "<{0}> From {1} on {2}: \"{3}\"...".format(
			self.__class__.__name__, self.name, self.date, self.feedback[:20])

def CreateTablesFromScratch():
	print("Creating database tables...")
	
	engine = create_engine('mysql://signin_creator:signin_creator@localhost/signin_db?charset=utf8')
	meta = MetaData()
	meta.reflect(bind = engine)
	meta.drop_all(bind = engine)
	
	Base.metadata.create_all(bind = engine)
	
	print("...Success")

_Session = None
_engine = None
session = None

def Connect():
	global _engine
	global _Session
	global session
	
	_engine = create_engine('mysql://signin:signin@localhost/signin_db?charset=utf8')
	_Session = sessionmaker(bind = _engine)
	session = _Session()

Connect()
