import web
import sys

sys.path.append('scriptLattes')
sys.path.append('scriptLattes/producoesBibliograficas/')
sys.path.append('scriptLattes/producoesTecnicas/')
sys.path.append('scriptLattes/producoesArtisticas/')
sys.path.append('scriptLattes/producoesUnitarias/')
sys.path.append('scriptLattes/orientacoes/')
sys.path.append('scriptLattes/eventos/')
sys.path.append('scriptLattes/charts/')
sys.path.append('scriptLattes/internacionalizacao/')

from grupo import *

urls = (
	"/scriptLattes", "ScriptLattes"
)
app = web.application(urls, globals())

class hello:
    def GET(self):
        return 'Hello, world!'

# Examplo de chamada: http://0.0.0.0:8080/scriptLattes?id=8571722708574643&id=0348490713417429&id=0620986273710878&id=8548608291351316
class ScriptLattes:
    def GET(self):
	novoGrupo = None
        listaIdMembros = web.input(id=[])
	if not listaIdMembros.id:
		return '<h1> faltou informar lista de membros </h1>'
	else :
	
		arquivoConfiguracao = './webservice/ws-padrao.config'

		novoGrupo = Grupo(arquivoConfiguracao, listaIdMembros.id)
		#novoGrupo.imprimirListaDeParametros()
		#novoGrupo.imprimirListaDeRotulos()

		if criarDiretorio(novoGrupo.obterParametro('global-diretorio_de_saida')):
			novoGrupo.carregarDadosCVLattes() #obrigatorio
			novoGrupo.compilarListasDeItems() # obrigatorio		
			novoGrupo.gerarGrafosDeColaboracoes()

			novoGrupo.calcularInternacionalizacao() # obrigatorio
			#novoGrupo.gerarGraficosDeBarras() # obrigatorio
			#novoGrupo.gerarMapaDeGeolocalizacao() # obrigatorio	
			return novoGrupo.gerarOntologia()
		else:
			return 'erro ao obter resultado'		

if __name__ == "__main__":
    app.run()

