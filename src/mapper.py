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
    def __init__(self, topic, topic_file):
        self.topic = topic
        place_file = open(topic_file)
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
        for item in self.place_data:
            coords = self.lat_long(item['place_name'])
            if type(coords) is str:
                print(coords)
                continue
            lat += [coords[0]]
            long += [coords[1]]
            name = item['place_name']
            count = item['count']
            places.update({name: [count, self.lat_long]})
            markers += [folium.Marker(location = coords, popup = folium.Popup(name),
                icon=folium.Icon(color=self.color(count),icon_color='green'))]

        m = folium.Map(location=[mean(lat), mean(long)], zoom_start=3, tiles='Mapbox bright')
        for mark in markers:
            mark.add_to(m)

        g = folium.FeatureGroup(name = "topic "+self.topic)
        for file in os.listdir("../topics/"+self.topic+"/geojsons"):
            if "DS_Store" in file: continue
            print(file)
            f = open("../topics/"+self.topic+"/geojsons/"+file,"r")

            g.add_child(folium.GeoJson("../topics/"+self.topic+"/geojsons/"+file))

        m.add_child(g)
        folium.LayerControl().add_to(m)


        m.save(outfile='../topics/'+self.topic+'/map-' + self.topic + '.html')
