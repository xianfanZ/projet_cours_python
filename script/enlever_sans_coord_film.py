# -*- coding: utf-8 -*-
#python3

# Élimine les tournages qui n'ont pas des géocoordonnées.
# Usage : python3 enlever_sans_coord_film.py
# Installer lxml (http://lxml.de/index.html)
# Résultat : film_changed.xml

from lxml import etree

sortie = "../xml/film_changed.xml"
tree = etree.parse("../data/film2011.xml") # Entrée = fichier obtenu sur opendata.paris.fr
node_geos = tree.xpath("/tournagesdefilmsparis2011/film/geo_coordinates")
for node_geo in node_geos:
	if node_geo.text == None:
		parent_node = node_geo.getparent()
		print (parent_node)
		parent_node.clear()
tree.write(sortie)

