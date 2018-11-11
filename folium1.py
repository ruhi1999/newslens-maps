import folium
import pandas
import json
from statistics import mean

#for getting lat and long coords
from geopy.geocoders import Nominatim

place_file = open("places_23000.json")
place_data = json.load(place_file)

geolocator = Nominatim(user_agent = "NewsLens")

mapper = folium.Map(location=[45.5236, -122.6750])

def color(count):
    if count > 100:
        return 'red'
    elif count > 10:
        return 'orange'
    else:
        return 'green'

def lat_long(name):
    loc = geolocator.geocode(name)
    return [loc.latitude, loc.longitude]

fg = folium.FeatureGroup(name = "topic 23000")

places = {}
lat = []
long = []
for item in place_data:
    lat_long = lat_long(item['place_name'])
    lat += lat_long[0]
    long += lat_long[1]
    name = item['place_name']
    count = item['count']
    places.update({name: [count, lat_long]})
    fg.add_child(folium.Marker(location = lat_long), popup = folium.Popup(name),
        icon=folium.Icon(color=color(count),icon_color='green')



mapper = folium.Map(location=[mean(lat), mean(long)], zoom_start=6, tiles='Mapbox bright')

mapper.add_child(fg)

mapper.add_child(folium.LayerControl())
mapper.save(outfile='map.html')
