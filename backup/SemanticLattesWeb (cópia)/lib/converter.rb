# -*- encoding : utf-8 -*-
# Este script gera as instâncias a partir de documentos XML de
# currículos Lattes
#
# Versão: 1.0
# Ano: 2009
#

require 'rubygems'
require 'pp'
gem 'libxml-ruby', '>= 1.1.3'
require 'xml'
require 'builder'
require 'yaml'
#require 'lib/lattes_ontology'
require File.expand_path('../lattes_ontology', __FILE__)

class Loader
  include LattesOntology

  def initialize
    @instituicoes =  YAML.load_file('storage/instituicoes.yaml')
    @departamentos =  YAML.load_file('storage/departamentos.yaml')
    @periodicos =  YAML.load_file('storage/periodicos.yaml')
    @edicoes_periodico =  YAML.load_file('storage/edicoes_periodico.yaml')
    @pessoas =  YAML.load_file('storage/pessoas.yaml')
    @artigos =  YAML.load_file('storage/artigos.yaml')
    @conferencias =  YAML.load_file('storage/conferencias.yaml')
    @edicao_conferencias =  YAML.load_file('storage/edicao_conferencias.yaml')
    @anais =  YAML.load_file('storage/anais.yaml')
    @livros =  YAML.load_file('storage/livros.yaml')
    @capitulos =  YAML.load_file('storage/capitulos.yaml')
    @orientacoes =  YAML.load_file('storage/orientacoes.yaml')
    @trabalhos =  YAML.load_file('storage/trabalhos.yaml')
  end
  
  # todos os dados já carregados/encontrados possuem uma chave de identificação
  # estas informações são persistidas utilizando YAML
  def sync
    File.open('storage/instituicoes.yaml', 'w') { |f| f.write(YAML.dump(@instituicoes)) }
    File.open('storage/departamentos.yaml', 'w') { |f| f.write(YAML.dump(@departamentos)) }
    File.open('storage/periodicos.yaml', 'w') { |f| f.write(YAML.dump(@periodicos)) }
    File.open('storage/edicoes_periodico.yaml', 'w') { |f| f.write(YAML.dump(@edicoes_periodico)) }
    File.open('storage/pessoas.yaml', 'w') { |f| f.write(YAML.dump(@pessoas)) }
    File.open('storage/artigos.yaml', 'w') { |f| f.write(YAML.dump(@artigos)) }
    File.open('storage/conferencias.yaml', 'w') { |f| f.write(YAML.dump(@conferencias)) }
    File.open('storage/edicao_conferencias.yaml', 'w') { |f| f.write(YAML.dump(@edicao_conferencias)) }
    File.open('storage/anais.yaml', 'w') { |f| f.write(YAML.dump(@anais)) }
    File.open('storage/livros.yaml', 'w') { |f| f.write(YAML.dump(@livros)) }
    File.open('storage/capitulos.yaml', 'w') { |f| f.write(YAML.dump(@capitulos)) }
    File.open('storage/orientacoes.yaml', 'w') { |f| f.write(YAML.dump(@orientacoes)) }
    File.open('storage/trabalhos.yaml', 'w') { |f| f.write(YAML.dump(@trabalhos)) }
  end
  
  def autores_trabalho(e, trabalho)
    autores = []
    trabalho.find('AUTORES').each do |autor|
      nome_completo = autor['NOME-COMPLETO-DO-AUTOR']
      @pessoas[nome_completo] = `uuidgen`.strip unless @pessoas.has_key?(nome_completo)

      e.Pessoa "rdf:about" => "##{@pessoas[nome_completo]}" do
      e.rdf :type, "rdf:resource" => "&owl;Thing"
        e.nome nome_completo
      end

      autores << @pessoas[nome_completo]
    end
    autores
  end

  def curriculo(content)
    xml = XML::Parser.string(content, :encoding => XML::Encoding::ISO_8859_1)
    doc = xml.parse
    curriculo = doc.find_first('/CURRICULO-VITAE')
    dados_gerais = curriculo.find_first('DADOS-GERAIS')
    producao_bibliografica = curriculo.find_first('PRODUCAO-BIBLIOGRAFICA')
    orientacoes_concluidas = curriculo.find_first('OUTRA-PRODUCAO/ORIENTACOES-CONCLUIDAS')
    orientacoes_andamento = curriculo.find_first('DADOS-COMPLEMENTARES/ORIENTACOES-EM-ANDAMENTO')

    # header of ontology instances
    output = ""
    output << OWL_HEADER

    e = Builder::XmlMarkup.new(:target => output, :indent => 2)
    def e._escape(text)
      return text if text =~ /^&(owl|xsd);/
      super(text)
    end

    autor_curriculo = doc.find_first('/CURRICULO-VITAE/DADOS-GERAIS')['NOME-COMPLETO']
    if !@pessoas.has_key?(autor_curriculo)
      @pessoas[autor_curriculo] = `uuidgen`.strip
    end

    detalhes = detalhes_profissionais(curriculo)
