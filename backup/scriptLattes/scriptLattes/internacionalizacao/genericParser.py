#!/usr/bin/python
import re
import urllib, urllib2
import  unicodedata
from HTMLParserNew import HTMLParser
class genericParser(HTMLParser):
    	def __init__(self,parserField):
	    HTMLParser.__init__(self)
	    self.recording = 0 
	    self.data = []
	    self.field = parserField

	def handle_starttag(self, tag, attrs):

	    if tag==self.field[1]:
		   for attr in attrs:
		        if self.field[2] == attr[0] and attr[1]==self.field[3]:
		  	      self.recording = 1
	def handle_endtag(self, tag):
	    if tag == self.field[1]:
		if self.recording == 1:
	      		self.recording -=1
	def handle_data(self, data):
	    if self.recording:			
			data = ''.join((c for c in unicodedata.normalize('NFD',unicode(data.decode("utf-8"))) if unicodedata.category(c) != 'Mn'))
			self.data.append(data)
	

	
