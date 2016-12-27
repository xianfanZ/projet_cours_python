# _*_ coding:utf-8_*_

from geopy.distance import vincenty
from lxml import etree


def get_coor_monuments(file_name):
	dico = {}
	tree_monuments = etree.parse("/Users/wangyizhe/Desktop/projetPy/monuments_coord.xml")
	nodes_monu = tree_monuments.xpath("/monuments/monument")
	for monument in nodes_monu:
		name = [name.text for name in monument.iterchildren(tag="name")][0]
		#print (name)
		p1 = None
		attribut = monument.get('espace')
		for coor in monument.iterchildren(tag="coordinates"):
			coor1, coor2=coor.text.split(",")
			p1= (float(coor1), float(coor2))
			#print (p)
		dico.setdefault(attribut, [ ]).append(p1)
	return (dico)


def get_idfilm_far(dico_dis_min):
	
	


def calcul_distance(dico_film):
	dico = get_coor_monuments("/Users/wangyizhe/Desktop/projetPy/monuments_coord.xml")
	dico_dis_min={}
	for id_film, p2 in dico_film.items():
		dico_comparer = {}
		for key, value in dico.items():
			for p1 in value:
				distance = vincenty(p1, p2).meters
				dico_comparer.setdefault(id_film, []).append((distance, key))
		for v in dico_comparer.values():
			v.sort()
			distance_min = v[0]
			#print (distance_min)
			dico_dis_min[id_film] = distance_min
	get_idfilm_far(dico_dis_min)
	#return (dico_dis_min)
		
		
		#print (dico_comparer)




def get_coor_films():

	tree_film = etree.parse("/Users/wangyizhe/Desktop/projetPy/film_final.xml")
	nodes_film = tree_film.xpath("/tournagesdefilmsparis2011/film")
	dico_film={}
	for film in nodes_film:
		id_film = film.get('id')
		for coora in film.iterchildren(tag="geo1"):
			coor_a = float(coora.text)
		for coorb in film.iterchildren(tag="geo2"):
			coor_b = float(coorb.text)
		p2 = (coor_a, coor_b)
		dico_film[id_film]=p2
	#print (dico_film)
	calcul_distance(dico_film)

		#distance = vincenty(p1, p2).meters
		#print(distance)
		#if distance > ????????????:
get_coor_films()		





	


