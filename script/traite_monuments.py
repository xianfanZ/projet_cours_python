# -*- coding: utf-8 -*-
#python3

# Obtention geocoordonnées des monuments parisiens choisis
# Modélisation en geojson et xml
# Usage : python3 traite_monuments.py

from geopy.geocoders import Nominatim
from geopy.geocoders import GeoNames
import re,collections

def my_monuments_list(nomfichier):
	"""
	Lecture fichier des monuments choisis.
	Retourne liste des monuments.
	"""
	my_monuments = []
	with open(nomfichier, "r") as liste_mon:
		for ligne in liste_mon:
			ligne = ligne.strip()
			my_monuments.append(ligne)
	return my_monuments

def my_monuments_dico(nomfichier):
	"""
	Lecture fichier des monuments choisis.
	Retourne dictionnaire des monuments dont les clés sont les étiquettes de l'espace
	"""
	etiquettes = re.compile("(<\+>|<\+\+>|<\+\+\+>|<rectangle>)")
	my_monuments = []
	dico_monuments = collections.defaultdict(list)
	with open(nomfichier, "r") as liste_mon:
		for ligne in liste_mon:
			ligne = ligne.strip()
			if re.match(etiquettes,ligne):
				my_monuments.append((re.match(etiquettes,ligne).group(),re.sub(etiquettes,'',ligne)))
			else:
				my_monuments.append(('standard',ligne))
		for etiquette, monument in my_monuments:
			dico_monuments[etiquette].append(monument)
	return dico_monuments

def extract_coord_list(listemon):
	"""
	Extraction des coordonnées des monuments recherchés.
	arg : liste des monuments choisis
	Retourne : liste de tuples (monument, latitude, longitude)
	"""
	geolocatorOSM = Nominatim()#Open Street Maps
	geolocatorGN = GeoNames(username="nidiah")
	prob = ["Hôtel de Ville", "Pont Neuf", "Place de la Concorde"]#obtention de coordonnees erronnées avec Open Street Maps
	mon_coord = []
	for monument in listemon:
		if monument not in prob:
			location = geolocatorOSM.geocode(monument)#coordonnées avec Open Street Maps
			mon_coord.append( (monument, location.latitude, location.longitude) )
		else:
			location = geolocatorGN.geocode(monument)#coordonnées avec GeoNames
			mon_coord.append( (monument, location.latitude, location.longitude) )
	return mon_coord

def extract_coord_dico(dicomon):
	"""
	Extraction des coordonnées des monuments recherchés.
	arg : dictionnaire des monuments choisis et les étiquette de l'espace
	Retourne : dictionnaire de tuples etiquette d'espace: [(monument, latitude, longitude),...]
	"""
	# Le même méthode d'extraction que la fonction extract_coord_list(listmon)
	geolocatorOSM = Nominatim()
	geolocatorGN = GeoNames(username="nidiah")
	prob = ["Hôtel de Ville", "Pont Neuf", "Place de la Concorde"]
	dico_coord = {}
	for etiquette in dicomon:
		mon_coord = []
		for monument in dicomon[etiquette]:
			if monument not in prob:
				location = geolocatorOSM.geocode(monument)
				mon_coord.append((monument, location.latitude, location.longitude))
		dico_coord[etiquette] = mon_coord
	return dico_coord

def modelis_coord_geojson(listemoncoord):
	"""
	Construit un fichier geojson de monuments choisis et geocoordonnées
	arg : liste des monuments et coordonnées
	Retourne fichier geojson
	"""
	with open("../json/monuments_coord.geojson", "w") as sortie:
		sortie.write( "{\"type\":\"FeatureCollection\", \"features\":\n\n [ " )
		for element in listemoncoord:
			sortie.write( "{\"type\": \"Feature\", " )
			sortie.write( "\"geometry\": { " )
			sortie.write( "\"type\": \"Point\", " )
			sortie.write( "\"coordinates\": "+ str([element[1], element[2]])+" }, " )
			sortie.write( "\"properties\": { " )
			sortie.write( "\"name\": \""+element[0]+"\" } },\n\n" )
		sortie.write(" ] }")

def modelis_coord_xml(dico_coord):
    """
	Construit un fichier xml de monuments choisis et geocoordonnées
	arg : liste des monuments et coordonnées
	Retourne fichier xml
	"""
    sortie = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n"
    sortie += "<!DOCTYPE monuments SYSTEM \"../grammaire/monuments_coord.dtd\">\n"
    sortie +="<monuments>\n"
    for etiquette in dico_coord:
		# Les balises d'étiquette doivent être remplacé par les entités
        attr = etiquette.replace("<","&lt;")
        attr = attr.replace(">","&gt;")
        for element in dico_coord[etiquette]:
            sortie += "\t<monument espace='"+attr+"'>\n"
            sortie += "\t\t"+"<name>"+element[0]+"</name>"+"\n"
            sortie += "\t\t"+"<coordinates>"+str(element[1])+','+str(element[2])+"</coordinates>"+"\n"
            sortie += "\t</monument>\n"
    sortie += "</monuments>"
    with open("../xml/monuments_coord.xml", "w") as f:
        f.write(sortie)
    return


def main():
	monuments = my_monuments_dico("../data/liste_de_monuments.txt")
	print("Extraction coordonnées monuments...")
	monument_coordonees = extract_coord_dico(monuments)
	print("Construction sortie geojson")
	modelis_coord_geojson(monument_coordonees)
	print("Construction sortie xml")
	modelis_coord_xml(monument_coordonees)
	print("Fin")

if __name__ == '__main__':
    main()
