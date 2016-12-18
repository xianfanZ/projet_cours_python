import xml.etree.ElementTree as ET
import folium
import json
map_osm = folium.Map(location=[48.8737791, 2.29503722603767]) 
geo_path = r'../json/monuments_coord.geojson'
tree = ET.parse('../xml/monuments_coord.xml')
for elem in tree.iter(tag='monument'):
    name = elem.find('name').text
    coor = elem.find('coordinates').text
    folium.Marker(location=[coor],popup=name).add_to(map_osm)
    
#with open('../json/monuments_coord.geojson','r') as file:
    #monuments = json.dumps(file)
    #print(monuments)
    
#for monument in monuments:
#    print(monument)
#    folium.Marker(location = [monument["geometry"]["coordinates"][1],monument["geometry"]["coordinates"][0]])
    
#data2 = pd.read_json(json.dumps(data["features"]), typ='frame')


#folium.GeoJson('../json/monuments_coord.geojson').add_to(map_osm)
map_osm.save('../cartes/carte_monuments.html')
