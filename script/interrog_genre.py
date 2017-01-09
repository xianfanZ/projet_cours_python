# -*- coding: utf-8 -*-
#python3

# Obtention du genre préféré par monument
# Usage : python3 interrog.py
# Installer 
# Données source : ../xml/film_genre_pays.xml
# Résultat : genre préféré par monument

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

def mk_dico_genre_prefere(dico_monument_genre):
	"""
	Construit dictionnaire de genres préférés par monument.
	param: dictionnaire {monument: {genre, nº tournages}
	return: dico {monument: genre préféré}
	"""
	dico_genre_prefere = {}
	for key in dico_monument_genre:
		sorted_k = sorted(dico_monument_genre[key], key=(dico_monument_genre[key]).get, reverse=True)
		if sorted_k[0] == "N/A":
			dico_genre_prefere[key] = sorted_k[1]
		else:
			dico_genre_prefere[key] = sorted_k[0]
	return dico_genre_prefere



def main():
	print("Calcul du nombre de tournages de chaque genre par monument...")
	dico = mk_dico_monument_genre("../xml/films_genre_pays.xml")
	print("Genre préféré par monument :\n")
	dico2 = mk_dico_genre_prefere(dico)
	for key2 in dico2:
		print("{} {}\n".format(key2, dico2[key2]) )



if __name__ == '__main__':
	main()

