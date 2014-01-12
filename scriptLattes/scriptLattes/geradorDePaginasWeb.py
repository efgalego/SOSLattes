#!/usr/bin/python
# encoding: utf-8
# filename: geradorDePaginasWeb
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


import datetime
import re
import math
from graficoDeInternacionalizacao import *


class GeradorDePaginasWeb:
	grupo = None
	dir = None
	version = None
	extensaoPagina = None
	arquivoRis = None

	def __init__(self, grupo):
		self.grupo = grupo
		self.version = 'V8.05'
		self.dir = self.grupo.obterParametro('global-diretorio_de_saida')
		
		if self.grupo.obterParametro('global-criar_paginas_jsp'):
			self.extensaoPagina = '.jsp'
			self.html1 = '<%@ page language="java" contentType="text/html; charset=ISO8859-1" pageEncoding="ISO8859-1"%> <%@ taglib prefix="f" uri="http://java.sun.com/jsf/core"%> <f:verbatim>'
			self.html2 = '</f:verbatim>'
		else:
			self.extensaoPagina = '.html'
			self.html1 = '<html>'
			self.html2 = '</html>'


		if self.grupo.obterParametro('relatorio-salvar_publicacoes_em_formato_ris'): 
			prefix = self.grupo.obterParametro('global-prefixo')+'-' if not self.grupo.obterParametro('global-prefixo')=='' else ''
			self.arquivoRis = open(self.dir+"/"+prefix+"publicacoes.ris", 'w')

		self.gerarPaginaDeMembros()

		self.gerarPaginasDeProducoesBibliograficas()
		self.gerarPaginasDeProducoesTecnicas()
		self.gerarPaginasDeProducoesArtisticas()

		if self.grupo.obterParametro('relatorio-mostrar_orientacoes'):
			self.gerarPaginasDeOrientacoes()

		if self.grupo.obterParametro('relatorio-incluir_projeto'):
			self.gerarPaginasDeProjetos()

		if self.grupo.obterParametro('relatorio-incluir_premio'):
			self.gerarPaginasDePremios()

		if self.grupo.obterParametro('relatorio-incluir_participacao_em_evento'):
			self.gerarPaginasDeParticipacaoEmEventos()
		
		if self.grupo.obterParametro('relatorio-incluir_organizacao_de_evento'):
			self.gerarPaginasDeOrganizacaoDeEventos()
		
		if self.grupo.obterParametro('grafo-mostrar_grafo_de_colaboracoes'):
			self.gerarPaginaDeGrafosDeColaboracoes()

		if self.grupo.obterParametro('relatorio-incluir-internacionalizacao'):
			self.gerarPaginasDeInternacionalizacao()
		
		# final do fim! 
		self.gerarPaginaPrincipal()
		
		if self.grupo.obterParametro('relatorio-salvar_publicacoes_em_formato_ris'): 
			self.arquivoRis.close()


	def gerarPaginaPrincipal(self):
		nomeGrupo = self.grupo.obterParametro('global-nome_do_grupo').decode("utf8")

		s = self.html1+' \
        <head> \
           <title>'+nomeGrupo+'</title> \
           <meta name="Generator" content="scriptLattes"> \
           <link rel="stylesheet" href="scriptLattes.css" type="text/css">  \
           <meta http-equiv="Content-Type" content="text/html; charset=utf-8">'
		if self.grupo.obterParametro('mapa-mostrar_mapa_de_geolocalizacao'):
			s+= self.grupo.mapaDeGeolocalizacao.mapa #.encode("utf8")

		s+= '</head> \n \
        <body onload="initialize()" onunload="GUnload()"> <div id="header">  \
        <center> <h2> '+nomeGrupo+'</h2>'

		s+='[ <a href=membros'+self.extensaoPagina+'>Membros</a> \
            | <a href=#producaoBibliografica>Produção bibliográfica</a> \
            | <a href=#producaoTecnica>Produção técnica</a> \
            | <a href=#producaoArtistica>Produção artística</a> '.decode("utf8")

		if self.grupo.obterParametro('relatorio-mostrar_orientacoes'):
			s+='| <a href=#orientacoes>Orientações</a> '.decode("utf8")

		if self.grupo.obterParametro('relatorio-incluir_projeto'):
			s+='| <a href=#projetos>Projetos</a> '.decode("utf8")

		if self.grupo.obterParametro('relatorio-incluir_premio'):
			s+='| <a href=#premios>Prêmios</a> '.decode("utf8")

		if self.grupo.obterParametro('relatorio-incluir_participacao_em_evento') or self.grupo.obterParametro('relatorio-incluir_organizacao_de_evento'):
			s+='| <a href=#eventos>Eventos</a> '.decode("utf8")

		if self.grupo.obterParametro('grafo-mostrar_grafo_de_colaboracoes'):
			s+='| <a href=#grafo>Grafo de colaborações</a> '.decode("utf8")

		if self.grupo.obterParametro('mapa-mostrar_mapa_de_geolocalizacao'):
			s+='| <a href=#mapa>Mapa de geolocalização</a> '.decode("utf8")

		if self.grupo.obterParametro('relatorio-incluir-internacionalizacao'):
			s+='| <a href=#internacionalizacao>Internacionalização</a> '.decode("utf8")

		s+=' ] </center><br></div>'
		s+='<h3 id="producaoBibliografica">Produção bibliográfica</h3> <ul>'.decode("utf8")

		if self.nPB0>0:
			s+= '<li> <a href="PB0-0'+self.extensaoPagina+'">Artigos completos publicados em periódicos</a> '.decode("utf8")+'('+str(self.nPB0)+')'
		if self.nPB1>0:
			s+= '<li> <a href="PB1-0'+self.extensaoPagina+'">Livros publicados/organizados ou edições</a> '.decode("utf8")+'('+str(self.nPB1)+')'
		if self.nPB2>0:
			s+= '<li> <a href="PB2-0'+self.extensaoPagina+'">Capítulos de livros publicados </a> '.decode("utf8")+'('+str(self.nPB2)+')'
		if self.nPB3>0:
			s+= '<li> <a href="PB3-0'+self.extensaoPagina+'">Textos em jornais de notícias/revistas </a> '.decode("utf8")+'('+str(self.nPB3)+')'
		if self.nPB4>0:
			s+= '<li> <a href="PB4-0'+self.extensaoPagina+'">Trabalhos completos publicados em anais de congressos </a> '.decode("utf8")+'('+str(self.nPB4)+')'
		if self.nPB5>0:
			s+= '<li> <a href="PB5-0'+self.extensaoPagina+'">Resumos expandidos publicados em anais de congressos </a> '.decode("utf8")+'('+str(self.nPB5)+')'
		if self.nPB6>0:
			s+= '<li> <a href="PB6-0'+self.extensaoPagina+'">Resumos publicados em anais de congressos </a> '.decode("utf8")+'('+str(self.nPB6)+')'
		if self.nPB7>0:
			s+= '<li> <a href="PB7-0'+self.extensaoPagina+'">Artigos aceitos para publicação </a> '.decode("utf8")+'('+str(self.nPB7)+')'
		if self.nPB8>0:
			s+= '<li> <a href="PB8-0'+self.extensaoPagina+'">Apresentações de trabalho </a> '.decode("utf8")+'('+str(self.nPB8)+')'
		if self.nPB9>0:
			s+= '<li> <a href="PB9-0'+self.extensaoPagina+'">Demais tipos de produção bibliográfica </a> '.decode("utf8")+'('+str(self.nPB9)+')'
		if self.nPB>0:
			s+= '<li> <a href="PB-0'+self.extensaoPagina+'">Total de produção bibliográfica</a> '.decode("utf8")+'('+str(self.nPB)+')'
		else:
			s+= '<i>Nenhum item achado nos currículos Lattes</i>'.decode("utf8")


		s+='</ul> <h3 id="producaoTecnica">Produção técnica</h3> <ul>'.decode("utf8")
		if self.nPT0>0:
			s+= '<li> <a href="PT0-0'+self.extensaoPagina+'">Programas de computador com registro de patente</a> '.decode("utf8")+'('+str(self.nPT0)+')'
		if self.nPT1>0:
			s+= '<li> <a href="PT1-0'+self.extensaoPagina+'">Programas de computador sem registro de patente</a> '.decode("utf8")+'('+str(self.nPT1)+')'
		if self.nPT2>0:
			s+= '<li> <a href="PT2-0'+self.extensaoPagina+'">Produtos tecnológicos</a> '.decode("utf8")+'('+str(self.nPT2)+')'
		if self.nPT3>0:
			s+= '<li> <a href="PT3-0'+self.extensaoPagina+'">Processos ou técnicas</a> '.decode("utf8")+'('+str(self.nPT3)+')'
		if self.nPT4>0:
			s+= '<li> <a href="PT4-0'+self.extensaoPagina+'">Trabalhos técnicos</a> '.decode("utf8")+'('+str(self.nPT4)+')'
		if self.nPT5>0:
			s+= '<li> <a href="PT5-0'+self.extensaoPagina+'">Demais tipos de produção técnica</a> '.decode("utf8")+'('+str(self.nPT5)+')'
		if self.nPT>0:
			s+= '<li> <a href="PT-0'+self.extensaoPagina+'">Total de produção técnica</a> '.decode("utf8")+'('+str(self.nPT)+')'
		else:
			s+= '<i>Nenhum item achado nos currículos Lattes</i>'.decode("utf8")


		s+='</ul> <h3 id="producaoArtistica">Produção artística</h3> <ul>'.decode("utf8")
		if self.nPA>0:
			s+= '<li> <a href="PA-0'+self.extensaoPagina+'">Total de produção artística</a> '.decode("utf8")+'('+str(self.nPA)+')'
		else:
			s+= '<i>Nenhum item achado nos currículos Lattes</i>'.decode("utf8")


		if self.grupo.obterParametro('relatorio-mostrar_orientacoes'):
			s+='</ul> <h3 id="orientacoes">Orientações</h3> <ul>'.decode("utf8")
			s+='<li><b>Orientações em andamento</b>'.decode("utf8")
			s+='<ul>'
			if self.nOA0>0:
				s+= '<li> <a href="OA0-0'+self.extensaoPagina+'">Supervisão de pós-doutorado</a> '.decode("utf8")+'('+str(self.nOA0)+')'
			if self.nOA1>0:
				s+= '<li> <a href="OA1-0'+self.extensaoPagina+'">Tese de doutorado</a> '.decode("utf8")+'('+str(self.nOA1)+')'
			if self.nOA2>0:
				s+= '<li> <a href="OA2-0'+self.extensaoPagina+'">Dissertação de mestrado</a> '.decode("utf8")+'('+str(self.nOA2)+')'
			if self.nOA3>0:
				s+= '<li> <a href="OA3-0'+self.extensaoPagina+'">Monografia de conclusão de curso de aperfeiçoamento/especialização</a> '.decode("utf8")+'('+str(self.nOA3)+')'
			if self.nOA4>0:
				s+= '<li> <a href="OA4-0'+self.extensaoPagina+'">Trabalho de conclusão de curso de graduação</a> '.decode("utf8")+'('+str(self.nOA4)+')'
			if self.nOA5>0:
				s+= '<li> <a href="OA5-0'+self.extensaoPagina+'">Iniciação científica</a> '.decode("utf8")+'('+str(self.nOA5)+')'
			if self.nOA6>0:
				s+= '<li> <a href="OA6-0'+self.extensaoPagina+'">Orientações de outra natureza</a> '.decode("utf8")+'('+str(self.nOA6)+')'
			if self.nOA>0:
				s+= '<li> <a href="OA-0'+self.extensaoPagina+'">Total de orientações em andamento</a> '.decode("utf8")+'('+str(self.nOA)+')'
			else:
				s+= '<i>Nenhum item achado nos currículos Lattes</i>'.decode("utf8")
			s+='</ul>'
			
			s+='<li><b>Supervisões e orientações concluídas</b>'.decode("utf8")
			s+='<ul>'
			if self.nOC0>0:
				s+= '<li> <a href="OC0-0'+self.extensaoPagina+'">Supervisão de pós-doutorado</a> '.decode("utf8")+'('+str(self.nOC0)+')'
			if self.nOC1>0:
				s+= '<li> <a href="OC1-0'+self.extensaoPagina+'">Tese de doutorado</a> '.decode("utf8")+'('+str(self.nOC1)+')'
			if self.nOC2>0:
				s+= '<li> <a href="OC2-0'+self.extensaoPagina+'">Dissertação de mestrado</a> '.decode("utf8")+'('+str(self.nOC2)+')'
			if self.nOC3>0:
				s+= '<li> <a href="OC3-0'+self.extensaoPagina+'">Monografia de conclusão de curso de aperfeiçoamento/especialização</a> '.decode("utf8")+'('+str(self.nOC3)+')'
			if self.nOC4>0:
				s+= '<li> <a href="OC4-0'+self.extensaoPagina+'">Trabalho de conclusão de curso de graduação</a> '.decode("utf8")+'('+str(self.nOC4)+')'
			if self.nOC5>0:
				s+= '<li> <a href="OC5-0'+self.extensaoPagina+'">Iniciação científica</a> '.decode("utf8")+'('+str(self.nOC5)+')'
			if self.nOC6>0:
				s+= '<li> <a href="OC6-0'+self.extensaoPagina+'">Orientações de outra natureza</a> '.decode("utf8")+'('+str(self.nOC6)+')'
			if self.nOC>0:
				s+= '<li> <a href="OC-0'+self.extensaoPagina+'">Total de orientações concluídas</a> '.decode("utf8")+'('+str(self.nOC)+')' 
			else:
				s+= '<i>Nenhum item achado nos currículos Lattes</i>'.decode("utf8")
			s+='</ul>'


		if self.grupo.obterParametro('relatorio-incluir_projeto'):
			s+='</ul> <h3 id="projetos">Projetos de pesquisa</h3> <ul>'.decode("utf8")
			if self.nPj>0:
				s+= '<li> <a href="Pj-0'+self.extensaoPagina+'">Total de projetos de pesquisa</a> '.decode("utf8")+'('+str(self.nPj)+')'
			else:
				s+= '<i>Nenhum item achado nos currículos Lattes</i>'.decode("utf8")
			s+='</ul>'


		if self.grupo.obterParametro('relatorio-incluir_premio'):
			s+='</ul> <h3 id="premios">Prêmios e títulos</h3> <ul>'.decode("utf8")
			if self.nPm>0:
				s+= '<li> <a href="Pm-0'+self.extensaoPagina+'">Total de prêmios e títulos</a> '.decode("utf8")+'('+str(self.nPm)+')'
			else:
				s+= '<i>Nenhum item achado nos currículos Lattes</i>'.decode("utf8")
			s+='</ul>'

		
		if self.grupo.obterParametro('relatorio-incluir_participacao_em_evento'):
			s+='</ul> <h3 id="eventos">Participação em eventos</h3> <ul>'.decode("utf8")
			if self.nEp>0:
				s+= '<li> <a href="Ep-0'+self.extensaoPagina+'">Total de participação em eventos</a> '.decode("utf8")+'('+str(self.nEp)+')'
			else:
				s+= '<i>Nenhum item achado nos currículos Lattes</i>'.decode("utf8")
			s+='</ul>'

		
		if self.grupo.obterParametro('relatorio-incluir_organizacao_de_evento'):
			s+='</ul> <h3 id="eventos">Organização de eventos</h3> <ul>'.decode("utf8")
			if self.nEo>0:
				s+= '<li> <a href="Eo-0'+self.extensaoPagina+'">Total de organização de eventos</a> '.decode("utf8")+'('+str(self.nEo)+')'
			else:
				s+= '<i>Nenhum item achado nos currículos Lattes</i>'.decode("utf8")
			s+='</ul>'


		if self.grupo.obterParametro('grafo-mostrar_grafo_de_colaboracoes'):
			s+='</ul> <h3 id="grafo">Grafo de colaborações</h3> <ul>'.decode("utf8")
			s+='<a href="grafoDeColaboracoes'+self.extensaoPagina+'"><img src="grafoDeColaboracoesSemPesos-t.png" border=1> </a>'
		s+='</ul>'

		if self.grupo.obterParametro('mapa-mostrar_mapa_de_geolocalizacao'):
			s+='<h3 id="mapa">Mapa de geolocaliza&ccedil;&atilde;o</h3> <br> <div id="map_canvas" style="width: 800px; height: 600px"></div> <br>'
			s+='<b>Legenda</b><table>'
			if self.grupo.obterParametro('mapa-incluir_membros_do_grupo'):
				s+='<tr><td> <img src=lattesPoint0.png></td> <td> Membro (orientador) </td></tr>'.decode("utf8")
			if self.grupo.obterParametro('mapa-incluir_alunos_de_pos_doutorado'):
				s+='<tr><td> <img src=lattesPoint1.png></td> <td>  Pesquisador com pós-doutorado concluído e ID Lattes cadastrado no currículo do supervisor </td></tr>'.decode("utf8")
			if self.grupo.obterParametro('mapa-incluir_alunos_de_doutorado'):
				s+='<tr><td> <img src=lattesPoint2.png></td> <td>  Aluno com doutorado concluído e ID Lattes cadastrado no currículo do orientador </td></tr>'.decode("utf8")
			if self.grupo.obterParametro('mapa-incluir_alunos_de_mestrado'):
				s+='<tr><td> <img src=lattesPoint3.png></td> <td>  Aluno com mestrado e ID Lattes cadastrado no currículo do orientador </td></tr>'.decode("utf8")
			s+='</table>'


		########################################
		########################################
		if self.grupo.obterParametro('relatorio-incluir-internacionalizacao'):
			s+='</ul> <h3 id="internacionalizacao">Internacionalização</h3> <ul>'.decode("utf8")
			if self.nIn0>0:
				s+= '<li> <a href="In0-0'+self.extensaoPagina+'">Coautoria e internacionalização</a> '.decode("utf8")+'('+str(self.nIn0)+')'
			else:
				s+= '<i>Nenhuma publicação com DOI disponível para análise</i>'.decode("utf8")
			s+='</ul>'
		########################################
		########################################

		
		s+= self.paginaBottom()
		self.salvarPagina("index"+self.extensaoPagina, s)


	def gerarPaginasDeProducoesBibliograficas(self):
		self.nPB0=0
		self.nPB1=0
		self.nPB2=0
		self.nPB3=0
		self.nPB4=0
		self.nPB5=0
		self.nPB6=0
		self.nPB7=0
		self.nPB8=0
		self.nPB9=0
		self.nPB =0

		if self.grupo.obterParametro('relatorio-incluir_artigo_em_periodico'):
			self.nPB0 = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaArtigoEmPeriodico, "Artigos completos publicados em periódicos", "PB0", ris=True)
		if self.grupo.obterParametro('relatorio-incluir_livro_publicado'):
			self.nPB1 = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaLivroPublicado, "Livros publicados/organizados ou edições", "PB1", ris=True)
		if self.grupo.obterParametro('relatorio-incluir_capitulo_de_livro_publicado'):
			self.nPB2 = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaCapituloDeLivroPublicado, "Capítulos de livros publicados", "PB2", ris=True)
		if self.grupo.obterParametro('relatorio-incluir_texto_em_jornal_de_noticia'):
			self.nPB3 = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaTextoEmJornalDeNoticia, "Textos em jornais de notícias/revistas", "PB3", ris=True)
		if self.grupo.obterParametro('relatorio-incluir_trabalho_completo_em_congresso'):
			self.nPB4 = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaTrabalhoCompletoEmCongresso, "Trabalhos completos publicados em anais de congressos", "PB4", ris=True)
		if self.grupo.obterParametro('relatorio-incluir_resumo_expandido_em_congresso'):
			self.nPB5 = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaResumoExpandidoEmCongresso, "Resumos expandidos publicados em anais de congressos", "PB5", ris=True)
		if self.grupo.obterParametro('relatorio-incluir_resumo_em_congresso'):
			self.nPB6 = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaResumoEmCongresso, "Resumos publicados em anais de congressos", "PB6", ris=True)
		if self.grupo.obterParametro('relatorio-incluir_artigo_aceito_para_publicacao'):
			self.nPB7 = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaArtigoAceito, "Artigos aceitos para publicação", "PB7")
		if self.grupo.obterParametro('relatorio-incluir_apresentacao_de_trabalho'):
			self.nPB8 = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaApresentacaoDeTrabalho, "Apresentações de trabalho", "PB8")
		if self.grupo.obterParametro('relatorio-incluir_outro_tipo_de_producao_bibliografica'):
			self.nPB9 = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaOutroTipoDeProducaoBibliografica, "Demais tipos de produção bibliográfica", "PB9")
		# Total de produção bibliográfica
		self.nPB = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaPB, "Total de produção bibliográfica", "PB")


	def gerarPaginasDeProducoesTecnicas(self):
		self.nPT0=0
		self.nPT1=0
		self.nPT2=0
		self.nPT3=0
		self.nPT4=0
		self.nPT5=0
		self.nPT =0

		if self.grupo.obterParametro('relatorio-incluir_software_com_patente'):
			self.nPT0 = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaSoftwareComPatente, "Softwares com registro de patente", "PT0")
		if self.grupo.obterParametro('relatorio-incluir_software_sem_patente'):
			self.nPT1 = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaSoftwareSemPatente, "Softwares sem registro de patente", "PT1")
		if self.grupo.obterParametro('relatorio-incluir_produto_tecnologico'):
			self.nPT2 = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaProdutoTecnologico, "Produtos tecnológicos", "PT2")
		if self.grupo.obterParametro('relatorio-incluir_processo_ou_tecnica'):
			self.nPT3 = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaProcessoOuTecnica, "Processos ou técnicas", "PT3")
		if self.grupo.obterParametro('relatorio-incluir_trabalho_tecnico'):
			self.nPT4 = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaTrabalhoTecnico, "Trabalhos técnicos", "PT4")
		if self.grupo.obterParametro('relatorio-incluir_outro_tipo_de_producao_tecnica'):
			self.nPT5 = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaOutroTipoDeProducaoTecnica, "Demais tipos de produção técnica", "PT5")
		# Total de produções técnicas
		self.nPT = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaPT, "Total de produção técnica", "PT")


	def gerarPaginasDeProducoesArtisticas(self):
		self.nPA0 =0
		self.nPA  =0

		if self.grupo.obterParametro('relatorio-incluir_producao_artistica'):
			self.nPA0 = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaProducaoArtistica, "Produção artística/cultural", "PA0")
		# Total de produções técnicas
		self.nPA = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaPA, "Total de produção artística", "PA")


	def gerarPaginasDeOrientacoes(self):
		self.nOA0=0
		self.nOA1=0
		self.nOA2=0
		self.nOA3=0
		self.nOA4=0
		self.nOA5=0
		self.nOA6=0
		self.nOA =0

		if self.grupo.obterParametro('relatorio-incluir_orientacao_em_andamento_pos_doutorado'):
			self.nOA0 = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaOASupervisaoDePosDoutorado, "Supervisão de pós-doutorado", "OA0")
		if self.grupo.obterParametro('relatorio-incluir_orientacao_em_andamento_doutorado'):
			self.nOA1 = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaOATeseDeDoutorado, "Tese de doutorado", "OA1")
		if self.grupo.obterParametro('relatorio-incluir_orientacao_em_andamento_mestrado'):
			self.nOA2 = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaOADissertacaoDeMestrado, "Dissertação de mestrado", "OA2")
		if self.grupo.obterParametro('relatorio-incluir_orientacao_em_andamento_monografia_de_especializacao'):
			self.nOA3 = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaOAMonografiaDeEspecializacao, "Monografia de conclusão de curso de aperfeiçoamento/especialização", "OA3")
		if self.grupo.obterParametro('relatorio-incluir_orientacao_em_andamento_tcc'):
			self.nOA4 = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaOATCC, "Trabalho de conclusão de curso de graduação", "OA4")
		if self.grupo.obterParametro('relatorio-incluir_orientacao_em_andamento_iniciacao_cientifica'):
			self.nOA5 = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaOAIniciacaoCientifica, "Iniciação científica", "OA5")
		if self.grupo.obterParametro('relatorio-incluir_orientacao_em_andamento_outro_tipo'):
			self.nOA6 = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaOAOutroTipoDeOrientacao, "Orientações de outra natureza", "OA6")
		# Total de orientações em andamento
		self.nOA = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaOA, "Total de orientações em andamento", "OA")

		self.nOC0=0
		self.nOC1=0
		self.nOC2=0
		self.nOC3=0
		self.nOC4=0
		self.nOC5=0
		self.nOC6=0
		self.nOC =0

		if self.grupo.obterParametro('relatorio-incluir_orientacao_concluida_pos_doutorado'):
			self.nOC0 = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaOCSupervisaoDePosDoutorado, "Supervisão de pós-doutorado", "OC0")
		if self.grupo.obterParametro('relatorio-incluir_orientacao_concluida_doutorado'):
			self.nOC1 = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaOCTeseDeDoutorado, "Tese de doutorado", "OC1")
		if self.grupo.obterParametro('relatorio-incluir_orientacao_concluida_mestrado'):
			self.nOC2 = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaOCDissertacaoDeMestrado, "Dissertação de mestrado", "OC2")
		if self.grupo.obterParametro('relatorio-incluir_orientacao_concluida_monografia_de_especializacao'):
			self.nOC3 = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaOCMonografiaDeEspecializacao, "Monografia de conclusão de curso de aperfeiçoamento/especialização", "OC3")
		if self.grupo.obterParametro('relatorio-incluir_orientacao_concluida_tcc'):
			self.nOC4 = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaOCTCC, "Trabalho de conclusão de curso de graduação", "OC4")
		if self.grupo.obterParametro('relatorio-incluir_orientacao_concluida_iniciacao_cientifica'):
			self.nOC5 = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaOCIniciacaoCientifica, "Iniciação científica", "OC5")
		if self.grupo.obterParametro('relatorio-incluir_orientacao_concluida_outro_tipo'):
			self.nOC6 = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaOCOutroTipoDeOrientacao, "Orientações de outra natureza", "OC6")
		# Total de orientações concluídas
		self.nOC = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaOC, "Total de orientações concluídas", "OC")



	def gerarPaginasDeProjetos(self):
		self.nPj = 0
		self.nPj = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaProjetoDePesquisa, "Total de projetos de pesquisa", "Pj")


	def gerarPaginasDePremios(self):
		self.nPm = 0
		self.nPm = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaPremioOuTitulo, "Total de prêmios e títulos", "Pm")

	def gerarPaginasDeParticipacaoEmEventos(self):
		self.nEp = 0
		self.nEp = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaParticipacaoEmEvento, "Total de participação em eventos", "Ep")
	
	def gerarPaginasDeOrganizacaoDeEventos(self):
		self.nEo = 0
		self.nEo = self.gerarPaginaDeProducoes(self.grupo.compilador.listaCompletaOrganizacaoDeEvento, "Total de organização de eventos", "Eo")

	def gerarPaginasDeInternacionalizacao(self):
		self.nIn0 = 0
		self.nIn0 = self.gerarPaginaDeInternacionalizacao(self.grupo.listaDePublicacoesEinternacionalizacao, "Coautoria e internacionalização", "In0")



	def gerarPaginaDeProducoes(self, listaCompleta, tituloPagina, prefixo, ris=False):
		numeroTotalDeProducoes = 0

		keys = listaCompleta.keys()
		keys.sort(reverse=True) 
		if len(keys)>0: # apenas geramos páginas web para lista com pelo menos 1 elemento
			for ano in keys:
				numeroTotalDeProducoes += len(listaCompleta[ano])

			maxElementos = int(self.grupo.obterParametro('global-itens_por_pagina'))
			numeroDePaginas = int(math.ceil(numeroTotalDeProducoes/(maxElementos*1.0))) # dividimos os relatórios em grupos (e.g 1000 items)

			numeroDeItem = 1
			numeroDePaginaAtual = 0
			s = ''

			for ano in keys:
				anoRotulo = str(ano) if not ano==0 else '*itens sem ano'
				s+= '<h3 class="year">'+anoRotulo+'</h3> <table>'

				elementos = listaCompleta[ano]
				elementos.sort(key = lambda x: x.chave.lower())	# Ordenamos a lista em forma ascendente (hard to explain!)

				for index in range(0, len(elementos)):
					pub = elementos[index]
					s  += '<tr valign="top"><td>'+str(index+1)+'. &nbsp;</td> <td>'+ pub.html(self.grupo.listaDeMembros) +'</td></tr>'

					# armazenamos uma copia da publicacao (formato RIS)
					if self.grupo.obterParametro('relatorio-salvar_publicacoes_em_formato_ris') and ris==True:
						self.salvarPublicacaoEmFormatoRIS(pub)
				
					if numeroDeItem%maxElementos==0 or numeroDeItem==numeroTotalDeProducoes:
						st = self.paginaTop()
						st+= '\n<h3>'+tituloPagina.decode("utf8")+'</h3> <br> <img src="'+prefixo+'.png"> <br>'

						st+= 'Número total de itens: '.decode("utf8")+str(numeroTotalDeProducoes)+'<br>'
						st+= self.gerarIndiceDePaginas(numeroDePaginas, numeroDePaginaAtual, prefixo)
						st+= s #.decode("utf8") 
						st+= '</table>' 
						st+= self.paginaBottom()

						self.salvarPagina(prefixo+'-'+str(numeroDePaginaAtual)+self.extensaoPagina, st)
						numeroDePaginaAtual += 1

						if (index+1)<len(elementos):
							s = '<h3 class="year">'+anoRotulo+'</h3> <table>'
						else:
							s = '' 
					numeroDeItem += 1

				s+= '</table>' 
		return numeroTotalDeProducoes 


	def gerarIndiceDePaginas(self, numeroDePaginas, numeroDePaginaAtual, prefixo):
		if numeroDePaginas==1:
			return ''
		else:
			s = 'Página: '.decode("utf8")
			for i in range(0, numeroDePaginas):
				if i==numeroDePaginaAtual:
					s+= '<b>'+str(i+1)+'</b> &nbsp;'
				else:
					s+= '<a href="'+prefixo+'-'+str(i)+self.extensaoPagina+'">'+str(i+1)+'</a> &nbsp;'
			return '<center>'+s+'</center>'


	##################################################################################################
	def gerarPaginaDeInternacionalizacao(self, listaCompleta, tituloPagina, prefixo):
		numeroTotalDeProducoes = 0
		gInternacionalizacao = GraficoDeInternacionalizacao(listaCompleta)
		htmlCharts = gInternacionalizacao.criarGraficoDeBarrasDeOcorrencias()

		keys = listaCompleta.keys()
		keys.sort(reverse=True) 
		if len(keys)>0: # apenas geramos páginas web para lista com pelo menos 1 elemento
			for ano in keys:
				numeroTotalDeProducoes += len(listaCompleta[ano])

			s = self.paginaTop(cabecalho=htmlCharts)

			s+= '\n<h3>'+tituloPagina.decode("utf8")+'</h3> <br> <center> <table> <tr> <td valign="top"><div id="barchart_div"></div> </td> <td valign="top"><div id="geochart_div"></div> </td> </tr> </table> </center>'
			s+= '<table>'
			s+= '<tr><td>Número total de publicações realizadas SEM parceria com estrangeiros:</td><td>'.decode("utf8")+str(gInternacionalizacao.numeroDePublicacoesRealizadasSemParceirasComEstrangeiros())+'</td><td><i>(publicações realizadas só por pesquisadores brasileiros)</i></td></tr>'.decode("utf8")
			s+= '<tr><td>Número total de publicações realizadas COM parceria com estrangeiros:</td><td>'.decode("utf8")+str(gInternacionalizacao.numeroDePublicacoesRealizadasComParceirasComEstrangeiros())+'</td><td></td></tr>'
			s+= '<tr><td>Número total de publicações com parcerias NÂO identificadas:</td><td>'.decode("utf8")+str(gInternacionalizacao.numeroDePublicacoesComParceriasNaoIdentificadas())+'</td><td></td></tr>'
			s+= '<tr><td>Número total de publicações com DOI cadastrado:</td><td><b>'.decode("utf8")+str(numeroTotalDeProducoes)+'</b></td><td></td></tr>'
			s+= '</table>'

			s+= '<br> <font color="red">(*) A estimativa de "coautoria e internacionalização" é baseada na análise automática dos DOIs das publicações cadastradas nos CVs Lattes. A identificação de países, para cada publicação, é feita através de buscas simples de nomes de países.</font><br><p>'.decode("utf8")

			for ano in keys:
				anoRotulo = str(ano) if not ano==0 else '*itens sem ano'
				s+= '<h3 class="year">'+anoRotulo+'</h3> <table>'

				elementos = listaCompleta[ano]
				elementos.sort(key = lambda x: x.chave.lower())	# Ordenamos a lista em forma ascendente (hard to explain!)
				for index in range(0, len(elementos)):
					pub = elementos[index]
					s  += '<tr valign="top"><td>'+str(index+1)+'. &nbsp;</td> <td>'+ pub.html() +'</td></tr>'
				s+= '</table>' 
			s+= self.paginaBottom()
			self.salvarPagina(prefixo+'-0'+self.extensaoPagina, s)

		return numeroTotalDeProducoes 
	##################################################################################################


	def gerarPaginaDeGrafosDeColaboracoes(self):
		lista = ''
		if self.grupo.obterParametro('grafo-incluir_artigo_em_periodico'):
			lista += 'Artigos completos publicados em periódicos, '.decode("utf8")
		if self.grupo.obterParametro('grafo-incluir_livro_publicado'):
			lista += 'Livros publicados/organizados ou edições, '.decode("utf8")
		if self.grupo.obterParametro('grafo-incluir_capitulo_de_livro_publicado'):
			lista += 'Capítulos de livros publicados, '.decode("utf8")
		if self.grupo.obterParametro('grafo-incluir_texto_em_jornal_de_noticia'):
			lista += 'Textos em jornais de notícias/revistas, '.decode("utf8")
		if self.grupo.obterParametro('grafo-incluir_trabalho_completo_em_congresso'):
			lista += 'Trabalhos completos publicados em anais de congressos, '.decode("utf8")
		if self.grupo.obterParametro('grafo-incluir_resumo_expandido_em_congresso'):
			lista += 'Resumos expandidos publicados em anais de congressos, '.decode("utf8")
		if self.grupo.obterParametro('grafo-incluir_resumo_em_congresso'):
			lista += 'Resumos publicados em anais de congressos, '.decode("utf8")
		if self.grupo.obterParametro('grafo-incluir_artigo_aceito_para_publicacao'):
			lista += 'Artigos aceitos para publicação, '.decode("utf8")
		if self.grupo.obterParametro('grafo-incluir_apresentacao_de_trabalho'):
			lista += 'Apresentações de trabalho, '.decode("utf8")
		if self.grupo.obterParametro('grafo-incluir_outro_tipo_de_producao_bibliografica'):
			lista += 'Demais tipos de produção bibliográfica, '.decode("utf8")

		lista = lista.strip().strip(",")

		s= self.paginaTop()
		s+='\n<h3>Grafo de colabora&ccedil;&otilde;es</h3> \
        <a href=membros'+self.extensaoPagina+'>'+str(self.grupo.numeroDeMembros())+' curriculos Lattes</a> foram considerados, \
        gerando os seguintes grafos de colabora&ccedil;&otilde;es encontradas com base nas produ&ccedil;&otilde;es: <i>'+lista+'</i>. <br><p>'.decode("utf8")

		prefix = self.grupo.obterParametro('global-prefixo')+'-' if not self.grupo.obterParametro('global-prefixo')=='' else ''
		s+='Veja <a href="grafoDeColaboracoesInterativo'+self.extensaoPagina+'?entradaScriptLattes=./'+prefix+'matrizDeAdjacencia.xml">na seguinte página</a> uma versão interativa do grafo de colabora&ccedil;&otilde;es.<br><p><br><p>'.decode("utf8")

		s+='\nClique no nome dentro do vértice para visualizar o currículo Lattes. Para cada nó: o valor entre colchetes indica o número \
        de produ&ccedil;&otilde;es feitas em colabora&ccedil;&atilde;o apenas com os outros membros do próprio grupo. <br>'.decode("utf8")

		if self.grupo.obterParametro('grafo-considerar_rotulos_dos_membros_do_grupo'):
			s+='As cores representam os seguintes rótulos: '.decode("utf8")
			for i in range(0, len(self.grupo.listaDeRotulos)):
				rot = self.grupo.listaDeRotulos[i].decode("utf8")
				cor = self.grupo.listaDeRotulosCores[i].decode("utf8")
				if rot=='':
					rot = '[Sem rótulo]'.decode("utf8")
				s+='<span style="background-color:'+cor+'">&nbsp;&nbsp;&nbsp;&nbsp;</span>'+rot+ ' ' 
		s+='\
        <ul> \
        <li><b>Grafo de colabora&ccedil;&otilde;es sem pesos</b><br> \
            <img src=grafoDeColaboracoesSemPesos.png border=1 ISMAP USEMAP="#grafo1"> <br><p> \
        <li><b>Grafo de colabora&ccedil;&otilde;es com pesos</b><br> \
            <img src=grafoDeColaboracoesComPesos.png border=1 ISMAP USEMAP="#grafo2"> <br><p> \
        <li><b>Grafo de colabora&ccedil;&otilde;es com pesos normalizados</b><br> \
            <img src=grafoDeColaboracoesNormalizado.png border=1 ISMAP USEMAP="#grafo3"> \
        </ul>'.decode("utf8")
	
		cmapx1 = self.grupo.grafosDeColaboracoes.grafoDeCoAutoriaSemPesosCMAPX
		cmapx2 = self.grupo.grafosDeColaboracoes.grafoDeCoAutoriaComPesosCMAPX
		cmapx3 = self.grupo.grafosDeColaboracoes.grafoDeCoAutoriaNormalizadoCMAPX
		s+='<map id="grafo1" name="grafo1">'+cmapx1.decode("utf8")+'\n</map>\n'
		s+='<map id="grafo2" name="grafo2">'+cmapx2.decode("utf8")+'\n</map>\n'
		s+='<map id="grafo3" name="grafo3">'+cmapx3.decode("utf8")+'\n</map>\n'

		if self.grupo.obterParametro('grafo-incluir_grau_de_colaboracao'):
			s+='<br><p><h3>Grau de colaboração</h3> \
                O grau de colaboração (<i>Collaboration Rank</i>) é um valor numérico que indica o impacto de um membro no grafo de colaborações.\
				<br>Esta medida é similar ao <i>PageRank</i> para grafos direcionais (com pesos).<br><p>'.decode("utf8")

			ranks, autores, rotulos = zip(*sorted(zip(self.grupo.vectorRank, self.grupo.nomes, self.grupo.rotulos), reverse=True))

			s+='<table border=1><tr> <td><i><b>Collaboration Rank</b></i></td> <td><b>Membro</b></td> </tr>'
			for i in range(0, len(ranks)):
				s+='<tr><td>'+str(round(ranks[i],2))+'</td><td>'+autores[i]+'</td></tr>'
			s+='</table> <br><p>'

			if self.grupo.obterParametro('grafo-considerar_rotulos_dos_membros_do_grupo'):
				for i in range(0, len(self.grupo.listaDeRotulos)): 
					somaAuthorRank = 0

					rot = self.grupo.listaDeRotulos[i].decode("utf8")
					cor = self.grupo.listaDeRotulosCores[i].decode("utf8")
					s+='<b><span style="background-color:'+cor+'">&nbsp;&nbsp;&nbsp;&nbsp;</span>'+rot+'</b><br>'

					s+='<table border=1><tr> <td><i><b>AuthorRank</b></i></td> <td><b>Membro</b></td> </tr>'
					for i in range(0, len(ranks)):
						if rotulos[i]==rot:
							s+='<tr><td>'+str(round(ranks[i],2)) +'</td><td>'+autores[i]+'</td></tr>'
							somaAuthorRank += ranks[i]
					s+='</table> <br> Total: '+str(round(somaAuthorRank,2))+'<br><p>'
						
		s+= self.paginaBottom()
		self.salvarPagina("grafoDeColaboracoes"+self.extensaoPagina, s)

		# grafo interativo
		s= self.paginaTop()
		s+= '<applet code=MyGraph.class width=1280 height=800 archive="http://www.vision.ime.usp.br/creativision/graphview/graphview.jar,http://www.vision.ime.usp.br/creativision/graphview/prefuse.jar"></applet></body></html>'
		s+= self.paginaBottom()
		self.salvarPagina("grafoDeColaboracoesInterativo"+self.extensaoPagina, s)

		
		
	def gerarPaginaDeMembros(self):
		s= self.paginaTop()
		s+='\n<h3>Lista de membros</h3> <table> \
              <tr><td></td> <td></td> <td></td> <td></td> <td class="centered"><b><font size=-1>Bolsa de produtividade</font></b></td> <td class="centered"><b><font size=-1>Período de</font></b></td>           <td class="centered"><b><font size=-1>Data de          </font><b></td>  <td class="centered"></td></tr> \
              <tr><td></td> <td></td> <td></td> <td></td> <td class="centered"><b><font size=-1>em pesquisa do CNPq</font></b></td>    <td class="centered"><b><font size=-1>análise individual</font></b></td> <td class="centered"><b><font size=-1>atualização do CV</font><b></td>  <td class="centered"></td></tr>'.decode("utf8")

		elemento = 0
		for membro in self.grupo.listaDeMembros:
			elemento += 1
			bolsa = '('+membro.bolsaProdutividade+')' if not membro.bolsaProdutividade=='' else ''
			rotulo=  membro.rotulo if not membro.rotulo=='[sem rotulo]' else ''
			s+= '\n<tr> \
                     <td valign="center" height="40px">'+str(elemento)+'.</td> \
                     <td valign="top" height="40px"><img src="'+membro.foto+'" width="40px"></td> \
                     <td><a href="'+membro.url+'">'+membro.nomeCompleto+'</a></td> \
                     <td class="centered"><font size=-1>'+rotulo+'</font></td> \
                     <td class="centered"><font size=-1>'+bolsa+'</font></td> \
                     <td class="centered"><font size=-1>'+membro.periodo+'</font></td> \
                     <td class="centered"><font size=-1>'+membro.atualizacaoCV+'</font></td> \
                     <td class="centered"><a href="http://scholar.google.com.br/citations?view_op=search_authors&mauthors='+membro.nomeCompleto+'"><font size=-1>[ Cita&ccedil;&otilde;es em Google Acad&ecirc;mico | </font></a></td> \
                     <td class="centered"><a href="http://academic.research.microsoft.com/Search?query=author:('+membro.nomeCompleto+')"><font size=-1>Cita&ccedil;&otilde;es em Microsoft Acad&ecirc;mico ]</font></a></td> \
                 </tr>'
		s+='\n</table>'
		s+= self.paginaBottom()

		self.salvarPagina("membros"+self.extensaoPagina, s)

			

	def paginaTop(self, cabecalho=''):
		nomeGrupo = self.grupo.obterParametro('global-nome_do_grupo').decode("utf8")

		s = self.html1+' \
        <head> \
           <title>'+nomeGrupo+'</title> \
           <meta name="Generator" content="scriptLattes"> \
           <link rel="stylesheet" href="scriptLattes.css" type="text/css">  \
           <meta http-equiv="Content-Type" content="text/html; charset=utf8">'
		if (not cabecalho==''):
			s+= cabecalho
		s+=' \
        </head> \n \
        <body> <div id="header2"> <button onClick="history.go(-1)">Voltar</button> \
        <h2> '+nomeGrupo+'</h2> </div>'
		return s


	def paginaBottom(self):
		agora = datetime.datetime.now()
		dia = '0'+str(agora.day)
		mes = '0'+str(agora.month)
		ano = str(agora.year)
		hora    = '0'+str(agora.hour)
		minuto  = '0'+str(agora.minute)
		segundo = '0'+str(agora.second)

		dia = dia[-2:]
		mes = mes[-2:]
		hora    = hora[-2:]
		minuto  = minuto[-2:]
		segundo = segundo[-2:]
		data = dia+"/"+mes+"/"+ano+" "+hora+":"+minuto+":"+segundo

		s = '<br><p>'
		if not self.grupo.obterParametro('global-itens_desde_o_ano')=='' and not self.grupo.obterParametro('global-itens_ate_o_ano')=='':
			s+= '<br>(*) Relatório criado com produções desde '+self.grupo.obterParametro('global-itens_desde_o_ano')+' até ' +self.grupo.obterParametro('global-itens_ate_o_ano') 

		s+='\n<br>Data de processamento: '+data+'<br> \
        <div id="footer"> \
        Este arquivo foi gerado automaticamente por <a href="http://scriptlattes.sourceforge.net/">scriptLattes '+self.version+'</a> \
        (desenvolvido no <a href="http://cmcc.ufabc.edu.br/">CMCC-UFABC</a> e \
        no <a href="http://ccsl.ime.usp.br/">CCSL-IME/USP</a> por <a href="http://www.vision.ime.usp.br/~jmena">Jesús P. Mena-Chalco</a> e <a href="http://www.ime.usp.br/~cesar">Roberto M. Cesar-Jr</a>). \
        Os resultados estão sujeitos a falhas devido a inconsistências no preenchimento dos currículos Lattes. Caso note alguma falha, por favor, contacte o responsável por esta página: <a href="mailto:'+self.grupo.obterParametro('global-email_do_admin')+'">'+self.grupo.obterParametro('global-email_do_admin')+'</a> \
        </div> \
        <script type="text/javascript">\
        var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");\
        document.write(unescape("%3Cscript src=\'" + gaJsHost + "google-analytics.com/ga.js\' type=\'text/javascript\'%3E%3C/script%3E"));\
        </script>\
        <script type="text/javascript">\
        try {\
          var pageTracker = _gat._getTracker("'+self.grupo.obterParametro('global-google_analytics_key')+'");\
          pageTracker._trackPageview();\
        } catch(err) {}\
        </script> \
        </body>'+self.html2
		return s.decode("utf8")


	def salvarPagina(self, nome, conteudo):
		file = open(self.dir+"/"+nome, 'w')
 		file.write(conteudo.encode('utf8'))
		file.close()


	def salvarPublicacaoEmFormatoRIS(self, pub):
		self.arquivoRis.write(pub.ris().encode('utf8'))
		


