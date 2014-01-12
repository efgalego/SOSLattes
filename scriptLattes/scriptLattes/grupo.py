#!/usr/bin/python
# encoding: utf-8
# filename: grupo.py
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


import fileinput
import sets
import operator

from membro import *
from compiladorDeListas import *
from grafoDeColaboracoes import *
from graficoDeBarras import *
from mapaDeGeolocalizacao import *
from geradorDePaginasWeb import *
from authorRank import *
from analisadorDePublicacoes import *
from geradorOntologia import *

class Grupo:
	compilador = None
	listaDeParametros = []
	listaDeMembros = []
	listaDeRotulos = []
	listaDePublicacoesEinternacionalizacao = []

	arquivoConfiguracao = None
	itemsDesdeOAno = None
	itemsAteOAno = None
	diretorioCache = None

	matrizArtigoEmPeriodico = None
	matrizLivroPublicado = None
	matrizCapituloDeLivroPublicado = None
	matrizTextoEmJornalDeNoticia = None
	matrizTrabalhoCompletoEmCongresso = None
	matrizResumoExpandidoEmCongresso = None
	matrizResumoEmCongresso = None
	matrizArtigoAceito = None
	matrizApresentacaoDeTrabalho = None
	matrizOutroTipoDeProducaoBibliografica = None
	matrizSoftwareComPatente = None
	matrizSoftwareSemPatente = None
	matrizProdutoTecnologico = None
	matrizProcessoOuTecnica = None
	matrizTrabalhoTecnico = None
	matrizOutroTipoDeProducaoTecnica = None
	matrizProducaoArtistica = None

	matrizDeAdjacencia = None
	matrizDeFrequencia = None
	matrizDeFrequenciaNormalizada = None
	vetorDeCoAutoria = None
	grafosDeColaboracoes = None
	mapaDeGeolocalizacao = None

	vectorRank = None
	nomes = None
	rotulos = None

	def __init__(self, arquivo, listaIdMembros=[]):
		self.arquivoConfiguracao = arquivo
		self.carregarParametrosPadrao()
	
		# atualizamos a lista de parametros
		for linha in fileinput.input(self.arquivoConfiguracao):
			linha = linha.replace("\r","")
			linha = linha.replace("\n","")
			
			linhaPart = linha.partition("#") # eliminamos os comentários
			linhaDiv = linhaPart[0].split("=",1)

			if len(linhaDiv)==2:
				self.atualizarParametro(linhaDiv[0], linhaDiv[1])	

		# carregamos o periodo global
		ano1 = self.obterParametro('global-itens_desde_o_ano')
		ano2 = self.obterParametro('global-itens_ate_o_ano')
		if ano1.lower()=='hoje':
			ano1 = str(datetime.datetime.now().year)
		if ano2.lower()=='hoje':
			ano2 = str(datetime.datetime.now().year)
		if ano1=='':
			ano1 = '0'
		if ano2=='':
			ano2 = '10000'
		self.itemsDesdeOAno = int(ano1)
		self.itemsAteOAno = int(ano2)

		self.diretorioCache = self.obterParametro('global-diretorio_de_armazenamento_de_cvs')
		if not self.diretorioCache=='':
			criarDiretorio(self.diretorioCache)

		# carregamos a lista de membros
		idSequencial = 0	
		self.listaDeMembros = []
		if listaIdMembros:
			for identificador in listaIdMembros:
				if identificador != '':
					rotulo = '[Sem rotulo]'
					self.listaDeMembros.append(Membro(idSequencial, identificador, '', '', rotulo, self.itemsDesdeOAno, self.itemsAteOAno, self.diretorioCache))
					self.listaDeRotulos.append(rotulo)
					idSequencial+=1
		else:
			for linha in fileinput.input(self.obterParametro('global-arquivo_de_entrada')):
				linha = linha.replace("\r","") 
				linha = linha.replace("\n","")
			
				linhaPart = linha.partition("#") # eliminamos os comentários
				linhaDiv = linhaPart[0].split(",") 

				if not linhaDiv[0].strip()=='':
					identificador = linhaDiv[0].strip() if len(linhaDiv)>0  else ''
					nome          = linhaDiv[1].strip() if len(linhaDiv)>1  else ''
					periodo       = linhaDiv[2].strip() if len(linhaDiv)>2  else ''
					rotulo        = linhaDiv[3].strip() if len(linhaDiv)>3 and not linhaDiv[3].strip()=='' else '[Sem rotulo]' 
					rotulo        = rotulo.capitalize() 

					# atribuicao dos valores iniciais para cada membro
					###if 'xml' in identificador.lower():
					###### self.listaDeMembros.append(Membro(idSequencial, '', nome, periodo, rotulo, self.itemsDesdeOAno, self.itemsAteOAno, xml=identificador))
					###	self.listaDeMembros.append(Membro(idSequencial, identificador, nome, periodo, rotulo, self.itemsDesdeOAno, self.itemsAteOAno, diretorioCache))
					###else:
					self.listaDeMembros.append(Membro(idSequencial, identificador, nome, periodo, rotulo, self.itemsDesdeOAno, self.itemsAteOAno, self.diretorioCache))

					self.listaDeRotulos.append(rotulo)
					idSequencial+=1

		self.listaDeRotulos = list(sets.Set(self.listaDeRotulos)) # lista unica de rotulos
		self.listaDeRotulos.sort()
		self.listaDeRotulosCores =  ['']*len(self.listaDeRotulos) 

	def carregarDadosCVLattes(self):
		for membro in self.listaDeMembros:
			membro.carregarDadosCVLattes()
			membro.filtrarItemsPorPeriodo()
			print membro

	def gerarMapaDeGeolocalizacao(self):
		if self.obterParametro('mapa-mostrar_mapa_de_geolocalizacao'):
			self.mapaDeGeolocalizacao = MapaDeGeolocalizacao(self)

	def gerarPaginasWeb(self):
		paginasWeb = GeradorDePaginasWeb(self)

	def gerarOntologia(self):
		ontologia = GeradorOntologia(self)
		return ontologia.grafo.serialize()

	def compilarListasDeItems(self):
		self.compilador = CompiladorDeListas(self) # compilamos todo e criamos 'listasCompletas'

		# Grafos de coautoria 
		self.compilador.criarMatrizesDeColaboracao()

		[self.matrizDeAdjacencia, self.matrizDeFrequencia] = self.compilador.uniaoDeMatrizesDeColaboracao()
		self.vetorDeCoAutoria = self.matrizDeFrequencia.sum(axis=1) # suma das linhas = num. de items feitos em co-autoria (parceria) com outro membro do grupo
		self.matrizDeFrequenciaNormalizada = self.matrizDeFrequencia.copy()

		for i in range(0, self.numeroDeMembros()):
			if not self.vetorDeCoAutoria[i]==0:
				self.matrizDeFrequenciaNormalizada[i,:] /= float(self.vetorDeCoAutoria[i])

		# AuthorRank
		authorRank = AuthorRank(self.matrizDeFrequenciaNormalizada, 100)
		self.vectorRank = authorRank.vectorRank

		# Salvamos alguns dados para análise posterior (com outras ferramentas)
		prefix = self.obterParametro('global-prefixo')+'-' if not self.obterParametro('global-prefixo')=='' else ''

		# (1) matrizes 
		self.salvarMatrizTXT(self.matrizDeAdjacencia, prefix+"matrizDeAdjacencia.txt")
		self.salvarMatrizTXT(self.matrizDeFrequencia, prefix+"matrizDeFrequencia.txt")
		self.salvarMatrizTXT(self.matrizDeFrequenciaNormalizada, prefix+"matrizDeFrequenciaNormalizada.txt")
		self.salvarMatrizXML(self.matrizDeAdjacencia, prefix+"matrizDeAdjacencia.xml")
	
		# (2) listas de nomes e rótulos
		self.nomes = list([]) 
		self.rotulos = list([]) 
		for membro in self.listaDeMembros:
			self.nomes.append(membro.nomeCompleto)
			self.rotulos.append(membro.rotulo)
		self.salvarListaTXT(self.nomes, prefix+"listaDeNomes.txt")
		self.salvarListaTXT(self.rotulos, prefix+"listaDeRotulos.txt")

		# (3) medidas de authorRanks 
		self.salvarListaTXT(self.vectorRank, prefix+"authorRank.txt")


	def salvarListaTXT(self, lista, nomeArquivo):
		dir = self.obterParametro('global-diretorio_de_saida')
		arquivo = open(dir+"/"+nomeArquivo, 'w')

		for i in range(0,len(lista)):
			elemento = lista[i]
			if type(elemento)==type(unicode()):
				elemento = elemento.encode("utf8")
			else:
				elemento = str(elemento)
			arquivo.write(elemento+'\n')
		arquivo.close()


	def salvarMatrizTXT(self, matriz, nomeArquivo):
		dir = self.obterParametro('global-diretorio_de_saida')
		arquivo = open(dir+"/"+nomeArquivo, 'w')
		N = matriz.shape[0]

		for i in range(0,N):
			for j in range(0,N):
				arquivo.write(str(matriz[i , j])+' ')
			arquivo.write('\n')
		arquivo.close()


	def salvarMatrizXML(self, matriz, nomeArquivo):
		dir = self.obterParametro('global-diretorio_de_saida')
		arquivo = open(dir+"/"+nomeArquivo, 'w')

		s ='<?xml version="1.0" encoding="UTF-8"?> \
            \n<!--  An excerpt of an egocentric social network  --> \
            \n<graphml xmlns="http://graphml.graphdrawing.org/xmlns"> \
            \n<graph edgedefault="undirected"> \
            \n<!-- data schema --> \
            \n<key id="name" for="node" attr.name="name" attr.type="string"/> \
            \n<key id="nickname" for="node" attr.name="nickname" attr.type="string"/> \
            \n<key id="gender" for="node" attr.name="gender" attr.type="string"/> \
            \n<key id="image" for="node" attr.name="image" attr.type="string"/> \
            \n<key id="link" for="node" attr.name="link" attr.type="string"/> \
            \n<key id="amount" for="edge" attr.name="amount" attr.type="int"/> \
            \n<key id="pubs" for="node" attr.name="pubs" attr.type="int"/>'
 
		for i in range(0, self.numeroDeMembros()):
			membro = self.listaDeMembros[i]
			s+='\n<!-- nodes --> \
                \n<node id="'+str(membro.idMembro)+'"> \
                \n<data key="name">'+membro.nomeCompleto+'</data> \
                \n<data key="nickname">'+membro.nomeEmCitacoesBibliograficas+'</data> \
                \n<data key="gender">'+membro.sexo[0].upper()+'</data> \
                \n<data key="image">'+membro.foto+'</data> \
                \n<data key="link">'+membro.url+'</data> \
                \n<data key="pubs">'+str(int(self.vetorDeCoAutoria[i]))+'</data> \
                \n</node>'

		N = matriz.shape[0]
		for i in range(0,N):
			for j in range(0,N):
				if matriz[i,j]>0:
					s+='\n<!-- edges --> \
                        \n<edge source="'+str(i)+'" target="'+str(j)+'"> \
                        \n<data key="amount">'+str(matriz[i,j])+'</data> \
                        \n</edge>'
 
		s+='\n</graph>\
            \n</graphml>'

		arquivo.write(s.encode('utf8'))
		arquivo.close()

	def salvarVetorDeProducoes(self, vetor, nomeArquivo):
		dir = self.obterParametro('global-diretorio_de_saida')
		arquivo = open(dir+"/"+nomeArquivo, 'w')

		string = ''
		for i in range(0,len(vetor)):
			(prefixo, pAnos, pQuantidades) = vetor[i]

			string += "\n" + prefixo + ":"
			for j in range(0,len(pAnos)):
				string += str(pAnos[j]) + ',' + str(pQuantidades[j]) + ';'

		arquivo.write(string)
		arquivo.close()

	def salvarListaInternalizacaoTXT(self, listaDoiValido, nomeArquivo):
		dir = self.obterParametro('global-diretorio_de_saida')
		arquivo = open(dir+"/"+nomeArquivo, 'w')
		for i in range(0,len(listaDoiValido)):
			elemento = listaDoiValido[i]
			if type(elemento)==type(unicode()):
				elemento = elemento.encode("utf8")
			else:
				elemento = str(elemento)
			arquivo.write(elemento+'\n')
		arquivo.close()

	def gerarGraficosDeBarras(self):
		gBarra = GraficoDeBarras(self.obterParametro('global-diretorio_de_saida'))

		gBarra.criarGrafico(self.compilador.listaCompletaArtigoEmPeriodico, 'PB0', 'Numero de publicacoes')
		gBarra.criarGrafico(self.compilador.listaCompletaLivroPublicado, 'PB1', 'Numero de publicacoes')
		gBarra.criarGrafico(self.compilador.listaCompletaCapituloDeLivroPublicado, 'PB2', 'Numero de publicacoes')
		gBarra.criarGrafico(self.compilador.listaCompletaTextoEmJornalDeNoticia, 'PB3', 'Numero de publicacoes')
		gBarra.criarGrafico(self.compilador.listaCompletaTrabalhoCompletoEmCongresso, 'PB4', 'Numero de publicacoes')
		gBarra.criarGrafico(self.compilador.listaCompletaResumoExpandidoEmCongresso, 'PB5', 'Numero de publicacoes')
		gBarra.criarGrafico(self.compilador.listaCompletaResumoEmCongresso, 'PB6', 'Numero de publicacoes')
		gBarra.criarGrafico(self.compilador.listaCompletaArtigoAceito, 'PB7', 'Numero de publicacoes')
		gBarra.criarGrafico(self.compilador.listaCompletaApresentacaoDeTrabalho, 'PB8', 'Numero de publicacoes')
		gBarra.criarGrafico(self.compilador.listaCompletaOutroTipoDeProducaoBibliografica, 'PB9', 'Numero de publicacoes')

		gBarra.criarGrafico(self.compilador.listaCompletaSoftwareComPatente, 'PT0', 'Numero de producoes tecnicas')
		gBarra.criarGrafico(self.compilador.listaCompletaSoftwareSemPatente, 'PT1', 'Numero de producoes tecnicas')
		gBarra.criarGrafico(self.compilador.listaCompletaProdutoTecnologico, 'PT2', u'Numero de producoes tecnicas')
		gBarra.criarGrafico(self.compilador.listaCompletaProcessoOuTecnica, 'PT3', 'Numero de producoes tecnicas')
		gBarra.criarGrafico(self.compilador.listaCompletaTrabalhoTecnico, 'PT4', 'Numero de producoes tecnicas')
		gBarra.criarGrafico(self.compilador.listaCompletaOutroTipoDeProducaoTecnica, 'PT5', 'Numero de producoes tecnicas')

		gBarra.criarGrafico(self.compilador.listaCompletaProducaoArtistica, 'PA0', 'Numero de producoes artisticas')

		gBarra.criarGrafico(self.compilador.listaCompletaOASupervisaoDePosDoutorado, 'OA0', 'Numero de orientacoes')
		gBarra.criarGrafico(self.compilador.listaCompletaOATeseDeDoutorado, 'OA1', 'Numero de orientacoes')
		gBarra.criarGrafico(self.compilador.listaCompletaOADissertacaoDeMestrado, 'OA2', 'Numero de orientacoes')
		gBarra.criarGrafico(self.compilador.listaCompletaOAMonografiaDeEspecializacao, 'OA3', 'Numero de orientacoes')
		gBarra.criarGrafico(self.compilador.listaCompletaOATCC, 'OA4', 'Numero de orientacoes')
		gBarra.criarGrafico(self.compilador.listaCompletaOAIniciacaoCientifica, 'OA5', 'Numero de orientacoes')
		gBarra.criarGrafico(self.compilador.listaCompletaOAOutroTipoDeOrientacao, 'OA6', 'Numero de orientacoes')

		gBarra.criarGrafico(self.compilador.listaCompletaOCSupervisaoDePosDoutorado, 'OC0', 'Numero de orientacoes')
		gBarra.criarGrafico(self.compilador.listaCompletaOCTeseDeDoutorado, 'OC1', 'Numero de orientacoes')
		gBarra.criarGrafico(self.compilador.listaCompletaOCDissertacaoDeMestrado, 'OC2', 'Numero de orientacoes')
		gBarra.criarGrafico(self.compilador.listaCompletaOCMonografiaDeEspecializacao, 'OC3', 'Numero de orientacoes')
		gBarra.criarGrafico(self.compilador.listaCompletaOCTCC, 'OC4', 'Numero de orientacoes')
		gBarra.criarGrafico(self.compilador.listaCompletaOCIniciacaoCientifica, 'OC5', 'Numero de orientacoes')
		gBarra.criarGrafico(self.compilador.listaCompletaOCOutroTipoDeOrientacao, 'OC6', 'Numero de orientacoes')

		gBarra.criarGrafico(self.compilador.listaCompletaPremioOuTitulo, 'Pm', 'Numero de premios')
		gBarra.criarGrafico(self.compilador.listaCompletaProjetoDePesquisa, 'Pj', 'Numero de projetos')

		gBarra.criarGrafico(self.compilador.listaCompletaPB, 'PB', 'Numero de producoes bibliograficas')
		gBarra.criarGrafico(self.compilador.listaCompletaPT, 'PT', 'Numero de producoes tecnicas')
		gBarra.criarGrafico(self.compilador.listaCompletaPA, 'PA', 'Numero de producoes artisticas')
		gBarra.criarGrafico(self.compilador.listaCompletaOA, 'OA', 'Numero de orientacoes em andamento')
		gBarra.criarGrafico(self.compilador.listaCompletaOC, 'OC', 'Numero de orientacoes concluidas')
		
		gBarra.criarGrafico(self.compilador.listaCompletaParticipacaoEmEvento, 'Ep', 'Numero de Eventos')
		gBarra.criarGrafico(self.compilador.listaCompletaOrganizacaoDeEvento, 'Eo', 'Numero de Eventos')

		prefix = self.obterParametro('global-prefixo')+'-' if not self.obterParametro('global-prefixo')=='' else ''
		self.salvarVetorDeProducoes(gBarra.obterVetorDeProducoes(), prefix+'vetorDeProducoes.txt')


	def gerarGrafosDeColaboracoes(self):
		if self.obterParametro('grafo-mostrar_grafo_de_colaboracoes'):
			self.grafosDeColaboracoes = GrafoDeColaboracoes(self, self.obterParametro('global-diretorio_de_saida'))

	def gerarGraficoDeProporcoes(self):
		if self.obterParametro('relatorio-incluir_grafico_de_proporcoes_bibliograficas'):
			gProporcoes = GraficoDeProporcoes(self, self.obterParametro('global-diretorio_de_saida'))

	def calcularInternacionalizacao(self):
		if self.obterParametro('relatorio-incluir-internacionalizacao'):
			print "\n[ANALISANDO INTERNACIONALIZACAO]"
			self.analisadorDePublicacoes = AnalisadorDePublicacoes(self)
			self.listaDePublicacoesEinternacionalizacao = self.analisadorDePublicacoes.analisarInternacionalizacaoNaCoautoria()
			if self.analisadorDePublicacoes.listaDoiValido is not None:
				self.salvarListaInternalizacaoTXT( self.analisadorDePublicacoes.listaDoiValido, "Internacionalizacao.txt")


	def imprimirListasCompletas(self):
		self.compilador.imprimirListasCompletas()

	def imprimirMatrizesDeFrequencia(self):
		self.compilador.imprimirMatrizesDeFrequencia()
		print "\n[VETOR DE CO-AUTORIA]"
		print self.vetorDeCoAutoria
		print "\n[MATRIZ DE FREQUENCIA NORMALIZADA]"
		print self.matrizDeFrequenciaNormalizada

	def numeroDeMembros(self):
		return len(self.listaDeMembros)

	def ordenarListaDeMembros(self, chave):
		self.listaDeMembros.sort(key=operator.attrgetter(chave)) # ordenamos por nome

	def imprimirListaDeParametros(self):
		for par in self.listaDeParametros:# .keys():
			print "[PARAMETRO] ",par[0]," = ",par[1]
		print

	def imprimirListaDeMembros(self):
		for membro in self.listaDeMembros:
			print membro
		print

	def imprimirListaDeRotulos(self):
		for rotulo in self.listaDeRotulos:
			print "[ROTULO] ", rotulo

	def atualizarParametro(self, parametro, valor):
		parametro = parametro.strip().lower()
		valor = valor.strip()

		for i in range(0,len(self.listaDeParametros)):
			if parametro==self.listaDeParametros[i][0]:
				self.listaDeParametros[i][1] = valor
				return
		print "[AVISO IMPORTANTE] Nome de parametro desconhecido: "+parametro

	def obterParametro(self, parametro):
		for i in range(0,len(self.listaDeParametros)):
			if parametro==self.listaDeParametros[i][0]:
				if self.listaDeParametros[i][1].lower()=='sim':
					return 1
				if self.listaDeParametros[i][1].lower()=='nao' or self.listaDeParametros[i][1].lower()=='não':
					return 0

				return self.listaDeParametros[i][1]

	def atribuirCoNoRotulo(self, indice, cor):
		self.listaDeRotulosCores[indice] = cor

	def carregarParametrosPadrao(self):
		self.listaDeParametros.append(['global-nome_do_grupo', ''])
		self.listaDeParametros.append(['global-arquivo_de_entrada', ''])
		self.listaDeParametros.append(['global-diretorio_de_saida', ''])
		self.listaDeParametros.append(['global-email_do_admin', ''])
		self.listaDeParametros.append(['global-idioma', 'PT'])
		self.listaDeParametros.append(['global-itens_desde_o_ano', '']) 
		self.listaDeParametros.append(['global-itens_ate_o_ano', ''])      # hoje
		self.listaDeParametros.append(['global-itens_por_pagina', '1000'])
		self.listaDeParametros.append(['global-criar_paginas_jsp', 'nao'])
		self.listaDeParametros.append(['global-google_analytics_key', ''])
		self.listaDeParametros.append(['global-prefixo', ''])
		self.listaDeParametros.append(['global-diretorio_de_armazenamento_de_cvs', ''])

		self.listaDeParametros.append(['relatorio-salvar_publicacoes_em_formato_ris', 'nao'])
		self.listaDeParametros.append(['relatorio-incluir_artigo_em_periodico', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_livro_publicado', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_capitulo_de_livro_publicado', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_texto_em_jornal_de_noticia', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_trabalho_completo_em_congresso', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_resumo_expandido_em_congresso', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_resumo_em_congresso', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_artigo_aceito_para_publicacao', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_apresentacao_de_trabalho', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_outro_tipo_de_producao_bibliografica', 'sim'])

		self.listaDeParametros.append(['relatorio-incluir_software_com_patente', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_software_sem_patente', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_produto_tecnologico', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_processo_ou_tecnica', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_trabalho_tecnico', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_outro_tipo_de_producao_tecnica', 'sim'])

		self.listaDeParametros.append(['relatorio-incluir_producao_artistica', 'sim'])

		self.listaDeParametros.append(['relatorio-mostrar_orientacoes', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_orientacao_em_andamento_pos_doutorado', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_orientacao_em_andamento_doutorado', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_orientacao_em_andamento_mestrado', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_orientacao_em_andamento_monografia_de_especializacao', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_orientacao_em_andamento_tcc', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_orientacao_em_andamento_iniciacao_cientifica', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_orientacao_em_andamento_outro_tipo', 'sim'])

		self.listaDeParametros.append(['relatorio-incluir_orientacao_concluida_pos_doutorado', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_orientacao_concluida_doutorado', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_orientacao_concluida_mestrado', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_orientacao_concluida_monografia_de_especializacao', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_orientacao_concluida_tcc', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_orientacao_concluida_iniciacao_cientifica', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_orientacao_concluida_outro_tipo', 'sim'])

		self.listaDeParametros.append(['relatorio-incluir_projeto', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_premio', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_participacao_em_evento', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_organizacao_de_evento', 'sim'])


		self.listaDeParametros.append(['grafo-mostrar_grafo_de_colaboracoes', 'sim'])
		self.listaDeParametros.append(['grafo-mostrar_todos_os_nos_do_grafo', 'sim'])
		self.listaDeParametros.append(['grafo-considerar_rotulos_dos_membros_do_grupo', 'sim'])
		self.listaDeParametros.append(['grafo-mostrar_aresta_proporcional_ao_numero_de_colaboracoes', 'sim'])
		
		self.listaDeParametros.append(['grafo-incluir_artigo_em_periodico', 'sim'])
		self.listaDeParametros.append(['grafo-incluir_livro_publicado', 'sim'])
		self.listaDeParametros.append(['grafo-incluir_capitulo_de_livro_publicado', 'sim'])
		self.listaDeParametros.append(['grafo-incluir_texto_em_jornal_de_noticia', 'sim'])
		self.listaDeParametros.append(['grafo-incluir_trabalho_completo_em_congresso', 'sim'])
		self.listaDeParametros.append(['grafo-incluir_resumo_expandido_em_congresso', 'sim'])
		self.listaDeParametros.append(['grafo-incluir_resumo_em_congresso', 'sim'])
		self.listaDeParametros.append(['grafo-incluir_artigo_aceito_para_publicacao', 'sim'])
		self.listaDeParametros.append(['grafo-incluir_apresentacao_de_trabalho', 'sim'])
		self.listaDeParametros.append(['grafo-incluir_outro_tipo_de_producao_bibliografica', 'sim'])

		self.listaDeParametros.append(['grafo-incluir_software_com_patente', 'sim'])
		self.listaDeParametros.append(['grafo-incluir_software_sem_patente', 'sim'])
		self.listaDeParametros.append(['grafo-incluir_produto_tecnologico', 'sim'])
		self.listaDeParametros.append(['grafo-incluir_processo_ou_tecnica', 'sim'])
		self.listaDeParametros.append(['grafo-incluir_trabalho_tecnico', 'sim'])
		self.listaDeParametros.append(['grafo-incluir_outro_tipo_de_producao_tecnica', 'sim'])

		self.listaDeParametros.append(['grafo-incluir_producao_artistica', 'sim'])

		self.listaDeParametros.append(['grafo-incluir_grau_de_colaboracao', 'nao'])

		self.listaDeParametros.append(['mapa-mostrar_mapa_de_geolocalizacao', 'sim'])
		self.listaDeParametros.append(['mapa-incluir_membros_do_grupo', 'sim'])
		self.listaDeParametros.append(['mapa-incluir_alunos_de_pos_doutorado', 'sim'])
		self.listaDeParametros.append(['mapa-incluir_alunos_de_doutorado', 'sim'])
		self.listaDeParametros.append(['mapa-incluir_alunos_de_mestrado', 'nao'])

		self.listaDeParametros.append(['relatorio-incluir-internacionalizacao', 'nao'])

