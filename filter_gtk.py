 # -*- coding: utf-8 -*-
 
import sys

eatNewline = False
while True:
	line = sys.stdin.readline()

	if not line:
		break
		
	if eatNewline and line == '\n':
		continue	
		
	if line.find("Gtk-WARNING **:") < 0:
		print line,
	else:
		eatNewline = True
