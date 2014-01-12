require 'java'
require 'pp'
Dir["lib/*jar"].each { |jar| require jar }

# Definindo os Alias para as classes Java
BufferedReader = java.io.BufferedReader
FileReader = java.io.FileReader

FileManager     = com.hp.hpl.jena.util.FileManager

OntModel        = com.hp.hpl.jena.ontology.OntModel
OntModelSpec    = com.hp.hpl.jena.ontology.OntModelSpec
OntResource     = com.hp.hpl.jena.ontology.OntResource
InfModel        = com.hp.hpl.jena.rdf.model.InfModel
ModelFactory    = com.hp.hpl.jena.rdf.model.ModelFactory
Resource        = com.hp.hpl.jena.rdf.model.Resource
RDFNode         = com.hp.hpl.jena.rdf.model.RDFNode
Query           = com.hp.hpl.jena.query.Query
QueryExecution  = com.hp.hpl.jena.query.QueryExecution
QueryFactory    = com.hp.hpl.jena.query.QueryFactory
ResultSet       = com.hp.hpl.jena.query.ResultSet
ResultSetFormatter = com.hp.hpl.jena.query.ResultSetFormatter
Reasoner        = com.hp.hpl.jena.reasoner.Reasoner
TDBFactory      = com.hp.hpl.jena.tdb.TDBFactory

OWL             = com.hp.hpl.jena.vocabulary.OWL
RDF             = com.hp.hpl.jena.vocabulary.RDF
RDFS            = com.hp.hpl.jena.vocabulary.RDFS

GenericRuleReasoner = com.hp.hpl.jena.reasoner.rulesys.GenericRuleReasoner
Rule = com.hp.hpl.jena.reasoner.rulesys.Rule

PelletReasonerFactory = org.mindswap.pellet.jena.PelletReasonerFactory
SparqlDLExecutionFactory = com.clarkparsia.pellet.sparqldl.jena.SparqlDLExecutionFactory

