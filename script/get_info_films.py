#-*- coding: utf-8 -*-
#python3

# Obtention de plus d'informations sur les films qui sont à proximité des monuments
# Installer omdb wrapper https://github.com/dgilland/omdb.py 

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
		# nouveau fichier xml avec infos de genre et pays
		
		print("Obtention du genre et du pays d'origine depuis OMBD...")
		# requete sur OMDB pour obtenir plus d'infos sur chaque film
		# on cherche par directeur aussi pour eviter deux films différents avec le meme titre
		genres= []
		payss= []
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
				genres.append(genre)
				payss.append(pays)
		print("Fin.")
		return genres, payss
		sortie.close()


def ajoute_newinfo(liste1, liste2):
	entree = open("../xml/film_final.xml", "r")
	sortie = "../xml/films_genre_pays.xml"
	tree = etree.parse(entree)
	node_films = tree.xpath("/tournagesdefilmsparis2011/film")
	for node, genre, pays in zip(node_films, liste1, liste2):
		node_genre = etree.SubElement(node, "Genre") # nouveau noeud <Genre>
		node_pays = etree.SubElement(node, "Pays_origine") # nouveau noeud <Pays>
		node_genre.text = genre  
		node_pays.text = pays
	tree.write(sortie)


def main():
	g, p = get_info_film("/Users/nidiahernandez/Desktop/projet_cours_python/xml/film_final.xml")
	ajoute_newinfo(g, p)
if __name__ == '__main__':
	main()


