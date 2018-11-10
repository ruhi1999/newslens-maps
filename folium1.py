import folium
import pandas
import json

#for getting lat and long coords
from geopy.geocoders import Nominatim

place_file = open("places_23000.json")
place_data = json.load(place_file)

geolocator = Nominatim(user_agent = "NewsLens")

map = folium.map(location=[df['LAT'].mean(), df['LON'].mean()],
    zoom_start=6, tiles='Mapbox bright')


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
for item in place_data:
    lat_long = lat_long(item['place_name'])
    name = item['place_name']
    count = item['count']
    places.add(name: count, lat_long)
    fg.add_child(folium.Marker(location = lat_long), popup = folium.Popup(name),
        icon=folium.Icon(color=color(count),icon_color='green')

map.add_child(fg)

map.add_child(folium.LayerControl())
map.save(outfile='map.html')
