# -*- encoding : utf-8 -*-
require 'rubygems'
require 'sinatra'
require 'rest_client'
require 'haml'
require 'rack'

#require 'lib/lattes'
require File.expand_path('../lib/lattes', __FILE__)

#require 'lib/question_resolver'
require File.expand_path('../lib/question_resolver', __FILE__)

#require 'lib/converter'
require File.expand_path('../lib/converter', __FILE__)

#require 'lib/lattes_ontology'
require File.expand_path('../lib/lattes_ontology', __FILE__)
require File.expand_path('../lib/consultas_ontolattes', __FILE__)
require 'json'
require 'pp'
require 'sinatra/flash'

set :port, 9090

enable :sessions
class String
  def starts_with?(characters)
    self.match(/^#{characters}/i) ? true : false
  end
end

helpers do
  alias_method :h, :escape_html  
end

not_found do
  flash[:global] = "A página procurada não existe"
  redirect '/'
end

error do
#'So what happened was..' + env['sinatra.error'].name
  flash[:global] = "Algum erro ocorreu, contate o administrador"
  redirect '/'
end

# página inicial da aplicação
get '/' do
  query = OntoLattes::Consultas.buscarQuantidadeIndividuos
  response = RestClient.post 'http://0.0.0.0:4567/query/json',
    :query => query
    results = JSON(response)
    
  sumario = Hash.new {|hash, key| hash[key] = 0}
  results['results'].each {|result| sumario[result['tipo']['id'].downcase] = result['quantidade']['id']}      
  
  haml :index, :layout => !request.xhr?, :locals => { :sumario => sumario }
end

get '/carregarcurriculos' do
  query = OntoLattes::Consultas.buscarOutrosCurriculos
  response = RestClient.post 'http://0.0.0.0:4567/query/json',
    :query => query
    results = JSON(response)  
  
  haml :carregarcurriculos, :layout => !request.xhr?, :locals => {:results => results['results'], :size => results['size'] }
end

# realiza a carga de currículo, convertendo o documento para OWL
# e submetendo para a base de conhecimento
post '/carregar' do  
  ids = params[:ids]
  
  parametro = ''
  ids.split(',').each do |item|
    unless parametro == '' 
      parametro = parametro + '&'
    end
    parametro = parametro + 'id=' + item.strip 
  end  
          
  begin    
    resource = RestClient::Resource.new "http://0.0.0.0:8080/scriptLattes?#{parametro}", :timeout => 90000000
    response = resource.get
  rescue
    flash[:error] = "Problema de comunicação com o servidor scritptLattes."
    redirect '/carregar'
  end

  begin
    RestClient.put "http://localhost:4567/import/curriculo.owl", :data => response, :content_type => 'text/xml'
  rescue
    flash[:error] = "Problema de comunicação com o servidor SemanticLattes Server."
    redirect '/carregar'
  end

  flash[:success] = 'Currículo carregado com sucesso'
  params[:ids] = ''
  redirect '/index'
end

get '/restart' do
  begin
    `cp clean_storage/*.yaml storage/`
    RestClient.delete "http://0.0.0.0:4567/reset"
    flash[:global] = "Sistema Reiniciado. Todas as informações foram removidas."
    redirect '/carregarcurriculos'
  rescue
    flash[:error] = "Problema de comunicação com o servidor."
    redirect '/carregarcurriculos'
  end
end

get '/membros' do
  begin
    query = OntoLattes::Consultas.buscarDadosCurriculos()
    response = RestClient.post 'http://0.0.0.0:4567/query/json',
      :query => query
      results = JSON(response)
    
    haml :membros, :locals => { :results => results['results'], :size => results['size'] }
  rescue Exception => e
    flash[:error] = e.message
    redirect '/'
  end  
end

get '/orientacoesEmAndamento' do
  begin
    query = OntoLattes::Orientacoes.buscarTodasEmAndamento()
    response = RestClient.post 'http://0.0.0.0:4567/query/json',
      :query => query
      results = JSON(response)
    
    sumario = Hash.new {|hash, key| hash[key] = 0}
    results['results'].each {|result| sumario[result['ano']['id'].downcase] += 1}    
    
    haml :orientacoes, :locals => { :results => results['results'], :sumario => sumario, :size => results['size'], :titulo => 'Orientações em Andamento' }
  rescue Exception => e
    flash[:error] = e.message
    redirect '/'
  end
end

get '/orientacoesEmAndamento/:tipo' do
begin
    query = OntoLattes::Orientacoes.buscarPorTipoEmAndamento(params[:tipo])    
    response = RestClient.post 'http://0.0.0.0:4567/query/json',
      :query => query
      results = JSON(response)
    
    sumario = Hash.new {|hash, key| hash[key] = 0}
    results['results'].each {|result| sumario[result['ano']['id'].downcase] += 1}    
    
    haml :orientacoes, :locals => { :results => results['results'], :sumario => sumario, :size => results['size'], :titulo => 'Orientações em Andamento (filtro: '+ params[:tipo] + ')' }
  rescue Exception => e
    flash[:error] = e.message
    redirect '/'
  end
end

get '/orientacoesConcluidas' do
  begin
    query = OntoLattes::Orientacoes.buscarTodasConcluidas()
    response = RestClient.post 'http://0.0.0.0:4567/query/json',
      :query => query
      results = JSON(response)
    
    sumario = Hash.new {|hash, key| hash[key] = 0}
    results['results'].each {|result| sumario[result['ano']['id'].downcase] += 1}    
    
    haml :orientacoes, :locals => { :results => results['results'], :sumario => sumario, :size => results['size'], :titulo => 'Orientações Concluídas' }
  rescue Exception => e
    flash[:error] = e.message
    redirect '/'
  end
end

get '/orientacoesConcluidas/:tipo' do
begin
    query = OntoLattes::Orientacoes.buscarPorTipoConcluidas(params[:tipo])
    response = RestClient.post 'http://0.0.0.0:4567/query/json',
      :query => query
      results = JSON(response)
    
    sumario = Hash.new {|hash, key| hash[key] = 0}
    results['results'].each {|result| sumario[result['ano']['id'].downcase] += 1}    
    
    haml :orientacoes, :locals => { :results => results['results'], :sumario => sumario, :size => results['size'], :titulo => 'Orientações Concluídas (filtro: '+params[:tipo]+')' }
  rescue Exception => e
    flash[:error] = e.message
    redirect '/'
  end
end

get '/associarOrientacaoComFormacao/:uri' do
begin
    query = OntoLattes::Consultas.buscarFormacao()
    response = RestClient.post 'http://0.0.0.0:4567/query/json',
      :query => query
      results = JSON(response)
               
    haml :formacao, :locals => { :results => results['results'], :size => results['size'], :uri => params[:uri]}
  rescue Exception => e
    flash[:error] = e.message
    redirect '/'
  end
end

get '/associar/:left/:right' do
begin
    instrucao = OntoLattes::Construcoes.criarRelacionamento(params[:left], params[:right])
    response = RestClient.post 'http://0.0.0.0:4567/update',
      :command => instrucao
               
    flash[:global] = "Associação criada com sucesso!"
    redirect '/'
  rescue Exception => e
    flash[:error] = e.message
    redirect '/'
  end
end

get '/desassociar/:left/:right' do
begin
    instrucao = OntoLattes::Construcoes.removerRelacionamento(params[:left], params[:right])
    response = RestClient.post 'http://0.0.0.0:4567/update',
      :command => instrucao
               
    flash[:global] = "Associação removida com sucesso!"
    redirect '/'
  rescue Exception => e
    flash[:error] = e.message
    redirect '/'
  end
end

get '/inconsistencias' do
  begin
    query = OntoLattes::Orientacoes.buscarRelacionadasConcluida
    response = RestClient.post 'http://0.0.0.0:4567/query/json',
      :query => query
      concluidas = JSON(response)         
    for result in concluidas['results']
      lista = Array.new
      lista << addItemInconst("Nome do Orientador", result['nomeorientador'], result['Fnomeorientador'], "orientação", "formação")
      lista << addItemInconst("Nome do Orientado", result['nomeorientado'], result['Fnomeorientado'], "orientação", "formação")      
      lista << addItemInconst("Nome da Instituição", result['nomeinstituicao'], result['Fnomeinstituicao'], "orientação", "formação")
      lista << addItemInconst("Nome da Agência", result['nomeagencia'], result['Fnomeagencia'], "orientação", "formação")
      lista << addItemInconst("Tipo de Orientação", result['tipoDeOrientacao'], result['FtipoDeOrientacao'], "orientação", "formação")
      lista << addItemInconst("Ano Término", result['anoTermino'], result['FanoTermino'], "orientação", "formação")
      lista << addItemInconst("Título do Trabalho", result['titulo'], result['Ftitulo'], "orientação", "formação")
      result['lista'] = lista
      result['sumario'] = "Título do Trabalho: "+ (result['titulo'] ? result['titulo']['id'] : (result['Ftitulo'] ? result['Ftitulo'] : ""))
    end
    
    query = OntoLattes::Orientacoes.buscarRelacionadasEmAndamento
    response = RestClient.post 'http://0.0.0.0:4567/query/json',
      :query => query
      emandamento = JSON(response)         
    for result in emandamento['results']
      lista = Array.new
      lista << addItemInconst("Nome do Orientador", result['nomeorientador'], result['Fnomeorientador'], "orientação", "formação")
      lista << addItemInconst("Nome do Orientado", result['nomeorientado'], result['Fnomeorientado'], "orientação", "formação")      
      lista << addItemInconst("Nome da Instituição", result['nomeinstituicao'], result['Fnomeinstituicao'], "orientação", "formação")
      lista << addItemInconst("Nome da Agência", result['nomeagencia'], result['Fnomeagencia'], "orientação", "formação")
      lista << addItemInconst("Tipo de Orientação", result['tipoDeOrientacao'], result['FtipoDeOrientacao'], "orientação", "formação")
      lista << addItemInconst("Ano Término", result['anoTermino'], result['FanoTermino'], "orientação", "formação")
      lista << addItemInconst("Título do Trabalho", result['titulo'], result['Ftitulo'], "orientação", "formação")
      result['lista'] = lista
      result['sumario'] = "Título do Trabalho: "+ (result['titulo'] ? result['titulo']['id'] : (result['Ftitulo'] ? result['Ftitulo'] : ""))
    end        
    
    haml :inconsistencias, :locals => { :concluidas => concluidas['results'], :emandamento => emandamento['results'] }
  rescue Exception => e
    flash[:error] = e.message
    redirect '/'
  end
end

def addItemInconst(campo, left, right, tLeft, tRight)
  if left and right
    if left['id'] == right['id']
      msg = "Dados conferem: #{left['id']}."
      icone = "OK"
    elsif left['id'].include? right['id']
      msg = "Dados divergem: #{tRight.capitalize} esta contido(a) em #{tLeft}."
      icone = "Info"
    elsif right['id'].include? left['id']
      msg = "Dados divergem: #{tLeft.capitalize} esta contido(a) em #{tRight}."
      icone = "Info"
    else 
      msg = "Dados divergem: Orientação = #{left['id']} | Formação = #{right['id']}."
      icone = "No"
    end
  else
    if !left and right 
      msg = "Dados divergem: Não consta no(a) #{tLeft}."
      icone = "No"
    elsif !right and left
      msg = "Dados divergem: Não consta no(a) #{tRight}."
      icone = "No"
    else
      msg = "Nenhum valor informado para #{campo} em ambos os casos."
      icone = "OK"
    end    
  end  
  return {'campo' => campo, 'msg' => msg, 'left' => (left ? left['id'] : ""), 'right' => (right ? right['id'] : ""), 'icone' => icone }
end

get '/producoesbibliograficas' do
  begin
    query = OntoLattes::ProducaoBibliografica.buscarTodas
    response = RestClient.post 'http://0.0.0.0:4567/query/json',
      :query => query
      results = JSON(response)
    
    sumario = Hash.new {|hash, key| hash[key] = 0}
    results['results'].each {|result| sumario[result['ano']['id'].downcase] += 1}    
    
    haml :producoesbibliograficas, :locals => { :results => results['results'], :sumario => sumario, :size => results['size'], :titulo => 'Produções Bibliográfica (todas)' }
  rescue Exception => e
    flash[:error] = e.message
    redirect '/'
  end
end

get '/producoesbibliograficas/:tipo' do
  begin
    query = OntoLattes::ProducaoBibliografica.buscarProducaoPorTipo(params[:tipo])
    response = RestClient.post 'http://0.0.0.0:4567/query/json',
      :query => query
      results = JSON(response)
    
    sumario = Hash.new {|hash, key| hash[key] = 0}
    results['results'].each {|result| sumario[result['ano']['id'].downcase] += 1}    
    
    haml :producoesbibliograficas, :locals => { :results => results['results'], :sumario => sumario, :size => results['size'], :titulo => 'Produções Bibliográficas (filtro: '+ params[:tipo] +')' }
  rescue Exception => e
    flash[:error] = e.message
    redirect '/'
  end
end

get '/consultas' do
  haml :perguntas, :layout => !request.xhr?, :locals => { :q => params[:q] }
end

# interface para requisição do autocomplete
get '/questions' do
  result = QUESTION.select { |q| q.starts_with?(params[:q]) }
  result.join("\n")
end

# realiza consulta na base de conhecimento
get '/busca' do
  begin
    view, query = Question::Resolver.resolve(params[:q])
    response = RestClient.post 'http://0.0.0.0:4567/query/json',
    :query => query
    results = JSON(response)
    send_to = 'semantic/'+view
    haml :perguntas, :locals => { :results => results['results'], :size => results['size'], :q => params[:q], :send_to => send_to }
  rescue Exception => e
    flash[:error] = e.message
    redirect '/perguntas'
  end
end











# interface para submissão de currículo
get '/curriculo' do
  haml :upload, :locals => { :q => '' }
end

# pagina sobre o projeto
get '/sobre' do
  haml :sobre, :layout => false
end

# realiza a carga de currículo, convertendo o documento para OWL
# e submetendo para a base de conhecimento
post '/curriculo/upload' do
  if params[:curriculo].nil?
    flash[:error] = "Nenhum currículo foi recebido para carga no sistema."
    redirect '/curriculo'
  end
  filename = params[:curriculo][:filename]

  begin
    data = Loader.new.curriculo(params[:curriculo][:tempfile].read)
  rescue
    flash[:error] = "O currículo fornecido está inválido."
    redirect '/curriculo'
  end

  begin
  # RestClient.put "http://0.0.0.0:4567/import/curriculo.owl", :data => data, :content_type=>'text/xml'
    RestClient.put "http://localhost:4567/import/curriculo.owl", :data => data, :content_type=>'text/xml'
  rescue
    flash[:error] = "Problema de comunicação com o servidor."
    redirect '/curriculo'
  end

  flash[:success] = 'Currículo carregado com sucesso'
  redirect '/status'
end

# consulta a base de conhecimento para detalhes do KB
get '/status' do
  begin
    report = RestClient.get "http://0.0.0.0:4567/status"
    haml :status, :locals => { :q => '', :report => JSON(report), :report_title => "Instâncias da Base de Conhecimento" }
  rescue
    flash[:error] = "Problema de comunicação com o servidor."
    redirect '/curriculo'
  end
end

# consulta a base de conhecimento para detalhes do KB com inferência
get '/status/inference' do
  begin
    report = RestClient.get "http://0.0.0.0:4567/status/inferred"
    haml :status, :locals => { :q => '', :report => JSON(report), :report_title => "Inferência nas Instâncias da Base de Conhecimento" }
  rescue
    flash[:error] = "Problema de comunicação com o servidor."
    redirect '/curriculo'
  end
end

# questões para uso no autocomplete
QUESTION = [
  "Buscar por pessoa cujo nome começa com ...:",
  "Buscar por pessoa cujo nome contém ...:",
  "Quais são as dissertações de mestrado finalizadas sob orientação do professor ...?",
  "Quais são as dissertações de mestrado finalizadas sob orientação do pesquisador ...?",
  "Quais são as dissertações de mestrado finalizadas sob orientação de ...?",
  "Quais são as dissertações de mestrado em andamento sob orientação do professor ...?",
  "Quais são as dissertações de mestrado em andamento sob orientação do pesquisador ...?",
  "Quais são as dissertações de mestrado em andamento sob orientação de ...?",
  "Quais são as teses de doutorado finalizadas sob orientação do professor ...?",
  "Quais são as teses de doutorado finalizadas sob orientação do pesquisador ...?",
  "Quais são as teses de doutorado finalizadas sob orientação de ...?",
  "Quais são as teses de doutorado em andamento sob orientação do professor ...?",
  "Quais são as teses de doutorado em andamento sob orientação do pesquisador ...?",
  "Quais são as teses de doutorado em andamento sob orientação de ...?"
  #"Quais são os professores do departamento de ...?",
  #"Quais são os pesquisadores do departamento de ...?",
  #"Quais são as publicações dos professores do departamento de ...?",
  #"Quais são as publicações dos pesquisadores do departamento de ...?",
  #"Quais são as publicações em periódicos dos professores do departamento de ...?",
  #"Quais são as publicações em periódicos dos pesquisadores do departamento de ...?",
  #"Quais são as publicações em periódicos do professor ...?",
  #"Quais são as publicações em periódicos da professora ...?",
  #"Quais são as publicações em periódicos do pesquisador ...?",
  #"Quais são as publicações em periódicos da pesquisadora ...?",
  #"Quais são as publicações em conferências dos professores do departamento de ...?",
  #"Quais são as publicações em conferências dos pesquisadores do departamento de ...?",
  #"Quais são as publicações em conferências internacionais dos professores do departamento de ...?",
  #"Quais são as publicações em conferências internacionais dos pesquisadores do departamento de ...?",
  #"Quais são as publicações em conferências nacionais dos professores do departamento de ...?",
  #"Quais são as publicações em conferências nacionais dos pesquisadores do departamento de ...?",
  #"Quais são as publicações em conferências internacionais do professor ...?",
  #"Quais são as publicações em conferências internacionais do pesquisador ...?",
  #"Quais são as publicações em conferências nacionais do professor ...?",
  #"Quais são as publicações em conferências nacionais da professora ...?",
  #"Quais são as publicações em conferências nacionais do pesquisador ...?",
  #"Quais são as publicações em conferências nacionais da pesquisadora ...?",
  #  "Quais são os professores do departamento de ... que publicaram em co-autoria com o professor ...?",
  #  "Quais são os pesquisadores do departamento de ... que publicaram em co-autoria com o professor ...?",
  #  "Quais são os professores do departamento de ... que publicaram em co-autoria com o pesquisador ...?",
  #  "Quais são os pesquisadores do departamento de ... que publicaram em co-autoria com o pesquisador ...?",
  #"Quem escreveu a publicação ...?",
  #"Quais são os capítulos de livros publicados por professores do departamento de ...?",
  #"Quais são os capítulos de livros publicados por pesquisadores do departamento de ...?",
  #"Quais são os livros publicados por professores do departamento de ...?",
  #"Quais são os livros publicados por pesquisadores do departamento de ...?",
  #"Quais são os capítulos de livros publicados pelo professor ...?",
  #"Quais são os capítulos de livros publicados pelo pesquisador ...?",
  #"Quais são os livros publicados pelo professor ...?",
  #"Quais são os livros publicados pelo pesquisador ...?",
  #"Quais são as dissertações de mestrado finalizadas sob orientação dos professores do departamento de ...?",
  #"Quais são as dissertações de mestrado finalizadas sob orientação dos pesquisadores do departamento de ...?",
  #"Quais são as dissertações de mestrado em andamento sob orientação dos professores do departamento de ...?",
  #"Quais são as dissertações de mestrado em andamento sob orientação dos pesquisadores do departamento de ...?",
  #"Quais são as teses de doutorado finalizadas sob orientação dos professores do departamento de ...?",
  #"Quais são as teses de doutorado finalizadas sob orientação dos pesquisadores do departamento de ...?",
  #"Quais são as teses de doutorado em andamento sob orientação dos professores do departamento de ...?",
  #"Quais são as teses de doutorado em andamento sob orientação dos pesquisadores do departamento de ...?",
  #"Quais são os artigos Qualis ... já publicados em ...?",
  #"Quais são os artigos Qualis ... já publicados entre ... e ...?",
  #"Quais são os artigos Qualis ... já publicados pelo professor ...?",
  #"Quais são os artigos Qualis ... já publicados pelo pesquisador ...?",
  #"Quais são os artigos Qualis ... já publicados por professores do departamento de ...?",
  #"Quais são os artigos Qualis ... já publicados por pesquisadores do departamento de ...?"
]
