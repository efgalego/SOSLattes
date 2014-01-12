#!/usr/bin/python
# encoding: utf-8
# filename: depuradorDOIhtml.py
#
#  scriptLattes V8
#  Copyright 2005-2012: Jesús P. Mena-Chalco e Roberto M. Cesar-Jr.
#  http://scriptlattes.sourceforge.net/
#
#
#  Este programa é um software livre; você pode redistribui-lo e/ou 
#  modifica-lo dentro dos termos da Licença Pública Geral GNU como 
#  publicada pela Fundação do Software Livre (FSF); na versão 2 da 
#  Licença, ou (na sua opinião) qualquer versão.
#
#  Este programa é distribuído na esperança que possa ser util, 
#  mas SEM NENHUMA GARANTIA; sem uma garantia implicita de ADEQUAÇÂO a qualquer
#  MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a
#  Licença Pública Geral GNU para maiores detalhes.
#
#  Você deve ter recebido uma cópia da Licença Pública Geral GNU
#  junto com este programa, se não, escreva para a Fundação do Software
#  Livre(FSF) Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#


import HTMLParser
import re

from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint


class DepuradorDOIhtml(HTMLParser):
	dadosDaPublicacao = None

	def __init__(self, rawDOIhtml):
		HTMLParser.__init__(self)
		self.dadosDaPublicacao = ""
		self.feed(rawDOIhtml)

	def handle_data(self, dado):
		texto = dado.strip()
		if len(texto) > 0:
			texto = re.sub('[ \t\r\n]+', ' ', texto)
			self.dadosDaPublicacao += texto + ' '

	def handle_starttag(self, tag, attributes):
		if tag == 'p':
			self.dadosDaPublicacao += '\n'
		if tag == 'br':
			self.dadosDaPublicacao += '\n'
		if tag == 'li':
			self.dadosDaPublicacao += '\n'
		if tag == 'div':
			self.dadosDaPublicacao += '\n'

	def handle_startendtag(self, tag, attrs):
		if tag == 'br':
			self.dadosDaPublicacao += '\n'


	def obterDadosDaPublicacao(self):
		return self.dadosDaPublicacao.strip()

# ---------------------------------------------------------------------------- #
def stripBlanks(s):
	return re.sub('\s+', ' ', s).strip()

def htmlentitydecode(s):
	return re.sub('&(%s);' % '|'.join(name2codepoint), 
		lambda m: unichr(name2codepoint[m.group(1)]), s)

