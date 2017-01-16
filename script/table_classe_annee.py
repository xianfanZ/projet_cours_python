#_*_coding:utf8_*_
"""Créer le tableau du résultat du classement par année"""

from lxml import etree
import collections
import pandas as pd

def parser():

    """parser le fichier ilter_coord_films_new.xml et créer un dico 
    dont la clé est le nom du monument, la valeur est le dico dont la clé 
    est l'année et la valeur est le nombre du films choissant un lieu près de 
    ce monument pour le tournage"""

    dico = {}
    list_monument_2002 = []
    list_monument_2003 = []
    list_monument_2004 = []
    list_monument_2005 = []
    list_monument_2006 = []
    list_monument_2007 = []
    list_monument_2008 = []
    list_monument_2009 = []
    list_monument_2010 = []
    tree = etree.parse(
        "../xml/filter_coord_films_new.xml")
    nodes_date = tree.xpath(
        "/tournagesdefilmsparis2011/film/Date_Debut_Evenement")
    for date in nodes_date:
        if "2002" in date.text:
            parent_node = date.getparent()
            for child in parent_node.iterchildren(tag="Momument_proche"):
                monument = child.text
                list_monument_2002.append((monument, 2002))
        if "2003" in date.text:
            parent_node = date.getparent()
            for child in parent_node.iterchildren(tag="Momument_proche"):
                monument = child.text
                list_monument_2003.append((monument, 2003))
        if "2004" in date.text:
            parent_node = date.getparent()
            for child in parent_node.iterchildren(tag="Momument_proche"):
                monument = child.text
                list_monument_2004.append((monument, 2004))
        if "2005" in date.text:
            parent_node = date.getparent()
            for child in parent_node.iterchildren(tag="Momument_proche"):
                monument = child.text
                list_monument_2005.append((monument, 2005))
        if "2006" in date.text:
            parent_node = date.getparent()
            for child in parent_node.iterchildren(tag="Momument_proche"):
                monument = child.text
                list_monument_2006.append((monument, 2006))
        if "2007" in date.text:
            parent_node = date.getparent()
            for child in parent_node.iterchildren(tag="Momument_proche"):
                monument = child.text
                list_monument_2007.append((monument, 2007))
        if "2008" in date.text:
            parent_node = date.getparent()
            for child in parent_node.iterchildren(tag="Momument_proche"):
                monument = child.text
                list_monument_2008.append((monument, 2008))
        if "2009" in date.text:
            parent_node = date.getparent()
            for child in parent_node.iterchildren(tag="Momument_proche"):
                monument = child.text
                list_monument_2009.append((monument, 2009))
        if "2010" in date.text:
            parent_node = date.getparent()
            for child in parent_node.iterchildren(tag="Momument_proche"):
                monument = child.text
                list_monument_2010.append((monument, 2010))
    C1 = collections.Counter(list_monument_2002)
    C2 = collections.Counter(list_monument_2003)
    C3 = collections.Counter(list_monument_2004)
    C4 = collections.Counter(list_monument_2005)
    C5 = collections.Counter(list_monument_2006)
    C6 = collections.Counter(list_monument_2007)
    C7 = collections.Counter(list_monument_2008)
    C8 = collections.Counter(list_monument_2009)
    C9 = collections.Counter(list_monument_2010)
    dico[2002] = C1
    dico[2003] = C2
    dico[2004] = C3
    dico[2005] = C4
    dico[2006] = C5
    dico[2007] = C6
    dico[2008] = C7
    dico[2009] = C8
    dico[2010] = C9
    values_par_années = dico.values()
    dico_monument={}
    for data_année in values_par_années:
        for monument in data_année.keys():
            dico_monument.setdefault(monument[0], {}).update({monument[1]:data_année[monument]})
    return (dico_monument)


def table():

    """créer ke tableau à base du dico obtenu par la fonction parser"""

    a = parser()
    df = pd.DataFrame(data=a)
    df = df.fillna(' ').T
    print (df.to_html())

table()