#    
#    ####################################
#    # DADOS DO CURRICULO
#    ####################################
#
    detalhes[:instituicao].each do |i|
      @instituicoes[i] = `uuidgen`.strip unless @instituicoes.has_key?(i)
      e.Instituicao "rdf:about" => "##{@instituicoes[i]}" do
        e.rdf :type, "rdf:resource" => "&owl;Thing"
        e.nome i
      end
    end 

    detalhes[:departamento].each do |d|
      @departamentos[d] = `uuidgen`.strip unless @departamentos.has_key?(d)
      e.Departamento "rdf:about" => "##{@departamentos[d]}" do
        e.rdf :type, "rdf:resource" => "&owl;Thing"
        e.nome d
      end
    end 

    e.Pessoa "rdf:about" => "##{@pessoas[autor_curriculo]}" do
      e.rdf :type, "rdf:resource" => "&owl;Thing"
      e.rdf :type, "rdf:resource" => "#Professor" if professor?(curriculo)
      e.nome dados_gerais['NOME-COMPLETO']
      e.nomeParaCitacao dados_gerais['NOME-EM-CITACOES-BIBLIOGRAFICAS']
      e.temTitulo "rdf:resource" => "#TituloGraduado" if graduado?(curriculo)
      e.temTitulo "rdf:resource" => "#TituloMestre" if mestre?(curriculo)
      e.temTitulo "rdf:resource" => "#TituloDoutor" if doutor?(curriculo)
      detalhes[:instituicao].each do |i|
        e.temVinculoCom "rdf:resource" => "##{@instituicoes[i]}"
      end
      detalhes[:departamento].each do |d|
        e.trabalhaNoDepartamento "rdf:resource" => "##{@departamentos[d]}"
      end
    end
#    
#    ####################################
#    # ARTIGOS PUBLICADOS EM PERIODICOS
#    ####################################
#
    if !producao_bibliografica.nil? and !producao_bibliografica.find('ARTIGOS-PUBLICADOS/ARTIGO-PUBLICADO').nil?
      producao_bibliografica.find('ARTIGOS-PUBLICADOS/ARTIGO-PUBLICADO').each do |artigo|
        detalhamento = artigo.find_first('DETALHAMENTO-DO-ARTIGO')
        titulo_periodico = detalhamento['TITULO-DO-PERIODICO-OU-REVISTA']
        volume = detalhamento['VOLUME']
        fasciculo = detalhamento['FASCICULO']
        serie = detalhamento['SERIE']
    
        # generates a unique identifier based on name
        @periodicos[titulo_periodico] = `uuidgen`.strip unless @periodicos.has_key?(titulo_periodico)
          
        e.Periodico "rdf:about" => "##{@periodicos[titulo_periodico]}" do
          e.rdf :type, "rdf:resource" => "&owl;Thing"
          e.titulo titulo_periodico
          e.ISSN detalhamento['ISSN'] unless detalhamento['ISSN'].empty?
        end
    
        edicao = [titulo_periodico, volume, fasciculo, serie]
        @edicoes_periodico[edicao] = `uuidgen`.strip unless @edicoes_periodico.has_key?(edicao)
    
        e.EdicaoPeriodico "rdf:about" => "##{@edicoes_periodico[edicao]}" do
        e.rdf :type, "rdf:resource" => "&owl;Thing"
          e.volume detalhamento['VOLUME'] unless detalhamento['VOLUME'].empty?
          e.fasciculo detalhamento['FASCICULO'] unless detalhamento['FASCICULO'].empty?
          e.serie detalhamento['SERIE'] unless detalhamento['SERIE'].empty?
          e.localDePublicacao detalhamento['LOCAL-DE-PUBLICACAO'] unless detalhamento['LOCAL-DE-PUBLICACAO'].empty?
          e.ehEdicaoDoPeriodico "rdf:resource" => "##{@periodicos[titulo_periodico]}"
        end
    
        autores = autores_trabalho(e, artigo)
    
        dados = artigo.find_first('DADOS-BASICOS-DO-ARTIGO')
        titulo_artigo = dados['TITULO-DO-ARTIGO']
    
        # generates a unique identifier based on name
        @artigos[titulo_artigo] = `uuidgen`.strip unless @artigos.has_key?(titulo_artigo)
    
        e.ArtigoPeriodico "rdf:about" => "##{@artigos[titulo_artigo]}" do
          e.rdf :type, "rdf:resource" => "&owl;Thing"
          e.titulo titulo_artigo
          e.natureza dados['NATUREZA'] unless dados['NATUREZA'].empty?
          e.ano dados['ANO-DO-ARTIGO'], "rdf:datatype" => "&xsd;gYear" unless dados['ANO-DO-ARTIGO'].empty?
          e.paisDePublicacao dados['PAIS-DE-PUBLICACAO'] unless dados['PAIS-DE-PUBLICACAO']
          e.idioma dados['IDIOMA'] unless dados['IDIOMA']
          e.meioDeDivulgacao dados['MEIO-DE-DIVULGACAO'] unless dados['MEIO-DE-DIVULGACAO']
          e.paginaInicial detalhamento['PAGINA-INICIAL'] unless detalhamento['PAGINA-INICIAL'].empty?
          e.paginaFinal detalhamento['PAGINA-FINAL'] unless detalhamento['PAGINA-FINAL'].empty?
          e.ehPublicadoEmEdicaoPeriodico "rdf:resource" => "##{@edicoes_periodico[edicao]}"
          autores.each do |autor_uri|
            e.temAutor "rdf:resource" => "##{autor_uri}"
          end
        end
      end
    end
