import xml.etree.ElementTree as ET
import folium

# Projection des monuments et des tournages par genre dans une carte
# Usage : python3 project_carte.py
# Installer folium (https://github.com/python-visualization/folium)
# Données source : monuments_coord.xml, films_genre_pays.xml et films_genre_pays_nonfiltre.xml
# Résultat : carte_monuments_tournages_genre.html (tous les tournages) et carte_monuments_tournages_filtrés_genre.html (tournages proches)

def mark_monuments(nomfichier):
    """
    Projection des monuments dans la carte
    Arg: fichier XML de coordonnés des monuments
    Retourne: une carte OpenStreetMap
    """
    carte_monuments = folium.Map(location=[48.87, 2.33],zoom_start=13)
    tree = ET.parse(nomfichier)
    for elem in tree.iter(tag='monument'):
        name = elem.find('name').text
        coor = elem.find('coordinates').text
        if elem.attrib == {'espace': 'standard'}:
            folium.CircleMarker(location=[coor],radius=100,fill_color='#FFFFFF',popup=name).add_to(carte_monuments)
        elif elem.attrib == {'espace': '<+>'}:
            folium.CircleMarker(location=[coor],radius=150,fill_color='#FFFFFF',popup=name).add_to(carte_monuments)
        elif elem.attrib == {'espace': '<++>'}:
            folium.CircleMarker(location=[coor],radius=200,fill_color='#FFFFFF',popup=name).add_to(carte_monuments)
        else:
            folium.CircleMarker(location=[coor],radius=250,fill_color='#FFFFFF',popup=name).add_to(carte_monuments)
    return carte_monuments
    


def mark_tournage(carte,nomfichier):
    """
    Projection de tournages dans une carte OpenStreetMap
    Arg: la carte OpenStreetMap qui a déjà marqué les monuments, et le fichier XML des films
    """
    tree = ET.parse(nomfichier)
    for elem in tree.iter(tag = 'film'):
        lattitude = elem.find('geo1').text
        longtitude = elem.find('geo2').text
        genre = elem.find('Genre').text
        coor = lattitude + ',' + longtitude
        if genre == "N/A":# si genre non disponible, tournage non projete
            pass
        elif genre == "Comedy": #yellow
            folium.CircleMarker(location=[coor],radius=10, fill_color='#FFFF00',popup=genre).add_to(carte)
        elif genre == "Drama": #red
            folium.CircleMarker(location=[coor],radius=10, fill_color='#FF0000',popup=genre).add_to(carte)
        elif "Romance" in genre: #turquoise
            folium.CircleMarker(location=[coor],radius=10, fill_color='#00FFFF',popup=genre).add_to(carte)
        else: #grey
            folium.CircleMarker(location=[coor],radius=10, fill_color='#808080',popup=genre).add_to(carte)
    return carte



def main():
    print("Projection des monuments et tous les tournages dans une carte...")
    #print(timeit.timeit('marktournage()', globals=globals()))
    carte_monuments = mark_tournage(mark_monuments("../xml/monuments_coord.xml"),"../xml/films_genre_pays_nonfiltre.xml")
    print("Réussir à créer la carte!")
    carte_monuments.save('../cartes/carte_monuments_tournages_genre.html')
    print("Projection des monuments et les tournages filtrés dans une carte...")
    carte_tournages_filtres = mark_tournage(mark_monuments("../xml/monuments_coord.xml"),"/../xml/films_genre_pays.xml")
    print("Réussir à créer la carte!")
    carte_tournages_filtres.save('../cartes/carte_monuments_tournages_filtrés_genre.html')
    print("Fin")
if __name__ == '__main__':
    main()