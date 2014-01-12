# Este módulo contém uma interface para as queries SPARQL desenvolvidas.
# Todas as questões são parametrizadas e descritas abaixo.
#
# Versão: 1.0
# Ano: 2009
#
module OntoLattes
  
  STORED_GRAPH_ONTOLATTES = 'http://www.ime.usp.br/ontolattes'
  
  
  class Consultas
    def self.buscarQuantidadeIndividuos()
      <<-SPARQL
      SELECT ?tipo (COUNT(?individuo) AS ?quantidade)
      FROM <#{STORED_GRAPH_ONTOLATTES}>
      WHERE {
        ?individuo rdf:type ?tipo .
      }
      GROUP BY ?tipo
      ORDER BY ?tipo
      SPARQL
    end

    def self.buscarDadosCurriculos()
      <<-SPARQL
      SELECT ?nome ?id ?foto
      FROM <#{STORED_GRAPH_ONTOLATTES}>
      WHERE {
        ?cv onto:temDadosGerais ?dados .
        ?dados onto:nomeCompleto ?nome ;
           onto:nomeDoArquivoDeFoto ?foto ;
           onto:idLattes ?id .
      }
      ORDER BY DESC(?nome)
      SPARQL
    end

    def self.buscarOutrosCurriculos()
      <<-SPARQL
      SELECT DISTINCT ?nome ?id
      FROM <#{STORED_GRAPH_ONTOLATTES}>
      WHERE {
        {
          ?detalhes onto:nomeDoOrientado ?nome ;
                    onto:numeroIdOrientado ?id
          FILTER( str(?id) != "")
        } MINUS {
          ?dadosGerais onto:nomeCompleto ?nome ;
                       onto:idLattes ?id
        }
      }
      ORDER BY ?nome
      SPARQL
    end

    def self.buscarCurriculosDeOrientandos()
      <<-SPARQL
      SELECT ?orientador ?idorientador ?nome ?id
      FROM <#{STORED_GRAPH_ONTOLATTES}>
      WHERE {
        {
        ?cv onto:temDadosComplementares ?oam.
        ?cv onto:temDadosGerais ?dados .
        ?dados onto:nomeCompleto ?orientador .
        ?dados onto:idLattes ?idorientador .

        ?oam onto:temDetalhamento ?detalhes .
          ?detalhes onto:nomeDoOrientado ?nome ;
                    onto:numeroIdOrientado ?id
          FILTER( str(?id) != "")
        } MINUS {
          ?dadosGerais onto:nomeCompleto ?nome ;
                       onto:idLattes ?id
        }
      }
      ORDER BY ?orientador ?nome
      SPARQL
    end

    def self.buscarFormacao()
      <<-SPARQL
      SELECT ?nome ?id ?formacao ?anoInicio ?nivel ?anoConclusao ?anoObtencao ?orientador ?titulo ?nomeinstituicao ?nomeagencia ?op
      FROM <#{STORED_GRAPH_ONTOLATTES}>
      WHERE {
        ?cv onto:temDadosGerais ?dados .
        ?dados onto:nomeCompleto ?nome ;
                   onto:idLattes ?id .

        ?dados onto:temFormacaoAcademicaTitulacao ?formacao .
        ?formacao onto:anoDeInicio ?anoInicio .
        ?formacao onto:nivel ?nivel
        OPTIONAL { ?formacao onto:anoDeConclusao ?anoConclusao . }
        OPTIONAL { ?formacao onto:anoDeObtencaoDoTitulo ?anoObtencao . }
        OPTIONAL { ?formacao onto:nomeDoOrientador ?orientador . }
        OPTIONAL { ?formacao onto:tituloDoTrabalhoDeConclusaoDeCurso ?titulo . }
        OPTIONAL { ?formacao onto:tituloDaDissertacaoTese ?titulo . }
        OPTIONAL { ?formacao onto:tituloDoTrabalho ?titulo . }
        OPTIONAL { ?formacao onto:realizadoNaInstituicao ?instituicao . ?instituicao onto:nomeInstituicaoEmpresa ?nomeinstituicao . }
        OPTIONAL { ?formacao onto:financiadoPelaAgencia ?agencia . ?agencia onto:nomeAgencia ?nomeagencia . }
        OPTIONAL { ?formacao onto:estaRelacionadoCom ?op . }       
      }
      ORDER BY ?nome DESC(?anoInicio)
      SPARQL
    end
  end

  class Orientacoes
    def self.buscarPorTipoEmAndamento(tipoOrientacao)
      buscarPorFiltroEmAndamento('?oam rdf:type onto:'+ tipoOrientacao + ' .')
    end

    def self.buscarTodasEmAndamento()
      buscarPorFiltroEmAndamento('?oam rdf:type ?orient . ?orient rdfs:subClassOf onto:OrientacaoEmAndamento .')
    end

    def self.buscarPorFiltroEmAndamento(filtro)
      <<-SPARQL
      SELECT DISTINCT
        (?oam as ?uri) ?orientador ?idorientador ?orientando ?idorientando ?nomeinstituicao ?nomeagencia ?tipoDeOrientacao ?ano ?tituloDoTrabalho
      FROM <#{STORED_GRAPH_ONTOLATTES}>
      WHERE {
        ?cv onto:temDadosComplementares ?oam.
        #{filtro}
        ?cv onto:temDadosGerais ?dados .
        ?dados onto:nomeCompleto ?orientador .
        ?dados onto:idLattes ?idorientador .

        ?oam  onto:temDadosBasicosDeOrientacoes ?dbo ;
              onto:temDetalhamento ?detalhes .

        ?dbo onto:ano ?ano ;
             onto:tituloDoTrabalho ?tituloDoTrabalho .

        ?detalhes onto:tipoDeOrientacao ?tipoDeOrientacao .        
        OPTIONAL { ?detalhes onto:nomeDoOrientado ?orientando . }
        OPTIONAL { ?detalhes onto:realizadoNaInstituicao ?instituicao .
                   ?instituicao onto:nomeInstituicaoEmpresa ?nomeinstituicao }
        OPTIONAL { ?detalhes onto:financiadoPelaAgencia ?agencia . 
                   ?agencia onto:nomeAgencia ?nomeagencia . }
      }
      ORDER BY DESC(?ano)
      SPARQL
    end
    
    def self.buscarPorTipoConcluidas(tipoOrientacao)
      buscarPorFiltroConcluida('?op rdf:type onto:'+ tipoOrientacao + ' .')
    end

    def self.buscarTodasConcluidas()
      buscarPorFiltroConcluida('?op rdf:type ?orient . ?orient rdfs:subClassOf onto:OrientacoesConcluidas .')
    end

    def self.buscarPorFiltroConcluida(filtro)
      <<-SPARQL
      SELECT DISTINCT
        (?op as ?uri) ?orientador ?idorientador ?orientando ?idorientando ?nomeinstituicao ?nomeagencia ?tipoDeOrientacao ?ano ?tituloDoTrabalho
      FROM <#{STORED_GRAPH_ONTOLATTES}>
      WHERE {
        ?cv onto:temOutraProducao ?op.
        #{filtro}
        ?cv onto:temDadosGerais ?dados .
        ?dados onto:nomeCompleto ?orientador .
        ?dados onto:idLattes ?idorientador .

        ?op  onto:temDadosBasicosDeOrientacoes ?dboc ;
                  onto:temDetalhamento ?detalhes .

        ?dboc onto:ano ?ano ;
              onto:tituloDoTrabalho ?tituloDoTrabalho .

        ?detalhes onto:tipoDeOrientacao ?tipoDeOrientacao .
        OPTIONAL { ?detalhes onto:realizadoNaInstituicao ?instituicao .
                   ?instituicao onto:nomeInstituicaoEmpresa ?nomeinstituicao }
        OPTIONAL { ?detalhes onto:nomeDoOrientado ?orientando . }
        OPTIONAL { ?detalhes onto:financiadoPelaAgencia ?agencia . 
                   ?agencia onto:nomeAgencia ?nomeagencia . }
        OPTIONAL { ?detalhes onto:numeroIdOrientado ?idorientando . }
      }
      ORDER BY DESC(?ano)
      SPARQL
    end     
    
    def self.buscarRelacionadasEmAndamento()
      <<-SPARQL
      SELECT DISTINCT
        ?nomeorientador  ?nomeorientado  ?idorientado  ?nomeinstituicao  ?nomeagencia  ?tipoDeOrientacao  ?anoTermino  ?titulo
        ?Fnomeorientador ?Fnomeorientado ?Fidorientado ?Fnomeinstituicao ?Fnomeagencia ?FtipoDeOrientacao ?FanoTermino ?Ftitulo
      FROM <#{STORED_GRAPH_ONTOLATTES}>
      WHERE {
        ?cv onto:temDadosComplementares ?oam. ?cv onto:temDadosGerais ?dados . ?dados onto:nomeCompleto ?nomeorientador .
        ?oam onto:temDadosBasicosDeOrientacoes ?dbo ; onto:temDetalhamento ?detalhes .
        ?dbo onto:ano ?anoTermino ; onto:tituloDoTrabalho ?titulo .        
        ?oam rdf:type ?classe .
        ?classe rdfs:comment ?tipoDeOrientacao .
        OPTIONAL { ?detalhes onto:realizadoNaInstituicao ?instituicao . ?instituicao onto:nomeInstituicaoEmpresa ?nomeinstituicao }
        OPTIONAL { ?detalhes onto:nomeDoOrientado ?nomeorientado . }
        OPTIONAL { ?detalhes onto:financiadoPelaAgencia ?agencia . ?agencia onto:nomeAgencia ?nomeagencia . }
        OPTIONAL { ?detalhes onto:numeroIdOrientado ?idorientado . }
                
        ?oam onto:estaRelacionadoCom ?formacao .        
        
        ?Fcv onto:temDadosGerais ?Fdados . ?Fdados onto:nomeCompleto ?Fnomeorientado ; onto:idLattes ?Fidorientado .
        ?Fdados onto:temFormacaoAcademicaTitulacao ?formacao . ?formacao onto:anoDeInicio ?FanoInicio . ?formacao onto:nivel ?FtipoDeOrientacao
        OPTIONAL { ?formacao onto:anoDeConclusao ?FanoTermino . }
        OPTIONAL { ?formacao onto:realizadoNaInstituicao ?Finstituicao . ?Finstituicao onto:nomeInstituicaoEmpresa ?Fnomeinstituicao }
        OPTIONAL { ?formacao onto:financiadoPelaAgencia ?Fagencia . ?Fagencia onto:nomeAgencia ?Fnomeagencia . }                   
        OPTIONAL { ?formacao onto:nomeDoOrientador ?Fnomeorientador . }        
        OPTIONAL { ?formacao onto:tituloDoTrabalhoDeConclusaoDeCurso ?Ftitulo . }
        OPTIONAL { ?formacao onto:tituloDaDissertacaoTese ?Ftitulo . }
        OPTIONAL { ?formacao onto:tituloDoTrabalho ?Ftitulo . }                
      }
      ORDER BY DESC(?anoTermino)      
      SPARQL
    end
    
    def self.buscarRelacionadasConcluida()
      <<-SPARQL
      SELECT DISTINCT
        ?nomeorientador  ?nomeorientado  ?idorientado  ?nomeinstituicao  ?nomeagencia  ?tipoDeOrientacao  ?anoTermino  ?titulo
        ?Fnomeorientador ?Fnomeorientado ?Fidorientado ?Fnomeinstituicao ?Fnomeagencia ?FtipoDeOrientacao ?FanoTermino ?Ftitulo
      FROM <#{STORED_GRAPH_ONTOLATTES}>
      WHERE {
        ?cv onto:temOutraProducao ?op. ?cv onto:temDadosGerais ?dados . ?dados onto:nomeCompleto ?nomeorientador .
        ?op  onto:temDadosBasicosDeOrientacoes ?dboc ; onto:temDetalhamento ?detalhes .
        ?dboc onto:ano ?anoTermino ; onto:tituloDoTrabalho ?titulo .
        ?op rdf:type ?classe .
        ?classe rdfs:comment ?tipoDeOrientacao .
        OPTIONAL { ?detalhes onto:realizadoNaInstituicao ?instituicao . ?instituicao onto:nomeInstituicaoEmpresa ?nomeinstituicao }
        OPTIONAL { ?detalhes onto:nomeDoOrientado ?nomeorientado . }
        OPTIONAL { ?detalhes onto:financiadoPelaAgencia ?agencia . ?agencia onto:nomeAgencia ?nomeagencia . }
        OPTIONAL { ?detalhes onto:numeroIdOrientado ?idorientado . }
                
        ?op onto:estaRelacionadoCom ?formacao .        
        
        ?Fcv onto:temDadosGerais ?Fdados . ?Fdados onto:nomeCompleto ?Fnomeorientado ; onto:idLattes ?Fidorientado .
        ?Fdados onto:temFormacaoAcademicaTitulacao ?formacao . ?formacao onto:anoDeInicio ?FanoInicio . ?formacao onto:nivel ?FtipoDeOrientacao
        OPTIONAL { ?formacao onto:anoDeConclusao ?FanoTermino . }
        OPTIONAL { ?formacao onto:realizadoNaInstituicao ?Finstituicao . ?Finstituicao onto:nomeInstituicaoEmpresa ?Fnomeinstituicao }
        OPTIONAL { ?formacao onto:financiadoPelaAgencia ?Fagencia . ?Fagencia onto:nomeAgencia ?Fnomeagencia . }                   
        OPTIONAL { ?formacao onto:nomeDoOrientador ?Fnomeorientador . }        
        OPTIONAL { ?formacao onto:tituloDoTrabalhoDeConclusaoDeCurso ?Ftitulo . }
        OPTIONAL { ?formacao onto:tituloDaDissertacaoTese ?Ftitulo . }
        OPTIONAL { ?formacao onto:tituloDoTrabalho ?Ftitulo . }                
      }
      ORDER BY DESC(?anoTermino)      
      SPARQL
    end       
  end
  
  class ProducaoBibliografica
    def self.buscarProducaoPorTipo(tipo)
      case tipo
      when "ArtigosPublicados"
        self.buscarPorFiltro('onto:ArtigosPublicados', 'onto:temDetalhamentoDoArtigo')
      when "ArtigosAceitos"
        self.buscarPorFiltro('onto:ArtigosAceitosParaPublicacao', 'onto:temDetalhamentoDoArtigo')
      when "LivrosPublicados"
        self.buscarPorFiltro('onto:LivrosPublicadosOuOrganizados', 'onto:temDetalhamentoDoLivro')  
      when "CapitulosPublicados" 
        self.buscarPorFiltro('onto:CapitulosDeLivrosPublicados', 'onto:temDetalhamentoDoCapitulo')   
      when "TextosPublicados"
        self.buscarPorFiltro('onto:TextosEmJornaisOuRevistas', 'onto:temDetalhamentoDoTexto')  
      when "TrabalhosCongresso"
        self.buscarPorFiltro('onto:TrabalhosEmEventos', 'onto:temDetalhamentoDoTrabalho')  
      when "OutrasProducoes"
        self.buscarPorFiltro('onto:OutraProducaoBibliografica', 'onto:temDetalhamentoDeOutraProducao')
      else        
        print 'Tipo de producao nao encontrado'        
      end
    end
    
    def self.buscarTodas()
      # E agora?
    end
        
    def self.buscarPorFiltro(classePrincipal, propriedadeDetalhes)
      <<-SPARQL
      SELECT ?autor ?idautor ?titulo ?ano ?fasciculo ?paginaInicial ?paginaFinal ?tituloPeriodico ?volume 
             ?nomeLivroJornalRevistaEvento ?dataPublicacao ?tituloLivro ?edicao 
      FROM <#{STORED_GRAPH_ONTOLATTES}>
      WHERE {
        ?cv onto:temDadosGerais ?dados .
        ?dados onto:nomeCompleto ?autor ;
               onto:idLattes ?idautor .

        ?cv onto:temProducaoBibliografica ?pb.
        ?pb rdf:type #{classePrincipal} .
        ?pb onto:temDadosBasicos ?db .
        ?db onto:titulo ?titulo ;
            onto:ano ?ano .
                      
        ?pb #{propriedadeDetalhes} ?detalhes .
        OPTIONAL { ?detalhes onto:fasciculo ?fasciculo } .
        OPTIONAL { ?detalhes onto:paginaInicial ?paginaInicial } .
        OPTIONAL { ?detalhes onto:paginaFinal ?paginaFinal } .
        OPTIONAL { ?detalhes onto:tituloDoPeriodicoOuRevista ?tituloPeriodico } .
        OPTIONAL { ?detalhes onto:volume ?volume } .
        OPTIONAL { ?detalhes onto:numeroDaEdicaoRevisao ?edicao } .
        OPTIONAL { ?detalhes onto:tituloDoJornalOuRevista ?nomeLivroJornalRevistaEvento } .
        OPTIONAL { ?detalhes onto:tituloDoPeriodicoOuRevista ?nomeLivroJornalRevistaEvento } .
        OPTIONAL { ?detalhes onto:tituloDoJornalOuRevista ?nomeLivroJornalRevistaEvento } .        
        OPTIONAL { ?detalhes onto:dataDePublicacao ?dataPublicacao } .
        OPTIONAL { ?detalhes onto:tituloDoLivro ?tituloLivro } .
      }
      ORDER BY DESC(?ano)
      SPARQL
    end
  end
  
  class Construcoes
    def self.criarRelacionamento(left, right)
      <<-SPARQL
      INSERT DATA { 
        onto:#{left} onto:estaRelacionadoCom onto:#{right} .
      }      
      SPARQL
    end
    
    def self.removerRelacionamento(left, right)
      <<-SPARQL
      DELETE { ?left ?p ?right } 
      FROM <#{STORED_GRAPH_ONTOLATTES}>
      WHERE { 
        onto:#{left} onto:estaRelacionadoCom onto:#{right} .
        ?left ?p ?right
      }
      SPARQL
    end
  end
end
