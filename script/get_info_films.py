#-*- coding: utf-8 -*-
#python3

# installer omdb wrapper https://github.com/dgilland/omdb.py 

from lxml import etree
import omdb


"""
Obtenir plus d'infos sur les films à partir d'Open Movie Database
"""
films = []
with open("../xml/film_final.xml", "r") as fichierxml:
	tree = etree.parse(fichierxml)
	ti = tree.xpath("//film/Titre")
	"""rel = tree.xpath("//film/Realisateur")
	for titre, realisateur in zip(ti, rel):
		films.append( (titre.text, realisateur.text) )"""
	for titre in ti:
		films.append(titre.text)
	#print(films)

	for film in films:
		search = omdb.search(film, timeout=20)
		print(search)