#    
#    ####################################
#    # ARTIGOS PUBLICADOS EM CONFERENCIA
#    ####################################
#    
    if !producao_bibliografica.nil? and !producao_bibliografica.find('TRABALHOS-EM-EVENTOS/TRABALHO-EM-EVENTOS').nil?
      producao_bibliografica.find('TRABALHOS-EM-EVENTOS/TRABALHO-EM-EVENTOS').each do |trabalho|
        detalhamento = trabalho.find_first('DETALHAMENTO-DO-TRABALHO')
        classificacao = detalhamento['CLASSIFICACAO-DO-EVENTO']
        classificacao = "" if not classificacao =~ /(INTERNACIONAL|NACIONAL|REGIONAL|LOCAL)/
        nome_conferencia = detalhamento['NOME-DO-EVENTO'].gsub(/\s+/,' ')
        ano_realizacao = detalhamento['ANO-DE-REALIZACAO']

        conferencia = [nome_conferencia, classificacao]
        @conferencias[conferencia] = `uuidgen`.strip unless @conferencias.has_key?(conferencia)
        e.owl :Thing, "rdf:about" => "##{@conferencias[conferencia]}" do
          e.rdf :type, "rdf:resource" => "#Conferencia#{classificacao.capitalize}"
          e.nome nome_conferencia
        end

        # edicao da conferencia
        dados = trabalho.find_first('DADOS-BASICOS-DO-TRABALHO')

        edicao = [conferencia, ano_realizacao]
        @edicao_conferencias[edicao] = `uuidgen`.strip unless @edicao_conferencias.has_key?(nome_conferencia)
        e.EdicaoConferencia "rdf:about" => "##{@edicao_conferencias[edicao]}" do
          e.rdf :type, "rdf:resource" => "&owl;Thing"
          e.nome nome_conferencia
          e.ano ano_realizacao, "rdf:datatype" => "&xsd;gYear"
          e.pais dados['PAIS-DO-EVENTO'] unless dados['PAIS-DO-EVENTO'].empty?
          e.cidade detalhamento['CIDADE-DO-EVENTO'] unless detalhamento['CIDADE-DO-EVENTO'].empty?
          e.ehEdicaoDaConferencia "rdf:resource" => "##{@conferencias[conferencia]}"
        end
    
        titulo_anais = detalhamento['TITULO-DOS-ANAIS-OU-PROCEEDINGS']
        next if titulo_anais.empty?
    
        @anais[titulo_anais] = `uuidgen`.strip unless @anais.has_key?(titulo_anais)
        e.Anais "rdf:about" => "##{@anais[titulo_anais]}" do
          e.rdf :type, "rdf:resource" => "&owl;Thing"
          e.titulo titulo_anais
          e.ISBN detalhamento['ISBN'].gsub(/[^0-9xX]/, '') unless detalhamento['ISBN'].empty?
          e.editora detalhamento['NOME-DA-EDITORA'] unless detalhamento['NOME-DA-EDITORA'].empty?
          e.ehPublicadoEmEdicaoConferencia "rdf:resource" => "##{@edicao_conferencias[edicao]}"
        end
    
        autores = autores_trabalho(e, trabalho)
    
        titulo_artigo = dados['TITULO-DO-TRABALHO']
    
    
        @artigos[titulo_artigo] = `uuidgen`.strip unless @artigos.has_key?(titulo_artigo)
        e.ArtigoConferencia "rdf:about" => "##{@artigos[titulo_artigo]}" do
          e.rdf :type, "rdf:resource" => "&owl;Thing"
          e.titulo titulo_artigo
          e.tituloIngles dados['TITULO-DO-TRABALHO-INGLES'] unless dados['TITULO-DO-TRABALHO-INGLES'].empty?
          e.volume detalhamento['VOLUME'] unless detalhamento['VOLUME'].empty?
          e.fasciculo detalhamento['FASCICULO'] unless detalhamento['FASCICULO'].empty?
          e.serie detalhamento['SERIE'] unless detalhamento['SERIE'].empty?
          e.paginaInicial detalhamento['PAGINA-INICIAL'] unless detalhamento['PAGINA-INICIAL'].empty?
          e.paginaFinal detalhamento['PAGINA-FINAL'] unless detalhamento['PAGINA-FINAL'].empty?
          e.natureza dados['NATUREZA'] unless dados['NATUREZA'].empty?
          e.ano dados['ANO-DO-TRABALHO'], "rdf:datatype" => "&xsd;gYear" unless dados['ANO-DO-TRABALHO'].empty?
          e.idioma dados['IDIOMA'] unless dados['IDIOMA'].empty?
          e.meioDeDivulgacao dados['MEIO-DE-DIVULGACAO'] unless dados['MEIO-DE-DIVULGACAO'].empty?
          e.DOI dados['DOI'] unless dados['DOI'].empty?
          e.ehPublicadoEmAnais "rdf:resource" => "##{@anais[titulo_anais]}"
          autores.each do |autor_uri|
            e.temAutor "rdf:resource" => "##{autor_uri}"
          end
        end
      end
    end
