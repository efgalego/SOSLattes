from geolocalizador import *

endereco = u'Universidade de Sao Paulo, Instituto de Matematica e Estatastica, Departamento de Ciencia da Computacao. Rua do Matao 1010 Cidade Universitaria 05508090 - Sao Paulo, SP - Brasil Telefone: (11) 30916135 Ramal: 6235 Fax: (11) 30916134 URL da Homepage: http://www.ime.usp.br/~cesar/'.encode('utf8','replace')
g = Geolocalizador(endereco)


endereco = u'Universidade de Sao Paulo, Instituto de Matematica e Estatistica. Rua do Matao, 1010 - Cidade Universitaria Butanta 05508-090 - Sao Paulo, SP - Brasil URL da Homepage: http://www.vision.ime.usp.br/~jmena/'
g = Geolocalizador(endereco)


endereco = u'Universidade de Sao Paulo, Instituto de Matematica e Estatistica. Rua do Matao, 1010 - Cidade Universitaria Butanta 0090 - Arequipa,  - Peru URL da Homepage: http://www.vision.ime.usp.br/~jmena/'
g = Geolocalizador(endereco)


endereco = u'Universidade de Sao Paulo, Instituto de Matematica e Estatastica, Departamento de Cienci 6235 Fax: (11) 30916134 URL da Homepage: http://www.ime.usp.br/~cesar/'.encode('utf8','replace')
g = Geolocalizador(endereco)
