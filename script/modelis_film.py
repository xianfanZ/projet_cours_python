# -*- coding: utf-8 -*-

# Modélisation xml des tournages : 
# 1. filtrage des films qui n'ont pas des coordonnées,
# 2. split du noeud coordonnées en 2 (un pour latitude, un autre pour longitude)
# Usage : python3 get_info_films.py
# Installer lxml (http://lxml.de/index.html)
# Résultat : ../xml/film_final.xml

from lxml import etree

def delet_geo_vide():
	n = 1
	file = "../xml/film_changed.xml" #créer un nouveau fichier
	tree = etree.parse("../xml/film2011.xml") # parser le fichier xml à traiter
	node_geos = tree.xpath("/tournagesdefilmsparis2011/film/geo_coordinates")#aller au noeud "geo_coordinates"
	for node_geo in node_geos:
		if node_geo.text == None: # si le noeud geo_coordinates" est vide
			parent_node = node_geo.getparent()# aller à son noeud parent "film"
			#print (parent_node)
			parent_node.clear() #enlever tous les noeud fils du noeud "film"
	#enlever les noeud "film" vide
	for film in tree.xpath("/tournagesdefilmsparis2011/film"):
		if len(film) == 0: 
			film.getparent().remove(film)
		else:
			film.set('id', str(n))
			n+=1
	tree.write(file)

def separat_geo():
	delet_geo_vide()
	file_xml_final = "../xml/film_final.xml"
	tree = etree.parse("../xml/film_changed.xml")
	node_geos = tree.xpath("/tournagesdefilmsparis2011/film/geo_coordinates")
	#séparer le géocoord.
	for node_geo in node_geos:
		geo1, geo2 = node_geo.text.split(",")#séparer les geocoord
		parent_node = node_geo.getparent()
		parent_node.remove(node_geo)# enlever le noeud geo_coordinates
		#node = etree.Element(parent_node)
		child1 = etree.SubElement(parent_node, "geo1") #ajouter un nouveau noeud comme fils du noeud film
		child2 = etree.SubElement(parent_node, "geo2")
		child1.text = geo1 
		child2.text = geo2
	tree.write(file_xml_final) #write le résultat dans un nouveau fichier
separat_geo()