#    
#    ####################################
#    # LIVROS E CAPITULOS
#    ####################################
#    
    if !producao_bibliografica.nil? and !producao_bibliografica.find('LIVROS-E-CAPITULOS/LIVROS-PUBLICADOS-OU-ORGANIZADOS/LIVRO-PUBLICADO-OU-ORGANIZADO').nil?
      producao_bibliografica.find('LIVROS-E-CAPITULOS/LIVROS-PUBLICADOS-OU-ORGANIZADOS/LIVRO-PUBLICADO-OU-ORGANIZADO').each do |livro|
        detalhamento = livro.find_first('DETALHAMENTO-DO-LIVRO')
        dados = livro.find_first('DADOS-BASICOS-DO-LIVRO')
        titulo_livro = dados['TITULO-DO-LIVRO']
    
        autores = autores_trabalho(e, livro)
    
        livro = [titulo_livro, detalhamento['ISBN'].gsub(/[^0-9xX]/, '')]
        @livros[livro] = `uuidgen`.strip unless @livros.has_key?(livro)
        e.Livro "rdf:about" => "##{@livros[livro]}" do
          e.rdf :type, "rdf:resource" => "&owl;Thing"
          e.titulo titulo_livro
          e.numeroDeVolumes detalhamento['NUMERO-DE-VOLUMES'], "rdf:datatype" => "&xsd;unsignedInt" unless detalhamento['NUMERO-DE-VOLUMES'].empty?
          e.numeroDePaginas detalhamento['NUMERO-DE-PAGINAS'], "rdf:datatype" => "&xsd;unsignedInt" unless detalhamento['NUMERO-DE-PAGINAS'].empty?
          e.ISBN detalhamento['ISBN'].gsub(/[^0-9xX]/, '') unless detalhamento['ISBN'].empty?
          e.editora detalhamento['NOME-DA-EDITORA'] unless detalhamento['NOME-DA-EDITORA'].empty?
          e.idioma dados['IDIOMA'] unless dados['IDIOMA'].empty?
          e.ano dados['ANO'], "rdf:datatype" => "&xsd;gYear" unless dados['ANO'].empty?
          e.paisDePublicacao dados['PAIS-DE-PUBLICACAO'] unless dados['PAIS-DE-PUBLICACAO'].empty?
          autores.each do |autor_uri|
            e.temAutor "rdf:resource" => "##{autor_uri}"
          end
        end
      end
    end
    
    if !producao_bibliografica.nil? and !producao_bibliografica.find('LIVROS-E-CAPITULOS/CAPITULOS-DE-LIVROS-PUBLICADOS/CAPITULO-DE-LIVRO-PUBLICADO').nil?
      producao_bibliografica.find('LIVROS-E-CAPITULOS/CAPITULOS-DE-LIVROS-PUBLICADOS/CAPITULO-DE-LIVRO-PUBLICADO').each do |capitulo|
        detalhamento = capitulo.find_first('DETALHAMENTO-DO-CAPITULO')
        dados = capitulo.find_first('DADOS-BASICOS-DO-CAPITULO')
    
        titulo_livro = detalhamento['TITULO-DO-LIVRO']
        titulo_capitulo = dados['TITULO-DO-CAPITULO-DO-LIVRO']
        
        organizadores = []
        detalhamento['ORGANIZADORES'].split(';').map { |o| o.strip }.each do |organizador|
            @pessoas[organizador] = `uuidgen`.strip unless @pessoas.has_key?(organizador)

            e.Pessoa "rdf:about" => "##{@pessoas[organizador]}" do
            e.rdf :type, "rdf:resource" => "&owl;Thing"
              e.nome organizador
            end

            organizadores << @pessoas[organizador]
        end
    
        livro = [titulo_livro, detalhamento['ISBN'].gsub(/[^0-9xX]/, '')]
        @livros[livro] = `uuidgen`.strip unless @livros.has_key?(livro)
        e.Livro "rdf:about" => "##{@livros[livro]}" do
          e.rdf :type, "rdf:resource" => "&owl;Thing"
          e.titulo titulo_livro
          e.ISBN detalhamento['ISBN'].gsub(/[^0-9xX]/, '') unless detalhamento['ISBN'].empty?
          e.editora detalhamento['NOME-DA-EDITORA'] unless detalhamento['NOME-DA-EDITORA'].empty?
          e.idioma dados['IDIOMA'] unless dados['IDIOMA'].empty?
          e.ano dados['ANO'], "rdf:datatype" => "&xsd;gYear" unless dados['ANO'].empty?
          e.paisDePublicacao dados['PAIS-DE-PUBLICACAO'] unless dados['PAIS-DE-PUBLICACAO'].empty?
          organizadores.each do |autor_uri|
            e.temAutor "rdf:resource" => "##{autor_uri}"
          end
        end
        
        autores = autores_trabalho(e, capitulo)
    
        @capitulos[titulo_capitulo] = `uuidgen`.strip unless @capitulos.has_key?(titulo_capitulo)
        e.Capitulo "rdf:about" => "##{@capitulos[titulo_capitulo]}" do
          e.rdf :type, "rdf:resource" => "&owl;Thing"
          e.titulo titulo_capitulo
          e.ano dados['ANO'], "rdf:datatype" => "&xsd;gYear" unless dados['ANO'].empty?
          e.idioma dados['IDIOMA'] unless dados['IDIOMA'].empty?
          e.paginaInicial detalhamento['PAGINA-INICIAL'] unless detalhamento['PAGINA-INICIAL'].empty?
          e.paginaFinal detalhamento['PAGINA-FINAL'] unless detalhamento['PAGINA-FINAL'].empty?
          e.ehCapituloDoLivro "rdf:resource" => "##{@livros[livro]}"
          autores.each do |autor_uri|
            e.temAutor "rdf:resource" => "##{autor_uri}"
          end
        end
      end
    end
