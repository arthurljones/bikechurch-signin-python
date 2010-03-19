import wx
from copy import copy

sWhitespace = ' \t\n'

def SplitAndKeep(string, splitchars = " \t\n"):
	substrs = []
	
	i = 0
	while len(string) > 0:
		if string[i] in splitchars:
			substrs.append(string[:i])
			substrs.append(string[i])
			string = string[i+1:]
			i = 0
		else:
			i += 1
			if i >= len(string):	
				substrs.append(string)
				break
		
	return substrs

class AutowrappedStaticText(wx.StaticText):
	"""A StaticText-like widget which implements word wrapping."""
	def __init__(self, *args, **kwargs):
		wx.StaticText.__init__(self, *args, **kwargs)
		self.label = super(AutowrappedStaticText, self).GetLabel()
		self.pieces = SplitAndKeep(self.label, sWhitespace)
		self.Bind(wx.EVT_SIZE, self.OnSize)
		self.lastWrap = None
		self.Wrap()

	def SetLabel(self, newLabel):
		"""Store the new label and recalculate the wrapped version."""
		self.label = newLabel
		self.pieces = SplitAndKeep(self.label, sWhitespace)
		self.Wrap()

	def GetLabel(self):
		"""Returns the label (unwrapped)."""
		return self.label
	
	def Wrap(self):		
		"""Wraps the words in label."""
		maxWidth = self.GetParent().GetVirtualSizeTuple()[0] - 10

		#TODO: Fix this so that we're not wasting cycles, but so that it actually works
		#if self.lastWrap and self.lastWrap == maxWidth:
		#	return
			
		self.lastWrap = maxWidth	

		pieces = copy(self.pieces)
		lines = []
		currentLine = []
		currentString = ""

		while len(pieces) > 0:			
			nextPiece = pieces.pop(0)
			newString = currentString + nextPiece
			newWidth = self.GetTextExtent(newString)[0]
			currentPieceCount = len(currentLine)
			
			if (currentPieceCount > 0 and newWidth > maxWidth) or nextPiece == '\n':
				if currentPieceCount > 0 and currentLine[-1] in sWhitespace:
					currentLine = currentLine[:-1]
				if nextPiece in sWhitespace:
					pieces = pieces[1:]
						
				currentLine.append('\n')
				
				lines.extend(currentLine)
				currentLine = [nextPiece]
				currentString = nextPiece
			else:
				currentString += nextPiece
				currentLine.append(nextPiece)

		lines.extend(currentLine)
		line = "".join(lines)
		super(AutowrappedStaticText, self).SetLabel(line)
		self.Refresh()

	def OnSize(self, event):
		self.Wrap()
