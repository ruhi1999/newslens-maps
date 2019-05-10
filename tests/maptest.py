import sys, os
sys.path.insert(0, os.path.abspath('..'))
import src.shp2geojson
import src.shp_getter
import src.mapper

def test(topic):
    one = src.shp_getter.shp_getter("../data/initial-10/places_"+topic+".json",topic)
    one.get_shp()
    two = src.shp2geojson.shp2geojson(topic)
    two.get_geo()
    m = src.mapper.mapper(topic)
    m.map()