#    
#    ####################################
#    # ORIENTACOES
#    ####################################
#
    if !orientacoes_concluidas.nil? and !orientacoes_concluidas.find('ORIENTACOES-CONCLUIDAS-PARA-MESTRADO').nil?
      orientacoes_concluidas.find('ORIENTACOES-CONCLUIDAS-PARA-MESTRADO').each do |mestrado|
        detalhamento = mestrado.find_first('DETALHAMENTO-DE-ORIENTACOES-CONCLUIDAS-PARA-MESTRADO')
        dados = mestrado.find_first('DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS-PARA-MESTRADO')
        next if dados['TITULO'].empty? # ignore
        titulo = dados['TITULO']
        nome_orientado = detalhamento['NOME-DO-ORIENTADO']
        tipo_orientacao = detalhamento['TIPO-DE-ORIENTACAO']
        ano = dados['ANO']
    
        @pessoas[nome_orientado] = `uuidgen`.strip unless @pessoas.has_key?(nome_orientado)
        e.Pessoa "rdf:about" => "##{@pessoas[nome_orientado]}" do
          e.nome nome_orientado
          e.temTitulo "rdf:resource" => "#TituloMestre"
        end
    
        @trabalhos[titulo] = `uuidgen`.strip unless @trabalhos.has_key?(titulo)
        e.DissertacaoMestrado "rdf:about" => "##{@trabalhos[titulo]}" do
          e.rdf :type, "rdf:resource" => "&owl;Thing"
          e.titulo titulo
          e.ano ano, "rdf:datatype" => "&xsd;gYear"
          e.paisDePublicacao dados['PAIS'] unless dados['PAIS'].empty?
          e.idioma dados['IDIOMA'] unless dados['IDIOMA'].empty?
          e.temAutor "rdf:resource" => "##{@pessoas[nome_orientado]}"
        end
    
        orientacao = [titulo, ano]
        @orientacoes[orientacao] = `uuidgen`.strip unless @orientacoes.has_key?(orientacao)
    
        e.OrientacaoMestrado "rdf:about" => "##{@orientacoes[orientacao]}" do
          e.temOrientador "rdf:resource" => "##{@pessoas[autor_curriculo]}"
          e.temOrientado "rdf:resource" => "##{@pessoas[nome_orientado]}"
          e.temDissertacaoMestrado "rdf:resource" => "##{@trabalhos[titulo]}"
          e.statusOrientacao "FINALIZADO"
        end
      end
    end
