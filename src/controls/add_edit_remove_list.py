# -*- coding: utf-8 -*-

import wx
from src.ui import MakeStaticBoxSizer
		
class AddEditRemoveList(wx.Panel):
	def __init__(self, parent, label, buttonSuffix, items,
			addFunc, editFunc, removeFunc = None, strFunc = None, sortKey = None):
		wx.Panel.__init__(self, parent)
		self._items = items
		self._addFunc = addFunc
		self._editFunc = editFunc
		self._removeFunc = removeFunc if removeFunc else lambda: True
		self._sortKey = sortKey if sortKey else lambda x: x
		self._strFunc = strFunc if strFunc else str

		outerSizer = MakeStaticBoxSizer(self, label, wx.VERTICAL)
		self.SetSizer(outerSizer)
		
		self._list = wx.ListBox(self)
		outerSizer.Add(self._list, 1, wx.EXPAND | wx.ALL, 2)
	
		buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
		outerSizer.Add(buttonSizer, 0, wx.EXPAND)
		
		def AddButton(text, onClick):
			button = wx.Button(self,  label = "{0} {1}".format(text, buttonSuffix))
			button.Bind(wx.EVT_BUTTON, onClick)
			buttonSizer.Add(button, 1, wx.EXPAND | wx.ALL, 2)
			return button
	
		self._add = AddButton("Add", self._OnAdd)
		self._edit = AddButton("Edit", self._OnEdit)
		self._remove = AddButton("Remove", self._OnRemove)
		
		self._Populate()
		
		self._list.Bind(wx.EVT_LISTBOX, self._OnListClick)
		self._list.Bind(wx.EVT_LISTBOX_DCLICK, self._OnListClick)

	def _OnListClick(self, event):
		self._EnableEditRemove(self._list.GetSelection() >= 0)
				
	def _Populate(self):
		self._items.sort(key = self._sortKey)
		self._list.SetItems([self._strFunc(item) for item in self._items])
		self._EnableEditRemove(False)
		
	def _EnableEditRemove(self, enable):
		self._edit.Enable(enable)
		self._remove.Enable(enable)
		
	def _OnAdd(self, event):
		newItem = self._addFunc()
		if newItem is not None:
			self._items.append(newItem)
			self._Populate()
		
	def _OnEdit(self, event):
		if self._editFunc(self.GetSelection()):
			self._Populate()
		
	def _OnRemove(self, event):
		selection = self.GetSelection()
		if self._removeFunc(selection):
			self._items.remove(selection)
			self._Populate()
		
	def GetSelection(self):
		selection = self._list.GetSelection()
		return self._items[selection] if selection >= 0 else None
