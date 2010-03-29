 # -*- coding: utf-8 -*-
 
import wx, datetime
from ..ui_utils import AddLabel, MedFont, FormatTimediff, GetShoptimeTypeDescription
from ..controls.edit_name_panel import EditNamePanel
from ..controls.autowrapped_static_text import AutowrappedStaticText

def _GetShoptimes(person):
	result = []
	for time in person.shoptimes:
		startTime = time.start.strftime("%a %b %d %Y %I:%m%p")
		duration =  time.duration.strftime("%H:%M")
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
	'''TODO:
	OnSelect enables buttons
	'''
	
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
		
		outerSizer = wx.FlexGridSizer(3, 1)
		outerSizer.AddGrowableCol(0)
		outerSizer.AddGrowableRow(1)
		self.SetSizer(outerSizer)
		
		AddLabel(self, outerSizer, MedFont(), label)
		self.list = wx.ListBox(self)
		outerSizer.Add(self.list, 1, wx.EXPAND)
	
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
			person.firstName, person.lastName))
		self._controller = controller
		
		outerSizer = wx.FlexGridSizer(2, 1)
		outerSizer.AddGrowableRow(0)
		outerSizer.AddGrowableCol(0)
		self.SetSizer(outerSizer)

		panelsSizer = wx.FlexGridSizer(1, 2)
		panelsSizer.AddGrowableCol(1)
		panelsSizer.AddGrowableRow(0)
		outerSizer.Add(panelsSizer)

		listsSizer = wx.BoxSizer(wx.VERTICAL)
		panelsSizer.Add(listsSizer, 1, wx.EXPAND)

		posessive = person.PosessiveFirstName()
		shoptimes = AddEditRemoveList(self, person,
			"{0} shop usage:".format(posessive), "Hours", _GetShoptimes,
			self._AddShoptime, self._EditShoptime, self._RemoveShoptime)
				
		bikes = AddEditRemoveList(self, person,
			"{0} bikes:".format(posessive), "Bike", _GetBikes,
			self._AddBike, self._EditBike, self._RemoveBike)
			
		listsSizer.Add(shoptimes, 2, wx.EXPAND)
		listsSizer.Add(bikes, 1, wx.EXPAND)
				
		buttonSizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)
		outerSizer.Add(buttonSizer, 1, wx.ALIGN_RIGHT)
		
		ok = self.FindWindowById(wx.ID_OK)
		cancel = self.FindWindowById(wx.ID_CANCEL)
		
		ok.Bind(wx.EVT_BUTTON, self._OnOK)
		cancel.Bind(wx.EVT_BUTTON, self._OnCancel)
		
		infoSizer = wx.BoxSizer(wx.VERTICAL)
		panelsSizer.Add(infoSizer, 1, wx.EXPAND)
		self._nameEdit = EditNamePanel(self, controller)
		infoSizer.Add(self._nameEdit, 0, wx.EXPAND)
		
		self.Layout()
		self.Fit()
	
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
