#!/usr/bin/python
# caso 3 http://pubs.acs.org procura toda data entre affiliations e citation
import re
import urllib, urllib2
import  unicodedata
from HTMLParserNew import HTMLParser
class parser101021(HTMLParser):
    	def __init__(self):
	    HTMLParser.__init__(self)
	    self.recording = 0 
	    self.data = []
	    self.count =0
	def handle_starttag(self, tag, attrs):		
		if tag=='div':
			for attr in attrs:
				if 'class' == attr[0] and attr[1]=='affiliations':
		  	      		self.recording = 1
		  	      		self.count = 0
				if 'id' == attr[0] and attr[1]=='citation':
					if self.recording == 1:
		      				self.recording -=1
	def handle_data(self, data):
	    if self.recording:			
			data = ''.join((c for c in unicodedata.normalize('NFD',unicode(data.decode("utf-8"))) if unicodedata.category(c) != 'Mn'))
			self.data.append(data)
