# -*- coding: utf-8 -*-

# Construction du tableau de résultats
# Usage : python3 tableau_resultat.py
# Installer lxml (http://lxml.de/index.html)
# Résultat : ../web/tableu.html

from lxml import etree
import traite_monuments,math,interrog_genre,table_classe_annee
import pandas as pd



niv_espace = {
    "standard" : 11341,
    "<+>" : 17011,
    "<++>" : 22682,
    "<+++>" : 28352,
}


def mk_dico_monuments(nomfichier):
    """
    Construit dictionnaire de monuments avec le nombre de tournages d'à côté
    :param nomfichier: "../xml/filter_coord_films_new.xml"
    :return:dictionnaire de monument: dico_monuments{monument : nb_tournages}
    """
    dico_monuments = {}
    tree = etree.parse(nomfichier)
    for elem in tree.iter(tag='Monument_proche'):
        dico_monuments[elem.text] = dico_monuments.get(elem.text,0)+1
        #dico_monuments = OrderedDict(sorted(dico_monuments.items(), key=lambda t: t[1],reverse=True))
    return dico_monuments

def traite_valeur_vide(liste_monuments,mon_dico):
    """
    Ajouter les monuments qui ne sont pas dans un dictionnaire en metant une valeur vide
    :param un dictionnare qui manque des monuments
    :return: un nouveau dictionnaire avec tous les monuments dans la liste
    """
    new_dico = {}
    for monument in liste_monuments:
        if monument not in mon_dico:
            new_dico[monument] = ""
        else:
            new_dico[monument] = mon_dico[monument]
    return new_dico



def modelis_donnee():
    """
    Comninaison des tous les imformation sur les monuments dans un DataFrame
    :return: un DataFrame
    (obsolète)
    """
    #----------------------------------------------------------------------
    # créer le dictionnare de structure {monument:espace}
    #----------------------------------------------------------------------
    dico_espace_monuments = traite_monuments.my_monuments_dico("../data/liste_de_monuments.txt")
    for k in dico_espace_monuments:
        if k in niv_espace:
            dico_espace_monuments[niv_espace[k]] = dico_espace_monuments.pop(k)
    dico_monuments_espace = {} # inverser le clé et la valeur du dico_espace_monument{espace:[liste_monuments]}
    for espace, list_monuments in dico_espace_monuments.items():
        for monument in list_monuments:
            dico_monuments_espace[monument] = espace #dico_monuments_espace{monument:espace}
    liste_monuments = list(dico_monuments_espace.keys()) # créer la liste contenant tous les monuments

    #----------------------------------------------------------------------
    # créer le dictionnare de structure {monument:nb_tournages}
    #----------------------------------------------------------------------
    dico_monuments = mk_dico_monuments("../xml/filter_coord_films_new.xml")
    somme_films = sum(dico_monuments.values())
    dico_monuments = traite_valeur_vide(liste_monuments,dico_monuments)

    #----------------------------------------------------------------------
    # créer le dictionnare de structure {monument:pourcentage}
    #----------------------------------------------------------------------
    dico_pourcentage = {}
    for key, value in dico_monuments.items():
        if value != "":
            dico_pourcentage[key] = dico_monuments[key]/somme_films
        else:
            dico_pourcentage[key] = ''

    #----------------------------------------------------------------------
    # créer le dictionnare de structure {monument:genre_preféré}
    #----------------------------------------------------------------------
    dico_genre_prefere = interrog_genre.mk_dico_genre_prefere(interrog_genre.mk_dico_monument_genre("../xml/films_genre_pays.xml"))
    dico_genre_prefere = traite_valeur_vide(liste_monuments,dico_genre_prefere)

    #----------------------------------------------------------------------
    # construire un DataFrame
    #----------------------------------------------------------------------
    infos = ['espace','nb_tournages','pourcentage','genre_prefere']
    df = pd.DataFrame([dico_monuments_espace,dico_monuments,dico_pourcentage,dico_genre_prefere],index=infos)
    df.groupby(monument).sum()
    return df




def sortie_tableau():
    """
    Écriture d'un tableau des résultats en format html
    :return: un fichier html
    """
    #----------------------------------------------------------------------
    # Déclaration du fichier html et la tête du tableau
    #----------------------------------------------------------------------
    sortie = "<!DOCTYPE html SYSTEM \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n"
    sortie += "<html xmlns=\"http://www.w3.org/1999/xhtml\">\n"
    sortie += "\t<head><title>Tableau récapitulatif</title><meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" /><link rel=\"stylesheet\" type=\"text/css\" href=\"./css/table.css\"/></head>\n"
    sortie += "\t<body><div class=\"ficheResult\" align=\"center\"><h2>Fiche récapitulative des résultats obtenus</h2><table class=\"table_result\">\n"
    sortie += "\t\t<tr><th>Espace</th><th>monument</th><th>nb tournages</th><th>pourcentage</th><th>genre préféré</th></tr>\n"

    #----------------------------------------------------------------------
    # Préparation des données
    #----------------------------------------------------------------------
    dico_espace_monuments = traite_monuments.my_monuments_dico("../data/liste_de_monuments.txt")
    dico_genre_prefere = interrog_genre.mk_dico_genre_prefere(interrog_genre.mk_dico_monument_genre("../xml/films_genre_pays.xml"))
    dico_monuments = mk_dico_monuments("../xml/filter_coord_films_new.xml")
    somme_films = sum(dico_monuments.values())

    #----------------------------------------------------------------------
    # Écriture de tableau
    #----------------------------------------------------------------------
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
            if monument in dico_genre_prefere:
                genre = dico_genre_prefere[monument]
            else:
                genre = ""
            if monument in dico_monuments:
                pourcentage = dico_monuments[monument]/somme_films
                if cpt == 1:
                    sortie += "<td>{}</td><td>{}</td><td>{:.2%}</td><td>{}</td></tr>\n".format(monument,dico_monuments[monument],pourcentage,genre)
                else:
                    sortie += "\t\t\t<tr><td>{}</td><td>{}</td><td>{:.2%}</td><td>{}</td></tr>\n".format(monument,dico_monuments[monument],pourcentage,genre)
            else:
                sortie += "\t\t\t<tr><td>{}</td><td>{}</td><td></td><td>{}</td></tr>\n".format(monument,0,genre)
            cpt += 1
    sortie += "\t</table></div></body></html>"

    with open("../web/tableau.html","w") as f:
        f.write(sortie)

    return



def main():
    print(modelis_donnee())
    print("Écriture du tableau!")
    #sortie_tableau()



if __name__ == '__main__':
    main()

