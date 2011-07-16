#!/usr/bin/python
# -*- coding: utf-8 -*-

from subprocess import Popen
import os

output = open("output.txt", "ab")
error = open("errors.txt", "ab")
#"-u", "{0}/main.py".format(os.getcwd())
Popen(["/usr/bin/python", "-u", "{0}/__main__.py".format(os.getcwd())], stdout = output, stderr = error)