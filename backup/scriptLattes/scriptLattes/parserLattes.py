#!/usr/bin/python
# encoding: utf-8
# filename: parserLattes.py
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
import string
from tidylib import tidy_document
from htmlentitydefs import name2codepoint

# ---------------------------------------------------------------------------- #
from HTMLParser import HTMLParser
from formacaoAcademica import *
from areaDeAtuacao import *
from idioma import *
from premioOuTitulo import *
from projetoDePesquisa import *

from artigoEmPeriodico import *
from livroPublicado import *
from capituloDeLivroPublicado import *
from textoEmJornalDeNoticia import *
from trabalhoCompletoEmCongresso import *
from resumoExpandidoEmCongresso import *
from resumoEmCongresso import *
from artigoAceito import *
from apresentacaoDeTrabalho import *
from outroTipoDeProducaoBibliografica import *

from softwareComPatente import *
from softwareSemPatente import *
from produtoTecnologico import *
from processoOuTecnica import *
from trabalhoTecnico import *
from outroTipoDeProducaoTecnica import *
from producaoArtistica import *

from orientacaoEmAndamento import *
from orientacaoConcluida import *

from organizacaoDeEvento import *
from participacaoEmEvento import *


class ParserLattes(HTMLParser):
	item = None
	nomeCompleto = ''
	bolsaProdutividade = ''
	enderecoProfissional = ''
	sexo = ''
	nomeEmCitacoesBibliograficas = ''
	atualizacaoCV = ''
	foto = ''
	textoResumo = ''

	salvarNome = None
	salvarBolsaProdutividade = None
	salvarEnderecoProfissional = None
	salvarSexo = None
	salvarNomeEmCitacoes = None
	salvarAtualizacaoCV = None
	salvarTextoResumo = None
	salvarFormacaoAcademica = None
	salvarProjetoDePesquisa = None
	salvarAreaDeAtuacao = None
	salvarIdioma = None
	salvarPremioOuTitulo = None
	salvarItem = None
	salvarParticipacaoEmEvento = None
	salvarOrganizacaoDeEvento = None

	# novos atributos
	achouIdentificacao = None
	achouEndereco = None
	salvarParte1 = None
	salvarParte2 = None
	salvarParte3 = None
	achouProducoes = None
	achouProducaoEmCTA = None
	achouProducaoTecnica = None
	achouProducaoArtisticaCultural = None
	achouOutraProducaoArtisticaCultural = None
	achouBancas = None
	achouEventos = None
	achouOrientacoes = None
	achouOutrasInformacoesRelevantes = None
	spanInformacaoArtigo = None



	achouGrupo = None
	achouEnderecoProfissional = None
	achouSexo = None
	achouNomeEmCitacoes = None
	achouFormacaoAcademica = None
	achouProjetoDePesquisa = None
	achouAreaDeAtuacao = None
	achouIdioma = None
	achouPremioOuTitulo = None

	achouArtigoEmPeriodico = None
	achouLivroPublicado = None
	achouCapituloDeLivroPublicado = None
	achouTextoEmJornalDeNoticia = None
	achouTrabalhoCompletoEmCongresso = None
	achouResumoExpandidoEmCongresso = None
	achouResumoEmCongresso = None
	achouArtigoAceito = None
	achouApresentacaoDeTrabalho = None
	achouOutroTipoDeProducaoBibliografica = None

	achouSoftwareComPatente = None
	achouSoftwareSemPatente = None
	achouProdutoTecnologico = None
	achouProcessoOuTecnica = None
	achouTrabalhoTecnico = None
	achouOutroTipoDeProducaoTecnica = None
	achouProducaoArtistica = None

	achouOrientacoesEmAndamento	= None
	achouOrientacoesConcluidas = None
	achouSupervisaoDePosDoutorado = None
	achouTeseDeDoutorado = None
	achouDissertacaoDeMestrado = None
	achouMonografiaDeEspecializacao = None
	achouTCC = None
	achouIniciacaoCientifica = None
	achouOutroTipoDeOrientacao = None

	achouParticipacaoEmEvento = None
	achouOrganizacaoDeEvento = None

	procurarCabecalho = None
	partesDoItem = []

	listaIDLattesColaboradores = []
	listaFormacaoAcademica = []
	listaProjetoDePesquisa = []
	listaAreaDeAtuacao = []
	listaIdioma = []
	listaPremioOuTitulo = []

	listaArtigoEmPeriodico = []
	listaLivroPublicado = []
	listaCapituloDeLivroPublicado = []
	listaTextoEmJornalDeNoticia = []
	listaTrabalhoCompletoEmCongresso = []
	listaResumoExpandidoEmCongresso = []
	listaResumoEmCongresso = []
	listaArtigoAceito = []
	listaApresentacaoDeTrabalho = []
	listaOutroTipoDeProducaoBibliografica = []

	listaSoftwareComPatente = []
	listaSoftwareSemPatente = []
	listaProdutoTecnologico = []
	listaProcessoOuTecnica = []
	listaTrabalhoTecnico = []
	listaOutroTipoDeProducaoTecnica = []
	listaProducaoArtistica = []

	# Orientaççoes em andamento (OA)
	listaOASupervisaoDePosDoutorado = []
	listaOATeseDeDoutorado = []
	listaOADissertacaoDeMestrado = []
	listaOAMonografiaDeEspecializacao = []
	listaOATCC = []
	listaOAIniciacaoCientifica = []
	listaOAOutroTipoDeOrientacao = []

	# Orientações concluídas (OC)
	listaOCSupervisaoDePosDoutorado = []
	listaOCTeseDeDoutorado = []
	listaOCDissertacaoDeMestrado = []
	listaOCMonografiaDeEspecializacao = []
	listaOCTCC = []
	listaOCIniciacaoCientifica = []
	listaOCOutroTipoDeOrientacao = []

	# Eventos
	listaParticipacaoEmEvento = []
	listaOrganizacaoDeEvento = []

	# auxiliares
	doi = ''
	relevante = 0
	umaUnidade = 0
	idOrientando = None

	# ------------------------------------------------------------------------ #
	def __init__(self, idMembro, cvLattesHTML):
		HTMLParser.__init__(self)

		# inicializacao obrigatoria
		self.idMembro = idMembro
		self.sexo = 'Masculino'

		self.item = ''
		self.listaIDLattesColaboradores = []
		self.listaFormacaoAcademica = []
		self.listaProjetoDePesquisa = []
		self.listaAreaDeAtuacao = []
		self.listaIdioma = []
		self.listaPremioOuTitulo = []

		self.listaArtigoEmPeriodico = []
		self.listaLivroPublicado = []
		self.listaCapituloDeLivroPublicado = []
		self.listaTextoEmJornalDeNoticia = []
		self.listaTrabalhoCompletoEmCongresso = []
		self.listaResumoExpandidoEmCongresso = []
		self.listaResumoEmCongresso = []
		self.listaArtigoAceito = []
		self.listaApresentacaoDeTrabalho = []
		self.listaOutroTipoDeProducaoBibliografica = []

		self.listaSoftwareComPatente = []
		self.listaSoftwareSemPatente = []
		self.listaProdutoTecnologico = []
		self.listaProcessoOuTecnica = []
		self.listaTrabalhoTecnico = []
		self.listaOutroTipoDeProducaoTecnica = []
		self.listaProducaoArtistica = []

		self.listaOASupervisaoDePosDoutorado = []
		self.listaOATeseDeDoutorado = []
		self.listaOADissertacaoDeMestrado = []
		self.listaOAMonografiaDeEspecializacao = []
		self.listaOATCC = []
		self.listaOAIniciacaoCientifica = []
		self.listaOAOutroTipoDeOrientacao = []

		self.listaOCSupervisaoDePosDoutorado = []
		self.listaOCTeseDeDoutorado = []
		self.listaOCDissertacaoDeMestrado = []
		self.listaOCMonografiaDeEspecializacao = []
		self.listaOCTCC = []
		self.listaOCIniciacaoCientifica = []
		self.listaOCOutroTipoDeOrientacao = []

		self.listaParticipacaoEmEvento = []
		self.listaOrganizacaoDeEvento = []


		# inicializacao para evitar a busca exaustiva de algumas palavras-chave
		self.salvarAtualizacaoCV = 1 
		self.salvarFoto = 1
		self.procurarCabecalho = 0
		self.achouGrupo = 0
		self.doi = ''
		self.relevante = 0
		self.idOrientando = ''

		# contornamos alguns erros do HTML da Plataforma Lattes
		cvLattesHTML = cvLattesHTML.replace("<![CDATA[","")
		cvLattesHTML = cvLattesHTML.replace("]]>","")

		# feed it!
		cvLattesHTML, errors = tidy_document(cvLattesHTML, options={'numeric-entities':1})
		#print errors
		#print cvLattesHTML.encode("utf8")

		## tentativa errada (não previsível)
		# options = dict(output_xhtml=1, add_xml_decl=1, indent=1, tidy_mark=0)
		# cvLattesHTML = str(tidy.parseString(cvLattesHTML, **options)).decode("utf8")

		self.feed(cvLattesHTML)

	# ------------------------------------------------------------------------ #
	def handle_starttag(self, tag, attributes):

		if tag=='h2':
			for name, value in attributes:
				if name=='class' and value=='nome':
					self.salvarNome = 1
					self.item = ''
					break

		if tag=='p':
			for name, value in attributes:
				if name=='class' and value=='resumo':
					self.salvarTextoResumo = 1
					self.item = ''
					break

		if (tag=='br' or tag=='img') and self.salvarNome:
			self.nomeCompleto = stripBlanks(self.item)
			self.item = ''
			self.salvarNome = 0
			self.salvarBolsaProdutividade = 1

		if tag=='span' and self.salvarBolsaProdutividade:
			self.item = ''

		if tag=='div':
			for name, value in attributes:
				if name=='class' and value=='title-wrapper':
					self.umaUnidade = 1	
					break

			for name, value in attributes:
				if name=='class' and value=='layout-cell-pad-5':
					if self.achouNomeEmCitacoes:
						self.salvarNomeEmCitacoes = 1
						self.item = ''

					if self.achouSexo:
						self.salvarSexo = 1
						self.item = ''

					if self.achouEnderecoProfissional:
						self.salvarEnderecoProfissional = 1
						self.item = ''

					if self.salvarParte1:
						self.salvarParte1 = 0
						self.salvarParte2 = 1
				
				if name=='class' and value=='layout-cell-pad-5 text-align-right':
					self.item = ''
					if self.achouFormacaoAcademica or self.achouAtuacaoProfissional or self.achouProjetoDePesquisa or self.achouMembroDeCorpoEditorial or self.achouRevisorDePeriodico or self.achouAreaDeAtuacao or self.achouIdioma or self.achouPremioOuTitulo or self.salvarItem: 
						self.salvarParte1 = 1
						self.salvarParte2 = 0
						if not self.salvarParte3:
							self.partesDoItem = []


		if tag=='h1' and self.umaUnidade: 
			self.procurarCabecalho = 1

			self.achouIdentificacao = 0
			self.achouEndereco = 0
			self.achouFormacaoAcademica = 0
			self.achouAtuacaoProfissional = 0
			self.achouProjetoDePesquisa = 0
			self.achouMembroDeCorpoEditorial = 0
			self.achouRevisorDePeriodico = 0
			self.achouAreaDeAtuacao = 0
			self.achouIdioma = 0
			self.achouPremioOuTitulo = 0
			self.achouProducoes = 0
			#self.achouProducaoEmCTA = 0
			#self.achouProducaoTecnica = 0
			#self.achouProducaoArtisticaCultural = 0
			self.achouBancas = 0
			self.achouEventos = 0
			self.achouOrientacoes = 0
			self.achouOutrasInformacoesRelevantes = 0
			self.salvarItem = 0


		if tag=='img':
			if self.salvarFoto: 
				for name, value in attributes:
					if name=='src' and u'servletrecuperafoto' in value:
						self.foto = value
						self.salvarFoto = 0
						break

			if self.salvarItem:
				for name, value in attributes:
					if name=='src' and u'ico_relevante' in value:
						self.relevante = 1
						break

		if tag=='br':
			self.item = self.item + ' '
		
		if tag=='span':
			if self.achouProducaoEmCTA:
				for name, value in attributes:
					if name=='class' and value==u'informacao-artigo':
						self.spanInformacaoArtigo = 1
		
		if tag=='a':
			if self.salvarItem: # and self.achouArtigoEmPeriodico:
				for name, value in attributes:
					if name=='href' and u'doi' in value:
						self.doi = value
						break

					id = re.findall(u'http://lattes.cnpq.br/(\d{16})', value)
					if name=='href' and len(id)>0:
						self.listaIDLattesColaboradores.append(id[0])
						if self.achouOrientacoesEmAndamento or self.achouOrientacoesConcluidas:
							self.idOrientando = id[0]
						break


	# ------------------------------------------------------------------------ #
	def handle_endtag(self, tag):
		# Informações do pesquisador (pre-cabecalho)
		if tag=='h2':
			if self.salvarNome:
 				self.nomeCompleto = stripBlanks(self.item)
				self.salvarNome = 0
			if self.salvarBolsaProdutividade:
				self.salvarBolsaProdutividade = 0

		if tag=='p':
			if self.salvarTextoResumo:
				self.textoResumo = stripBlanks(self.item)
				self.salvarTextoResumo = 0

		if tag=='span' and self.salvarBolsaProdutividade:
			self.bolsaProdutividade = stripBlanks(self.item)
			self.bolsaProdutividade = re.sub('Bolsista de Produtividade em Pesquisa do CNPq - ','', self.bolsaProdutividade)
			self.bolsaProdutividade = self.bolsaProdutividade.strip('()')
			self.salvarBolsaProdutividade = 0


		# Cabeçalhos
		if tag=='h1' and self.procurarCabecalho:
			self.procurarCabecalho = 0


		if tag=='div': 
			if self.salvarNomeEmCitacoes:
				self.nomeEmCitacoesBibliograficas = stripBlanks(self.item)
				self.salvarNomeEmCitacoes = 0
				self.achouNomeEmCitacoes = 0
			if self.salvarSexo:
				self.sexo = stripBlanks(self.item)
				self.salvarSexo = 0
				self.achouSexo = 0
			if self.salvarEnderecoProfissional:
				self.enderecoProfissional = stripBlanks(self.item)
				self.enderecoProfissional = re.sub("\'", '', self.enderecoProfissional)
				self.enderecoProfissional = re.sub("\"", '', self.enderecoProfissional)
				self.salvarEnderecoProfissional = 0
				self.achouEnderecoProfissional = 0
			
			if (self.salvarParte1 and not self.salvarParte2) or (self.salvarParte2 and not self.salvarParte1) :
				if len(stripBlanks(self.item))>0:
					self.partesDoItem.append(stripBlanks(self.item)) # acrescentamos cada celula da linha numa lista!
					self.item = ''

				if self.salvarParte2:
					self.salvarParte1 = 0
					self.salvarParte2 = 0

					if self.achouFormacaoAcademica:
						iessimaFormacaoAcademica = FormacaoAcademica(self.partesDoItem) # criamos um objeto com a lista correspondentes às celulas da linha
						self.listaFormacaoAcademica.append(iessimaFormacaoAcademica) # acrescentamos o objeto de FormacaoAcademica

					#if self.achouAtuacaoProfissional:
					#	print self.partesDoItem

					if self.achouProjetoDePesquisa:
						if not self.salvarParte3:
							self.salvarParte3 = 1
						else:
							self.salvarParte3 = 0
							if len(self.partesDoItem)>=3:
								iessimoProjetoDePesquisa = ProjetoDePesquisa(self.idMembro, self.partesDoItem) # criamos um objeto com a lista correspondentes às celulas da linha
								self.listaProjetoDePesquisa.append(iessimoProjetoDePesquisa) # acrescentamos o objeto de ProjetoDePesquisa

					#if self.achouMembroDeCorpoEditorial:
					#	print self.partesDoItem

					#if self.achouRevisorDePeriodico:
					#	print self.partesDoItem
					
					if self.achouAreaDeAtuacao:
						iessimaAreaDeAtucao = AreaDeAtuacao(self.partesDoItem) # criamos um objeto com a lista correspondentes às celulas da linha
						self.listaAreaDeAtuacao.append(iessimaAreaDeAtucao) # acrescentamos o objeto de AreaDeAtuacao
					
					if self.achouIdioma:
						iessimoIdioma = Idioma(self.partesDoItem) # criamos um objeto com a lista correspondentes às celulas da linha
						self.listaIdioma.append(iessimoIdioma) # acrescentamos o objeto de Idioma

					if self.achouPremioOuTitulo:
						iessimoPremio = PremioOuTitulo(self.idMembro, self.partesDoItem) # criamos um objeto com a lista correspondentes às celulas da linha
						self.listaPremioOuTitulo.append(iessimoPremio) # acrescentamos o objeto de PremioOuTitulo

					if self.achouProducoes:
						if self.achouProducaoEmCTA:
							if self.achouArtigoEmPeriodico:
 	 							iessimoItem = ArtigoEmPeriodico(self.idMembro, self.partesDoItem, self.doi, self.relevante)
								self.listaArtigoEmPeriodico.append(iessimoItem)
								self.doi = ''
								self.relevante = 0
    
							if self.achouLivroPublicado:
	 	 						iessimoItem = LivroPublicado(self.idMembro, self.partesDoItem, self.relevante)
								self.listaLivroPublicado.append(iessimoItem)
								self.relevante = 0
    
							if self.achouCapituloDeLivroPublicado:
		 						iessimoItem = CapituloDeLivroPublicado(self.idMembro, self.partesDoItem, self.relevante)
								self.listaCapituloDeLivroPublicado.append(iessimoItem)
								self.relevante = 0
					
							if self.achouTextoEmJornalDeNoticia:
 		 						iessimoItem = TextoEmJornalDeNoticia(self.idMembro, self.partesDoItem, self.relevante)
								self.listaTextoEmJornalDeNoticia.append(iessimoItem)
								self.relevante = 0
					
							if self.achouTrabalhoCompletoEmCongresso:
 	 							iessimoItem = TrabalhoCompletoEmCongresso(self.idMembro, self.partesDoItem, self.doi, self.relevante)
								self.listaTrabalhoCompletoEmCongresso.append(iessimoItem)
								self.doi = ''
								self.relevante = 0
						
							if self.achouResumoExpandidoEmCongresso:
 	 							iessimoItem = ResumoExpandidoEmCongresso(self.idMembro, self.partesDoItem, self.doi, self.relevante)
								self.listaResumoExpandidoEmCongresso.append(iessimoItem)
								self.doi = ''
								self.relevante = 0
					
							if self.achouResumoEmCongresso:
 		 						iessimoItem = ResumoEmCongresso(self.idMembro, self.partesDoItem, self.doi, self.relevante)
								self.listaResumoEmCongresso.append(iessimoItem)
								self.doi = ''
								self.relevante = 0
    
							if self.achouArtigoAceito:
 		 						iessimoItem =  ArtigoAceito(self.idMembro, self.partesDoItem, self.doi, self.relevante)
								self.listaArtigoAceito.append(iessimoItem)
								self.doi = ''
								self.relevante = 0
					
							if self.achouApresentacaoDeTrabalho:
 		 						iessimoItem =  ApresentacaoDeTrabalho(self.idMembro, self.partesDoItem, self.relevante)
								self.listaApresentacaoDeTrabalho.append(iessimoItem)
    
							if self.achouOutroTipoDeProducaoBibliografica:
 		 						iessimoItem = OutroTipoDeProducaoBibliografica(self.idMembro, self.partesDoItem, self.relevante)
								self.listaOutroTipoDeProducaoBibliografica.append(iessimoItem)


						if self.achouProducaoTecnica:
							if self.achouSoftwareComPatente:
 	 							iessimoItem = SoftwareComPatente(self.idMembro, self.partesDoItem, self.relevante)
								self.listaSoftwareComPatente.append(iessimoItem)
    
							if self.achouSoftwareSemPatente:
 	 							iessimoItem = SoftwareSemPatente(self.idMembro, self.partesDoItem, self.relevante)
								self.listaSoftwareSemPatente.append(iessimoItem)
						
							if self.achouProdutoTecnologico:
 	 							iessimoItem = ProdutoTecnologico(self.idMembro, self.partesDoItem, self.relevante)
								self.listaProdutoTecnologico.append(iessimoItem)
    
							if self.achouProcessoOuTecnica:
 	 							iessimoItem = ProcessoOuTecnica(self.idMembro, self.partesDoItem, self.relevante)
								self.listaProcessoOuTecnica.append(iessimoItem)
    
							if self.achouTrabalhoTecnico:
 	 							iessimoItem = TrabalhoTecnico(self.idMembro, self.partesDoItem, self.relevante)
								self.listaTrabalhoTecnico.append(iessimoItem)
    
							if self.achouOutroTipoDeProducaoTecnica:
 	 							iessimoItem = OutroTipoDeProducaoTecnica(self.idMembro, self.partesDoItem, self.relevante)
								self.listaOutroTipoDeProducaoTecnica.append(iessimoItem)

						if self.achouProducaoArtisticaCultural:
							if self.achouOutraProducaoArtisticaCultural:
 								iessimoItem = ProducaoArtistica(self.idMembro, self.partesDoItem, self.relevante)
								self.listaProducaoArtistica.append(iessimoItem)

					#if self.achouBancas:

					if self.achouEventos:
						if self.achouParticipacaoEmEvento:
							self.listaParticipacaoEmEvento.append(ParticipacaoEmEvento(self.idMembro, self.partesDoItem))

						if self.achouOrganizacaoDeEvento:
							self.listaOrganizacaoDeEvento.append(OrganizacaoDeEvento(self.idMembro, self.partesDoItem))


					if self.achouOrientacoes:
						if self.achouOrientacoesEmAndamento:
							if self.achouSupervisaoDePosDoutorado:
								self.listaOASupervisaoDePosDoutorado.append( OrientacaoEmAndamento(self.idMembro, self.partesDoItem, self.idOrientando) )
								self.idOrientando = ''
							if self.achouTeseDeDoutorado:
								self.listaOATeseDeDoutorado.append( OrientacaoEmAndamento(self.idMembro, self.partesDoItem, self.idOrientando) )
								self.idOrientando = ''
							if self.achouDissertacaoDeMestrado:
								self.listaOADissertacaoDeMestrado.append( OrientacaoEmAndamento(self.idMembro, self.partesDoItem, self.idOrientando) )
								self.idOrientando = ''
							if self.achouMonografiaDeEspecializacao:
								self.listaOAMonografiaDeEspecializacao.append( OrientacaoEmAndamento(self.idMembro, self.partesDoItem, self.idOrientando) )
								self.idOrientando = ''
							if self.achouTCC:
								self.listaOATCC.append( OrientacaoEmAndamento(self.idMembro, self.partesDoItem, self.idOrientando) )
								self.idOrientando = ''
							if self.achouIniciacaoCientifica:
								self.listaOAIniciacaoCientifica.append( OrientacaoEmAndamento(self.idMembro, self.partesDoItem, self.idOrientando) )
								self.idOrientando = ''
							if self.achouOutroTipoDeOrientacao:
								self.listaOAOutroTipoDeOrientacao.append( OrientacaoEmAndamento(self.idMembro, self.partesDoItem, self.idOrientando) )
								self.idOrientando = ''

						if self.achouOrientacoesConcluidas :
							if self.achouSupervisaoDePosDoutorado:
								self.listaOCSupervisaoDePosDoutorado.append( OrientacaoConcluida(self.idMembro, self.partesDoItem, self.idOrientando, 'Pós Doutorado') )
								self.idOrientando = ''
							if self.achouTeseDeDoutorado:
								self.listaOCTeseDeDoutorado.append( OrientacaoConcluida(self.idMembro, self.partesDoItem, self.idOrientando, 'Doutorado') )
								self.idOrientando = ''
							if self.achouDissertacaoDeMestrado:
								self.listaOCDissertacaoDeMestrado.append( OrientacaoConcluida(self.idMembro, self.partesDoItem, self.idOrientando, 'Mestrado') )
								self.idOrientando = ''
							if self.achouMonografiaDeEspecializacao:
								self.listaOCMonografiaDeEspecializacao.append( OrientacaoConcluida(self.idMembro, self.partesDoItem, self.idOrientando, 'Especialização') )
								self.idOrientando = ''
							if self.achouTCC:
								self.listaOCTCC.append( OrientacaoConcluida(self.idMembro, self.partesDoItem, self.idOrientando, 'Graduação') )
								self.idOrientando = ''
							if self.achouIniciacaoCientifica:
								self.listaOCIniciacaoCientifica.append( OrientacaoConcluida(self.idMembro, self.partesDoItem, self.idOrientando, 'Iniciação Científica') )
								self.idOrientando = ''
							if self.achouOutroTipoDeOrientacao:
								self.listaOCOutroTipoDeOrientacao.append( OrientacaoConcluida(self.idMembro, self.partesDoItem, self.idOrientando, 'Outras') )
								self.idOrientando = ''


		if tag=='span':
			if self.spanInformacaoArtigo:
				self.spanInformacaoArtigo = 0


	# ------------------------------------------------------------------------ #
	def handle_data(self, dado):
		if not self.spanInformacaoArtigo:
			self.item = self.item + htmlentitydecode(dado)

		dado = stripBlanks(dado)
			
		if self.salvarAtualizacaoCV:
			data = re.findall(u'Última atualização do currículo em (\d{2}/\d{2}/\d{4})', dado)
			if len(data)>0: # se a data de atualizacao do CV for identificada
				self.atualizacaoCV = stripBlanks(data[0])
				self.salvarAtualizacaoCV = 0

		if self.procurarCabecalho:
			if u'Identificação'==dado:
				self.achouIdentificacao = 1
			if u'Endereço'==dado:
				self.achouEndereco = 1
			if u'Formação acadêmica/titulação'==dado:
				self.achouFormacaoAcademica = 1
			if u'Atuação Profissional'==dado:
				self.achouAtuacaoProfissional = 1
			if u'Projetos de pesquisa'==dado:
				self.achouProjetoDePesquisa = 1
			if u'Membro de corpo editorial'==dado:
				self.achouMembroDeCorpoEditorial = 1
			if u'Revisor de periódico'==dado:
				self.achouRevisorDePeriodico = 1
			if u'Áreas de atuação'==dado:
				self.achouAreaDeAtuacao = 1
			if u'Idiomas'==dado:
				self.achouIdioma = 1
			if u'Prêmios e títulos'==dado:
				self.achouPremioOuTitulo = 1
			if u'Produções'==dado:  # !---
				self.achouProducoes = 1
				#self.achouProducaoEmCTA = 1
			#if u'Produção técnica'==dado:
			#	self.achouProducaoTecnica = 1
			#if u'Produção artística/cultural'==dado:
			#	self.achouProducaoArtisticaCultural = 1
			if u'Bancas'==dado:
				self.achouBancas = 1
			if u'Eventos'==dado:
				self.achouEventos = 1
			if u'Orientações'==dado:
				self.achouOrientacoes = 1
			if u'Outras informações relevantes'==dado:
				self.achouOutrasInformacoesRelevantes = 1
			self.umaUnidade = 0
			
		if self.achouIdentificacao:
			if u'Nome em citações bibliográficas'==dado:
				self.achouNomeEmCitacoes = 1
			if u'Sexo'==dado:
				self.achouSexo = 1

		if self.achouEndereco:
			if u'Endereço Profissional'==dado:
				self.achouEnderecoProfissional = 1

		if self.achouProducoes:
			if u'Produção bibliográfica'==dado:
				self.achouProducaoEmCTA = 1
				self.achouProducaoTecnica = 0
				self.achouProducaoArtisticaCultural= 0
			if u'Produção técnica'==dado:
				self.achouProducaoEmCTA = 0
				self.achouProducaoTecnica = 1
				self.achouProducaoArtisticaCultural= 0
			if u'Produção artística/cultural'==dado:
				self.achouProducaoEmCTA = 0
				self.achouProducaoTecnica = 0
				self.achouProducaoArtisticaCultural= 1
			
			if u'Demais trabalhos'==dado:
				self.salvarItem = 0
				self.achouProducaoEmCTA = 0
				self.achouProducaoTecnica = 0
				self.achouProducaoArtisticaCultural= 0


			if self.achouProducaoEmCTA:
				if u'Artigos completos publicados em periódicos'==dado:
					self.salvarItem = 1
					self.achouArtigoEmPeriodico = 1
					self.achouLivroPublicado = 0
					self.achouCapituloDeLivroPublicado = 0
					self.achouTextoEmJornalDeNoticia = 0
					self.achouTrabalhoCompletoEmCongresso = 0
					self.achouResumoExpandidoEmCongresso = 0
					self.achouResumoEmCongresso = 0
					self.achouArtigoAceito = 0
					self.achouApresentacaoDeTrabalho = 0
					self.achouOutroTipoDeProducaoBibliografica = 0
				if u'Livros publicados/organizados ou edições'==dado:
					self.salvarItem = 1
					self.achouArtigoEmPeriodico = 0
					self.achouLivroPublicado = 1
					self.achouCapituloDeLivroPublicado = 0
					self.achouTextoEmJornalDeNoticia = 0
					self.achouTrabalhoCompletoEmCongresso = 0
					self.achouResumoExpandidoEmCongresso = 0
					self.achouResumoEmCongresso = 0
					self.achouArtigoAceito = 0
					self.achouApresentacaoDeTrabalho = 0
					self.achouOutroTipoDeProducaoBibliografica = 0
				if u'Capítulos de livros publicados'==dado:
					self.salvarItem = 1
					self.achouArtigoEmPeriodico = 0
					self.achouLivroPublicado = 0
					self.achouCapituloDeLivroPublicado = 1
					self.achouTextoEmJornalDeNoticia = 0
					self.achouTrabalhoCompletoEmCongresso = 0
					self.achouResumoExpandidoEmCongresso = 0
					self.achouResumoEmCongresso = 0
					self.achouArtigoAceito = 0
					self.achouApresentacaoDeTrabalho = 0
					self.achouOutroTipoDeProducaoBibliografica = 0
				if u'Textos em jornais de notícias/revistas'==dado:
					self.salvarItem = 1
					self.achouArtigoEmPeriodico = 0
					self.achouLivroPublicado = 0
					self.achouCapituloDeLivroPublicado = 0
					self.achouTextoEmJornalDeNoticia = 1
					self.achouTrabalhoCompletoEmCongresso = 0
					self.achouResumoExpandidoEmCongresso = 0
					self.achouResumoEmCongresso = 0
					self.achouArtigoAceito = 0
					self.achouApresentacaoDeTrabalho = 0
					self.achouOutroTipoDeProducaoBibliografica = 0
				if u'Trabalhos completos publicados em anais de congressos'==dado:
					self.salvarItem = 1
					self.achouArtigoEmPeriodico = 0
					self.achouLivroPublicado = 0
					self.achouCapituloDeLivroPublicado = 0
					self.achouTextoEmJornalDeNoticia = 0
					self.achouTrabalhoCompletoEmCongresso = 1
					self.achouResumoExpandidoEmCongresso = 0
					self.achouResumoEmCongresso = 0
					self.achouArtigoAceito = 0
					self.achouApresentacaoDeTrabalho = 0
					self.achouOutroTipoDeProducaoBibliografica = 0
				if u'Resumos expandidos publicados em anais de congressos'==dado:
					self.salvarItem = 1
					self.achouArtigoEmPeriodico = 0
					self.achouLivroPublicado = 0
					self.achouCapituloDeLivroPublicado = 0
					self.achouTextoEmJornalDeNoticia = 0
					self.achouTrabalhoCompletoEmCongresso = 0
					self.achouResumoExpandidoEmCongresso = 1
					self.achouResumoEmCongresso = 0
					self.achouArtigoAceito = 0
					self.achouApresentacaoDeTrabalho = 0
					self.achouOutroTipoDeProducaoBibliografica = 0
				if u'Resumos publicados em anais de congressos' in dado:
					self.salvarItem = 1
					self.achouArtigoEmPeriodico = 0
					self.achouLivroPublicado = 0
					self.achouCapituloDeLivroPublicado = 0
					self.achouTextoEmJornalDeNoticia = 0
					self.achouTrabalhoCompletoEmCongresso = 0
					self.achouResumoExpandidoEmCongresso = 0
					self.achouResumoEmCongresso = 1
					self.achouArtigoAceito = 0
					self.achouApresentacaoDeTrabalho = 0
					self.achouOutroTipoDeProducaoBibliografica = 0
				if u'Artigos aceitos para publicação'==dado:
					self.salvarItem = 1
					self.achouArtigoEmPeriodico = 0
					self.achouLivroPublicado = 0
					self.achouCapituloDeLivroPublicado = 0
					self.achouTextoEmJornalDeNoticia = 0
					self.achouTrabalhoCompletoEmCongresso = 0
					self.achouResumoExpandidoEmCongresso = 0
					self.achouResumoEmCongresso = 0
					self.achouArtigoAceito = 1
					self.achouApresentacaoDeTrabalho = 0
					self.achouOutroTipoDeProducaoBibliografica = 0
				if u'Apresentações de Trabalho'==dado:
					self.salvarItem = 1
					self.achouArtigoEmPeriodico = 0
					self.achouLivroPublicado = 0
					self.achouCapituloDeLivroPublicado = 0
					self.achouTextoEmJornalDeNoticia = 0
					self.achouTrabalhoCompletoEmCongresso = 0
					self.achouResumoExpandidoEmCongresso = 0
					self.achouResumoEmCongresso = 0
					self.achouArtigoAceito = 0
					self.achouApresentacaoDeTrabalho = 1
					self.achouOutroTipoDeProducaoBibliografica = 0
				if u'Outras produções bibliográficas'==dado:
				#if u'Demais tipos de produção bibliográfica'==dado:
					self.salvarItem = 1
					self.achouArtigoEmPeriodico = 0
					self.achouLivroPublicado = 0
					self.achouCapituloDeLivroPublicado = 0
					self.achouTextoEmJornalDeNoticia = 0
					self.achouTrabalhoCompletoEmCongresso = 0
					self.achouResumoExpandidoEmCongresso = 0
					self.achouResumoEmCongresso = 0
					self.achouArtigoAceito = 0
					self.achouApresentacaoDeTrabalho = 0
					self.achouOutroTipoDeProducaoBibliografica = 1

			if self.achouProducaoTecnica:
				#if u'Softwares com registro de patente'==dado:
				if u'Programas de computador com registro de patente'==dado:
					self.salvarItem = 1
					self.achouSoftwareComPatente = 1
					self.achouSoftwareSemPatente = 0
					self.achouProdutoTecnologico = 0
					self.achouProcessoOuTecnica = 0
					self.achouTrabalhoTecnico = 0
					self.achouOutroTipoDeProducaoTecnica = 0
				if u'Programas de computador sem registro de patente'==dado:
					self.salvarItem = 1
					self.achouSoftwareComPatente = 0
					self.achouSoftwareSemPatente = 1
					self.achouProdutoTecnologico = 0
					self.achouProcessoOuTecnica = 0
					self.achouTrabalhoTecnico = 0
					self.achouOutroTipoDeProducaoTecnica = 0
				if u'Produtos tecnológicos'==dado:
					self.salvarItem = 1
					self.achouSoftwareComPatente = 0
					self.achouSoftwareSemPatente = 0
					self.achouProdutoTecnologico = 1
					self.achouProcessoOuTecnica = 0
					self.achouTrabalhoTecnico = 0
					self.achouOutroTipoDeProducaoTecnica = 0
				if u'Processos ou técnicas'==dado:
					self.salvarItem = 1
					self.achouSoftwareComPatente = 0
					self.achouSoftwareSemPatente = 0
					self.achouProdutoTecnologico = 0
					self.achouProcessoOuTecnica = 1
					self.achouTrabalhoTecnico = 0
					self.achouOutroTipoDeProducaoTecnica = 0
				if u'Trabalhos técnicos'==dado:
					self.salvarItem = 1
					self.achouSoftwareComPatente = 0
					self.achouSoftwareSemPatente = 0
					self.achouProdutoTecnologico = 0
					self.achouProcessoOuTecnica = 0
					self.achouTrabalhoTecnico = 1
					self.achouOutroTipoDeProducaoTecnica = 0
				if u'Demais tipos de produção técnica'==dado:
					self.salvarItem = 1
					self.achouSoftwareComPatente = 0
					self.achouSoftwareSemPatente = 0
					self.achouProdutoTecnologico = 0
					self.achouProcessoOuTecnica = 0
					self.achouTrabalhoTecnico = 0
					self.achouOutroTipoDeProducaoTecnica = 1
				#if u'Demais trabalhos'==dado:
				#	self.salvarItem = 0
				#	self.achouSoftwareComPatente = 0
				#	self.achouSoftwareSemPatente = 0
				#	self.achouProdutoTecnologico = 0
				#	self.achouProcessoOuTecnica = 0
				#	self.achouTrabalhoTecnico = 0
				#	self.achouOutroTipoDeProducaoTecnica = 0
    
			if self.achouProducaoArtisticaCultural:
				#if u'Produção artística/cultural'==dado:
				if u'Outras produções artísticas/culturais'==dado or u'Artes Cênicas'==dado or u'Música'==dado:
					# separar as listas de producoes artisticas por tipos 
					self.salvarItem = 1
					self.achouOutraProducaoArtisticaCultural = 1
			
		if self.achouBancas:
			if u'Participação em bancas de trabalhos de conclusão'==dado:
				self.salvarItem = 0

		if self.achouEventos:
			if u'Participação em eventos, congressos, exposições e feiras'==dado:
				self.salvarItem = 1
				self.achouParticipacaoEmEvento  = 1
				self.achouOrganizacaoDeEvento = 0
			if u'Organização de eventos, congressos, exposições e feiras'==dado:
				self.salvarItem = 1
				self.achouParticipacaoEmEvento  = 0
				self.achouOrganizacaoDeEvento = 1

		if self.achouOrientacoes:
			if u'Orientações e supervisões em andamento'==dado:
				self.achouOrientacoesEmAndamento  = 1
				self.achouOrientacoesConcluidas = 0
			if u'Orientações e supervisões concluídas'==dado:
				self.achouOrientacoesEmAndamento  = 0
				self.achouOrientacoesConcluidas = 1

			# Tipos de orientações (em andamento ou concluídas)
			if u'Supervisão de pós-doutorado'==dado:
				self.salvarItem = 1
				self.achouSupervisaoDePosDoutorado = 1
				self.achouTeseDeDoutorado = 0
				self.achouDissertacaoDeMestrado = 0
				self.achouMonografiaDeEspecializacao = 0
				self.achouTCC = 0
				self.achouIniciacaoCientifica = 0
				self.achouOutroTipoDeOrientacao = 0
			if u'Tese de doutorado'==dado:
				self.salvarItem = 1
				self.achouSupervisaoDePosDoutorado = 0
				self.achouTeseDeDoutorado = 1
				self.achouDissertacaoDeMestrado = 0
				self.achouMonografiaDeEspecializacao = 0
				self.achouTCC = 0
				self.achouIniciacaoCientifica = 0
				self.achouOutroTipoDeOrientacao = 0
			if u'Dissertação de mestrado'==dado:
				self.salvarItem = 1
				self.achouSupervisaoDePosDoutorado = 0
				self.achouTeseDeDoutorado = 0
				self.achouDissertacaoDeMestrado = 1
				self.achouMonografiaDeEspecializacao = 0
				self.achouTCC = 0
				self.achouIniciacaoCientifica = 0
				self.achouOutroTipoDeOrientacao = 0
			if u'Monografia de conclusão de curso de aperfeiçoamento/especialização'==dado:
				self.salvarItem = 1
				self.achouSupervisaoDePosDoutorado = 0
				self.achouTeseDeDoutorado = 0
				self.achouDissertacaoDeMestrado = 0
				self.achouMonografiaDeEspecializacao = 1
				self.achouTCC = 0
				self.achouIniciacaoCientifica = 0
				self.achouOutroTipoDeOrientacao = 0
			if u'Trabalho de conclusão de curso de graduação'==dado:
				self.salvarItem = 1
				self.achouSupervisaoDePosDoutorado = 0
				self.achouTeseDeDoutorado = 0
				self.achouDissertacaoDeMestrado = 0
				self.achouMonografiaDeEspecializacao = 0
				self.achouTCC = 1
				self.achouIniciacaoCientifica = 0
				self.achouOutroTipoDeOrientacao = 0
			if u'Iniciação científica' in dado or u'Iniciação Científica'==dado:
				self.salvarItem = 1
				self.achouSupervisaoDePosDoutorado = 0
				self.achouTeseDeDoutorado = 0
				self.achouDissertacaoDeMestrado = 0
				self.achouMonografiaDeEspecializacao = 0
				self.achouTCC = 0
				self.achouIniciacaoCientifica = 1
				self.achouOutroTipoDeOrientacao = 0
			if u'Orientações de outra natureza'==dado:
				self.salvarItem = 1
				self.achouSupervisaoDePosDoutorado = 0
				self.achouTeseDeDoutorado = 0
				self.achouDissertacaoDeMestrado = 0
				self.achouMonografiaDeEspecializacao = 0
				self.achouTCC = 0
				self.achouIniciacaoCientifica = 0
				self.achouOutroTipoDeOrientacao = 1


		if self.achouOutrasInformacoesRelevantes:
			self.salvarItem = 0


# ---------------------------------------------------------------------------- #
def stripBlanks(s):
	return re.sub('\s+', ' ', s).strip()

def htmlentitydecode(s):                                                                               
	return re.sub('&(%s);' % '|'.join(name2codepoint),                                                 
		lambda m: unichr(name2codepoint[m.group(1)]), s)   

