require 'rubygems'
require 'sinatra'
require 'lib/kb.rb'
require 'json'
require 'erb'
require 'pp'

error do
  'So what happened was..' + env['sinatra.error'].name
end

helpers do
  include Ontology::KB
end

get '/' do
  erb :index
end

# request query por interface web
post '/query' do
  q = Ontology::Query.new
  q.answer(params[:query]).to_json
end

# consulta para chamadas JSON
post '/query/json' do
  content_type :json
  puts params[:query]
  q = Ontology::Query.new
  report = q.answer(params[:query])
  response = {}
  response[:size] = report.size
  response[:results] = report
  response.to_json
end

# obtêm detalhes do base de conhecimento
get '/status' do
  content_type :json
  storage.report.to_json
end

# obtêm detalhes do base de conhecimento com inferência
get '/status/inferred' do
  content_type :json
  storage.inferred_report.to_json
end

# interface para carga de currículos na base de conhecimento
put '/import/:curriculo' do
  path = File.join('tmp', params[:curriculo])
  File.open(path, 'w') { |f| f.write(params[:data]) }
  storage.load_data(path)
  'Success'
end

# limpa a base de conhecimento
delete '/reset' do
  storage.cleanup
  'Success'
end
