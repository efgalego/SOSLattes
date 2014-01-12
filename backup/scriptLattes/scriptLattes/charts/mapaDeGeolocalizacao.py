#!/usr/bin/python
# encoding: utf-8
# filename: mapaDeGeolocalizacao.py
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


from membro import *

class MapaDeGeolocalizacao:
	mapa = None

	def __init__(self, grupo):
		self.grupo = grupo

		print "\n[CRIANDO MAPA DE GEOLOCALIZAÇÃO] (Esta operação pode demorar)"
		self.gerarMapa()


	def gerarMapa(self):
		self.mapa = '<script type="text/javascript" src="https://maps.google.com/maps/api/js?sensor=false"></script> \n'
		self.mapa+= '<script type="text/javascript"> \n\
  function setMarker0(map, latx, lngx, name, address, cvlattes, photo) { \n\
    var image = new google.maps.MarkerImage("lattesPoint0.png"); \n\
    var contentString = "<table> <tr bgcolor=#006400><td><font color=#ffffff>"+name+"</font></td></tr> <tr><td> <table><tr><td valign=top> <img src="+photo+" width=90px> </td><td> <font size=-2>"+address+"<br><p><a href="+cvlattes+" target=_blank>"+cvlattes+"</a></font></td></tr> </table>  </td></tr> </table> "; \n\
    var infowindow = new google.maps.InfoWindow({ content: contentString, maxWidth: 400, maxHeight: 400 }); \n\
    var myLatLng = new google.maps.LatLng(latx, lngx); \n\
    var marker = new google.maps.Marker({ position: myLatLng, map: map, icon: image }); \n\
    google.maps.event.addListener(marker, "click", function() { infowindow.open(map, marker); }); \n\
 } \n\
 function setMarker1(map, latx, lngx, name, address, advisors, cvlattes, photo) { \n\
   var image = new google.maps.MarkerImage("lattesPoint1.png"); \n\
   var contentString = " <table> <tr bgcolor=#990808><td><font color=#ffffff>"+name+"</font></td></tr> <tr><td> <table><tr><td valign=top> <img src="+photo+" width=100px> </td><td> <font size=-2>"+address+"<br><b>"+advisors+"</b> <br><p><a href="+cvlattes+" target=_blank>"+cvlattes+"</a></font></td></tr> </table>  </td></tr> </table>"; \n\
   var infowindow = new google.maps.InfoWindow({ content: contentString, maxWidth: 400, maxHeight: 400 }); \n\
   var myLatLng = new google.maps.LatLng(latx, lngx); \n\
   var marker = new google.maps.Marker({ position: myLatLng, map: map, icon: image }); \n\
   google.maps.event.addListener(marker, "click", function() { infowindow.open(map, marker); }); \n\
 } \n\
 function setMarker2(map, latx, lngx, name, address, advisors, cvlattes, photo) { \n\
   var image = new google.maps.MarkerImage("lattesPoint2.png"); \n\
   var contentString =" <table> <tr bgcolor=#333399><td><font color=#ffffff>"+name+"</font></td></tr> <tr><td> <table><tr><td valign=top> <img src="+photo+" width=100px> </td><td> <font size=-2>"+address+"<br><b>"+advisors+"</b> <br><p><a href="+cvlattes+" target=_blank>"+cvlattes+"</a></font></td></tr> </table>  </td></tr> </table>"; \n\
   var infowindow = new google.maps.InfoWindow({ content: contentString, maxWidth: 400, maxHeight: 400 }); \n\
   var myLatLng = new google.maps.LatLng(latx, lngx); \n\
   var marker = new google.maps.Marker({ position: myLatLng, map: map, icon: image }); \n\
   google.maps.event.addListener(marker, "click", function() { infowindow.open(map, marker); }); \n\
 } \n\
 function setMarker3(map, latx, lngx, name, address, advisors, cvlattes, photo) { \n\
   var image = new google.maps.MarkerImage("lattesPoint3.png"); \n\
   var contentString = " <table> <tr bgcolor=#eced0c><td><font color=#000000>"+name+"</font></td></tr> <tr><td> <table><tr><td valign=top> <img src="+photo+" width=100px> </td><td> <font size=-2>"+address+"<br><b>"+advisors+"</b> <br><p><a href="+cvlattes+" target=_blank>"+cvlattes+"</a></font></td></tr> </table>  </td></tr> </table>"; \n\
   var infowindow = new google.maps.InfoWindow({ content: contentString, maxWidth: 400, maxHeight: 400 }); \n\
   var myLatLng = new google.maps.LatLng(latx, lngx); \n\
   var marker = new google.maps.Marker({ position: myLatLng, map: map, icon: image }); \n\
   google.maps.event.addListener(marker, "click", function() { infowindow.open(map, marker); }); \n\
 } \n\
 function initialize() {  \n\
   var latlng = new google.maps.LatLng(0,0);  \n\
   var options = { zoom: 2, center: latlng, mapTypeId: google.maps.MapTypeId.ROADMAP }; \n\
   var map = new google.maps.Map(document.getElementById("map_canvas"), options); \n\
 \n'
      
         	cvsProcessados = set([])
      
      
         	if self.grupo.obterParametro('mapa-incluir_membros_do_grupo'):
         		for membro in self.grupo.listaDeMembros:
         			cvsProcessados.add(membro.idLattes)
      
         			membro.obterCoordenadasDeGeolocalizacao()
         			if not membro.enderecoProfissionalLat=='0' and not membro.enderecoProfissionalLon=='0':
         				self.mapa += '\n    setMarker0(map, '+membro.enderecoProfissionalLat+'+0.001*Math.random(), '+membro.enderecoProfissionalLon+'+0.001*Math.random(), "'+membro.nomeCompleto+'", "'+membro.enderecoProfissional+'", "'+membro.url+'", "'+membro.foto+'");'


		if self.grupo.obterParametro('mapa-incluir_alunos_de_pos_doutorado'):
			keys =self.grupo.compilador.listaCompletaOCSupervisaoDePosDoutorado.keys()
			for ano in keys:		
				for aluno in self.grupo.compilador.listaCompletaOCSupervisaoDePosDoutorado[ano]:
					idOrientando = aluno.idOrientando

					if len(idOrientando)==16 and cvsProcessados.isdisjoint([idOrientando]):
						print "\n-Processando o CV do ex-posdoc: "+idOrientando+" "+membro.nomeCompleto.encode('utf8')
						membro = Membro('', idOrientando, '', '', '', '', '', self.grupo.diretorioCache)
						membro.carregarDadosCVLattes()
						membro.obterCoordenadasDeGeolocalizacao()
						if not membro.enderecoProfissionalLat=='0' and not membro.enderecoProfissionalLon=='0':
							self.mapa += '\n    setMarker1(map, '+membro.enderecoProfissionalLat+'+0.001*Math.random(), '+membro.enderecoProfissionalLon+'+0.001*Math.random(), "'+membro.nomeCompleto+'","'+membro.enderecoProfissional+'","'+self.obterNomesDosOrientadores(aluno, self.grupo.listaDeMembros)+'","'+membro.url+'","'+membro.foto+'");'
						cvsProcessados.add(idOrientando)


		if self.grupo.obterParametro('mapa-incluir_alunos_de_doutorado'):
			keys =self.grupo.compilador.listaCompletaOCTeseDeDoutorado.keys()
			for ano in keys:		
				for aluno in self.grupo.compilador.listaCompletaOCTeseDeDoutorado[ano]:
					idOrientando = aluno.idOrientando

					if len(idOrientando)==16 and cvsProcessados.isdisjoint([idOrientando]):
						print "\n-Processando o CV do ex-aluno de doutorado: "+idOrientando+" "+membro.nomeCompleto.encode('utf8')
						membro = Membro('', idOrientando, '', '', '', '', '', self.grupo.diretorioCache)
						membro.carregarDadosCVLattes()
						membro.obterCoordenadasDeGeolocalizacao()
						if not membro.enderecoProfissionalLat=='0' and not membro.enderecoProfissionalLon=='0':
							self.mapa += '\n    setMarker2(map, '+membro.enderecoProfissionalLat+'+0.001*Math.random(), '+membro.enderecoProfissionalLon+'+0.001*Math.random(), "'+membro.nomeCompleto+'","'+membro.enderecoProfissional+'","'+self.obterNomesDosOrientadores(aluno, self.grupo.listaDeMembros)+'","'+membro.url+'","'+membro.foto+'");'
						cvsProcessados.add(idOrientando)


		if self.grupo.obterParametro('mapa-incluir_alunos_de_mestrado'):
			keys =self.grupo.compilador.listaCompletaOCDissertacaoDeMestrado.keys()
			for ano in keys:		
				for aluno in self.grupo.compilador.listaCompletaOCDissertacaoDeMestrado[ano]:
					idOrientando = aluno.idOrientando

					if len(idOrientando)==16 and cvsProcessados.isdisjoint([idOrientando]):
						print "\n-Processando o CV do ex-aluno de mestrado: "+idOrientando+" "+membro.nomeCompleto.encode('utf8')
						membro = Membro('', idOrientando, '', '', '', '', '', self.grupo.diretorioCache)
						membro.carregarDadosCVLattes()
						membro.obterCoordenadasDeGeolocalizacao()
						if not membro.enderecoProfissionalLat=='0' and not membro.enderecoProfissionalLon=='0':
							self.mapa += '\n    setMarker3(map, '+membro.enderecoProfissionalLat+'+0.001*Math.random(), '+membro.enderecoProfissionalLon+'+0.001*Math.random(), "'+membro.nomeCompleto+'","'+membro.enderecoProfissional+'","'+self.obterNomesDosOrientadores(aluno, self.grupo.listaDeMembros)+'","'+membro.url+'","'+membro.foto+'");'
						cvsProcessados.add(idOrientando)


		self.mapa+= '\
  } \n\
</script>\n'


		#print "--------------------------------------------------------------------"
		#print self.mapa.encode('utf8','replace')
		#print "--------------------------------------------------------------------"
		print "\n[MAPA DE GEOLOCALIZACAO CRIADO]"


	def obterNomesDosOrientadores(self, aluno, listaDeMembros):
		lista = list(aluno.idMembro)
		if len(lista)==1:
			m = listaDeMembros[lista[0]]
			s = aluno.tipoDeOrientacao+': '+m.nomeCompleto
		else:
			s = 'Orientadores: ' 
			for i in lista:
				m = listaDeMembros[i]
				s+= m.nomeCompleto+', '
			s= s.rstrip(', ')+'.'

		return s

