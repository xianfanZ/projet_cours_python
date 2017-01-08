# -*- coding: utf-8 -*-
#python3

# Interroger les données
# Usage : python3 interrog.py
# Installer 
# Données source : film_genre_pays.xml
# Résultat : stats

from lxml import etree

def mk_dico_monument_genre(fichier):
	"""
	Construit dictionnaire de genres par monument. 
	arg: fichier ../xml/films_genre_pays.xml
	sortie : dico {monument: {genre, nº tournages}
	"""
	mon_gp = {}
	with open(fichier, "r") as fichierxml:
		tree = etree.parse(fichierxml)
		monuments = tree.xpath("//film/Monument_proche")
		for monument in monuments:
			mon_gp.setdefault(monument.text, {})
			# on est situés dans le noeud 'Monument proche' de chaque tournage
			# on obtient les genres correspondant à chaque monument
			genres_par_monument = monument.xpath(".//following-sibling::node()[1]") 
			for genre in genres_par_monument:
				if genre.text not in mon_gp[monument.text]:
					mon_gp[monument.text][genre.text] = 1 
				else:
					mon_gp[monument.text][genre.text]+= 1 
	#//Monument_proche[text()="Centre Pompidou"]/following-sibling::node()[1]/text()
	#print(mon_gp["Centre Pompidou"])
	return mon_gp


def main():
	dico = mk_dico_monument_genre("/Users/nidiahernandez/Desktop/projet_cours_python/xml/films_genre_pays.xml")
	for key in dico:
		sorted_k = sorted(dico[key], key=(dico[key]).get, reverse=True)
		print("Monument : {}".format(key))
		try:
			sorted_k[0] == "N/A"
			print("Genre péféré: {}".format(sorted_k[1]))
		except:
			print("Genre péféré: {}".format(sorted_k[0]))

if __name__ == '__main__':
	main()

