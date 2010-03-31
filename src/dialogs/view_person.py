 # -*- coding: utf-8 -*-
 
import wx, datetime
from ..ui import (AddLabel, MedFont, FormatTimediff, GetShoptimeTypeDescription, 
	EditPersonPanel, EditMemberPanel, MakeStaticBoxSizer)
from ..controls.autowrapped_static_text import AutowrappedStaticText

def _GetShoptimes(person):
	result = []
	for time in person.shoptimes:
		startTime = time.start.strftime("%a %b %d %Y %I:%m%p")
		duration =  FormatTimediff(time.end - time.start)
		description = GetShoptimeTypeDescription(time.type)
		string = "{0}: {2} for {1}".format(startTime, duration, description)
		
		result.append((string, time))
	
	result.reverse()
	return result
		
def _GetBikes(person):
	result = []
	for bike in person.bikes:
		string = []
		string.append(bike.color)
		if bike.brand:
			string.append(bike.brand)
		if bike.model:
			string.append(bike.model)
		
		string.append("{0} bike:".format(bike.type))
		string.append("S/N {0}".format(bike.serial))
		
		result.append((" ".join(string), bike))
		
	return result
		
class AddEditRemoveList(wx.Panel):
	def __init__(self, parent, person, label, buttonSuffix, getItems,
			onAdd, onEdit, onRemove):
		'''getItems is a function that takes a db.Person and returns a list of tuples:
		   (string, object); string will be displayed in the list, and object will
		   be returned from GetValue when its associated string is selected in the list.'''
		wx.Panel.__init__(self, parent)
		self._GetItems = getItems
		self._person = person
		self._onAddFunc = onAdd
		self._onEditFunc = onEdit
		self._onRemoveFunc = onRemove

		outerSizer = MakeStaticBoxSizer(self, label, wx.VERTICAL)
		self.SetSizer(outerSizer)
		
		self.list = wx.ListBox(self)
		outerSizer.Add(self.list, 1, wx.EXPAND | wx.ALL, 2)
	
		add = wx.Button(self, wx.ID_ANY, "Add {0}".format(buttonSuffix))
		edit = wx.Button(self, wx.ID_ANY, "Edit {0}".format(buttonSuffix))
		remove = wx.Button(self, wx.ID_ANY, "Remove {0}".format(buttonSuffix))
		
		add.Bind(wx.EVT_BUTTON, self._OnAdd)
		edit.Bind(wx.EVT_BUTTON, self._OnEdit)
		remove.Bind(wx.EVT_BUTTON, self._OnRemove)
		
		buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
		buttonSizer.Add(add, 1, wx.EXPAND | wx.ALL, 2)
		buttonSizer.Add(edit, 1, wx.EXPAND | wx.ALL, 2)
		buttonSizer.Add(remove, 1, wx.EXPAND | wx.ALL, 2)
		
		outerSizer.Add(buttonSizer, 0, wx.EXPAND)
		self._Populate()
		
	def OnSigninClick(self, event, type):
		if type == "worktrade":
			if not self._controller.AuthenticateMechanic("do worktrade"):
				return
				
		elif type == "volunteer":
			if not self._controller.AuthenticateMechanic("volunteer"):
				return
			
		selection = self.nameListBox.GetSelection()
		if self.nameListBox.GetCount() == 0 or selection < 0:
			name = self.nameEntry.GetValue()
			nameWords = name.split()
			numWords = len(nameWords)
			halfWords = int(ceil(numWords / 2.0))
			firstName = " ".join(nameWords[:halfWords])
			lastName = " ".join(nameWords[halfWords:])
			
			if self._controller.ShowNewPersonDialog(firstName, lastName):
				self._controller.SignPersonIn(None, type)
				self.ResetValues()
		else:
			if self._controller.SignPersonIn(self.people[selection], type):
				self.ResetValues()
				
	def _Populate(self):
		itemPairs = self._GetItems(self._person)
		self.items = [pair[1] for pair in itemPairs]
		names = [pair[0] for pair in itemPairs]
		self.list.SetItems(names)
		
	def _OnAdd(self, event):
		self._onAddFunc(self._person)
		self._Populate()
		
	def _OnEdit(self, event):
		self._onEditFunc(self._person, self.GetSelection())
		self._Populate()
		
	def _OnRemove(self, event):
		self._onRemoveFunc(self._person, self.GetSelection())
		self._Populate()
		
	def GetSelection(self):
		selection = self.list.GetSelection()
		return self.items[selection] if selection >= 0 else None
		
