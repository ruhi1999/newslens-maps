#!/usr/bin/env python
# coding: utf-8

"""Takes country names and outputs their GeoJSON files."""

import folium
import requests
from bs4 import BeautifulSoup
import urllib.request
import geotag
import kml2geojson
import zipfile
import os

class Convert:
    def __init__(self, topic):
        self.topic = topic





#update path here as needed
place_file = open("initial-10/places_"+self.topic+".json")
places = json.load(place_file)
path = ("./self.topics/" + self.topic)
os.mkdir(path)
os.mkdir(path + "/kmz-files")
os.mkdir(path + "/kml-files")
os.mkdir(path + "/geojsons")

# soup.
# https://gadm.org/maps.html

r = requests.get("https://gadm.org/maps.html")
htmlcontent = BeautifulSoup(r.content, "html.parser")
countries = []
country_containers = htmlcontent.find('div', class_="container-fluid main-container").p.small
# print(country_containers)

country_codes = {}
count = 'A'

for a_tag in country_containers.find_all('a', href=True):
    name = a_tag.string
    if name[0].islower():
        name = count + name
        count = chr(ord(count) + 1)
        if (count == 'X'):
            count = chr(ord(count) + 1)
    country_codes.update({name: (a_tag['href'][5:8])})

def get_geojson(code):
    url="https://biogeo.ucdavis.edu/data/gadm3.6/kmz/gadm36_" + code + "_0.kmz"

    urllib.request.urlretrieve(url, path + "/kmz-files/" + code + ".kml.zip")
    print(code)
    zf = zipfile.ZipFile(path + "/kmz-files/" + code + ".kml.zip")

    zf.extractall(path + "/kml-files/")
    zf.close()
    kml2geojson.main.convert(path + '/kml-files/gadm36_' + code + "_0.kml", path + "/geojsons/", separate_folders=False, style_type=None, style_filename='style.json')


# https://biogeo.ucdavis.edu/data/gadm3.6/kmz/gadm36_AFG_0.kmz
GT = geotag.Geotag()
place_names = []

for place in places:
    tag = place["geotag"]
    if (tag in GT.path2entry):
        tag = GT.path2entry[tag]
        place_names.append(tag['name'])

print(place_names)

for place in place_names:
    if (place in country_codes.keys()):
        country = country_codes.get(place)
        get_geojson(country)





#   {
#     "story_type": "World Affairs",
#     "story_id": 186150,
#     "story_name": "Venezuela opposition leader",
#     "geotext": "Venezuela",
#     "geotag": "VE"
#   }

# def geojson_list():
#     geojsons = []
#     for item in os.listdir('./geojsons'):
#         file = os.path.dirname(item)
#         code = file[-7:-4]
#         dict_ =    {"story_type": "World Affairs",
#                     "story_id": place_num,
#                     "story_name": "Venezuela opposition leader",
#                     "geotext": country_codes.keys()[country_codes.values().index(code)],
#                     "geotag": code,
#                     "geojson_file": file
#                    }
#         geojsons.append(dict_)

#     with open('geojson_list.json', 'w') as f:
#         json.dump(geojsons, f)
