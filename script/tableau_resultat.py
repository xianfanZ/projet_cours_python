#coding:utf-8

from lxml import etree
from collections import OrderedDict
import traite_monuments,math

tree = etree.parse("../xml/filter_coord_films_new.xml")
dico_monuments = {}
dico_espace_monuments = traite_monuments.my_monuments_dico("../data/liste_de_monuments.txt")

for elem in tree.iter(tag='Momument_proche'):
    dico_monuments[elem.text] = dico_monuments.get(elem.text,0)+1
dico_monuments = OrderedDict(sorted(dico_monuments.items(), key=lambda t: t[1],reverse=True))
somme_films = sum(dico_monuments.values())

sortie = "<!DOCTYPE html SYSTEM \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n"
sortie += "<html xmlns=\"http://www.w3.org/1999/xhtml\">\n"
sortie += "\t<head><title>Tableau récapitulatif</title><meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" /><link rel=\"stylesheet\" type=\"text/css\" href=\"./css/table.css\"/></head>\n"
sortie += "\t<body><div class=\"ficheResult\" align=\"center\"><h2>Fiche récapitulative des résultats obtenus</h2><table class=\"table_result\">\n"
sortie += "\t\t<tr><th>Espace</th><th>monument</th><th>nb tournages</th><th>pourcentage</th></tr>\n"


for niv in dico_espace_monuments:
    list_monuments = dico_espace_monuments[niv]
    lignespan = len(list_monuments)
    print(niv,lignespan)
    if niv == "standard":
        sortie += "\t\t\t<tr><td rowspan=\"{}\">{}m<sup>2</sup></td>".format(lignespan,int(10*19**2*math.pi))
    elif niv == "<+>":
        sortie += "\t\t\t<tr><td rowspan=\"{}\">{}m<sup>2</sup></td>".format(lignespan,int(15*19**2*math.pi))
    elif niv == "<++>":
        sortie += "\t\t\t<tr><td rowspan=\"{}\">{}m<sup>2</sup></td>".format(lignespan,int(20*19**2*math.pi))
    else:
        sortie += "\t\t\t<tr><td rowspan=\"{}\">{}m<sup>2</sup></td>".format(lignespan,int(25*19**2*math.pi))
    cpt = 1
    for monument in list_monuments:
        if monument in dico_monuments:
            pourcentage = dico_monuments[monument]/somme_films
            if cpt == 1:
                sortie += "<td>{}</td><td>{}</td><td>{:.2%}</td></tr>\n".format(monument,dico_monuments[monument],pourcentage)
            else:
                sortie += "\t\t\t<tr><td>{}</td><td>{}</td><td>{:.2%}</td></tr>\n".format(monument,dico_monuments[monument],pourcentage)
        else:
            sortie += "\t\t\t<tr><td>{}</td><td>{}</td><td></td></tr>\n".format(monument,0)
        cpt += 1
sortie += "\t</table></div></body></html>"

with open("../web/tableu.html","w") as f:
    f.write(sortie)