#    
#    # ORIENTACOES CONCLUIDAS - DOUTORADO
#    
    if !orientacoes_concluidas.nil? and !orientacoes_concluidas.find('ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO').nil?
      orientacoes_concluidas.find('ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO').each do |doutorado|
        detalhamento = doutorado.find_first('DETALHAMENTO-DE-ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO')
        dados = doutorado.find_first('DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO')
        next if dados['TITULO'].empty? # ignore
        titulo = dados['TITULO']
        nome_orientado = detalhamento['NOME-DO-ORIENTADO']
        tipo_orientacao = detalhamento['TIPO-DE-ORIENTACAO']
        ano = dados['ANO']
    
        @pessoas[nome_orientado] = `uuidgen`.strip unless @pessoas.has_key?(nome_orientado)
        e.Pessoa "rdf:about" => "##{@pessoas[nome_orientado]}" do
          e.nome nome_orientado
          e.temTitulo "rdf:resource" => "#TituloDoutor"
        end
    
        @trabalhos[titulo] = `uuidgen`.strip unless @trabalhos.has_key?(titulo)
        e.TeseDoutorado "rdf:about" => "##{@trabalhos[titulo]}" do
          e.rdf :type, "rdf:resource" => "&owl;Thing"
          e.titulo titulo
          e.ano ano, "rdf:datatype" => "&xsd;gYear"
          e.paisDePublicacao dados['PAIS'] unless dados['PAIS'].empty?
          e.idioma dados['IDIOMA'] unless dados['IDIOMA'].empty?
          e.temAutor "rdf:resource" => "##{@pessoas[nome_orientado]}"
        end
    
        orientacao = [titulo, ano]
        @orientacoes[orientacao] = `uuidgen`.strip unless @orientacoes.has_key?(orientacao)
    
        e.OrientacaoDoutorado "rdf:about" => "##{@orientacoes[orientacao]}" do
          e.temOrientador "rdf:resource" => "##{@pessoas[autor_curriculo]}"
          e.temOrientado "rdf:resource" => "##{@pessoas[nome_orientado]}"
          e.temTeseDoutorado "rdf:resource" => "##{@trabalhos[titulo]}"
          e.statusOrientacao "FINALIZADO"
        end
      end
    end
