#!/usr/bin/python
# encoding: utf-8
#
import re

if __name__ == "__main__":
	texto = "Título: A Lógica das Estruturas de Features e suas Aplicações,Ano de Obtenção: 1995. Orientador: Flávio Soares Corrêa da Silva. Bolsista do(a): Coordenação de Aperfeiçoamento de Pessoal de Nível Superior, CAPES, Brasil."
	print "Texto: "+texto

	m = re.search('(.*)Título: (?P<t>.*?)[,]', texto, re.IGNORECASE)
	if (m is not None):
		print "Achou Título: "+m.group('t')
		print "Inicio: %d Termina: %d" % (m.start(), m.end())

		texto = texto[0:m.start()]+texto[m.end():len(texto)]
		print texto

	m = re.search('(.*)Ano de obtenção: (?P<a>.*?)[\.]', texto, re.IGNORECASE)
	if (m is not None):
		print "Achou Ano: "+m.group('a')
		print "Inicio: %d Termina: %d" % (m.start(), m.end())

		texto = texto[0:m.start()]+texto[m.end():len(texto)]
		print texto		
	
	m = re.search('(.*)Orientador: (?P<o>.*)["."]', texto, re.IGNORECASE)
	if (m is not None):
		print "Achou Orientador: "+m.group('o')
		print "Inicio: %d Termina: %d" % (m.start(), m.end())

		texto = texto[0:m.start()]+texto[m.end():len(texto)]
		print texto		

	m = re.search('(.*)Bolsista do\(a\): (?P<ag>.*)["."]', texto, re.IGNORECASE)
	if (m is not None):
		print "Achou Agencia: "+m.group('ag')
		print "Inicio: %d Termina: %d" % (m.start(), m.end())

		texto = texto[0:m.start()]+texto[m.end():len(texto)]
		print texto		

