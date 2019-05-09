#!/usr/bin/env python
# coding: utf-8

# creates a map from the passed in topic
import folium
import pandas
import json
from statistics import mean
import os
import io
from geopy.geocoders import Nominatim

class mapper:
    def __init__(self, topic):
        self.topic = topic
        self.path = ("./topics/" + self.topic)
        place_file = open(path)
        self.place_data = json.load(place_file)
        self.geolocator = Nominatim(user_agent = "NewsLens")

    def color(self, count):
        if count > 100:
            return 'red'
        elif count > 10:
            return 'orange'
        else:
            return 'green'

    def lat_long(self, name):
        loc = self.geolocator.geocode(name, timeout=2)
        if loc is not None:
            coords = [loc.latitude, loc.longitude]
            print(loc.address)
            return coords
        return "*****not found: "  + name

    def map(self):
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
            markers += [folium.Marker(location = coords, popup = folium.Popup(name),
                icon=folium.Icon(color=color(count),icon_color='green'))]

        m = folium.Map(location=[mean(lat), mean(long)], zoom_start=3, tiles='Mapbox bright')
        for mark in markers:
            mark.add_to(m)

        g = folium.FeatureGroup(name = "topic "+topic)
        for file in os.listdir("./topics/"+topic+"/geojsons"):
            if "DS_Store" in file: continue
            print(file)
            f = open("./topics/"+topic+"/geojsons/"+file,"r")

            g.add_child(folium.GeoJson("./topics/"+topic+"/geojsons/"+file))

        m.add_child(g)
        folium.LayerControl().add_to(m)


        m.save(outfile='./topics/'+topic+'/map-' + topic + '.html')
