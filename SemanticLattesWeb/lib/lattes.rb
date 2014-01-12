# Este módulo contém uma interface para as queries SPARQL desenvolvidas.
# Todas as questões são parametrizadas e descritas abaixo.
#
# Versão: 1.0
# Ano: 2009
#
module Lattes   
  class Pessoa
    def self.busque_professores_por_departamento(departamento)
      busque_por_departamento(departamento, 'Professor')
    end
    
    def self.busque_pesquisador_por_departamento(departamento)
      busque_por_departamento(departamento, 'Pesquisador')
    end
    
    def self.busque_por_nome(nome, pessoa='Pessoa')
      <<-SPARQL
      SELECT *
      WHERE {
        ?pessoa rdf:type lattes:#{pessoa} ;
          lattes:nome ?pessoa_nome .
        ?cv onto:estaRelacionadoCom ?pessoa .
        ?cv onto:temDadosGerais ?dados .        
        OPTIONAL { ?dados onto:idLattes ?pessoa_id }
        OPTIONAL { ?dados onto:nomeEmCitacoesBibliograficas ?pessoa_citacao }
        FILTER regex(str(?pessoa_nome), '#{nome}', 'i')
      }
      ORDER BY DESC(?pessoa_nome)
      SPARQL
    end
    
    def self.busque_por_departamento(departamento, pessoa='Pessoa')
      <<-SPARQL
      SELECT *
      WHERE {
        ?pessoa rdf:type lattes:#{pessoa} ;
          lattes:trabalhaNoDepartamento ?departamento .
        ?departamento lattes:nome ?departamento_nome .          
        ?cv onto:estaRelacionadoCom ?pessoa .
        ?cv onto:temDadosGerais ?dados .
        ?dados onto:nomeCompleto ?pessoa_nome .        
        OPTIONAL { ?dados onto:nomeEmCitacoesBibliograficas ?pessoa_citacao }
        FILTER regex(?departamento_nome, '#{departamento}', 'i')
      }
      ORDER BY DESC(?nome)
      SPARQL
    end
    
    def self.busque_por_coautor(nome, departamento, pessoa='Pessoa')
      <<-SPARQL
      SELECT *
      WHERE {
      ?autor rdf:type lattes:#{pessoa};
        lattes:nome ?autor_nome;
        lattes:publicouCom ?pessoa.
      ?pessoa rdf:type lattes:#{pessoa};
        lattes:nome ?pessoa_nome;
        lattes:trabalhaNoDepartamento ?departamento.
      ?departamento lattes:nome ?departamento_nome.
      OPTIONAL { ?pessoa lattes:nomeParaCitacao ?pessoa_citacao }
      FILTER regex(?autor_nome, '#{nome}', 'i')
      }
      SPARQL
    end
  end
  
  class Publicacao
    def self.busque_por_departamento(departamento, pessoa='Pessoa')
      <<-SPARQL
      SELECT *
      WHERE {
      ?pessoa rdf:type lattes:#{pessoa};
        lattes:nome ?pessoa_nome;
        lattes:publicou ?publicacao;
        lattes:trabalhaNoDepartamento ?departamento.
      ?departamento lattes:nome ?departamento_nome.
      ?publicacao rdf:type lattes:Publicacao;
        lattes:titulo ?publicacao_titulo;
        lattes:ano ?publicacao_ano.
      OPTIONAL { ?publicacao lattes:idioma ?publicacao_idioma }
      FILTER regex(?departamento_nome, '.*#{departamento}', 'i')
      }
      ORDER BY DESC(?publicacao_ano)
      SPARQL
    end
    
    def self.busque_por_titulo(titulo, pessoa='Pessoa')
      <<-SPARQL
      SELECT *
      WHERE {
      ?pessoa rdf:type lattes:#{pessoa};
        lattes:nome ?pessoa_nome;
        lattes:publicou ?publicacao;
        lattes:trabalhaNoDepartamento ?departamento.
      ?departamento lattes:nome ?departamento_nome.
      ?publicacao rdf:type lattes:Publicacao;
        lattes:titulo ?publicacao_titulo;
        lattes:ano ?publicacao_ano.
      OPTIONAL { ?publicacao lattes:idioma ?publicacao_idioma }
      FILTER regex(?publicacao_titulo, '#{titulo}', 'i')
      }
      ORDER BY DESC(?publicacao_ano)
      SPARQL
    end
  end
  
  class ArtigoPeriodico
    def self.busque_por_departamento(departamento, pessoa='Pessoa')
      <<-SPARQL
      SELECT *
      WHERE {
      ?pessoa rdf:type lattes:#{pessoa};
        lattes:nome ?pessoa_nome;
        lattes:publicou ?artigo;
        lattes:trabalhaNoDepartamento ?departamento.
      ?departamento lattes:nome ?departamento_nome.
      ?artigo rdf:type lattes:ArtigoPeriodico;
        lattes:titulo ?artigo_titulo;
        lattes:ano ?artigo_ano;
        lattes:ehPublicadoEmEdicaoPeriodico ?periodico_edicao.
      ?periodico_edicao lattes:ehEdicaoDoPeriodico ?periodico.
      ?periodico lattes:titulo ?periodico_titulo;
        lattes:ISSN ?periodico_ISSN.
      OPTIONAL { ?artigo lattes:idioma ?artigo_idioma }
      FILTER regex(?departamento_nome, '#{departamento}', 'i')
      }
      ORDER BY DESC(?artigo_ano)
      SPARQL
    end
    
    def self.busque_por_professor(nome)
      busque_por_pessoa(nome, 'Professor')
    end
    
    def self.busque_por_pesquisador(nome)
      busque_por_pessoa(nome, 'Pesquisador')
    end
    
    def self.busque_por_estrato_e_periodo(estrato, start_year, end_year)
      <<-SPARQL
      SELECT DISTINCT 
        ?artigo_titulo ?artigo_ano 
        ?periodico_titulo ?periodico_ISSN ?periodico_estrato 
        ?area_nome 
        ?pessoa_nome 
        ?departamento_nome
      WHERE { 
        ?artigo rdf:type lattes:ArtigoPeriodico; 
          lattes:titulo ?artigo_titulo; 
          lattes:ano ?artigo_ano; 
          lattes:temAutor ?pessoa; 
          lattes:ehPublicadoEmEdicaoPeriodico ?periodico_edicao. 
        ?pessoa lattes:nome ?pessoa_nome.
        ?periodico_edicao lattes:ehEdicaoDoPeriodico ?periodico. 
        ?periodico lattes:titulo ?periodico_titulo; 
          lattes:ISSN ?periodico_ISSN; 
          qualis:ehClassificadoPor ?classificacao. 
        ?classificacao qualis:estrato ?periodico_estrato;
          qualis:classificadoNaArea ?area.
        ?area qualis:nome_area ?area_nome.
        OPTIONAL { 
          ?pessoa lattes:trabalhaNoDepartamento ?departamento. 
          ?departamento lattes:nome ?departamento_nome. 
        } 
        FILTER (?area_nome = 'ENGENHARIAS IV') 
        FILTER regex(?periodico_estrato, '#{estrato}', 'i') 
        FILTER (str(?artigo_ano) >= '#{start_year}' 
                && str(?artigo_ano) <= '#{end_year}')
      }
      ORDER BY ASC(?periodico_estrato) ASC(?artigo_titulo)
      SPARQL
    end
    
    def self.busque_por_estrato_e_pessoa(estrato, nome, pessoa=Pessoa)
      <<-SPARQL
      SELECT DISTINCT 
        ?artigo_titulo ?artigo_ano 
        ?periodico_titulo ?periodico_ISSN ?periodico_estrato 
        ?area_nome 
        ?pessoa_nome 
        ?departamento_nome
      WHERE { 
        ?artigo rdf:type lattes:ArtigoPeriodico; 
          lattes:titulo ?artigo_titulo; 
          lattes:ano ?artigo_ano; 
          lattes:temAutor ?pessoa; 
          lattes:ehPublicadoEmEdicaoPeriodico ?periodico_edicao. 
        ?pessoa rdf:type lattes:#{pessoa};
          lattes:nome ?pessoa_nome.
        ?periodico_edicao lattes:ehEdicaoDoPeriodico ?periodico. 
        ?periodico lattes:titulo ?periodico_titulo; 
          lattes:ISSN ?periodico_ISSN; 
          qualis:ehClassificadoPor ?classificacao. 
        ?classificacao qualis:estrato ?periodico_estrato;
          qualis:classificadoNaArea ?area.
        ?area qualis:nome_area ?area_nome.
        OPTIONAL { 
          ?pessoa lattes:trabalhaNoDepartamento ?departamento. 
          ?departamento lattes:nome ?departamento_nome. 
        } 
        FILTER (?area_nome = 'ENGENHARIAS IV') 
        FILTER regex(?periodico_estrato, '#{estrato}', 'i') 
        FILTER regex(?pessoa_nome, '#{nome}', 'i')
      }
      ORDER BY ASC(?periodico_estrato) ASC(?artigo_titulo)
      SPARQL
    end
    
    def self.busque_por_estrato_e_departamento(estrato, pessoa, departamento)
      <<-SPARQL
      SELECT DISTINCT 
        ?artigo_titulo ?artigo_ano 
        ?periodico_titulo ?periodico_ISSN ?periodico_estrato 
        ?area_nome 
        ?pessoa_nome 
        ?departamento_nome
      WHERE { 
        ?artigo rdf:type lattes:ArtigoPeriodico; 
          lattes:titulo ?artigo_titulo; 
          lattes:ano ?artigo_ano; 
          lattes:temAutor ?pessoa; 
          lattes:ehPublicadoEmEdicaoPeriodico ?periodico_edicao. 
        ?pessoa rdf:type lattes:#{pessoa};
          lattes:nome ?pessoa_nome;
          lattes:trabalhaNoDepartamento ?departamento. 
        ?departamento lattes:nome ?departamento_nome.
        ?periodico_edicao lattes:ehEdicaoDoPeriodico ?periodico. 
        ?periodico lattes:titulo ?periodico_titulo; 
          lattes:ISSN ?periodico_ISSN; 
          qualis:ehClassificadoPor ?classificacao. 
        ?classificacao qualis:estrato ?periodico_estrato;
          qualis:classificadoNaArea ?area.
        ?area qualis:nome_area ?area_nome.
        OPTIONAL { 
          
        } 
        FILTER (?area_nome = 'ENGENHARIAS IV') 
        FILTER regex(?periodico_estrato, '#{estrato}', 'i') 
        FILTER regex(?departamento_nome, '#{departamento}', 'i')
      }
      ORDER BY ASC(?periodico_estrato) ASC(?artigo_titulo)
      SPARQL
    end
    
    def self.busque_por_pessoa(nome, pessoa='Pessoa')
      <<-SPARQL
      SELECT *
      WHERE {
        ?pessoa rdf:type lattes:#{pessoa};
          lattes:nome ?pessoa_nome;
          lattes:publicou ?artigo;
          lattes:trabalhaNoDepartamento ?departamento.
        ?departamento lattes:nome ?departamento_nome.
        ?artigo rdf:type lattes:ArtigoPeriodico;
          lattes:titulo ?artigo_titulo;
          lattes:ano ?artigo_ano;
          lattes:ehPublicadoEmEdicaoPeriodico ?periodico_edicao.
        ?periodico_edicao lattes:ehEdicaoDoPeriodico ?periodico.
        ?periodico lattes:titulo ?periodico_titulo;
          lattes:ISSN ?periodico_ISSN.
        OPTIONAL { ?artigo lattes:idioma ?artigo_idioma }
        FILTER regex(?pessoa_nome, '#{nome}', 'i')
      }
      ORDER BY DESC(?artigo_ano)
      SPARQL
    end
  end
  
  class ArtigoConferencia
    def self.busque_por_departamento(departamento, pessoa='Pessoa', conferencia='Conferencia')
      <<-SPARQL
      SELECT DISTINCT *
      WHERE {
        ?pessoa rdf:type lattes:#{pessoa};
          lattes:nome ?pessoa_nome;
          lattes:publicou ?artigo;
          lattes:trabalhaNoDepartamento ?departamento.
        ?departamento lattes:nome ?departamento_nome.
        ?artigo rdf:type lattes:ArtigoConferencia;
          lattes:titulo ?artigo_titulo;
          lattes:ano ?artigo_ano;
          lattes:ehPublicadoEmConferencia ?conferencia.
        ?conferencia rdf:type lattes:#{conferencia};
          lattes:nome ?conferencia_nome.
        OPTIONAL { ?artigo lattes:idioma ?artigo_idioma }
        FILTER regex(?departamento_nome, '#{departamento}', 'i')
      }
      ORDER BY DESC(?artigo_ano)
      SPARQL
    end
    
    def self.busque_por_professor(nome, conferencia='Conferencia')
      busque_por_pessoa(nome, conferencia, 'Professor')
    end
    
    def self.busque_por_pesquisador(nome, conferencia='Conferencia')
      busque_por_pessoa(nome, conferencia, 'Pesquisador')
    end
    
    def self.busque_por_pessoa(nome, conferencia='Conferencia', pessoa='Pessoa')
      <<-SPARQL
      SELECT *
      WHERE {
        ?pessoa rdf:type lattes:#{pessoa};
          lattes:publicou ?artigo;
          lattes:nome ?pessoa_nome.
        ?artigo rdf:type lattes:ArtigoConferencia;
          lattes:titulo ?artigo_titulo;
          lattes:ano ?artigo_ano;
          lattes:ehPublicadoEmConferencia ?conferencia.
        ?conferencia rdf:type lattes:#{conferencia};
          lattes:nome ?conferencia_nome.
        OPTIONAL { ?artigo lattes:idioma ?artigo_idioma }
        FILTER regex(?pessoa_nome, '#{nome}', 'i')
      }
      ORDER BY DESC(?artigo_ano)
      SPARQL
    end
  end
  
  class Livro
    def self.busque_por_departamento(departamento, pessoa='Pessoa')
      <<-SPARQL
      SELECT *
      WHERE {
      ?pessoa rdf:type lattes:#{pessoa};
        lattes:nome ?pessoa_nome;
        lattes:trabalhaNoDepartamento ?departamento;
        lattes:publicou ?livro.
      ?departamento lattes:nome ?departamento_nome.
      ?livro rdf:type lattes:Livro;
          lattes:titulo ?livro_titulo;
          lattes:ano ?livro_ano.
      OPTIONAL { ?livro lattes:idioma ?livro_idioma }
      OPTIONAL { ?livro lattes:numeroDePaginas ?livro_paginas }
      OPTIONAL { ?livro lattes:numeroDeVolumes ?livro_volumes }
      FILTER regex(?departamento_nome, '#{departamento}', 'i')
      }
      ORDER BY DESC(?livro_ano)
      SPARQL
    end
    
    def self.busque_por_pessoa(nome, pessoa='Pessoa')
      <<-SPARQL
      SELECT *
      WHERE {
      ?pessoa rdf:type lattes:#{pessoa};
        lattes:nome ?pessoa_nome;
        lattes:trabalhaNoDepartamento ?departamento;
        lattes:publicou ?livro.
      ?departamento lattes:nome ?departamento_nome.
      ?livro rdf:type lattes:Livro;
          lattes:titulo ?livro_titulo;
          lattes:ano ?livro_ano.
      OPTIONAL { ?livro lattes:idioma ?livro_idioma }
      OPTIONAL { ?livro lattes:numeroDePaginas ?livro_paginas }
      OPTIONAL { ?livro lattes:numeroDeVolumes ?livro_volumes }
      FILTER regex(?pessoa_nome, '#{nome}', 'i')
      }
      ORDER BY DESC(?livro_ano)
      SPARQL
    end
  end

  class Capitulo
    def self.busque_por_departamento(departamento, pessoa='Pessoa')
      <<-SPARQL
      SELECT *
      WHERE {
      ?pessoa rdf:type lattes:#{pessoa};
        lattes:nome ?pessoa_nome;
        lattes:trabalhaNoDepartamento ?departamento;
        lattes:publicou ?capitulo.
      ?departamento lattes:nome ?departamento_nome.
      ?capitulo rdf:type lattes:Capitulo;
        lattes:ehCapituloDoLivro ?livro;
        lattes:titulo ?capitulo_titulo;
        lattes:ano ?capitulo_ano.
      ?livro lattes:titulo ?livro_titulo.
      OPTIONAL { ?capitulo lattes:idioma ?capitulo_idioma }
      OPTIONAL { ?capitulo lattes:paginaInicial ?capitulo_paginicio }
      OPTIONAL { ?capitulo lattes:paginaFinal ?capitulo_pagfim }
      FILTER regex(?departamento_nome, '#{departamento}', 'i')
      }
      ORDER BY DESC(?capitulo_ano)
      SPARQL
    end
    
    def self.busque_por_pessoa(nome, pessoa='Pessoa')
      <<-SPARQL
      SELECT *
      WHERE {
      ?pessoa rdf:type lattes:#{pessoa};
        lattes:nome ?pessoa_nome;
        lattes:trabalhaNoDepartamento ?departamento;
        lattes:publicou ?capitulo.
      ?departamento lattes:nome ?departamento_nome.
      ?capitulo rdf:type lattes:Capitulo;
        lattes:ehCapituloDoLivro ?livro;
        lattes:titulo ?capitulo_titulo;
        lattes:ano ?capitulo_ano.
      ?livro lattes:titulo ?livro_titulo.
      OPTIONAL { ?capitulo lattes:idioma ?capitulo_idioma }
      OPTIONAL { ?capitulo lattes:paginaInicial ?capitulo_paginicio }
      OPTIONAL { ?capitulo lattes:paginaFinal ?capitulo_pagfim }
      FILTER regex(?pessoa_nome, '#{nome}', 'i')
      }
      ORDER BY DESC(?capitulo_ano)
      SPARQL
    end
  end
  
  class Orientacao
    def self.busque_por_departamento(departamento, status='FINALIZADO|EM_ANDAMENTO', orientacao='Orientacao', pessoa='Pessoa')
      <<-SPARQL
      SELECT *
      WHERE {
      ?orientador rdf:type lattes:#{pessoa};
        lattes:nome ?orientador_nome;
        lattes:possuiOrientacao ?orientacao;
        lattes:trabalhaNoDepartamento ?departamento.
      ?departamento lattes:nome ?departamento_nome.
      ?orientacao rdf:type lattes:#{orientacao};
        lattes:statusOrientacao ?orientacao_status;
        lattes:temOrientado ?orientado;
        lattes:temTrabalho ?trabalho.
      ?orientado lattes:nome ?orientado_nome.
      ?trabalho lattes:titulo ?trabalho_titulo.
      OPTIONAL { ?orientado lattes:nomeParaCitacao ?orientado_citacao }
      OPTIONAL { ?trabalho lattes:ano ?trabalho_ano }
      OPTIONAL { ?trabalho lattes:idioma ?trabalho_idioma }
      FILTER regex(?departamento_nome, '#{departamento}', 'i')
      FILTER regex(?orientacao_status, '#{status}', 'i')
      }
      SPARQL
    end
    
    def self.busque_por_pessoa(nome, status='FINALIZADO|EM_ANDAMENTO', orientacao='Orientacao', pessoa='Pessoa')
      <<-SPARQL
      SELECT *
      WHERE {
      ?orientador rdf:type lattes:#{pessoa};
        lattes:nome ?orientador_nome;
        lattes:possuiOrientacao ?orientacao.
      ?orientacao rdf:type lattes:#{orientacao};
        lattes:statusOrientacao ?orientacao_status;
        lattes:temOrientado ?orientado;
        lattes:temTrabalho ?trabalho.
      ?orientado lattes:nome ?orientado_nome.
      ?trabalho lattes:titulo ?trabalho_titulo.
      OPTIONAL { ?orientado lattes:nomeParaCitacao ?orientado_citacao }
      OPTIONAL { ?trabalho lattes:ano ?trabalho_ano }
      OPTIONAL { ?trabalho lattes:idioma ?trabalho_idioma }
      FILTER regex(?orientador_nome, '#{nome}', 'i')
      FILTER regex(?orientacao_status, '#{status}', 'i')
      }
      SPARQL
    end
  end
end
