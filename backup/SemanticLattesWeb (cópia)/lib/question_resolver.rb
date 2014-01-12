# -*- encoding : utf-8 -*-
# Este módulo realiza o reconhecimento da consulta solicitada
#
# O reconhecimento retorna qual o template deve ser utilizado
# para exibição dos dados retornados e a query correspondente da consulta
#
# Obs. Quando aplicadas uma expressão regular /regex/ numa string
# os grupos encontrados nos padrões são guardados em váriaveis globais
# $n, onde 'n' é a posição do grupo.
#
# Versão: 1.0
# Ano: 2009
#
module Question
  class Resolver
    include Lattes

    def self.resolve(question)
      case question
      when /Buscar por (professor|pesquisador|pessoa)(?:es)? cujo nome contém ?(.+)\:/i
        ['pessoas', Pessoa.busque_por_nome(regexify($2), $1.capitalize)]
      when /Buscar por (professor|pesquisador|pessoa)(?:es)? cujo nome começa com ?(.+)\:/i
        ['pessoas', Pessoa.busque_por_nome(regexify_begin($2), $1.capitalize)]
      when /Quais s(?:a|ã)o os (professor|pesquisador)(?:es)? do (?:depto|departamento) (?:de )?(.+)\?/i
        ['pessoas', Pessoa.busque_por_departamento(regexify($2), $1.capitalize)]
      when /Quais s(?:a|ã)o as (?:publicacoes|publicações) d(?:os|as)? (professor|pesquisador)(?:es|a)? do (?:depto|departamento) (?:de )?(.+)\?/i
        ['publicacoes', Publicacao.busque_por_departamento(regexify($2), $1.capitalize)]
      when /Quais s(?:a|ã)o as (?:publicacoes|publicações) em (?:periodicos|periódicos) dos (professor|pesquisador)(?:es)? do (?:depto|departamento) (?:de )?(.+)\?/i
        ['artigos_periodico', ArtigoPeriodico.busque_por_departamento(regexify($2), $1.capitalize)]
      when /Quais s(?:a|ã)o as (?:publicacoes|publicações) em (?:periodicos|periódicos) d(?:o|a) (professor|pesquisador)a? (.+)\?/i
        ['artigos_periodico', ArtigoPeriodico.busque_por_pessoa(regexify_end($2), $1.capitalize)]
      when /Quais s(?:a|ã)o as (?:publicacoes|publicações) em (?:conferencias|conferências) dos (professor|pesquisador)(?:es)? do (?:depto|departamento) (?:de )?(.+)\?/i
        ['artigos_conferencia', ArtigoConferencia.busque_por_departamento(regexify($2), $1.capitalize)]
      when /Quais s(?:a|ã)o as (?:publicacoes|publicações) em (?:conferencias|conferências) (internacionais|nacionais) dos (professor|pesquisador)(?:es)? do (?:depto|departamento) (?:de )?(.+)\?/i
        conferencia = $1.eql?('nacionais') ? 'ConferenciaNacional' : 'ConferenciaInternacional'
        ['artigos_conferencia', ArtigoConferencia.busque_por_departamento(regexify($3), $2.capitalize, conferencia)]
      when /Quais s(?:a|ã)o as (?:publicacoes|publicações) em (?:conferencias|conferências) (internacionais|nacionais) d(?:o|a)? (professor|pesquisador)(?:a)? (.+)\?/i
        conferencia = $1.eql?('nacionais') ? 'ConferenciaNacional' : 'ConferenciaInternacional'
        ['artigos_conferencia', ArtigoConferencia.busque_por_pessoa(regexify_end($3), conferencia, $2.capitalize)]
      #when /Quais s(?:a|ã)o os (professor|pesquisador)(?:es)? do (?:depto|departamento) (?:de )?(.+) que publicaram em co-autoria com (?:o|a)? (professor|pesquisador)(?:a)? (.+)\?/i
      #  [:pessoas, Pessoa.busque_por_coautor(regexify($4), regexify_end($2), $1.capitalize)]
      #when /Quais s(?:a|ã)o as (?:publicacoes|publicações) em que o (professor|pesquisador) (.+) figura como 1o autor\?/i
      when /Quem escreveu a (?:publicacao|publicação) (.+)\?/i
        ['publicacoes', Publicacao.busque_por_titulo(regexify($1))]
      #when /Quem s(?:a|ã)o os orientandos do (professor|pesquisador) (.+)\?/i
      #when /Quem s(?:a|ã)o os orientandos de (ic|mestrado|doutorado) do (professor|pesquisador) (.+)\?/i
      #when /Quais (alunos|orientandos) possuem (?:publicacoes|publicações) com seu orientador\?/i
      #when /Quais (professor|pesquisador)(?:es)? do (?:depto|departamento) (?:de )?(.+) publicaram no ano (\d{4})\?/i
      #when /Quais (professor|pesquisador)(?:es)? do (?:depto|departamento) (?:de )?(.+) publicaram em (conferencias|conferências) no ano (\d{4})\?/i
      #when /Quais (professor|pesquisador)(?:es)? do (?:depto|departamento) (?:de )?(.+) publicaram em (conferencias|conferências) (internacionais|nacionais) no ano (\d{4})\?/i
      #when /Quais (professor|pesquisador)(?:es)? do (?:depto|departamento) (?:de )?(.+) possuem registro de patente\?/i
      #when /Quais (professor|pesquisador)(?:es)? do (?:depto|departamento) (?:de )?(.+) publicaram (livros|capitulos de livros)\?/i
      when /Quais s(?:a|ã)o os cap(?:í|i)tulos de livros publicados por (professor|pesquisador)(?:es)? do (?:depto|departamento) (?:de )?(.+)\?/i
        ['capitulos', Capitulo.busque_por_departamento(regexify($2), $1.capitalize)]
      when /Quais s(?:a|ã)o os cap(?:í|i)tulos de livros publicados pel(?:o|a) (professor|pesquisador)a? (.+)\?/i
        ['capitulos', Capitulo.busque_por_pessoa(regexify_end($2), $1.capitalize)]
      when /Quais s(?:a|ã)o os livros publicados por (professor|pesquisador)(?:es)? do (?:depto|departamento) (?:de )?(.+)\?/i
        ['livros', Livro.busque_por_departamento(regexify($2), $1.capitalize)]
      when /Quais s(?:a|ã)o os livros publicados pel(?:o|a) (professor|pesquisador)a? (.+)\?/i
        ['livros', Livro.busque_por_pessoa(regexify_end($2), $1.capitalize)]
      when /Quais s(?:a|ã)o as (teses de doutorado|disserta(?:co|çõ)es de mestrado) (finalizadas|em andamento) sob (?:orientacao|orientação) dos (professor|pesquisador)(?:es)? do (?:departamento|depto) (?:de )?(.+)\?/i
        orientacao = $1.eql?('teses de doutorado') ? 'OrientacaoDoutorado' : 'OrientacaoMestrado'
        status = $2.eql?('finalizadas') ? 'FINALIZADO' : 'EM_ANDAMENTO'
        ['orientacao', Orientacao.busque_por_departamento(regexify($4), status, orientacao, $3.capitalize)]
      when /Quais s(?:a|ã)o as (teses de doutorado|disserta(?:co|çõ)es de mestrado) (finalizadas|em andamento) sob (?:orientacao|orientação) d(?:o|a) (professor|pesquisador)a? (.+)\?/i
        orientacao = $1.eql?('teses de doutorado') ? 'OrientacaoDoutorado' : 'OrientacaoMestrado'
        pessoa = $3.capitalize
        status = $2.eql?('finalizadas') ? 'FINALIZADO' : 'EM_ANDAMENTO'
        ['orientacao', Orientacao.busque_por_pessoa(regexify_end($4), status, orientacao, pessoa)]
      when /Quais s(?:a|ã)o as (teses de doutorado|disserta(?:co|çõ)es de mestrado) (finalizadas|em andamento) sob (?:orientacao|orientação) de (.+)\?/i
        orientacao = $1.eql?('teses de doutorado') ? 'OrientacaoDoutorado' : 'OrientacaoMestrado'
        pessoa = 'Pessoa'
        status = $2.eql?('finalizadas') ? 'FINALIZADO' : 'EM_ANDAMENTO'
        ['orientacao', Orientacao.busque_por_pessoa(regexify_end($3), status, orientacao, pessoa)]
      when /Quais s(?:a|ã)o os artigos Qualis ([A-Z][0-9]?) j(?:a|á) publicados em (\d{4})\?/i
        ['artigos_periodico', ArtigoPeriodico.busque_por_estrato_e_periodo(stratify($1), $2, $2)]
      when /Quais s(?:a|ã)o os artigos Qualis ([A-Z][0-9]?) j(?:a|á) publicados entre (\d{4}) e (\d{4})\?/i
        ['artigos_periodico', ArtigoPeriodico.busque_por_estrato_e_periodo(stratify($1), $2, $3)]
      when /Quais s(?:a|ã)o os artigos Qualis ([A-Z][0-9]?) j(?:a|á) publicados pel(?:o|a) (professor|pesquisador)a? (.+)\?/i
        ['artigos_periodico', ArtigoPeriodico.busque_por_estrato_e_pessoa(stratify($1), regexify_end($3), $2.capitalize)]
      when /Quais s(?:a|ã)o os artigos Qualis ([A-Z][0-9]?) j(?:a|á) publicados por (professor|pesquisador)(?:es)? do (?:depto|departamento) (?:de )?(.+)\?/i
        ['artigos_periodico', ArtigoPeriodico.busque_por_estrato_e_departamento(stratify($1), $2.capitalize, regexify($3))]
      else
        raise 'Consulta inválida'
      end
    end
    
    private
    def self.stratify str
      return str if str.length == 2
      str + "[0-9]"
    end
    
    def self.regexify str
      ".*#{str.gsub(/\s+/, '.*')}"
    end
    
    def self.regexify_end str
      "#{str.gsub(/\s+/, '.*')}.*"
    end
    
    def self.regexify_begin str
      "^#{str.gsub(/\s+/, '.*')}"
    end
  end
end
