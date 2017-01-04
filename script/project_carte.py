import xml.etree.ElementTree as ET
import folium


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
            folium.CircleMarker(location=[coor],radius=100,fill_color='#3186cc',popup=name).add_to(carte_monuments)
        elif elem.attrib == {'espace': '<+>'}:
            folium.CircleMarker(location=[coor],radius=150,fill_color='#3186cc',popup=name).add_to(carte_monuments)
        elif elem.attrib == {'espace': '<++>'}:
            folium.CircleMarker(location=[coor],radius=200,fill_color='#3186cc',popup=name).add_to(carte_monuments)
        else:
            folium.CircleMarker(location=[coor],radius=250,fill_color='#3186cc',popup=name).add_to(carte_monuments)
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
        coor = lattitude + ',' + longtitude
        folium.CircleMarker(location=[coor],radius=1).add_to(carte)
    return carte



def main():
    print("Projection des monuments et tous les tournages dans une carte...")
    carte_monuments = mark_tournage(mark_monuments("../xml/monuments_coord.xml"),"../xml/film_final.xml")
    print("Réussir à créer la carte!")
    carte_monuments.save('../cartes/carte_monuments_tournages.html')
    print("Projection des monuments et les tournages filtrés dans une carte...")
    carte_tournages_filtres = mark_tournage(mark_monuments("../xml/monuments_coord.xml"),"../xml/filter_coord_films.xml")
    print("Réussir à créer la carte!")
    carte_tournages_filtres.save('../cartes/carte_monuments_tournages_filtrés.html')
    print("Fin")
if __name__ == '__main__':
    main()