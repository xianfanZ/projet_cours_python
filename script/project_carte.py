import xml.etree.ElementTree as ET
import folium
import json

carte = folium.Map(location=[48.87, 2.33],zoom_start=13)
def mark_monuments(map_osm):
    geo_path = r'../json/monuments_coord.geojson'
    tree = ET.parse('../xml/monuments_coord.xml')
    for elem in tree.iter(tag='monument'):
        name = elem.find('name').text
        coor = elem.find('coordinates').text
        folium.CircleMarker(location=[coor],radius=70,fill_color='#3186cc',popup=name).add_to(map_osm)
    return
    


def mark_tournage(map_osm):
    tree = ET.parse('../xml/film_final.xml')
    for elem in tree.iter(tag = 'film'):
        lattitude = elem.find('geo1').text
        longtitude = elem.find('geo2').text
        coor = lattitude + ',' + longtitude
        folium.Marker(location=[coor]).add_to(map_osm)
    return
    
#with open('../json/monuments_coord.geojson','r') as file:
    #monuments = json.dumps(file)
    #print(monuments)
    
#for monument in monuments:
#    print(monument)
#    folium.Marker(location = [monument["geometry"]["coordinates"][1],monument["geometry"]["coordinates"][0]])
    
#data2 = pd.read_json(json.dumps(data["features"]), typ='frame')


#folium.GeoJson('../json/monuments_coord.geojson').add_to(map_osm)
mark_monuments(carte)
mark_tournage(carte)
carte.save('../cartes/carte_monuments.html')
