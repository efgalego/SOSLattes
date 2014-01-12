#!/usr/bin/python
# encoding: utf-8
# filename: graficoDeBarras.py
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
import matplotlib
matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt
import operator
import math
	
class GraficoDeInternacionalizacao:
	listaCompleta = None
	vetorDePaises = None
	vetorDeQuantidades = None

	publicacoesComParceriasNaoIdentificadas = 0
	publicacoesRealizadasSemParceirasComEstrangeiros = 0
	publicacoesRealizadasComParceirasComEstrangeiros = 0


	def __init__(self, listaCompleta):
		self.listaCompleta = []
		self.listaCompleta = listaCompleta

		listaDePaisesEquantidades = {}
		keys = self.listaCompleta.keys()
		for ano in keys:
			elementos = self.listaCompleta[ano]
			for index in range(0, len(elementos)):
				publicacaoEinternacionalizacao = elementos[index]

				# publicações sem identificação de paises
				if publicacaoEinternacionalizacao.listaDePaises is not None:
					if (len(publicacaoEinternacionalizacao.listaDePaises)==0):
						self.publicacoesComParceriasNaoIdentificadas += 1
					else:
						soBrasil = True

						for pais in publicacaoEinternacionalizacao.listaDePaises:
							if (not pais=='Brazil'):
								soBrasil = False
							if listaDePaisesEquantidades.get(pais)==None:
								listaDePaisesEquantidades[pais] = 0
							listaDePaisesEquantidades[pais]+=1
	
						if (soBrasil):
							self.publicacoesRealizadasSemParceirasComEstrangeiros += 1
						else:
							self.publicacoesRealizadasComParceirasComEstrangeiros += 1

		listaDePaisesEquantidadesOrd = sorted(listaDePaisesEquantidades.items(), key=operator.itemgetter(1,0), reverse=True)

		self.vetorDePaises = []
		self.vetorDeQuantidades = []
		for item in listaDePaisesEquantidadesOrd:
			if not item[0]=="Brazil": # a principio todos foram elaborados com participação brasileira
				self.vetorDePaises.append(item[0].title())
				self.vetorDeQuantidades.append(item[1])

	def numeroDePublicacoesRealizadasSemParceirasComEstrangeiros(self):
		return self.publicacoesRealizadasSemParceirasComEstrangeiros

	def numeroDePublicacoesRealizadasComParceirasComEstrangeiros(self):
		return self.publicacoesRealizadasComParceirasComEstrangeiros

	def numeroDePublicacoesComParceriasNaoIdentificadas(self):
		return self.publicacoesComParceriasNaoIdentificadas


	def criarGraficoDeBarrasDeOcorrencias(self):
		script = ""

		if len(self.vetorDePaises)>0: # Apenas para listas com elemtos
			print "\n[CRIANDO GRAFICO DE BARRAS - INTERNACIONALIZACAO]"
			print self.vetorDePaises
			print self.vetorDeQuantidades

			script = "<script type='text/javascript' src='https://www.google.com/jsapi'></script>"

			# ---------------------------------------------------------------- #
			# Geomap
			script+=" \
            <script type='text/javascript'>\
            google.load('visualization', '1', {'packages': ['geochart']});\
            google.setOnLoadCallback(drawRegionsMap);\
            function drawRegionsMap() {\
              var data = new google.visualization.DataTable();\
              data.addColumn('string', 'Pais');\
              data.addColumn('number', 'Ocorrencias');\
              data.addRows(["

			for index in range(0,len(self.vetorDePaises)):
				script+= "\n['" + self.vetorDePaises[index] + "', " + str(self.vetorDeQuantidades[index]) + "], "

			script+= "\
              ]);\
              var options = {width: 500, height: 300};\
              var chart = new google.visualization.GeoChart(document.getElementById('geochart_div'));\
              chart.draw(data, options);\
            };\
            </script>"


			# ---------------------------------------------------------------- #
			# Barchart
			height = str(int((math.floor(len(self.vetorDePaises)/2)+1)*40))

			script+= " \
            <script type='text/javascript'>\
            google.load('visualization', '1', {packages:['corechart']});\
            google.setOnLoadCallback(drawChart);\
            function drawChart() {\
              var data = new google.visualization.DataTable();\
              data.addColumn('string', 'Pais');\
              data.addColumn('number', 'Ocorrencias');\
              data.addRows(["

			for index in range(0,len(self.vetorDePaises)):
				script+= "\n['" + self.vetorDePaises[index] + "', " + str(self.vetorDeQuantidades[index]) + "], "

			script+= " \
              ]);\
              var options = {\
                width: 500, height: "+str(height)+",\
                vAxis: {title: 'Pais',  titleTextStyle: {color: 'black'}},\
                legend: 'none',\
                chd: 's:underp',\
                chm: 'N,00CC00,0,-1,11',\
                chds:'0,1'\
              };\
              var chart = new google.visualization.BarChart(document.getElementById('barchart_div'));\
              chart.draw(data, options);\
            }\
            </script>"

		return script
			
