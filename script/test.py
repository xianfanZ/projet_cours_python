from geopy.geocoders import Nominatim
from geopy.geocoders import GeoNames
import re,collections

def my_monuments_dico(nomfichier):
	"""
	Lecture fichier des monuments choisis.
	Retourne dictionnaire des monuments dont les clés sont les étiquettes de l'espace
	"""
	etiquettes = re.compile("(<\+>|<\+\+>|<\+\+\+>|<rectangle>)")
	my_monuments = []
	dico_monuments = collections.defaultdict(list)
	with open(nomfichier, "r") as liste_mon:
		for ligne in liste_mon:
			ligne = ligne.strip()
			if re.match(etiquettes,ligne):
				my_monuments.append((re.match(etiquettes,ligne).group(),re.sub(etiquettes,'',ligne)))
			else:
				my_monuments.append(('standard',ligne))
		for etiquette, monument in my_monuments:
			dico_monuments[etiquette].append(monument)
	return dico_monuments

dico_monuments = (my_monuments_dico("../data/liste_de_monuments.txt"))

def extract_coor_dico(dicomon):
    geolocatorOSM = Nominatim()#Open Street Maps
    geolocatorGN = GeoNames(username="nidiah")
    prob = ["Hôtel de Ville", "Pont Neuf", "Place de la Concorde"]
    dico_coord = {}
    for etiquette in dicomon:
        mon_coord = []
        for monument in dicomon[etiquette]:
            if monument not in prob:
                location = geolocatorOSM.geocode(monument)
                mon_coord.append((monument, location.latitude, location.longitude))
        dico_coord[etiquette] = mon_coord
    return dico_coord


dico_coord = extract_coor_dico(dico_monuments)

def modelis_coord_xml(dico_coord):
    """
	Construit un fichier xml de monuments choisis et geocoordonnées
	arg : liste des monuments et coordonnées
	Retourne fichier xml
	"""
    sortie = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n"
    sortie += "<!DOCTYPE monuments SYSTEM \"monuments_coord.dtd\">\n"
    sortie +="<monuments>\n"
    for etiquette in dico_coord:
        attr = etiquette.replace("<","&lt;")
        attr = attr.replace(">","&gt;")
        for element in dico_coord[etiquette]:
            sortie += "\t<monument espace='"+attr+"'>\n"
            sortie += "\t\t"+"<name>"+element[0]+"</name>"+"\n"
            sortie += "\t\t"+"<coordinates>"+str(element[1])+','+str(element[2])+"</coordinates>"+"\n"
            sortie += "\t</monument>\n"
        sortie += "</monuments>"
    with open("../xml/monuments_coord.xml", "w") as f:
        f.write(sortie)
    return


