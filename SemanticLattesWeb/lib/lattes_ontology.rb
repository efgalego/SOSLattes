# -*- encoding : utf-8 -*-
# Este módulo auxilia em a obter algumas informações do currículo
#
# Versão: 1.0
# Ano: 2009
#

module LattesOntology  
  def create_owl_doc(output_file)
    xml = XML::Parser.file(output_file, :encoding => XML::Encoding::ISO_8859_1)
    doc = xml.parse
  end

  def professor?(curriculo)
    atuacoes_profissionais = curriculo.find_first('DADOS-GERAIS/ATUACOES-PROFISSIONAIS')
    atuacoes_profissionais.find('ATUACAO-PROFISSIONAL').each do |atuacao|
      atuacao.find('VINCULOS').each do |vinculo|
        if vinculo['MES-FIM'].empty? and vinculo['ANO-FIM'].empty?
          if /professor/i =~ vinculo['OUTRO-ENQUADRAMENTO-FUNCIONAL-INFORMADO'] or /professor/i =~ vinculo['OUTRO-VINCULO-INFORMADO']
            return true
          end
        end
      end
    end
    return false
  end
  
  def graduado?(curriculo)
    path = 'DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO/GRADUACAO'
    curriculo.find(path).each do |graduacao|
      return true unless graduacao['ANO-DE-CONCLUSAO'].empty?
    end
    false
  end
  
  def mestre?(curriculo)
    path = 'DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO/MESTRADO'
    curriculo.find(path).each do |mestrado|
      return true unless mestrado['ANO-DE-CONCLUSAO'].empty?
    end
    false
  end

  def doutor?(curriculo)
    path = 'DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO/DOUTORADO'
    curriculo.find(path).each do |doutorado|
      return true unless doutorado['ANO-DE-CONCLUSAO'].empty?
    end
    false
  end

  def detalhes_profissionais(curriculo)
    profissional = { :departamento => [], :instituicao => [] }
    atuacoes_path = 'DADOS-GERAIS/ATUACOES-PROFISSIONAIS/ATUACAO-PROFISSIONAL'
    
    curriculo.find(atuacoes_path).each do |atuacao|
      instituicao = atuacao['NOME-INSTITUICAO']
      vinculos = atuacao.find('VINCULOS').each do |vinculo|
        if vinculo['ANO-FIM'].empty?
          profissional[:instituicao] << instituicao
        end  
      end
      
      atuacao.find('ATIVIDADES-DE-PESQUISA-E-DESENVOLVIMENTO/PESQUISA-E-DESENVOLVIMENTO').each do |pesquisa|
        if pesquisa['FLAG-PERIODO'] =~ /ATUAL/
          next if pesquisa['NOME-UNIDADE'].empty?
          departamento = pesquisa['NOME-UNIDADE']
          profissional[:departamento] << departamento unless profissional[:departamento].include?(departamento)
        end
      end
      
      atuacao.find('ATIVIDADES-DE-EXTENSAO-UNIVERSITARIA/EXTENSAO-UNIVERSITARIA').each do |extensao|
        if extensao['FLAG-PERIODO'] =~ /ATUAL/
          next if extensao['NOME-UNIDADE'].empty?
          departamento = extensao['NOME-UNIDADE']
          profissional[:departamento] << departamento unless profissional[:departamento].include?(departamento)
        end
      end
      
      atuacao.find('ATIVIDADES-DE-CONSELHO-COMISSAO-E-CONSULTORIA/CONSELHO-COMISSAO-E-CONSULTORIA').each do |atividade|
        if atividade['FLAG-PERIODO'] =~ /ATUAL/
          next if atividade['NOME-UNIDADE'].empty?
          departamento = atividade['NOME-UNIDADE']
          profissional[:departamento] << departamento unless profissional[:departamento].include?(departamento)
        end
      end
      
      atuacao.find('ATIVIDADES-DE-PARTICIPACAO-EM-PROJETO/PARTICIPACAO-EM-PROJETO').each do |atividade|
        if atividade['FLAG-PERIODO'] =~ /ATUAL/
          next if atividade['NOME-UNIDADE'].empty?
          departamento = atividade['NOME-UNIDADE']
          profissional[:departamento] << departamento unless profissional[:departamento].include?(departamento)
        end
      end
    end
    profissional
  end

    OWL_HEADER = <<-OWL
<?xml version="1.0" encoding="UTF-8"?>

<!DOCTYPE rdf:RDF [
    <!ENTITY owl "http://www.w3.org/2002/07/owl#" >
    <!ENTITY xsd "http://www.w3.org/2001/XMLSchema#" >
    <!ENTITY owl2xml "http://www.w3.org/2006/12/owl2-xml#" >
    <!ENTITY rdfs "http://www.w3.org/2000/01/rdf-schema#" >
    <!ENTITY rdf "http://www.w3.org/1999/02/22-rdf-syntax-ns#" >
    <!ENTITY curriculo "http://www.semanticlattes.com.br/curriculo#" >
]>


<rdf:RDF xmlns="http://www.semanticlattes.com.br/curriculo#"
     xml:base="http://www.semanticlattes.com.br/curriculo"
     xmlns:owl2xml="http://www.w3.org/2006/12/owl2-xml#"
     xmlns:curriculo="http://www.semanticlattes.com.br/curriculo#"
     xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
     xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
     xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
     xmlns:owl="http://www.w3.org/2002/07/owl#">
    OWL

    OWL_FOOTER = <<-OWL
</rdf:RDF>
    OWL
end
