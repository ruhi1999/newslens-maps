
"""Creates a map from city markers and GeoJSON regions."""

import folium
import pandas
import json
from statistics import mean
import os
from geopy.geocoders import Nominatim

class Mapper:
    def __init__(self, topic):
        self.topic = topic

    #update path below as needed
    place_file = open("./initial-10/places_"+self.topic+".json")
    place_data = json.load(place_file)

    geolocator = Nominatim(user_agent = "NewsLens")

    def color(count):
        if count > 100:
            return 'red'
        elif count > 10:
            return 'orange'
        else:
            return 'green'

    def lat_long(name):
        loc = geolocator.geocode(name, timeout=2000)
        if loc is not None:
            coords = [loc.latitude, loc.longitude]
            print(loc.address)
            return coords
        return "*****not found: "  + name


    #fg = folium.FeatureGroup(name = "self.topic "+self.topic)

    m = folium.Map(location=[0,0], zoom_start=3, tiles='Mapbox bright')
    markers = []

    places = {}
    lat = []
    long = []
    for item in place_data:
        coords = lat_long(item['place_name'])
        if type(coords) is str:
            print(coords)
            continue
        lat += [coords[0]]
        long += [coords[1]]
        name = item['place_name']
        count = item['count']
        places.update({name: [count, lat_long]})
        #fg.add_child(folium.Marker(location = coords, popup = folium.Popup(name),
           # icon=folium.Icon(color=color(count),icon_color='green')))
        markers += [folium.Marker(location = coords, popup = folium.Popup(name),
            icon=folium.Icon(color=color(count),icon_color='green'))]

    m = folium.Map(location=[mean(lat), mean(long)], zoom_start=3, tiles='Mapbox bright')
    for mark in markers:
        mark.add_to(m)


    g = folium.FeatureGroup(name = "self.topic 154145")
    for file in os.listdir("./self.topics/"+self.topic+"/geojsons"):
        folium.GeoJson("./self.topics/"+self.topic+"/geojsons/"+file).add_to(m)
    folium.LayerControl().add_to(m)

    m.save(outfile='./self.topics/'+self.topic+'/map' + self.topic + '.html')


# In[ ]:
