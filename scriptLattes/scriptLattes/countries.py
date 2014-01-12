#!/usr/bin/python
# encoding: utf-8
#

import string
import re

paises = {
	"Abkhazia":       ["Apsny", "Abkhaziya"],
	"Afghanistan":    ["Afghanestan"],
	"Albania":        ["Shqipëria"],
	"Algeria":        ["Al-Jazā'ir"],
	"American Samoa": ["Amerika Sāmoa"],
	"Andorra":        [],
	"Angola":         [],
	"Anguilla":       [],
	"Antigua and Barbuda": [],
	"Argentina":      [],
	"Armenia":        ["Hayastán"],
	"Aruba":          [],
	"Australia":      [],
	"Austria":        ["Österreich"],
	"Azerbaijan":     ["Azərbaycan"],
	"The Bahamas":    ["Bahamas"],
	"Bahrain":        ["Al-Baḥrayn"],
	"Bangladesh":     [],
	"Barbados":       [],
	"Belarus":        ["Belorussiya", "Belorussiâ"],
	"Belgium":        ["België", "Belgique", "Belgien"],
	"Belize":         [],
	"Benin":          ["Bénin"],
	"Bermuda":        [],
	"Bhutan":         ["Druk Yul"],
	"Bolivia":        ["Volívia"],
	"Bosnia and Herzegovina": ["Bosna i Hercegovina"],
	"Botswana":       [],
	"Brazil":         ["Brasil"],
	"Brunei":         [],
	"Bulgaria":       ["Bulgariya", "Bălgarija"],
	"Burkina Faso":   [],
	"Burma":          ["Myanmar"],
	"Burundi":        [],
	"Cambodia":       ["Kampuchea"],
	"Cameroon":       ["Cameroun"],
	"Canada":         [],
	"Cape Verde":     ["Cabo Verde"],
	"Cayman Islands": [],
	"Central African Republic" : ["République Centrafricaine"],
	"Chad":           ["Tchad"],
	"Chile":          [],
	"China":          [],
	"Christmas Island": [],
	"Cocos Islands":  [],
	"Colombia":       [],
	"Comoros":        ["Komori", "Comores"],
	"Congo":          [],
	"Cook Islands":   [],
	"Costa Rica":     [],
	"Cote dIvoire":   ["Côte d'Ivoire", "Cote d'Ivoire"],
	"Croatia":        ["Hrvatska"],
	"Cuba":           [],
	"Cyprus":         ["Kypros"],
	"Czech Republic": ["Česká republika", "Česko"],
	"Denmark":        ["Danmark"],
	"Djibouti":       ["Jībūtī"],
	"Dominica":       [],
	"Dominican Republic": ["República Dominicana", "Republica Dominicana"],
	"East Timor":     ["Timor Lorosa'e", "Timor-Leste"],
	"Ecuador":        [],
	"Egypt":          [],
	"El Salvador":    [],
	"Equatorial Guinea": ["Guinea Ecuatorial"],
	"Eritrea":        ["Iritriya"],
	"Estonia":        ["Eesti"],
	"Ethiopia":       ["Ityop'ia", "Ityopia"],
	"Faroe Islands":  [],
	"Fiji":           ["Viti"],
	"Finland":        ["Suomi"],
	"France":         [],
	"French Guiana":  ["Guyane"],
	"French Polynesia": ["Polynésie française"],
	"Gabon":          [],
	"The Gambia":     [],
	"Georgia":        ["Sak'art'velo"],
	"Germany":        ["Deutschland"],
	"Ghana":          [],
	"Gibraltar":      [],
	"Greece":         ["Hellas", "Ellada"],
	"Greenland":      ["Kalaallit Nunaat"],
	"Grenada":        [],
	"Guadeloupe":     [],
	"Guam":           [],
	"Guatemala":      [],
	"Guernsey":       [],
	"Guinea":         ["Guinée"],
	"Guinea-Bissau":  ["Guiné-Bissau"],
	"Guyana":         [],
	"Haiti":          ["Haïti", "Ayiti"],
	"Honduras":       [],
	"Hungary":        ["Magyarország"],
	"Iceland":        ["Ísland"],
	"India":          ["Bhārat"],
	"Indonesia":      [],
	"Iran":           ["Īrān"],
	"Iraq":           ["Al-'Iraq"],
	"Ireland":        ["Éire"],
	"Isle of Man":    ["Ellan Vannin"],
	"Israel":         ["Yisrael"],
	"Italy":          ["Italia"],
	"Jamaica":        [],
	"Japan":          ["Nippon", "Nihon"],
	"Jersey":         ["Jèrri"],
	"Jordan":         ["Al-’Urdun"],
	"Kazakhstan":     ["Qazaqstan", "Kazakhstán"],
	"Kenya":          [],
	"Kiribati":       [],
	"South Korea":    [],
	"North Korea":    [],
	"Kosovo":         ["Kosova", "Косово"],
	"Kuwait":         ["Al-Kuwayt"],
	"Kyrgyzstan":     ["Kirgizija"],
	"Laos":           ["Lao"],
	"Latvia":         ["Latvija"],
	"Lebanon":        ["Lubnān"],
	"Lesotho":        [],
	"Liberia":        [],
	"Libya":          ["Lībiyā"],
	"Liechtenstein":  [],
	"Lithuania":      ["Lietuva"],
	"Luxembourg":     ["Lëtzebuerg", "Luxembourg"],
	"Macedonia":      ["Makedonija"],
	"Madagascar":     ["Madagasikara"],
	"Malawi":         [],
	"Malaysia":       [],
	"Maldives":       ["Dhivehi Raajje"],
	"Mali":           [],
	"Malta":          [],
	"Marshall Islands": [],
	"Martinique":     [],
	"Mauritania":     ["Mauritanie"],
	"Mauritius":      [],
	"Mayotte":        [],
	"Mexico":         ["México"],
	"Federated States of Micronesia": [],
	"Moldova":        [],
	"Monaco":         [],
	"Mongolia":       [],
	"Montenegro":     ["Crna Gora"],
	"Montserrat":     [],
	"Morocco":        ["Al-Maghrib"],
	"Mozambique":     ["Moçambique"],
	"Namibia":        [],
	"Nauru":          ["Naoero", "Nauruo"],
	"Nepal":          ["Nepāla"],
	"Netherlands":    ["Nederland"],
	"New Caledonia":  ["Nouvelle-Calédonie"],
	"New Zealand":    ["Aotearoa"],
	"Nicaragua":      [],
	"Niger":          [],
	"Nigeria":        [],
	"Niue":           [],
	"Norfolk Island": [],
	"Northern Ireland": [],
	"Northern Mariana Islands": [],
	"Norway":         ["Norge", "Noreg"],
	"Oman":           [],
	"Pakistan":       [],
	"Palau":          ["Belau"],
	"Palestinian National Authority": ["Filastīn"],
	"Panama":         ["Panamá"],
	"Papua New Guinea": ["Papua Niugini"],
	"Paraguay":       ["Paraguái"],
	"Peru":           ["Perú"],
	"Philippines":    ["Pilipinas", "Filipinas"],
	"Pitcairn Islands": [],
	"Poland":         ["Polska"],
	"Portugal":       [],
	"Puerto Rico":    [],
	"Qatar":          [],
	"Reunion":        ["Réunion"],
	"Romania":        ["România"],
	"Russia":         ["Rossiya", "Rossiâ"],
	"Rwanda":         [],
	"Saint-Pierre and Miquelon": ["Saint-Pierre et Miquelon"],
	"Saint Helena":   [],
	"Saint Kitts and Nevis": [],
	"Saint Lucia":    [],
	"Saint Vincent and the Grenadines": [],
	"Samoa":          [],
	"San Marino":     [],
	"Sao Tome and Principe": ["São Tomé and Príncipe", "São Tomé e Príncipe"],
	"Saudi Arabia":   [],
	"Senegal":        ["Sénégal"],
	"Serbia":         ["Srbija"],
	"Seychelles":     ["Sesel"],
	"Sierra Leone":   [],
	"Singapore":      ["Singapura", "Singapur"],
	"Slovakia":       ["Slovensko"],
	"Slovenia":       ["Slovenija"],
	"Solomon Islands": [],
	"Somalia":        ["Soomaaliya"],
	"South Africa":   ["Suid-Afrika"],
	"South Sudan":    [],
	"South Ossetia":  ["Khussar Iryston"],
	"Spain":          ["España", "Espanya", "Espainia", "Espanha"],
	"Sri Lanka":      ["Sri Lankā"],
	"Sudan":          ["As-Sudan"],
	"Suriname":       [],
	"Svalbard":       [],
	"Swaziland":      [],
	"Sweden":         ["Sverige"],
	"Switzerland":    ["Schweiz", "Suisse", "Svizzera", "Svizra"],
	"Syria":          ["Suriyah"],
	"Taiwan":         [],
	"Tajikistan":     ["Tojikistan"],
	"Tanzania":       [],
	"Thailand":       ["Mueang Thai"],
	"Togo":           [],
	"Tokelau":        [],
	"Tonga":          [],
	"Trinidad and Tobago": [],
	"Tunisia":        ["Tunis"],
	"Turkey":         ["Türkiye"],
	"Turkish Republic of Northern Cyprus": [],
	"Turkmenistan":   ["Türkmenistan"],
	"Turks and Caicos Islands": [],
	"Tuvalu":         [],
	"Uganda":         [],
	"Ukraine":        ["Ukraїna"],
	"United Arab Emirates": ["UAE", "The Emirates"],
	"United Kingdom": ["UK", "Britain"],
	"United States":  ["USA", "America", "U.S.", "Estados Unidos", "América"],
	"Uruguay":        ["República Oriental del Uruguay"],
	"Uzbekistan":     ["O'zbekiston", "Ozbekiston"],
	"Vanuatu":        [],
	"Vatican City":   ["Civitas Vaticana", "Vatican", "vaticano"],
	"Venezuela":      [],
	"Vietnam":        [],
	"Virgin Islands": [],
	"Vojvodina":      ["Vojvodyna"],
	"Wallis and Futuna": ["Wallis-et-Futuna", "Wallis et Futuna"],
	"Yemen":          ["Al-Yaman"],
	"Zambia":         [],
	"Zimbabwe":       [],
}


def identificarPaisesEmPublicacao(urlDOI, paises):
	prefixo = ",\s*"
	doihtml = urlDOI
	listaDePaisesIdentificados = []

	for key in paises.keys():
		nomeDePais = key
		# Procuramos o nome em ingles (nome original)
		if procurarPais(doihtml, nomeDePais, prefixo):
			listaDePaisesIdentificados.append(nomeDePais)
		else:
			if len(paises[nomeDePais])>0:
				# Procuramos os nomes alternativos dos países
				for nomeAlternativoDePais in paises[nomeDePais]:
					if procurarPais(doihtml, nomeAlternativoDePais, prefixo):
						listaDePaisesIdentificados.append(nomeDePais)
						break
	return listaDePaisesIdentificados


def procurarPais(doihtml, nomeDePais, prefixo):
	nomeDePais = nomeDePais.lower()

	if re.search(prefixo+re.escape(nomeDePais)+r"\b", doihtml):
		return True
	if re.search(prefixo+re.escape(nomeDePais)+r"\Z", doihtml):
		return True
	if re.search(prefixo+re.escape(nomeDePais)+r"\W", doihtml):
		return True
	if re.search(prefixo+re.escape(nomeDePais)+r"\s", doihtml):
		return True
	return False


texto = "A, Brasil wavelet subspace method for real-time face tracking Rogerio S. Ferisa, , \
Volker Kruegerb, , Roberto M. Cesar Jr.c, , a Department of Computer Science, University of California, \
Santa Barbara, CA 93106, USA b Department of Computer Science, Aalborg University Esbjerg, Niels Bohrs \
Vej 8, 6700 Esbjerg,Denmark. Department of Computer Science,  Republica Dominicana Univ \
ersity of São Paulo, Rua do Matão 1010, 05508-900 São Paulo-SP, rasil Available online 17 September 2004. a 							\
			Signal & Image Process. Dept., CNRS UMR, Paris, France&nbsp; barusa  \
usability archilemetinium antipiperulatum  in Canada, aNGOLA,PERú,bRASilians, Panamá, chile"

texto = texto.lower()
# procurar por apenas palavras completas e nao substring



print identificarPaisesEmPublicacao(texto, paises)

