# -*- coding: utf-8 -*-
#python3

# Interroger les données
# Usage : python3 interrog.py
# Installer matplotlib
# Données source : film_genre_pays.xml
# Résultat : comparaison tournages par pays

from lxml import etree
import matplotlib.pyplot as plt

def mk_dico_monument_pays_filtre(fichier):
	"""
	Construit dictionnaire de tournages par pays d'origine. 
	arg: fichier ../xml/films_genre_pays.xml (tournages proches d'un monument)
	sortie : dico {pays_origine: film1, film2... }
	"""
	mon_gp = {}
	with open(fichier, "r") as fichierxml:
		tree = etree.parse(fichierxml)
		payss = tree.xpath("//film/Pays_origine")
		for pays in payss:
			mon_gp.setdefault(pays.text, [])
			#print(mon_gp)
			tournages_par_pays = pays.xpath(".//parent::node()/@*") 
			for tournage in tournages_par_pays:
				#print(tournage)
				if tournage not in mon_gp[pays.text]:
					mon_gp[pays.text].append(tournage)
	#//Pays_origine[text()="France"]/parent::node()/@*
	#print(mon_gp["France"])
	return mon_gp

def mk_chart_fr_etr(dico):
	"""
	Construit un pie chart de tournages selon pays d'origine
	arg: dictionnaire de tournages par pays
	"""
	notfr = 0
	fr = 0
	na = 0
	for key in sorted(dico):
		if "France" not in key:
			if key != "N/A":
				notfr+=len(dico[key])
			else:
				na+=len(dico[key])
		else:
			fr+=len(dico[key])
	labels = ["France", "Étrangère", "N/A"]
	t = notfr+na+fr
	sizes = [fr*100/t, notfr*100/t, na*100/t]
	#explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
	fig1, ax1 = plt.subplots()
	ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
	        shadow=True, startangle=90)
	ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

	ax1.set_title("Tournages proches des monuments selon pays d'origine", fontsize=20)
	
	plt.show()

def mk_chart_france(dico):
	"""
	Construit un pie chart de tournages français et co-productions françaises
	arg: dictionnaire de tournages par pays
	"""
	di = {"France":0, "Co-production française":0}
	# Obtention des données pour le graphique
	for key in sorted(dico):
		if key == "N/A":
			pass
		elif "France" not in key:
			pass
		elif "France" == key:
			di["France"]=len(dico[key])
		else:
			di["Co-production française"]+=len(dico[key])
	total = di["France"] + di["Co-production française"]
	sizes = [ di["France"]*100/total , di["Co-production française"]*100/total ]
	labels = ["France", "Co-production française"]
	# Construction du graphique
	fig1, ax1 = plt.subplots()
	ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
	        shadow=True, startangle=90)
	ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
	ax1.set_title("Tournages proches des monuments\nProductions et co-productions françaises", fontsize=20)

	plt.show()

def main():
	dico_filtre = mk_dico_monument_pays_filtre("xml/films_genre_pays.xml")
	"""print("Construction chart tournages français/étranger")
	mk_chart_fr_etr(dico_filtre)"""
	print("Construction chart tournages français/co-productions françaises")
	mk_chart_france(dico_filtre)


		
if __name__ == '__main__':
	main()

