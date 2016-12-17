# -*- coding: utf-8 -*-

from lxml import etree

def delet_deo_vide():
	file = "film_changed.xml"
	tree = etree.parse("film2011.xml")
	node_geos = tree.xpath("/tournagesdefilmsparis2011/film/geo_coordinates")
	for node_geo in node_geos:
		if node_geo.text == None:
			parent_node = node_geo.getparent()
			print (parent_node)
			parent_node.clear()
	for film in tree.xpath("/tournagesdefilmsparis2011/film"):
		if len(film) == 0:
			film.getparent().remove(film)
	tree.write(file)

def separat_geo():
	delet_deo_vide()
	file_xml_final = "film_final.xml"
	tree = etree.parse("film_changed.xml")
	node_geos = tree.xpath("/tournagesdefilmsparis2011/film/geo_coordinates")
	for node_geo in node_geos:
		geo1, geo2 = node_geo.text.split(",")
		parent_node = node_geo.getparent()
		parent_node.remove(node_geo)
		#node = etree.Element(parent_node)
		child1 = etree.SubElement(parent_node, "geo1")
		child2 = etree.SubElement(parent_node, "geo2")
		child1.text = geo1
		child2.text = geo2
	tree.write(file_xml_final)
separat_geo()