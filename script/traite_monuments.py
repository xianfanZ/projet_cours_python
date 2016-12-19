# -*- coding: utf-8 -*-
#python3

# Obtention geocoordonnées des monuments parisiens choisis
# Modélisation en geojson et xml
# Usage : python3 traite_monuments.py

from geopy.geocoders import Nominatim
from geopy.geocoders import GeoNames

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

def extract_coord(listemon):
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

def modelis_coord_xml(listemoncoord):
	"""
	Construit un fichier xml de monuments choisis et geocoordonnées
	arg : liste des monuments et coordonnées
	Retourne fichier xml 
	"""
	with open("../xml/monuments_coord.xml", "w") as sortie:
		sortie.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n")
		sortie.write("<!DOCTYPE monuments SYSTEM \"monuments_coord.dtd\">\n")
		sortie.write("<monuments>\n")
		for element in listemoncoord:
			sortie.write("\t<monument>\n")
			sortie.write("\t\t"+"<name>"+element[0]+"</name>"+"\n")
			sortie.write("\t\t"+"<coordinates>"+str(element[1])+','+str(element[2])+"</coordinates>"+"\n")
			sortie.write("\t</monument>\n")
		sortie.write("</monuments>")


def main():
	monuments = my_monuments_list("../data/liste_de_monuments.txt")
	print("Extraction coordonnées monuments...")
	monument_coordonees = extract_coord(monuments)
	print("Construction sortie geojson")
	modelis_coord_geojson(monument_coordonees)
	print("Construction sortie xml")
	modelis_coord_xml(monument_coordonees)
	print("Fin")

if __name__ == '__main__':
    main()
