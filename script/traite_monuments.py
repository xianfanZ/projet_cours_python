# -*- coding: utf-8 -*-
#python3

# Traitement des fichiers des geocoordonnées des monuments de la France pour obtenir les coordonnées 
# des monuments parisiens choisis

from geopy.geocoders import Nominatim

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
	Retourne fichier geojson de monuments choisis et geocoordonnées 
	"""
	with open("../json/monuments_coord.geojson", "w") as sortie:
		sortie.write( "{\"type\":\"FeatureCollection\",\"features:\"\n\n[\n\n")
		geolocator = Nominatim()
		for monument in listemon:
			#location = geolocator.geocode(monument, geometry="geojson") La sortie geojson de geopy est trop verbeuse et rend des coordonnées de polygones
			#print(location.raw)
			location = geolocator.geocode(monument)
			sortie.write( "{\"type\": \"Feature\",\n" )
			sortie.write( " \"geometry\": {\n" )
			sortie.write( "   \"type\": \"Point\",\n" )
			sortie.write( "   \"coordinates\": "+ str([location.latitude, location.longitude] )+"\n },\n" )
			sortie.write( " \"properties: {\n" )
			sortie.write( "   \"name\": \""+monument+"\"\n }\n},\n\n" )
		sortie.write("]")

def extract_coord_xml(listemon):
	with open("../xml/monuments_coord.xml", "w") as sortie:
		sortie.write("<monuments>")
		geolocator = Nominatim()
		for monument in listemon:
			location = geolocator.geocode(monument)
			sortie.write("\t<monument>\n")
			sortie.write("\t\t"+"<name>"+monument+"</name>"+"\n")
			sortie.write("\t\t"+"<coordinates>"+str(location.latitude)+','+str(location.longitude)+"</coordinates>"+"\n")
			sortie.write("\t</monument>\n")
		sortie.write("</monuments>")


def main():
	monuments = my_monuments_list("../data/liste_de_monuments.txt")
	extract_coord(monuments)
	extract_coord_xml(monuments)

if __name__ == '__main__':
    main()
