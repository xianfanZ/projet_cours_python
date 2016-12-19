import xml.etree.ElementTree as ET
import folium


#carte_monuments = folium.Map(location=[48.87, 2.33],zoom_start=13)
#carte_monuments_tournages = folium.Map(location=[48.87, 2.33],zoom_start=13)
def mark_monuments(map_osm):
    tree = ET.parse('../xml/monuments_coord.xml')
    for elem in tree.iter(tag='monument'):
        name = elem.find('name').text
        coor = elem.find('coordinates').text
        folium.CircleMarker(location=[coor],radius=100,fill_color='#3186cc',popup=name).add_to(map_osm)
    return
    


def mark_tournage(map_osm):
    tree = ET.parse('../xml/film_final.xml')
    for elem in tree.iter(tag = 'film'):
        lattitude = elem.find('geo1').text
        longtitude = elem.find('geo2').text
        coor = lattitude + ',' + longtitude
        folium.CircleMarker(location=[coor],radius=1).add_to(map_osm)
    return

carte_tournages = folium.Map(location=[48.87, 2.33],zoom_start=13)



#with open('../json/monuments_coord.geojson','r') as file:
    #monuments = json.dumps(file)
    #print(monuments)
    
#for monument in monuments:
#    print(monument)
#    folium.Marker(location = [monument["geometry"]["coordinates"][1],monument["geometry"]["coordinates"][0]])
    
#data2 = pd.read_json(json.dumps(data["features"]), typ='frame')


#folium.GeoJson('../json/monuments_coord.geojson').add_to(map_osm)
#mark_monuments(carte_monuments)
#mark_monuments(carte_monuments_tournages)
mark_tournage(carte_tournages)
mark_monuments(carte_tournages)
#carte_monuments.save('../cartes/carte_monuments.html')
#carte_monuments_tournages.save('../cartes/carte_monuments_tournages.html')
carte_tournages.save('../cartes/carte_monuments_tournages.html')