#    
#    # ORIENTACOES CONCLUIDAS - POS-DOUTORADO
#    
    if !orientacoes_concluidas.nil? and !orientacoes_concluidas.find('ORIENTACOES-CONCLUIDAS-PARA-POS-DOUTORADO').nil?
      orientacoes_concluidas.find('ORIENTACOES-CONCLUIDAS-PARA-POS-DOUTORADO').each do |posdoutorado|
        detalhamento = posdoutorado.find_first('DETALHAMENTO-DE-ORIENTACOES-CONCLUIDAS-PARA-POS-DOUTORADO')
        dados = posdoutorado.find_first('DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS-PARA-POS-DOUTORADO')
        next if dados['TITULO'].empty? # ignore
        titulo = dados['TITULO']
        nome_orientado = detalhamento['NOME-DO-ORIENTADO']
        tipo_orientacao = detalhamento['TIPO-DE-ORIENTACAO']
        ano = dados['ANO']
    
        @pessoas[nome_orientado] = `uuidgen`.strip unless @pessoas.has_key?(nome_orientado)
        e.Pessoa "rdf:about" => "##{@pessoas[nome_orientado]}" do
          e.nome nome_orientado
        end
    
        @trabalhos[titulo] = `uuidgen`.strip unless @trabalhos.has_key?(titulo)
        e.Trabalho "rdf:about" => "##{trabalhos[titulo]}" do
          e.rdf :type, "rdf:resource" => "&owl;Thing"
          e.titulo titulo
          e.ano ano, "rdf:datatype" => "&xsd;gYear"
          e.paisDePublicacao dados['PAIS'] unless dados['PAIS'].empty?
          e.idioma dados['IDIOMA'] unless dados['IDIOMA'].empty?
          e.temAutor "rdf:resource" => "##{@pessoas[nome_orientado]}"
        end
    
        orientacao = [titulo, ano]
        @orientacoes[orientacao] = `uuidgen`.strip unless @orientacoes.has_key?(orientacao)
    
        e.OrientacaoPosDoutorado "rdf:about" => "##{@orientacoes[orientacao]}" do
          e.temOrientador "rdf:resource" => "##{@pessoas[autor_curriculo]}"
          e.temOrientado "rdf:resource" => "##{@pessoas[nome_orientado]}"
          e.temTrabalho "rdf:resource" => "##{@trabalhos[titulo]}"
          e.statusOrientacao "FINALIZADO"
        end
      end
    end
    
    # ORIENTACOES CONCLUIDAS - OUTRAS
    
    if !orientacoes_concluidas.nil? and !orientacoes_concluidas.find('OUTRAS-ORIENTACOES-CONCLUIDAS').nil?
      orientacoes_concluidas.find('OUTRAS-ORIENTACOES-CONCLUIDAS').each do |outras|
        detalhamento = outras.find_first('DETALHAMENTO-DE-OUTRAS-ORIENTACOES-CONCLUIDAS')
        dados = outras.find_first('DADOS-BASICOS-DE-OUTRAS-ORIENTACOES-CONCLUIDAS')
        next if dados['TITULO'].empty? # ignore
        titulo = dados['TITULO']
        nome_orientado = detalhamento['NOME-DO-ORIENTADO']
        tipo_orientacao = detalhamento['TIPO-DE-ORIENTACAO']
        ano = dados['ANO']
    
        @pessoas[nome_orientado] = `uuidgen`.strip unless @pessoas.has_key?(nome_orientado)
        e.Pessoa "rdf:about" => "##{@pessoas[nome_orientado]}" do
          e.nome nome_orientado
        end
    
        @trabalhos[titulo] = `uuidgen`.strip unless @trabalhos.has_key?(titulo)
        e.Trabalho "rdf:about" => "##{@trabalhos[titulo]}" do
          e.rdf :type, "rdf:resource" => "&owl;Thing"
          e.titulo titulo
          e.ano ano, "rdf:datatype" => "&xsd;gYear"
          e.paisDePublicacao dados['PAIS'] unless dados['PAIS'].empty?
          e.idioma dados['IDIOMA'] unless dados['IDIOMA'].empty?
          e.temAutor "rdf:resource" => "##{@pessoas[nome_orientado]}"
        end
    
        orientacao = [titulo, ano]
        @orientacoes[orientacao] = `uuidgen`.strip unless @orientacoes.has_key?(orientacao)
    
        e.Orientacao "rdf:about" => "##{@orientacoes[orientacao]}" do
          e.temOrientador "rdf:resource" => "##{@pessoas[autor_curriculo]}"
          e.temOrientado "rdf:resource" => "##{@pessoas[nome_orientado]}"
          e.temTrabalho "rdf:resource" => "##{@trabalhos[titulo]}"
          e.statusOrientacao "FINALIZADO"
        end
      end
    end
    
    # ORIENTACOES EM ANDAMENTO - MESTRADO
    
    if !orientacoes_andamento.nil? and !orientacoes_andamento.find('ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO').nil?
      orientacoes_andamento.find('ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO').each do |mestrado|
        detalhamento = mestrado.find_first('DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO')
        dados = mestrado.find_first('DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO')
        next if dados['TITULO-DO-TRABALHO'].empty?
        titulo = dados['TITULO-DO-TRABALHO']
        nome_orientando = detalhamento['NOME-DO-ORIENTANDO']
        tipo_orientacao = detalhamento['TIPO-DE-ORIENTACAO']
        ano = dados['ANO']
    
        @pessoas[nome_orientando] = `uuidgen`.strip unless @pessoas.has_key?(nome_orientando)
        e.Pessoa "rdf:about" => "##{@pessoas[nome_orientando]}" do
          e.rdf :type, "rdf:resource" => "#EstudanteMestrado"
          e.nome nome_orientando
        end
    
        @trabalhos[titulo] = `uuidgen`.strip unless @trabalhos.has_key?(titulo)
        e.DissertacaoMestrado "rdf:about" => "##{@trabalhos[titulo]}" do
          e.rdf :type, "rdf:resource" => "&owl;Thing"
          e.titulo titulo
          e.ano ano, "rdf:datatype" => "&xsd;gYear"
          e.paisDePublicacao dados['PAIS'] unless dados['PAIS'].empty?
          e.idioma dados['IDIOMA'] unless dados['IDIOMA'].empty?
          e.temAutor "rdf:resource" => "##{@pessoas[nome_orientando]}"
          e.sendoElaboradoPor "rdf:resource" => "##{@pessoas[nome_orientando]}"
        end

        orientacao = [titulo, ano]
        @orientacoes[orientacao] = `uuidgen`.strip unless @orientacoes.has_key?(orientacao)

        e.OrientacaoMestrado "rdf:about" => "##{@orientacoes[orientacao]}" do
          e.temOrientador "rdf:resource" => "##{@pessoas[autor_curriculo]}"
          e.temOrientado "rdf:resource" => "##{@pessoas[nome_orientando]}"
          e.temDissertacaoMestrado "rdf:resource" => "##{@trabalhos[titulo]}"
          e.statusOrientacao "EM_ANDAMENTO"
        end
      end
    end
    
    # ORIENTACOES EM ANDAMENTO - DOUTORADO
    
    if !orientacoes_andamento.nil? and !orientacoes_andamento.find('ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO').nil?
      orientacoes_andamento.find('ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO').each do |doutorado|
        detalhamento = doutorado.find_first('DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO')
        dados = doutorado.find_first('DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO')
        next if dados['TITULO-DO-TRABALHO'].empty?
        titulo = dados['TITULO-DO-TRABALHO']
        nome_orientando = detalhamento['NOME-DO-ORIENTANDO']
        tipo_orientacao = detalhamento['TIPO-DE-ORIENTACAO']
        ano = dados['ANO']
    
        @pessoas[nome_orientando] = `uuidgen`.strip unless @pessoas.has_key?(nome_orientando)
        e.Pessoa "rdf:about" => "##{@pessoas[nome_orientando]}" do
          e.nome nome_orientando
        end
    
        @trabalhos[titulo] = `uuidgen`.strip unless @trabalhos.has_key?(titulo)
        e.TeseDoutorado "rdf:about" => "##{@trabalhos[titulo]}" do
          e.rdf :type, "rdf:resource" => "&owl;Thing"
          e.titulo titulo
          e.ano ano, "rdf:datatype" => "&xsd;gYear"
          e.paisDePublicacao dados['PAIS'] unless dados['PAIS'].empty?
          e.idioma dados['IDIOMA'] unless dados['IDIOMA'].empty?
          e.temAutor "rdf:resource" => "##{@pessoas[nome_orientando]}"
          e.sendoElaboradoPor "rdf:resource" => "##{@pessoas[nome_orientando]}"
        end
    
        orientacao = [titulo, ano]
        @orientacoes[orientacao] = `uuidgen`.strip unless @orientacoes.has_key?(orientacao)
    
        e.OrientacaoDoutorado "rdf:about" => "##{@orientacoes[orientacao]}" do
          e.temOrientador "rdf:resource" => "##{@pessoas[autor_curriculo]}"
          e.temOrientado "rdf:resource" => "##{@pessoas[nome_orientando]}"
          e.temTeseDoutorado "rdf:resource" => "##{@trabalhos[titulo]}"
          e.statusOrientacao "EM_ANDAMENTO"
        end
      end
    end

    ##
    # END
    ##
    

    sync

    # footer of ontology instances
    output << OWL_FOOTER
    output
  end
end
