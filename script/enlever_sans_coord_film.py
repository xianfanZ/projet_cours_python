# -*- coding: utf-8 -*-
#python3

# Synopsis :
# Usage :

from lxml import etree

file = "xml/film_changed.xml"
tree = etree.parse("data/film2011.xml")
node_geos = tree.xpath("/tournagesdefilmsparis2011/film/geo_coordinates")
for node_geo in node_geos:
	if node_geo.text == None:
		parent_node = node_geo.getparent()
		print (parent_node)
		parent_node.clear()
tree.write(file)

