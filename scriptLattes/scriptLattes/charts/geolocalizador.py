#!/usr/bin/python
# encoding: utf-8
# filename: geolocalizador.py
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


import urllib2    
import re

class Geolocalizador:
	endereco = None
	lat = None
	lon = None
	cidade = None
	uf = None
	cep = None
	pais = None


	def __init__(self, endereco):
		self.endereco = endereco

		aux = re.findall(r'(.*) URL.*', self.endereco)
		if len(aux)>0:
			self.endereco = aux[0]
		aux = re.findall(r'(.*) Telefone.*', self.endereco)
		if len(aux)>0:
			self.endereco = aux[0]
		self.obterCoordenadas()


	def obterCoordenadas(self):
		print "[ENDEREÇO] " + self.endereco.encode('utf8')

		self.cidade = ''
		self.uf = ''
		self.cep = ''
		self.pais = ''
		
		# - Fortaleza, CE - Brasil 
		aux = re.findall(r' - ([^-]*), (\w+) - Brasil', self.endereco)
		if len(aux)>0:
			(self.cidade,self.uf) = aux[0]

			aux = re.findall(r'(\d\d\d\d\d\d\d\d)', re.sub('\s*-\s*', '', self.endereco))
			if len(aux)>0:
				self.cep = aux[0]
		
			if self.cep=='':
				self.cep = self.obterNomeCapital(self.uf)
			if not self.uf=='':
				#uf = 'brazil ' +self.obterNomeUF(uf)
				self.uf = self.obterNomeUF(self.uf)

			self.pais = 'brasil'
		else:
			# - La Garde CEDEX, - França
			aux = re.findall(r' - ([^-]*), - (.*)', self.endereco)
			if len(aux)>0:
				(self.cidade,self.pais) = aux[0]

		print "  .Pais   = "+self.pais.encode('utf8')
		print "  .UF     = "+self.uf
		print "  .Cidade = "+self.cidade.encode('utf8')
		print "  .CEP    = "+self.cep

		self.cep = self.corrigirCEP(self.cep)

		chave = self.pais+" "+self.uf+" "+ self.cidade+" "+ self.cep
		chave = re.sub('\s+','+', chave)
		query = "http://maps.google.com/maps/geo?q="+chave.encode('utf8')+"&output=csv&sensor=false"
		print "  .Query  = "+query

		req = urllib2.Request(query)
		res = urllib2.urlopen(req).read()
		print "  .Resp.  = "+res

		vars = res.split(",")
		self.lat = vars[2]
		self.lon = vars[3]

		print "  .Verif. = http://www.gorissen.info/Pierre/maps/googleMapLocation.php?lat="+self.lat+"&lon="+self.lon+"&setLatLon=Set"
		# se acha muito útil este trecho código, então me convide um café :-)


	def obterNomeUF(self, uf):
		uf = uf.lower().strip()

		nome = ''
		if uf=='ac':
			nome = 'acre'
		if uf=='al':
			nome = 'alagoas'
		if uf=='ap':
			nome = 'amapa'
		if uf=='am':
			nome = 'amazonas'
		if uf=='ba':
			nome = 'bahia'
		if uf=='ce':
			nome = 'ceara'
		if uf=='df':
			nome = 'brasilia'
		if uf=='es':
			nome = 'espirito santo'
		if uf=='go':
			nome = 'goias'
		if uf=='ma':
			nome = 'maranhao'
		if uf=='mt':
			nome = 'mato grosso'
		if uf=='ms':
			nome = 'mato grosso do sul'
		if uf=='mg':
			nome = 'minas gerais'
		if uf=='pa':
			nome = 'para'
		if uf=='pb':
			nome = 'paraiba'
		if uf=='pr':
			nome = 'parana'
		if uf=='pe':
			nome = 'pernambuco'
		if uf=='pi':
			nome = 'piaui'
		if uf=='rj':
			nome = 'rio de janeiro'
		if uf=='rn':
			nome = 'rio grande do norte'
		if uf=='rs':
			nome = 'rio grande do sul'
		if uf=='ro':
			nome = 'rondonia'
		if uf=='rr':
			nome = 'roraima'
		if uf=='sc':
			nome = 'santa catarina'
		if uf=='sp':
			nome = 'sao paulo'
		if uf=='se':
			nome = 'sergipe'
		if uf=='to':
			nome = 'tocantins'

		return nome


	def obterNomeCapital (self, uf):
		uf = uf.lower().strip()

		nome = ''
		if uf=='ac':
			nome = 'rio branco'
		if uf=='al':
			nome = 'maceio'
		if uf=='ap':
			nome = 'macapa'
		if uf=='am':
			nome = 'manaus'
		if uf=='ba':
			nome = 'salvador'
		if uf=='ce':
			nome = 'fortaleza'
		if uf=='df':
			nome = 'brasilia'
		if uf=='es':
			nome = 'vitoria'
		if uf=='go':
			nome = 'goiania'
		if uf=='ma':
			nome = 'sao luis'
		if uf=='mt':
			nome = 'cuiaba'
		if uf=='ms':
			nome = 'campo grande'
		if uf=='mg':
			nome = 'belo horizonte'
		if uf=='pa':
			nome = 'belem'
		if uf=='pb':
			nome = 'joao pessoa'
		if uf=='pr':
			nome = 'curitiba'
		if uf=='pe':
			nome = 'recibe'
		if uf=='pi':
			nome = 'teresina'
		if uf=='rj':
			nome = 'rio de janeiro'
		if uf=='rn':
			nome = 'natal'
		if uf=='rs':
			nome = 'porto alegre'
		if uf=='ro':
			nome = 'porto velho'
		if uf=='rr':
			nome = 'boa vista'
		if uf=='sc':
			nome = 'florianopolis'
		if uf=='sp':
			nome = 'sao paulo'
		if uf=='se':
			nome = 'aracaju'
		if uf=='to':
			nome = 'palmas'

		return nome

	# Este procedimento permite trocar um CEP por outro, a fim de
	# refinar a localização geográfica usando o Google Maps.
	#
	# Em casos específicos a agência de Correios define CEPs especiais 
	# que o Google Map não os interpreta corretamente:
	# http://www.correios.com.br/servicos/cep/default.cfm

	def corrigirCEP(self, cep):
		if cep=='05508900':
			return '05508090'  # IME-USP
		if cep=='01246904':
			return '01246000'  # Av. Dr. Arnaldo 715
		if cep=='01246906':
			return '01246000'  # Av. Dr. Arnaldo 715
		if cep=='70770901':
			return '70770200'  # Brasília

		return cep
