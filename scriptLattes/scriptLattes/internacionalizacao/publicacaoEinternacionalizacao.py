#!/usr/bin/python
# encoding: utf-8
# filename: publicacaoEinternacionalizacao.py
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


from scriptLattes import *
from geradorDePaginasWeb import *

class PublicacaoEinternacionalizacao:
	publicacao = None
	ano = None
	chave = None
	listaDePaises = None

	def __init__(self, publicacao):
		self.publicacao = publicacao
		self.ano   = publicacao.ano
		self.chave = publicacao.titulo # chave de comparação entre os objetos
		self.listaDePaises = []

	def atribuirListaDeIndicesDePaises(self, listaDePaisesIdentificados):
		self.listaDePaises = listaDePaisesIdentificados
		

	def html(self):
		s = ' <a href="'+self.publicacao.doi+'" target="_blank" style="PADDING-RIGHT:4px;"><img border=0 src="doi.png"></a>'
		s+= self.publicacao.titulo + '. <br>' 

		if self.listaDePaises is not None: 
			if len(self.listaDePaises)>0:
				s+= '<b>'
				for index in range(0, len(self.listaDePaises)):
					s+= self.listaDePaises[index].title() + ", " 
				s = s.rstrip(", ")
				s+= '.</b>'
			else:
				s+= '<i>[Pa&iacute;s n&atilde;o identificado]</i>'
		else:
				s+= '<i><font color=red>[N&atilde;o foi poss&iacute;vel obter dados do DOI]</font></i>'

		return s

