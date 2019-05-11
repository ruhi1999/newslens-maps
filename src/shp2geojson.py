#!/usr/bin/env python
# coding: utf-8

import subprocess
import os

class shp2geojson:
    def __init__(self, topic):
        self.topic = topic
        self.path = ("../topics/" + self.topic)
        if not os.path.exists(self.path + "/geojsons"):
            os.mkdir(self.path + "/geojsons")

    def get_geo(self, simplif="0.3"):
        shp_files = self.path+"/shp"
        for shp in os.listdir(shp_files):
            if "shp" in shp and "0" in shp:
                print(subprocess.check_output(["mapshaper", shp_files+"/"+shp, "-simplify", simplif+"%", "-o", "format=geojson", self.path+"/geojsons/"+shp+".json"]))
