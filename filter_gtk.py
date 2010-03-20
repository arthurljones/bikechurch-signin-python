 # -*- coding: utf-8 -*-
 
import sys

while True:
	line = sys.stdin.readline()
	
	if not line:
		break
	elif "Gtk-WARNING **:" in line:
		sys.stdin.readline()
	else:
		print line,
