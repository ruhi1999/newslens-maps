#!/usr/bin/env python
# coding: utf-8

import subprocess
import os

class shp2geojson:
    def __init__(self, topic):
        self.topic = topic
        self.path = ("./topics/" + self.topic)

    def get_shp(self):
        shp_files = self.path+"/shp-files"
        for shp in os.listdir(shp_files):
            if "shp" in shp and "0" in shp:
                print(subprocess.check_output(["mapshaper", shp_files+"/"+shp, "-simplify", "0.3%", "-o", "format=geojson", path+"/geojsons/"+shp+".json"]))
