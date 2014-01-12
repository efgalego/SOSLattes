#!/usr/bin/python
# encoding: utf-8
# filename: geradorOntologia.py
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

import sys
import datetime
import re
import math
import rdflib
import uuid
from rdflib import Namespace, BNode, Literal, URIRef, Graph
from rdflib.namespace import XSD

onto = Namespace("http://www.ime.usp.br/ontolattes#")
owl = Namespace("http://www.w3.org/2002/07/owl#")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
semant = Namespace("http://www.semanticlattes.com.br/curriculo#")

class GeradorOntologia:
	grupo = None
	dir = None
	version = None
	extensao = None
	nomeGrupo = None
	
	grafo = None
		
	def __init__(self, grupo):
		self.grupo = grupo		
		self.dir = self.grupo.obterParametro('global-diretorio_de_saida')
		
		self.extensao = self.grupo.obterParametro('ontologia-extensao_arquivo')
		if (self.extensao == None):
			self.extensao = 'owl'
		
		self.nomeGrupo = self.grupo.obterParametro('global-nome_do_grupo').decode("utf8")
		
		self.grafo = Graph()		
		#file_name = sys.path[0]+'/resources/ont_lattes_base.owl'
		#result = self.grafo.parse(file_name, format="xml")
		
		self.gerarMembros()
		self.gerarProducoesBibliograficas()

		if self.grupo.obterParametro('relatorio-mostrar_orientacoes'):
			self.gerarOrientacoes()

		self.salvarOntologia()

	def salvarOntologia(self):
		file = open(self.dir+'/'+self.nomeGrupo+'.'+self.extensao, 'w')
		file.write(self.grafo.serialize())
		file.close()	

	def gerarMembros(self):			
		elemento = 0
		for membro in self.grupo.listaDeMembros:
			elemento += 1

			for area in membro.listaAreaDeAtuacao:
				print "Area de atuacao " + area.descricao
			
			nomeTag = 'cv-'+membro.nomeCompleto.replace(' ', '-').lower()
			curriculo = URIRef("http://www.ime.usp.br/ontolattes#" + nomeTag)			

			dadosGerais = self.uriCVMembro(membro, "dg")
			
			self.grafo.add(( curriculo, rdf['type'], URIRef(onto['CurriculoVitae']) ))
			self.grafo.add(( dadosGerais, rdf['type'], URIRef(onto['DadosGerais']) ))
			self.grafo.add(( curriculo , onto['temDadosGerais'], dadosGerais ))			

			self.grafo.add(( dadosGerais, onto['nomeCompleto'], Literal(membro.nomeCompleto) ))			
			self.grafo.add(( dadosGerais, onto['nomeEmCitacoesBibliograficas'], Literal(membro.nomeEmCitacoesBibliograficas) ))
			self.grafo.add(( dadosGerais, onto['sexo'], Literal(membro.sexo) ))	
			self.grafo.add(( dadosGerais, onto['nomeDoArquivoDeFoto'], Literal(membro.foto) ))
			self.grafo.add(( dadosGerais, onto['idLattes'], Literal(membro.idLattes) ))	

			curriculoSemant = URIRef("http://www.semanticlattes.com.br/curriculo#_" + nomeTag)
			self.grafo.add(( curriculoSemant, rdf['type'], URIRef(semant['Pessoa']) ))
			self.grafo.add(( curriculo, onto['estaRelacionadoCom'], curriculoSemant ))
		

			# Montar Endereço Profissional:
			membro.obterCoordenadasDeGeolocalizacao()
			endProfissional = self.uriCVMembro(membro, "ende_prof")
			self.grafo.add(( endProfissional, rdf['type'], URIRef("http://www.ime.usp.br/ontolattes#EnderecoProfissional") ))
			self.grafo.add(( dadosGerais , onto['temEndereco'], endProfissional ))

			self.grafo.add(( endProfissional, onto['logradouro'], Literal(membro.enderecoProfissional) ))
			self.grafo.add(( endProfissional, onto['cep'], Literal(membro.enderecoProfissionalCep) ))	
			self.grafo.add(( endProfissional, onto['uf'], Literal(membro.enderecoProfissionalUf) ))
			self.grafo.add(( endProfissional, onto['cidade'], Literal(membro.enderecoProfissionalCidade) ))
			self.grafo.add(( endProfissional, onto['pais'], Literal(membro.enderecoProfissionalPais) ))
			self.grafo.add(( endProfissional, onto['latitude'], Literal(membro.enderecoProfissionalLat) ))
			self.grafo.add(( endProfissional, onto['longitude'], Literal(membro.enderecoProfissionalLon) ))


			# Montar Formação Acadêmica
			lista = list(membro.listaFormacaoAcademica)
			for i in lista:
				print i.descricao
				if (len(re.findall(u'Livre-docência', i.tipo)) > 0):
					self.adicionarFormacaoAcademica(membro, dadosGerais, 'LivreDocencia', i)	
				elif (len(re.findall(u'Pós-Doutorado', i.tipo)) > 0):
					self.adicionarFormacaoAcademica(membro, dadosGerais, 'PosDoutorado', i)
				elif (len(re.findall(u'Doutorado', i.tipo)) > 0):
					self.adicionarFormacaoAcademica(membro, dadosGerais, 'Doutorado', i)
				elif (len(re.findall(u'Mestrado', i.tipo)) > 0):
					self.adicionarFormacaoAcademica(membro, dadosGerais, 'Mestrado', i)
				elif (len(re.findall(u'Graduação', i.tipo)) > 0):
					self.adicionarFormacaoAcademica(membro, dadosGerais, 'Graduacao', i)
				# Faltou terminar os outros...


	def gerarProducoesBibliograficas(self):
		if self.grupo.obterParametro('relatorio-incluir_artigo_em_periodico'):
			self.incluirListaABaseDeConhecimento(self.grupo.compilador.listaCompletaArtigoEmPeriodico, "ProducaoBibliografica", "ArtigoPublicado")
		if self.grupo.obterParametro('relatorio-incluir_artigo_aceito_para_publicacao'):
			self.incluirListaABaseDeConhecimento(self.grupo.compilador.listaCompletaArtigoAceito, "ProducaoBibliografica", "ArtigoAceito")
		if self.grupo.obterParametro('relatorio-incluir_livro_publicado'):
			self.incluirListaABaseDeConhecimento(self.grupo.compilador.listaCompletaLivroPublicado, "ProducaoBibliografica", "LivroPublicado")
		if self.grupo.obterParametro('relatorio-incluir_capitulo_de_livro_publicado'):
			self.incluirListaABaseDeConhecimento(self.grupo.compilador.listaCompletaCapituloDeLivroPublicado, "ProducaoBibliografica", "LivroCapituloPublicado")
		if self.grupo.obterParametro('relatorio-incluir_texto_em_jornal_de_noticia'):
			self.incluirListaABaseDeConhecimento(self.grupo.compilador.listaCompletaTextoEmJornalDeNoticia, "ProducaoBibliografica", "TextoJornalRevistaPublicado")
		if self.grupo.obterParametro('relatorio-incluir_trabalho_completo_em_congresso'):
			self.incluirListaABaseDeConhecimento(self.grupo.compilador.listaCompletaTrabalhoCompletoEmCongresso, "ProducaoBibliografica", "TrabalhoCongressoCompleto")
		if self.grupo.obterParametro('relatorio-incluir_resumo_expandido_em_congresso'):
			self.incluirListaABaseDeConhecimento(self.grupo.compilador.listaCompletaResumoExpandidoEmCongresso, "ProducaoBibliografica", "TrabalhoCongressoResumoExpandido")
		if self.grupo.obterParametro('relatorio-incluir_resumo_em_congresso'):
			self.incluirListaABaseDeConhecimento(self.grupo.compilador.listaCompletaResumoEmCongresso, "ProducaoBibliografica", "TrabalhoCongressoResumo")
		if self.grupo.obterParametro('relatorio-incluir_apresentacao_de_trabalho'):
			self.incluirListaABaseDeConhecimento(self.grupo.compilador.listaCompletaApresentacaoDeTrabalho, "ProducaoBibliografica", "TrabalhoApresentacao")
		if self.grupo.obterParametro('relatorio-incluir_outro_tipo_de_producao_bibliografica'):
			self.incluirListaABaseDeConhecimento(self.grupo.compilador.listaCompletaOutroTipoDeProducaoBibliografica, "ProducaoBibliografica", "Outros")

	def gerarOrientacoes(self):
		if self.grupo.obterParametro('relatorio-incluir_orientacao_em_andamento_pos_doutorado'):
			self.incluirListaABaseDeConhecimento(self.grupo.compilador.listaCompletaOASupervisaoDePosDoutorado, "OrientacaoEmAndamento", "PosDoutorado")
		if self.grupo.obterParametro('relatorio-incluir_orientacao_em_andamento_doutorado'):
			self.incluirListaABaseDeConhecimento(self.grupo.compilador.listaCompletaOATeseDeDoutorado, "OrientacaoEmAndamento", "Doutorado")
		if self.grupo.obterParametro('relatorio-incluir_orientacao_em_andamento_mestrado'):
			self.incluirListaABaseDeConhecimento(self.grupo.compilador.listaCompletaOADissertacaoDeMestrado, "OrientacaoEmAndamento", "Mestrado") 
		if self.grupo.obterParametro('relatorio-incluir_orientacao_em_andamento_monografia_de_especializacao'):
			self.incluirListaABaseDeConhecimento(self.grupo.compilador.listaCompletaOAMonografiaDeEspecializacao, "OrientacaoEmAndamento", "AperfeicoamentoEspecializacao")
		if self.grupo.obterParametro('relatorio-incluir_orientacao_em_andamento_tcc'):
			self.incluirListaABaseDeConhecimento(self.grupo.compilador.listaCompletaOATCC, "OrientacaoEmAndamento", "Graduacao")
		if self.grupo.obterParametro('relatorio-incluir_orientacao_em_andamento_iniciacao_cientifica'):
			self.incluirListaABaseDeConhecimento(self.grupo.compilador.listaCompletaOAIniciacaoCientifica, "OrientacaoEmAndamento", "IniciacaoCientifica")
		if self.grupo.obterParametro('relatorio-incluir_orientacao_em_andamento_outro_tipo'):
			self.incluirListaABaseDeConhecimento(self.grupo.compilador.listaCompletaOAOutroTipoDeOrientacao, "OrientacaoEmAndamento", "Outras")

		if self.grupo.obterParametro('relatorio-incluir_orientacao_concluida_pos_doutorado'):
			self.incluirListaABaseDeConhecimento(self.grupo.compilador.listaCompletaOCSupervisaoDePosDoutorado, "OrientacaoConcluida", "PosDoutorado")
		if self.grupo.obterParametro('relatorio-incluir_orientacao_concluida_doutorado'):
			self.incluirListaABaseDeConhecimento(self.grupo.compilador.listaCompletaOCTeseDeDoutorado, "OrientacaoConcluida", "Doutorado")			
		if self.grupo.obterParametro('relatorio-incluir_orientacao_concluida_mestrado'):
			self.incluirListaABaseDeConhecimento(self.grupo.compilador.listaCompletaOCDissertacaoDeMestrado, "OrientacaoConcluida", "Mestrado")
		if self.grupo.obterParametro('relatorio-incluir_orientacao_concluida_monografia_de_especializacao'):
			self.incluirListaABaseDeConhecimento(self.grupo.compilador.listaCompletaOCMonografiaDeEspecializacao, "OrientacaoConcluida", "AperfeicoamentoEspecializacao")
		if self.grupo.obterParametro('relatorio-incluir_orientacao_concluida_tcc'):
			self.incluirListaABaseDeConhecimento(self.grupo.compilador.listaCompletaOCTCC, "OrientacaoConcluida", "Graduacao")
		if self.grupo.obterParametro('relatorio-incluir_orientacao_concluida_iniciacao_cientifica'):
			self.incluirListaABaseDeConhecimento(self.grupo.compilador.listaCompletaOCIniciacaoCientifica, "OrientacaoConcluida", "IniciacaoCientifica")
		if self.grupo.obterParametro('relatorio-incluir_orientacao_concluida_outro_tipo'):
			self.incluirListaABaseDeConhecimento(self.grupo.compilador.listaCompletaOCOutroTipoDeOrientacao, "OrientacaoConcluida", "Outras")

	
	def incluirListaABaseDeConhecimento(self, listaCompleta, tema, tipo):
		keys = listaCompleta.keys()
		keys.sort(reverse=True) 
		if len(keys) > 0:
			for ano in keys:
				elementos = listaCompleta[ano]
				for index in range(0, len(elementos)):
					item = elementos[index]
					if tema == 'OrientacaoEmAndamento':
						self.adicionarOrientacaoEmAndamento(item, tipo, ano, index)
					elif tema == 'OrientacaoConcluida':
						self.adicionarOrientacaoConcluida(item, tipo, ano, index)
					elif tema == 'ProducaoBibliografica':
						self.adicionarProducaoBibliografica(item, tipo, ano, index)
						

	def adicionarOrientacaoEmAndamento(self, item, tipo, ano, index):
		uriOrientacao = URIRef("http://www.ime.usp.br/ontolattes#OrientacaoEmAndamentoDe"+ tipo) 
		uriDadosBasicos = URIRef("http://www.ime.usp.br/ontolattes#DadosBasicosDaOrientacaoEmAndamentoDe"+ tipo)
		uriDetalhamento = URIRef("http://www.ime.usp.br/ontolattes#DetalhamentoDaOrientacaoEmAndamentoDe" + tipo)
		
		newUUID = uuid.uuid4()

		oam = URIRef("http://www.ime.usp.br/ontolattes#oam-"+ str(newUUID))
		self.grafo.add(( oam, rdf['type'], uriOrientacao ))					
	
		dbo = URIRef("http://www.ime.usp.br/ontolattes#dbo-"+ str(newUUID))
		self.grafo.add(( dbo, rdf['type'], uriDadosBasicos ))
		self.grafo.add(( oam , onto['temDadosBasicosDeOrientacoes'], dbo ))			

		self.addSeHouverValor(dbo, onto['ano'], item.ano, 'int')
		self.grafo.add(( dbo , onto['tituloDoTrabalho'], Literal(item.tituloDoTrabalho) ))					
		#self.grafo.add(( dbo , onto['natureza'], Literal() ))
		#self.grafo.add(( dbo , onto['homePage'], Literal() ))
		#self.grafo.add(( dbo , onto['pais'], dbo ))									
		#self.grafo.add(( dbo , onto['doi'], dbo ))
		#self.grafo.add(( dbo , onto['idioma'], dbo ))

		detalhes = URIRef("http://www.ime.usp.br/ontolattes#dba-detalhes-"+ str(newUUID))
		self.grafo.add(( detalhes, rdf['type'], uriDetalhamento ))
		self.grafo.add(( oam , onto['temDetalhamento'], detalhes ))			
		self.grafo.add(( detalhes , onto['tipoDeOrientacao'], Literal(item.tipoDeOrientacao) ))		
		self.grafo.add(( detalhes , onto['nomeDoOrientado'], Literal(item.nome) ))		
		self.addSeHouverValor(detalhes, onto['numeroIdOrientado'], item.idOrientando, 'string')
		#self.grafo.add(( detalhes , onto['flagBolsa'], Literal(True if item.bolsa == 1 else False) ))		

		instituicao = self.uriAuxiliar('InstituicaoEmpresa', 'nomeInstituicaoEmpresa', 'inst', item.instituicao)
		if instituicao:		
			self.grafo.add(( detalhes , onto['realizadoNaInstituicao'], instituicao ))								

		agencia = self.uriAuxiliar('AgenciaFinanciadora', 'nomeAgencia', 'agencia', item.agenciaDeFomento)
		if agencia:
			self.grafo.add(( detalhes , onto['financiadoPelaAgencia'], agencia ))		

		lista = list(item.idMembro)
		for i in lista:
			curriculo = self.uriCVMembro(self.grupo.listaDeMembros[i], "cv")
			self.grafo.add(( curriculo, onto['temDadosComplementares'], oam ))

		##### Inclusão das Instâncias no Semantic Lattes: #####
		if tipo == 'Mestrado':
			uri = URIRef("http://www.semanticlattes.com.br/curriculo#_orientacao_mestrado_" + str(newUUID))
			classeOrientacao = URIRef(semant['OrientacaoMestrado'])
			classeTrabalho = URIRef(semant['DissertacaoMestrado'])
		elif tipo == 'Doutorado':
			uri = URIRef("http://www.semanticlattes.com.br/curriculo#_orientacao_doutorado_" + str(newUUID))
			classeOrientacao = URIRef(semant['OrientacaoDoutorado'])
			classeTrabalho = URIRef(semant['TeseDoutorado'])
		elif tipo == 'PosDoutorado':
			uri = URIRef("http://www.semanticlattes.com.br/curriculo#_orientacao_posdoutorado_" + str(newUUID))
			classeOrientacao = URIRef(semant['OrientacaoPosDoutorado'])
			classeTrabalho = URIRef(semant['Trabalho'])
		else:
			uri = URIRef("http://www.semanticlattes.com.br/curriculo#_orientacao_" + str(newUUID))
			classeOrientacao = URIRef(semant['Orientacao'])
			classeTrabalho = URIRef(semant['Trabalho'])			

		if uri:
			self.grafo.add(( uri, rdf['type'], classeOrientacao ))
			self.grafo.add(( oam, onto['estaRelacionadoCom'], uri ))						
			
			uriEstudante = URIRef("http://www.semanticlattes.com.br/curriculo#_estudante_" + str(newUUID))
			self.grafo.add(( uriEstudante, rdf['type'], URIRef(semant['Estudante']) ))
			self.grafo.add(( uri, semant['temOrientado'], uriEstudante ))						

			uriTrabalho = URIRef("http://www.semanticlattes.com.br/curriculo#_trabalho_" + str(newUUID))
			self.grafo.add(( uriTrabalho, rdf['type'], classeTrabalho ))
			self.grafo.add(( uri, semant['temTrabalho'], uriTrabalho ))


	def adicionarOrientacaoConcluida(self, item, tipo, ano, index):
		uriOutraProducao = URIRef("http://www.ime.usp.br/ontolattes#OrientacoesConcluidasPara"+ tipo) 		
		uriDadosBasicos = URIRef("http://www.ime.usp.br/ontolattes#DadosBasicosDeOrientacoesConcluidasPara"+ tipo)
		uriDetalhamento = URIRef("http://www.ime.usp.br/ontolattes#DetalhamentoDeOrientacoesConcluidasPara" + tipo)

		newUUID = uuid.uuid4()

		op = URIRef("http://www.ime.usp.br/ontolattes#op-"+ str(newUUID))
		self.grafo.add(( op, rdf['type'], uriOutraProducao ))					
	
		dboc = URIRef("http://www.ime.usp.br/ontolattes#dboc-"+ str(newUUID))
		self.grafo.add(( dboc, rdf['type'], uriDadosBasicos ))
		self.grafo.add(( op , onto['temDadosBasicosDeOrientacoes'], dboc ))			
		self.addSeHouverValor(dboc, onto['ano'], item.ano, 'int')
		
		self.grafo.add(( dboc , onto['tituloDoTrabalho'], Literal(item.tituloDoTrabalho) ))					
		#self.grafo.add(( dboc , onto['flagRelevancia'], Literal(True if item.relevante == 1 else False) ))					
		#self.grafo.add(( dboc , onto['natureza'], Literal() ))
		#self.grafo.add(( dboc , onto['homePage'], Literal() ))
		#self.grafo.add(( dboc , onto['pais'], dbo ))									
		#self.grafo.add(( dboc , onto['doi'], dbo ))
		#self.grafo.add(( dboc , onto['idioma'], dbo ))

		detalhes = URIRef("http://www.ime.usp.br/ontolattes#dboc-detalhes-"+ str(newUUID))
		self.grafo.add(( detalhes, rdf['type'], uriDetalhamento ))
		self.grafo.add(( op , onto['temDetalhamento'], detalhes ))			
		self.grafo.add(( detalhes , onto['tipoDeOrientacao'], Literal(item.tipoDeOrientacao) ))		
		self.grafo.add(( detalhes , onto['nomeDoOrientado'], Literal(item.nome) ))				
		self.addSeHouverValor(detalhes, onto['numeroIdOrientado'], item.idOrientando, 'string')
		#self.grafo.add(( detalhes , onto['flagBolsa'], Literal(True if item.bolsa == 1 else False) ))		
		#self.grafo.add(( detalhes , onto['numeroDePaginas'], Literal() ))		

		instituicao = self.uriAuxiliar('InstituicaoEmpresa', 'nomeInstituicaoEmpresa', 'inst', item.instituicao)
		if instituicao:		
			self.grafo.add(( detalhes , onto['realizadoNaInstituicao'], instituicao ))								

		agencia = self.uriAuxiliar('AgenciaFinanciadora', 'nomeAgencia', 'agencia', item.agenciaDeFomento)
		if agencia:
			self.grafo.add(( detalhes , onto['financiadoPelaAgencia'], agencia ))		

		lista = list(item.idMembro)
		for i in lista:
			curriculo = self.uriCVMembro(self.grupo.listaDeMembros[i], "cv")
			self.grafo.add(( curriculo, onto['temOutraProducao'], op ))

		##### Inclusão das Instâncias no Semantic Lattes: #####
		if tipo == 'Mestrado':
			uri = URIRef("http://www.semanticlattes.com.br/curriculo#_orientacao_mestrado_" + str(newUUID))
			classeOrientacao = URIRef(semant['OrientacaoMestrado'])
			classeTrabalho = URIRef(semant['DissertacaoMestrado'])
		elif tipo == 'Doutorado':
			uri = URIRef("http://www.semanticlattes.com.br/curriculo#_orientacao_doutorado_" + str(newUUID))
			classeOrientacao = URIRef(semant['OrientacaoDoutorado'])
			classeTrabalho = URIRef(semant['TeseDoutorado'])
		elif tipo == 'PosDoutorado':
			uri = URIRef("http://www.semanticlattes.com.br/curriculo#_orientacao_posdoutorado_" + str(newUUID))
			classeOrientacao = URIRef(semant['OrientacaoPosDoutorado'])
			classeTrabalho = URIRef(semant['Trabalho'])
		else:
			uri = URIRef("http://www.semanticlattes.com.br/curriculo#_orientacao_" + str(newUUID))
			classeOrientacao = URIRef(semant['Orientacao'])
			classeTrabalho = URIRef(semant['Trabalho'])			

		if uri:
			self.grafo.add(( uri, rdf['type'], classeOrientacao ))
			self.grafo.add(( op, onto['estaRelacionadoCom'], uri ))						
			
			uriEstudante = URIRef("http://www.semanticlattes.com.br/curriculo#_estudante_" + str(newUUID))
			self.grafo.add(( uriEstudante, rdf['type'], URIRef(semant['Estudante']) ))
			self.grafo.add(( uri, semant['temOrientado'], uriEstudante ))						

			uriTrabalho = URIRef("http://www.semanticlattes.com.br/curriculo#_trabalho_" + str(newUUID))
			self.grafo.add(( uriTrabalho, rdf['type'], classeTrabalho ))
			self.grafo.add(( uri, semant['temTrabalho'], uriTrabalho ))


	def adicionarArtigoPublicado(self, item):
		prefixo = "artpub"

		newUUID = str(uuid.uuid4())
		pb = URIRef("http://www.ime.usp.br/ontolattes#"+ prefixo +"-"+ newUUID)
		self.grafo.add(( pb, rdf['type'], URIRef("http://www.ime.usp.br/ontolattes#ArtigosPublicados") ))
		#self.grafo.add(( pb , onto['sequenciaProducao'], item. ))

		periodico = URIRef("http://www.semanticlattes.com.br/curriculo#_periodico_" + newUUID)
		self.grafo.add(( periodico, rdf['type'], URIRef(semant['Periodico']) ))

		edicao = URIRef("http://www.semanticlattes.com.br/curriculo#_edicaoperiodico_" + newUUID)
		self.grafo.add(( edicao, rdf['type'], URIRef(semant['EdicaoPeriodico']) ))
		self.grafo.add(( edicao, semant['ehEdicaoDoPeriodico'], periodico ))

		artigo = URIRef("http://www.semanticlattes.com.br/curriculo#_artigoperiodico_" + newUUID)
		self.grafo.add(( artigo, rdf['type'], URIRef(semant['ArtigoPeriodico']) ))
		self.grafo.add(( pb, onto['estaRelacionadoCom'], artigo ))
		self.grafo.add(( artigo, semant['ehPublicadoEmEdicaoPeriodico'], edicao ))

		dbpb = URIRef("http://www.ime.usp.br/ontolattes#db-"+ prefixo +"-"+ newUUID)
		self.grafo.add(( dbpb, rdf['type'], URIRef("http://www.ime.usp.br/ontolattes#DadosBasicos") ))
		self.grafo.add(( pb , onto['temDadosBasicos'], dbpb ))			
		self.addSeHouverValor(dbpb, onto['ano'], item.ano, 'int')
		self.grafo.add(( dbpb , onto['titulo'], Literal(item.titulo) ))		
		self.grafo.add(( dbpb , onto['temRelevancia'], Literal(True if item.relevante == 1 else False) ))
		#self.grafo.add(( dboc , onto['natureza'], Literal() ))
		#self.grafo.add(( dboc , onto['homePage'], Literal() ))
		#self.grafo.add(( dboc , onto['temIdioma'], Literal() ))

		detalhes = URIRef("http://www.ime.usp.br/ontolattes#db-"+ prefixo +"-detalhes-"+ newUUID)
		self.grafo.add(( detalhes, rdf['type'], URIRef("http://www.ime.usp.br/ontolattes#DetalhamentoDoArtigo") ))
		self.grafo.add(( pb , onto['temDetalhamentoDoArtigo'], detalhes ))		
		#self.grafo.add(( detalhes , onto['realizadoNaInstituicao'], Literal(item.instituicao) ))
		#self.grafo.add(( detalhes , onto['financiadoPelaAgencia'], Literal(item.agenciaDeFomento) ))
		#self.grafo.add(( detalhes , onto['flagBolsa'], Literal(True if item.bolsa == 1 else False) ))

		#self.addSeHouverValor(dbpb, onto['tipoDeLivro'], item.?, 'string')
		self.grafo.add(( detalhes , onto['fasciculo'], Literal(item.numero) ))
		self.addPaginas(detalhes, onto['paginaInicial'], onto['paginaFinal'], item.paginas)
		self.grafo.add(( detalhes , onto['tituloDoLivro'], Literal(item.titulo) ))
		self.grafo.add(( detalhes , onto['tituloDoPeriodicoOuRevista'], Literal(item.revista) ))			
		self.grafo.add(( detalhes , onto['volume'], Literal(item.volume) ))		

		lista = list(item.idMembro)
		for i in lista:
			curriculo = self.uriCVMembro(self.grupo.listaDeMembros[i], "cv")
			self.grafo.add(( curriculo, onto['temProducaoBibliografica'], pb ))


	def adicionarProducaoBibliografica(self, item, tipo, ano, index):		
		if tipo == 'ArtigoPublicado': 
			return self.adicionarArtigoPublicado(item)

		uriSemantic = None		
		if tipo.startswith('Artigo'):
			uriDetalhamento = URIRef("http://www.ime.usp.br/ontolattes#DetalhamentoDoArtigo")
			uriDadosBasicos = URIRef("http://www.ime.usp.br/ontolattes#DadosBasicos")
			uriPropDetalhe = onto['temDetalhamentoDoArtigo']
			if tipo == 'ArtigoPublicado':
				uriTipo = URIRef("http://www.ime.usp.br/ontolattes#ArtigosPublicados")
				prefixo = "artpub"
				uriSemantic = URIRef(semant['ArtigoPeriodico'])							
			elif tipo == 'ArtigoAceito':
				uriTipo = URIRef("http://www.ime.usp.br/ontolattes#ArtigosAceitosParaPublicacao")
				prefixo = "artact"
		elif tipo.startswith('Livro'):
			uriDadosBasicos = URIRef('http://www.ime.usp.br/ontolattes#DadosBasicosDoLivro')
			uriSemantic = URIRef(semant['Livro'])
			if tipo == 'LivroPublicado':
				uriPropDetalhe = onto['temDetalhamentoDoLivro']
				uriTipo = URIRef("http://www.ime.usp.br/ontolattes#LivrosPublicadosOuOrganizados")				
				prefixo = "lvrpub"
				uriDetalhamento = URIRef("http://www.ime.usp.br/ontolattes#DetalhamentoDoLivro")
			elif tipo == 'LivroCapituloPublicado':
				uriPropDetalhe = onto['temDetalhamentoDoCapitulo']
				uriTipo = URIRef("http://www.ime.usp.br/ontolattes#CapitulosDeLivrosPublicados")				
				prefixo = 'cappub'
				uriDetalhamento = URIRef('http://www.ime.usp.br/ontolattes#DetalhamentoDoCapitulo')
		elif tipo == 'TextoJornalRevistaPublicado':
			uriTipo = URIRef('http://www.ime.usp.br/ontolattes#TextosEmJornaisOuRevistas')
			uriDetalhamento = URIRef('http://www.ime.usp.br/ontolattes#DetalhamentoDoTexto')
			uriDadosBasicos = URIRef('http://www.ime.usp.br/ontolattes#DadosBasicos')
			prefixo = 'txtjrn'
			uriPropDetalhe = onto['temDetalhamentoDoTexto']
		elif tipo.startswith('Trabalho'):
			uriTipo = URIRef('http://www.ime.usp.br/ontolattes#TrabalhosEmEventos')			
			uriDetalhamento = URIRef('http://www.ime.usp.br/ontolattes#DetalhamentoDoTrabalho')
			uriDadosBasicos = URIRef('http://www.ime.usp.br/ontolattes#DadosBasicos')
			uriPropDetalhe = onto['temDetalhamentoDoTrabalho']
			if tipo == 'TrabalhoCongressoCompleto':
				prefixo = 'tblgcompl'
			elif tipo == 'TrabalhoCongressoResumoExpandido':
				prefixo = 'tblgresex'
			elif tipo == 'TrabalhoCongressoResumo':
				prefixo = 'tblgresum'
			elif tipo == 'TrabalhoApresentacao':
				prefixo = 'tblapres'
			uriSemantic = URIRef(semant['Conferencia'])
		elif tipo == 'Outros':
			uriTipo = URIRef('http://www.ime.usp.br/ontolattes#OutraProducaoBibliografica')
			prefixo = 'otr'
			uriDetalhamento = URIRef('http://www.ime.usp.br/ontolattes#DetalhamentoDeOutraProducao')
			uriDadosBasicos = URIRef('http://www.ime.usp.br/ontolattes#DadosBasicos')
			uriPropDetalhe = onto['temDetalhamentoDeOutraProducao']
			
		newUUID = str(uuid.uuid4())
		pb = URIRef("http://www.ime.usp.br/ontolattes#"+ prefixo +"-"+ newUUID)
		self.grafo.add(( pb, rdf['type'], uriTipo ))
		#self.grafo.add(( pb , onto['sequenciaProducao'], item. ))

		if (uriSemantic is not None):			
			pbSmtc = URIRef("http://www.semanticlattes.com.br/curriculo#_" + newUUID)
			self.grafo.add(( pbSmtc, rdf['type'], uriSemantic ))
			self.grafo.add(( pb, onto['estaRelacionadoCom'], pbSmtc ))

		dbpb = URIRef("http://www.ime.usp.br/ontolattes#db-"+ prefixo +"-"+ newUUID)
		self.grafo.add(( dbpb, rdf['type'], uriDadosBasicos ))
		self.grafo.add(( pb , onto['temDadosBasicos'], dbpb ))			
		self.addSeHouverValor(dbpb, onto['ano'], item.ano, 'int')
		self.grafo.add(( dbpb , onto['titulo'], Literal(item.titulo) ))		
		self.grafo.add(( dbpb , onto['temRelevancia'], Literal(True if item.relevante == 1 else False) ))		
		#self.grafo.add(( dboc , onto['natureza'], Literal() ))
		#self.grafo.add(( dboc , onto['homePage'], Literal() ))
		#self.grafo.add(( dboc , onto['temIdioma'], Literal() ))
		for autor in item.autores.split(";"):
			self.grafo.add(( dbpb , onto['autor'], Literal(autor) ))

		detalhes = URIRef("http://www.ime.usp.br/ontolattes#db-"+ prefixo +"-detalhes-"+ newUUID)
		self.grafo.add(( detalhes, rdf['type'], uriDetalhamento ))
		self.grafo.add(( pb , uriPropDetalhe, detalhes ))		
		#self.grafo.add(( detalhes , onto['realizadoNaInstituicao'], Literal(item.instituicao) ))
		#self.grafo.add(( detalhes , onto['financiadoPelaAgencia'], Literal(item.agenciaDeFomento) ))
		#self.grafo.add(( detalhes , onto['flagBolsa'], Literal(True if item.bolsa == 1 else False) ))
		if tipo.startswith("Artigo"):
			#self.addSeHouverValor(dbpb, onto['tipoDeLivro'], item.?, 'string')
			self.grafo.add(( detalhes , onto['fasciculo'], Literal(item.numero) ))
			self.addPaginas(detalhes, onto['paginaInicial'], onto['paginaFinal'], item.paginas)
			self.grafo.add(( detalhes , onto['tituloDoLivro'], Literal(item.titulo) ))
			self.grafo.add(( detalhes , onto['tituloDoPeriodicoOuRevista'], Literal(item.revista) ))			
			self.grafo.add(( detalhes , onto['volume'], Literal(item.volume) ))		
		elif tipo.startswith("Livro"):
			if tipo == 'LivroPublicado':
				self.addSeHouverValor(detalhes, onto['numeroDaEdicaoRevisao'], item.edicao, 'int' )
				self.addSeHouverValor(detalhes, onto['numeroDePaginas'], item.paginas, 'string' )
				self.addSeHouverValor(detalhes, onto['numeroDeVolumes'], item.volume, 'int' )
			elif tipo == 'LivroCapituloPublicado':
				self.addSeHouverValor(detalhes, onto['nomeDaEditora'] , item.editora, 'string' )
				self.addSeHouverValor(detalhes, onto['numeroDaEdicaoRevisao'], item.edicao, 'int' )
				self.addSeHouverValor(detalhes, onto['numeroDeVolumes'], item.volume, 'int' )
				self.addPaginas(detalhes, onto['paginaInicial'], onto['paginaFinal'], item.paginas)
				self.addSeHouverValor(detalhes, onto['tituloDoLivro'], item.livro, 'string' )
				#self.grafo.add(( detalhes , onto['cidadeDaEditora'], Literal(item.numero) ))
				#self.grafo.add(( detalhes , onto['isbn'], Literal(item.numero) ))
				#self.grafo.add(( detalhes , onto['numeroDaSerie'], Literal(item.numero) ))
				#self.addSeHouverValor(detalhes, onto['organizadores'], item.?, 'string' )
		elif tipo == 'TextoJornalRevistaPublicado':
			self.addSeHouverValor(detalhes, onto['dataDePublicacao'], item.data, 'string' )
			self.addSeHouverValor(detalhes, onto['tituloDoJornalOuRevista'], item.nomeJornal, 'string' )
			self.addPaginas(detalhes, onto['paginaInicial'], onto['paginaFinal'], item.paginas)
			self.addSeHouverValor(detalhes, onto['volume'], item.volume, 'string' )
			#self.addSeHouverValor(detalhes, onto['issn'], item.livro, 'string' )
			#self.addSeHouverValor(detalhes, onto['localDePublicacao'], item.livro, 'string
		elif tipo.startswith('Trabalho'):
			self.grafo.add((detalhes , onto['ano'], Literal(item.ano) ))
			if tipo == 'TrabalhoCongressoCompleto' or tipo == 'TrabalhoCongressoResumoExpandido' or tipo == 'TrabalhoCongressoResumo':
				self.addSeHouverValor(detalhes, onto['nomeDoEvento'], item.volume, 'string' )
				self.addSeHouverValor(detalhes, onto['volume'], item.volume, 'string' )
			#self.addSeHouverValor(detalhes, onto['cidadeDaEditora'], item.volume, 'string' )
			#self.addSeHouverValor(detalhes, onto['cidadeDoEvento'], item.volume, 'string' )
			#self.addSeHouverValor(detalhes, onto['classificacaoDoEvento'], item.volume, 'string' )
			#self.addSeHouverValor(detalhes, onto['fasciculo'], item.volume, 'string' )
			#self.addSeHouverValor(detalhes, onto['isbn'], item.volume, 'string' )
			#self.addSeHouverValor(detalhes, onto['nomeDaEditora'], item.volume, 'string' )
			#self.addSeHouverValor(detalhes, onto['serie'], item.volume, 'string' )
			#self.addSeHouverValor(detalhes, onto['tituloDosAnaisOuPreceedings'], item.volume, 'string' )
		#elif tipo == 'Outros':
			#self.addSeHouverValor(detalhes, onto['cidadeDaEditora'], item.volume, 'string' )
			#self.addSeHouverValor(detalhes, onto['issn-isbn'], item.volume, 'string' )
			#self.addSeHouverValor(detalhes, onto['nomeDaEditora'], item.volume, 'string' )
			#self.addSeHouverValor(detalhes, onto['numeroDePaginas'], item.volume, 'string' )			
		
		# Será necessário que a ontologia seja capaz de reconhecer os autores da publicação 
		# e se há relação com algum dos membros.
		lista = list(item.idMembro)
		for i in lista:
			curriculo = self.uriCVMembro(self.grupo.listaDeMembros[i], "cv")
			self.grafo.add(( curriculo, onto['temProducaoBibliografica'], pb ))




	def adicionarFormacaoAcademica(self, membro, dadosGerais, tipo, item):
		formacao = self.uriCVMembro(membro, "form-acad"+ str(uuid.uuid4()))
		self.grafo.add(( formacao, rdf['type'], URIRef("http://www.ime.usp.br/ontolattes#" + tipo) ))
		self.grafo.add(( dadosGerais, onto['temFormacaoAcademicaTitulacao'], formacao ))
		self.addSeHouverValor(formacao, onto['anoDeInicio'], item.anoInicio, 'int')
		self.addSeHouverValor(formacao, onto['anoDeConclusao'], item.anoConclusao, 'int')
		self.grafo.add(( formacao, onto['nivel'], Literal(item.tipo) ))	
		if (item.nomeOrientador != ''):				
			self.grafo.add(( formacao, onto['nomeDoOrientador'], Literal(item.nomeOrientador) ))	
		if (tipo == 'Graduacao'):
			self.grafo.add(( formacao, onto['tituloDoTrabalhoDeConclusaoDeCurso'], Literal(item.tituloTrabalho) ))
		elif (tipo == 'Mestrado' or tipo == 'Doutorado'):
			self.addSeHouverValor(formacao, onto['anoDeObtencaoDoTitulo'], item.anoObtencao, 'int')
			self.addSeHouverValor(formacao, onto['tituloDaDissertacaoTese'], item.tituloTrabalho, 'string')
		elif (tipo == 'PosDoutorado'):
			self.addSeHouverValor(formacao, onto['anoDeObtencaoDoTitulo'], item.anoObtencao, 'int')
		elif (tipo == 'LivreDocencia'):
			self.addSeHouverValor(formacao, onto['tituloDoTrabalho'], item.tituloTrabalho, 'string')

		instituicao = self.uriAuxiliar('InstituicaoEmpresa', 'nomeInstituicaoEmpresa', 'inst', item.nomeInstituicao)
		if instituicao:		
			self.grafo.add(( formacao, onto['realizadoNaInstituicao'], instituicao ))

		agencia = self.uriAuxiliar('AgenciaFinanciadora', 'nomeAgencia', 'agencia', item.financiadoPelaAgencia)
		if agencia:
			self.grafo.add(( formacao , onto['financiadoPelaAgencia'], agencia ))

		
	def uriCVMembro(self, membro, prefixo):
		nomeTag = membro.nomeCompleto.replace(' ', '-').lower()
		membroOnto = URIRef("http://www.ime.usp.br/ontolattes#" + prefixo +"-"+ nomeTag)
		return membroOnto

	def uriAuxiliar(self, classe, propriedade, prefixo, nome):
		if len(nome) > 0:
			tag = nome.replace(' ', '-').lower()
			individuo = URIRef("http://www.ime.usp.br/ontolattes#"+ prefixo +"-"+ tag)

			if not (individuo, None, None) in self.grafo:	
				self.grafo.add(( individuo, rdf['type'], URIRef("http://www.ime.usp.br/ontolattes#"+ classe) ))
				self.grafo.add(( individuo, onto[propriedade], Literal(nome) ))

			return individuo


	def addSeHouverValor(self, sujeito, propriedade, valor, tipo):
		if valor :
			if tipo == 'int':
				if isinstance(valor, (str,unicode)) and valor.strip().isdigit():
					self.grafo.add(( sujeito, propriedade, Literal(int(valor.strip())) ))
				elif isinstance(valor, int):
					self.grafo.add(( sujeito, propriedade, Literal(valor) ))
				else:
					print 'Nao foi possivel converter o valor '+ valor.encode('utf8','replace') +' para int. '+ sujeito.encode('utf8','replace') +' '+ propriedade.encode('utf8','replace') +' '+ str(type(valor))
			elif tipo == 'GYear':
				if isinstance(valor, (str,unicode)) and valor.strip().isdigit():
					self.grafo.add(( sujeito, propriedade, Literal(int(valor), datatype=XSD.gYear) )) 
				else:
					print 'Nao foi possivel converter o valor '+ valor.encode('utf8','replace') +' para gYear. '+ sujeito.encode('utf8','replace') +' '+ propriedade.encode('utf8','replace') +' '+ str(type(valor))
			elif tipo == 'boolean':
				self.grafo.add(( sujeito, propriedade, Literal(True if valor == 1 or valor == '1' else False) ))
			elif len(valor) > 0:
				self.grafo.add(( sujeito, propriedade, Literal(valor) ))

	def addPaginas(self, sujeito, propPagInicial, propPagFinal, valor):
		partes = valor.rpartition("-")
		if partes[1]=='': # se nao existe numero
			paginaInicial = '1'		
			paginaFinal = valor
		else:
			paginaInicial = partes[0]
			paginaFinal = partes[1]
		if (paginaInicial.isdigit()):
			self.addSeHouverValor(sujeito, propPagInicial, paginaInicial, 'int')
		if (paginaFinal.isdigit()):
			self.addSeHouverValor(sujeito, propPagFinal, paginaFinal, 'int')