def menuHTMLdeBuscaPB(titulo):
	titulo = re.sub('\s+','+', titulo)

	s = '<br>\
         <font size=-1> \
         [ <a href="http://scholar.google.com/scholar?hl=en&lr=&q='+titulo+'&btnG=Search">cita&ccedil;&otilde;es Google Scholar</a> | \
           <a href="http://academic.research.microsoft.com/Search?query='+titulo+'">cita&ccedil;&otilde;es Microsoft Acad&ecirc;mico</a> | \
           <a href="http://www.google.com/search?btnG=Google+Search&q='+titulo+'">busca Google</a> ] \
         </font><br>'
	return s


def menuHTMLdeBuscaPT(titulo):
	titulo = re.sub('\s+','+', titulo)

	s = '<br>\
         <font size=-1> \
         [ <a href="http://www.google.com/search?btnG=Google+Search&q='+titulo+'">busca Google</a> | \
           <a href="http://www.bing.com/search?q='+titulo+'">busca Bing</a> ] \
         </font><br>'
	return s

def menuHTMLdeBuscaPA(titulo):
	titulo = re.sub('\s+','+', titulo)

	s = '<br>\
         <font size=-1> \
         [ <a href="http://www.google.com/search?btnG=Google+Search&q='+titulo+'">busca Google</a> | \
           <a href="http://www.bing.com/search?q='+titulo+'">busca Bing</a> ] \
         </font><br>'
	return s

