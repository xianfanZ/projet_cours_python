# -*- coding: utf-8 -*-
#python3

# Traitement des fichiers des geocoordonnées des monuments de la France pour obtenir les coordonnées 
# des monuments parisiens choisis

from lxml import etree

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

def extract_coord_1(listemon, fichiermon): # pas finie. Parsing avec module?
	"""
	Traitement fichier json geocoordonnées des monuments de la France.
	Extraction des coordonnées des monuments recherchés.
	args : liste des monuments choisis, nom fichier coordonnées json
	"""
	with open("monuments-nettoye.json", "w") as sortie:
		entree = open(fichiermon, "r").read()
		entree = entree.replace("\\u00e9", "é")
		entree = entree.replace("\\u00e8", "è")
		entree = entree.replace("\\u00f4", "ô")
		entree = entree.replace("\\u00c9", "É")
		entree = entree.replace("\\u00e2", "â")
		sortie.write(entree)
	#for element in listemon:
	#	if element in entree:
	#		print(element)
	sortie.close()

def extract_coord_2(listemon, fichiermon2): # Finalement, cette fonction ne sert à rien parce que  
											# le fichier monuments.odt ne contient qu'un seul des monuments recherchés
	"""
	Traitement deuxième fichier geocoordonnées des monuments de la France.
	Extraction des coordonnées des monuments recherchés.
	args: liste des monuments choisis, content.xml issu du fichier odt des monuments
	"""
	tree = etree.parse(fichiermon2)
	# on utilise xpath pour recuperer le contenu textuel du fichier
	elements = tree.xpath("//office:body/office:spreadsheet/table:table/table:table-row/table:table-cell/text:p",
                  namespaces={"office":"urn:oasis:names:tc:opendocument:xmlns:office:1.0",
                              "table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0",
                              "text":"urn:oasis:names:tc:opendocument:xmlns:text:1.0"})
	
	els= [] # contenu textuel de chaque cellule
	for elem in elements:
		els.append(elem.text)

	for el in els:
		if el in listemon: 
			lat = els.index(el)+1
			lon = els.index(el)+2
			print(el, els[lat], els[lon])



def main():
	monuments = my_monuments_list("liste_de_monuments.txt")
	extract_coord_1(monuments, "monuments.json")
	#extract_coord_2(monuments, "content.xml")

if __name__ == '__main__':
    main()