class ViewPersonDialog(wx.Dialog):
	def __init__(self, controller,  person):
		wx.Dialog.__init__(self, None, title = "Viewing Info For {0} {1}".format(
			person.firstName, person.lastName), size = (720, 500))
		self._controller = controller
		
		outerSizer = wx.FlexGridSizer(2, 1)
		outerSizer.AddGrowableRow(0)
		outerSizer.AddGrowableCol(0)
		self.SetSizer(outerSizer)

		panelsSizer = wx.FlexGridSizer(1, 2)
		panelsSizer.AddGrowableCol(0)
		panelsSizer.AddGrowableRow(0)
		outerSizer.Add(panelsSizer, 1, wx.EXPAND)
		
		buttonSizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)
		outerSizer.Add(buttonSizer, 1, wx.ALIGN_RIGHT)

		listsSizer = wx.BoxSizer(wx.VERTICAL)
		infoSizer = wx.FlexGridSizer(1, 1)
		infoSizer.AddGrowableCol(0)
		
		panelsSizer.Add(infoSizer, 1, wx.EXPAND)
		panelsSizer.Add(listsSizer, 1, wx.EXPAND)
		
		posessive = person.PosessiveFirstName()
		
		shoptimes = AddEditRemoveList(self, person,
			"{0} Shop Usage".format(posessive), "Hours", _GetShoptimes,
			self._AddShoptime, self._EditShoptime, self._RemoveShoptime)
				
		bikes = AddEditRemoveList(self, person,
			"{0} Bikes".format(posessive), "Bike", _GetBikes,
			self._AddBike, self._EditBike, self._RemoveBike)
			
		listsSizer.Add(shoptimes, 2, wx.EXPAND | wx.ALL, 8)
		listsSizer.Add(bikes, 1, wx.EXPAND | wx.ALL, 8)
				
		ok = self.FindWindowById(wx.ID_OK)
		cancel = self.FindWindowById(wx.ID_CANCEL)
		
		ok.Bind(wx.EVT_BUTTON, self._OnOK)
		cancel.Bind(wx.EVT_BUTTON, self._OnCancel)
		
		def AddEditPanel(label, PanelType):
			editSizer = MakeStaticBoxSizer(self, "{0} {1}".format(posessive, label))
			panel = PanelType(self, controller)
			editSizer.Add(panel, 1, wx.EXPAND | wx.ALL, 8)
			infoSizer.Add(editSizer, 1, wx.EXPAND | wx.ALL, 8)
			return panel
		
		self._personEditPanel = AddEditPanel("Name", EditPersonPanel)
		self._personEditPanel.Set(person)
		self._memberEditPanel = AddEditPanel("Member Info", EditMemberPanel)
		if person.memberInfo:
			self._memberEditPanel.Set(person.memberInfo)
	
	def _OnOK(self, event):
		self.EndModal(wx.ID_OK)
		
	def _OnCancel(self, event):
		self.EndModal(wx.ID_CANCEL)
		
	def _AddShoptime(self, person):
		print "TODO: Add {0}'s Shoptime".format(person)
		
	def _EditShoptime(self, person, shoptime):
		print "TODO: Edit {0}'s Shoptime {1}".format(person, shoptime)
		
	def _RemoveShoptime(self, person, shoptime):
		print "TODO: Remove {0}'s Shoptime {1}".format(person, shoptime)
	
	def _AddBike(self, person):
		print "TODO: Add {0}'s Bike".format(person)
		
	def _EditBike(self, person, shoptime):
		print "TODO: Edit {0}'s Bike {1}".format(person, shoptime)
		
	def _RemoveBike(self, person, shoptime):
		print "TODO: Remove {0}'s Bike {1}".format(person, shoptime)		
