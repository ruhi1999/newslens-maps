#!/usr/bin/env python
# coding: utf-8

import json
import folium
import pandas
import requests
import os
from bs4 import BeautifulSoup
import urllib.request
from .geotag import Geotag
import zipfile
from xml.dom import minidom




class shp_getter:
    def __init__(self,topic_file,topic):
        self.place_file = open(topic_file)
        self.places = json.load(self.place_file)
        self.path = ("../topics/" + topic)

        if not os.path.exists(self.path):
            os.mkdir(self.path)
        if not os.path.exists(self.path + "/shp"):
            os.mkdir(self.path + "/shp")
        if not os.path.exists(self.path + "/shp-zipped"):
            os.mkdir(self.path + "/shp-zipped")


    def get_shp(self):
        r = requests.get("https://gadm.org/maps.html")
        htmlcontent = BeautifulSoup(r.content, "html.parser")
        countries = []
        country_containers = htmlcontent.find('div', class_="container-fluid main-container").p.small


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

        GT = Geotag()
        place_names = []

        for place in self.places:
            tag = place["geotag"]
            if (tag in GT.path2entry):
                tag = GT.path2entry[tag]
                place_names.append(tag['name'])

        print(place_names)

        for place in place_names:
            print(place)
            if place in country_codes.keys():
                country = country_codes.get(place)
                self.scrape(country)


    def scrape(self, code):
        url = "https://biogeo.ucdavis.edu/data/gadm3.6/shp/gadm36_" + code + "_shp.zip"

        urllib.request.urlretrieve(url, self.path + "/shp-zipped/" + code + "_shp.zip")
        print(code)
        zf = zipfile.ZipFile(self.path + "/shp-zipped/" + code + "_shp.zip")

        zf.extractall(self.path + "/shp/")
        print("extracted")
        zf.close()
