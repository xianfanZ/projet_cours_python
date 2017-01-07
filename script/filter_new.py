# _*_ coding:utf-8_*_

from geopy.distance import vincenty
from lxml import etree

"""on va éliminer les leux de tournage qui ne sont proche à aucun monument"""

def get_coor_monuments():
	"""créer un dico dont la clé est le type de momument, la valeur est une liste de coordonnées
	return (dico)"""

	dico = {}
	tree_monuments = etree.parse("../xml/monuments_coord.xml") #parser le fichier xml de monuments 
	nodes_monu = tree_monuments.xpath("/monuments/monument") # aller dans les noeuds monument
	for monument in nodes_monu: # pour chaque noeud monument
		name = [name.text for name in monument.iterchildren(tag="name")][0] #obtenir la liste de noms des monuments
		#print (name)
		p1 = None
		attribut = monument.get('espace') #obtenir le type de radius
		for coor in monument.iterchildren(tag="coordinates"): #obtenir la coordonée du monument
			coor1, coor2=coor.text.split(",")
			p1= (float(coor1), float(coor2))
			#print (p)
		dico.setdefault(attribut, [ ]).append((p1, name))
	#print (dico)
	return (dico)


def get_idfilm_far(standard):

	"""éliminer les noeuds films sui ne sont proche à aucun monument selon l'id du film"""

	file = "../xml/filter_coord_films_new.xml"# créer un nouveau fichier pour le résultat
	tree= etree.parse("../xml/film_final.xml")
	films = tree.xpath("/tournagesdefilmsparis2011/film")
	for film in films:
		parent_node = film.getparent()
		if film.get("id") not in [item[0] for item in standard]: # si l'id du film n'est pas dans la liste 
			parent_node.remove(film)
		else:
			for i in standard:
				if i[0] == film.get("id"):
					child1= etree.SubElement(film, "Monument_proche", type_radius=i[2])#ajouter les nouveaux noeuds et l'attribut
					child1.text = i[1] #ajouter le texte entre les balises
	tree.write(file)
	


def calcul_distance(dico_film):

	""" trouver le momument qui est le plus proche pour chaque film et calculer la distance. 
	Et puis, faire un dico {"idFilm":(distance, type de radius)}, le type de radius et le type de 
	radius du momument qui sont le plus proche  du film. A la fin, on récupérer les Id des films qui ne 
	conforment pas à nos critères"""

	dico = get_coor_monuments()
	dico_dis_min={}
	for id_film, p2 in dico_film.items(): #récupérer l'id du film et la coordonée du film
		dico_comparer = {}
		for key, value in dico.items(): #pour récupérer la coordonée du momument
			for chaque_value in value:
				p1 = chaque_value[0]
				distance = vincenty(p1, p2).meters #calculer la distance
				dico_comparer.setdefault(id_film, []).append((distance, key, chaque_value[1]))# créer le nouveau dico
		#print (dico_comparer)
		for liste in dico_comparer.values():
			v = [(element[0], element[2], element[1]) for element in liste ]
			v.sort()
			distance_min = v[0] #trouver le momument le plus proche
			dico_dis_min[id_film] = distance_min
	standard=[]
	unPlus=[]
	deuxPlus=[]
	troisPlus=[]
	#filtrer les films
	for key in dico_dis_min:
		if dico_dis_min[key][2] =='standard' and dico_dis_min[key][0] <10*19:
			standard.append((key, dico_dis_min[key][1],dico_dis_min[key][2]))
		elif dico_dis_min[key][2] =='<+>' and dico_dis_min[key][0] < 15*19:
			unPlus.append((key, dico_dis_min[key][1],dico_dis_min[key][2]))
		elif dico_dis_min[key][2] == '<++>' and dico_dis_min[key][0]<20*19:
			deuxPlus.append((key, dico_dis_min[key][1],dico_dis_min[key][2]))
		elif dico_dis_min[key][2] == '<+++>' and dico_dis_min[key][0] < 25*19:
			troisPlus.append((key,dico_dis_min[key][1],dico_dis_min[key][2]))
	#concaténer les quatre listes en un
	standard.extend(unPlus)
	standard.extend(deuxPlus)
	standard.extend(troisPlus)
	get_idfilm_far(standard)

		

def get_coor_films():
	"""obtenir les coordonnées des lieux de tournage"""
	tree_film = etree.parse("../xml/film_final.xml")
	nodes_film = tree_film.xpath("/tournagesdefilmsparis2011/film")
	dico_film={}
	for film in nodes_film:
		id_film = film.get('id')
		for coora in film.iterchildren(tag="geo1"):
			coor_a = float(coora.text) # changer le type 
		for coorb in film.iterchildren(tag="geo2"):
			coor_b = float(coorb.text)
		p2 = (coor_a, coor_b)
		dico_film[id_film]=p2
	calcul_distance(dico_film)
get_coor_films()	