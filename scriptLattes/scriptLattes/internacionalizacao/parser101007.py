#!/usr/bin/python
# caso 4 http://www.springerlink.com/ procura tag a e o title Permissions & Reprints
import urllib, urllib2
from HTMLParserNew import HTMLParser
class parser101007(HTMLParser):
    	def __init__(self):
	    HTMLParser.__init__(self)
	    self.recording = 0 
	    self.data = []
	def handle_starttag(self, tag, attrs):
	    if tag=='a':
		   for attr in attrs:
		        if 'title' == attr[0] and attr[1]=='Permissions & Reprints':
				self.data.append(attrs)
