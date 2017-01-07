#-*- coding: utf-8 -*-
#python3

# Obtention de plus d'informations sur les tournages qui sont à proximité des monuments
# Usage : python3 get_info_films.py
# Installer omdb wrapper (https://github.com/dgilland/omdb.py)
# Résultat : films_genre_pays.xml

from lxml import etree
import omdb
import json

def get_info_film(fichier):
	"""
	Obtenir plus d'infos sur les films (pays d'origine et genre) à partir d'Open Movie Database
	arg: fichier xml des tournages de films
	sortie: fichier xml de tournages avec info de genre et pays
	"""
	# creation liste des films auxquels on est intérésées
	films = []
	# obtention titre et realisateur a partir de notre fichier de films
	with open(fichier, "r") as fichierxml:
		tree = etree.parse(fichierxml)
		ti = tree.xpath("//film/Titre")
		rel = tree.xpath("//film/Realisateur") 
		for titre, realisateur in zip(ti, rel):
			films.append( (titre.text, realisateur.text) )
		print("Collecte des données depuis OMBD...")
		genres= [] #liste de genres de tous les tournages
		payss= [] #liste de pays de tous les tournages
		# requete sur OMDB pour obtenir plus d'infos sur chaque film
		# on cherche par directeur aussi pour eviter deux films différents avec le meme titre
		for film, realisateur in films:	
			res = omdb.request(t=film, director=realisateur) 
			infofilm = json.loads( (res.content).decode("utf-8") )
			try:
				genre = infofilm["Genre"]
			except KeyError:
				genre = "N/A"
			try:
				pays = infofilm["Country"]
			except KeyError:
				pays = "N/A"
			finally:
				print(film, genre, pays)
				genres.append(genre)
				payss.append(pays)
		print("Fin.")
		return genres, payss


def ajoute_newinfo(liste1, liste2):
	"""
	Ajoute deux noeuds à la modélisation des tournages.
	Args: liste de genres de chaque tournage, liste de pays d'origine de chaque tournage
	Sortie: modélisation xml pour les tournages avec info de genre et de pays
	"""
	# tournages proches d'un monument
	entree = open("../xml/filter_coord_films_new.xml", "r")
	# nouveau fichier xml avec infos de genre et pays
	sortie = open("../xml/films_genre_pays.xml", "w")
	tree = etree.parse(entree)
	# ajout de nouvelles infos à chaque tournage
	node_films = tree.xpath("/tournagesdefilmsparis2011/film")
	for node, genre, pays in zip(node_films, liste1, liste2):
		node_genre = etree.SubElement(node, "Genre") # nouveau noeud <Genre>
		node_pays = etree.SubElement(node, "Pays_origine") # nouveau noeud <Pays>
		node_genre.text = genre # contenu du noeud = info obtenu d'OMDB
		node_pays.text = pays
	tree.write(sortie)
	entree.close()
	sortie.close()


def main():
	print("Obtention du genre et du pays d'origine des tournages")
	g, p = get_info_film("../xml/filter_coord_films_new.xml") # Obtention des infos pour les tournages proches d'un monument
	print("Modélisation des informations obtenues en xml")
	ajoute_newinfo(g, p)
	print("Voir résultat sur 'filter_genre_pays.xml'")

if __name__ == '__main__':
	main()