# O módulo contém uma abstração para uma aplicação utilizando Jena
module Ontology
  LATTES_NS = "http://www.semanticlattes.com.br/curriculo#"
  QUALIS_CAPES_NS = "http://qualis.capes.gov.br/qualis-capes.owl#"
  
  # O KB (Knowledge Base) mantém uma instância estática da base
  # para evitar recarga pela aplicação
  module KB
    class TDB
      attr_reader :model, :inferred
      
      def initialize
        initialize_schema
        initialize_equivalent_data
        initialize_rules
        initialize_reasoner
        
        @model = TDBFactory.assembleModel('config/tdb-assembler.ttl')
        @ruled.add(@model)
        @inferred.add(@ruled)
        p "after model size: #{@model.size}"
      end
      
      # permite carregar novas instâncias atualizando a base de dados
      def load_data(fileOrUri)
        p "before model size: #{@model.size}"
        model = ModelFactory.createDefaultModel
        FileManager.get.readModel(model, fileOrUri)
        @ruled.add(model)
        @inferred.add(@ruled)
        @model.add(model)
        @model.commit
        p "after model size: #{@model.size}"
      end
      
      # obtêm relatório das instâncias
      def report
        retrieve_report(@model)
      end
      
      # obtêm relatório com inferência
      def inferred_report
        retrieve_report(@inferred)
      end
      
      # obtêm a quantidade de instâncias
      def size
        @model.size
      end
      
      # remove todas as instâncias da base
      def cleanup
        @inferred.remove(@ruled)
        @ruled.remove(@model)
        @model.removeAll # remove do TDB
        p "MODEL: #{@model.size}"
        p "SCHEMA: #{@schema.size}"
        p "INFERRED: #{@inferred.size}"
      end
      
      # fecha conexão com o TDB
      def close
        @model.close
      end
      
      private
      
      # inicializa a carga das ontologias na memória
      def initialize_schema
          p "initialize schema ------------------"
          @schema = ModelFactory.createDefaultModel
          p "before: #{@schema.size}"
          #FileManager.get.readModel(@schema, 'ontology/curriculo.n3')
          #FileManager.get.readModel(@schema, 'ontology/qualis.n3')
          #FileManager.get.readModel(@schema, 'ontology/qualis_periodicos.n3')
	  FileManager.get.readModel(@schema, 'ontology/ontolattes.owl')
          p "after: #{@schema.size}"
          p "end load schema --------------"
      end
      
      # inicializa as equivalências da ontologias
      def initialize_equivalent_data
        # define que periodicos são equivalentes
        #resource = @schema.getResource(QUALIS_CAPES_NS + "Periodico");
        #obj = @schema.getResource(LATTES_NS + "Periodico");
        #@schema.add(resource, OWL.equivalentClass, obj);

        # define que a propriedade ISSN são equivalentes
        #resource = @schema.getResource(QUALIS_CAPES_NS + "ISSN");
        #obj = @schema.getResource(LATTES_NS + "ISSN");
        #@schema.add(resource, OWL.equivalentProperty, obj);

        # define que o titulo_periodico é uma subpropriedade de titulo
        #resource = @schema.getResource(QUALIS_CAPES_NS + "titulo_periodico");
        #obj = @schema.getResource(LATTES_NS + "titulo");
        #@schema.add(resource, RDFS.subPropertyOf, obj);
      end
      
      # inicializa o motor de regras
      def initialize_rules
        @parser = Rule.rulesParserFromReader(BufferedReader.new(FileReader.new("ontology/lattes.rules")))
        @ruleReasoner = GenericRuleReasoner.new(Rule.parseRules(@parser))
        @ruled = ModelFactory.createInfModel(@ruleReasoner, @schema)
      end
      
      # inicializa o reasoner
      def initialize_reasoner
        @reasoner = PelletReasonerFactory.theInstance.create
        @inferred = ModelFactory.createInfModel(@reasoner, @schema)
      end
      
      # gera um relatório simples das instâncias
      def retrieve_report(model)
        report = {}
        model.listResourcesWithProperty(RDF.type).each do |resource|
          resource.listProperties(RDF.type).each do |stmt|
            key = stmt.getObject.toString
            next if key =~ /(www.w3.org|capes.gov.br|#Thing$)/
            report[key] ||= 0
            report[key] += 1
          end
        end
        report
      end
    end
    
    # instância estática do KB
    @@storage = TDB.new
    def storage
      @@storage
    end
  end
  
  # Provê uma abstração de query do SPARQL
  class Query
    include KB
    
    # executa a query SPARQL sobre o KB
    def answer(question)
      response = []
      begin
        query = QueryFactory.create(QUERY_TEMPLATE.sub(/%command%/, question))
        qexec = SparqlDLExecutionFactory.create(query, storage.inferred)
        results = qexec.execSelect
        response = parse_results(results)
      ensure
        qexec.close if qexec
      end
      response
    end
    
    private
    # trata o resultado gerando um hash como resultado
    # ao invês de QuerySolution do Jena
    def parse_results(results)
      list = []
      results.each do |result|
        list << result_to_hash(result)
      end
      list
    end
    
    # trata o resultado de acordo com a conveção de nomes adotada
    # os paramêtros de cada um são separados por '_', de modo que
    # pessoa_nome, gere uma entrada do tipo row['pessoa']['nome']
    def result_to_hash(result)
      hash = {}
      result.varNames.each do |name|
        next if name =~ /\?\w+/
        node = hash
        properties = name.split('_')
        if properties.size < 2
          label = properties.first.to_sym
          hash[label] ||= {}
          hash[label][:id] = value(result, name)
        else
          (0...properties.size-1).each do |i|
            label = properties[i].to_sym
            node[label] ||= {}
            node = node[label]
          end
          node[properties.last.to_sym] = value(result, name)
        end
      end
      hash
    end
    
    # obtêm o valor da RDFNode do Jena, que pode ser
    # anônimo, literal ou resource
    def value(result, name)
      node = result.get(name)

      if node.isLiteral
        return result.getLiteral(name).getString
      elsif node.isResource
        return result.getResource(name).getLocalName
      else
        return nil
      end
    end
    
    QUERY_TEMPLATE = <<-EOF
      PREFIX lattes: <http://www.semanticlattes.com.br/curriculo#>
      PREFIX qualis: <http://qualis.capes.gov.br/qualis-capes.owl#>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
      PREFIX owl: <http://www.w3.org/2002/07/owl#>
      PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
      PREFIX onto:<http://a.com/ontology/>
      %command%
    EOF
  end
end
