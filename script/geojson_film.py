import json
from lxml import etree

#def transfer_xml_json():

def write_in_file_json(list_json):
	with open("film.json", "w") as fo:
		content = "{"+str(list_json) +"}"
		fo.write(content)

def json_film(file_name):
	tree = etree.parse(file_name)
	nodes_film = tree.xpath("/tournagesdefilmsparis2011/film")
	list_json = []
	for node_film in nodes_film:
		dic_film = {}
		for child in node_film.getchildren():
			json_child = {}
			child_tag = child.tag
			chilld_text = child.text
			dic_film[child_tag] = chilld_text
		list_json.append(dic_film)
	#write_in_file_json(list_json)
json_film("film_final.xml")

