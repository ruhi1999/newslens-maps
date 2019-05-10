from collections import Counter
import csv, os, json

class Geotag():
    def __init__(self):
  #      self.nl_root = os.environ['newslens_root']
        self.create_structures()

    def tsv_read(self, f, keys):
        obj = []
        for line in csv.reader(f, delimiter='\t'):
            if line[0][0] != '#': # The line is not a comment
                obj.append({k: v for k, v in zip(keys, line)})
        return obj

    def create_structures(self):

        with open("./data/geo_countries.tsv", "r") as f:   self.countries = self.tsv_read(f, ["ISO", "ISO3", "ISO-Numeric", "fips", "name", "Capital", "Area(in sq km)", "Population", "Continent", "tld", "CurrencyCode", "CurrencyName", "Phone", "Postal Code Format", "Postal Code Regex", "Languages", "geonameid", "neighbours", "EquivalentFipsCode"])
        with open("./data/geo_admin1.tsv", "r") as f:      self.admin1 = self.tsv_read(f, ["geotext", "name", "asciiname", "geonameid"])
        with open("./data/geo_admin2.tsv", "r") as f:      self.admin2 = self.tsv_read(f, ["geotext", "name", "asciiname", "geonameid"])
        with open("./data/geo_cities15000.tsv", "r") as f: self.cities = self.tsv_read(f, ["geonameid", "name", "asciiname", "alternatenames", "latitude", "longitude", "feature class", "feature code", "country code", "cc2", "admin1 code", "admin2 code", "admin3 code", "admin4 code", "population", "elevation", "dem", "timezone", "modification date"])

        self.all_names = Counter()

        self.geography = []
        self.geoid2entry = {}
        self.path2entry = {}
        self.text2path = {}

        for country in self.countries:
            path = country['ISO']
            entry = {"geoid": country['geonameid'], "name": country['name'], "path": path, "depth": 0, "population": 0}
            self.geography.append(entry)
            self.geoid2entry[country['geonameid']] = entry
            self.path2entry[path] = entry
            self.all_names[country['name']] += 1

        for ad1 in self.admin1:
            path = ad1['geotext'].replace(".", "/")
            entry = {"geoid": ad1['geonameid'], "name": ad1['asciiname'], "path": path, "depth": 1, "population": 0}
            self.geography.append(entry)
            self.geoid2entry[ad1['geonameid']] = entry
            self.path2entry[path] = entry
            self.all_names[ad1['asciiname']] += 1

        for ad2 in self.admin2:
            path = ad2['geotext'].replace(".", "/")
            entry = {"geoid": ad2['geonameid'], "name": ad2['asciiname'], "path": path, "depth": 2, "population": 0}
            self.geography.append(entry)
            self.geoid2entry[ad2['geonameid']] = entry
            self.path2entry[path] = entry
            self.all_names[ad2['asciiname']] += 1

        for city in self.cities:
            city['population'] = int(city['population'])
            path = city['country code']
            if path in self.path2entry: self.path2entry[path]['population'] += city['population']
            if len(city['admin1 code']) > 0:
                path += "/"+city['admin1 code']
                if path in self.path2entry: self.path2entry[path]['population'] += city['population']
                if len(city['admin2 code']) > 0:
                    path += "/"+city['admin2 code']
                    if path in self.path2entry: self.path2entry[path]['population'] += city['population']

            path += "/"+city['asciiname']

            entry = {'geoid': city['geonameid'], "name": city['asciiname'], "path": path, "depth": 3, "population": city['population']}

            self.geography.append(entry)
            self.geoid2entry[city['geonameid']] = entry
            self.path2entry[path] = entry
            self.all_names[city['asciiname']] += 1

        # Object useful for Geotag creation

        for g in sorted(self.geography, key=lambda x: -x['population']):
            if g['name'] not in self.text2path:
                self.text2path[g['name']] = g['path']

    def query(self, text):
        if text in self.text2path:
            path = self.text2path[text]
            entry = self.path2entry[path]
            full_text = self.get_text_description(entry)
            return path, full_text
        else:
            return "", ""

    def get_text_description(self, entry):
        if entry['depth'] == 0: full_text = entry['name']
        if entry['depth'] == 1: # It's an admin 1:  a state or a region, we will return California, US
            full_text = entry['name']+ ", "+entry['path'].split('/')[0]
        if entry['depth'] >= 2:
            country_ISO = entry['path'].split('/')[0]
            if country_ISO == 'US':
                full_text = entry['name']+", "+entry['path'].split('/')[1]
            else:
                country_name = self.path2entry[country_ISO]['name']
                if len(country_name) < 10:
                    full_text = entry['name']+", "+country_name
                else:
                    full_text = entry['name']+", "+country_ISO

        return full_text

    def extract(self):
        extracted_geotag = [{"text": "Global", "id": ""}]
        for g in sorted(self.geography, key=lambda x: x['path']):
            if g['depth'] <= 1 or g['population'] >= 10**6:
                name = ("-" * g['depth']) + " " + g['name']
                if len(g['name']) < 25:
                    extracted_geotag.append({'text': name, 'id': g['path']})
        with open(self.nl_root+"common/data/geotag.json", 'w') as f:
            json.dump(extracted_geotag, f)

if __name__ == "__main__":
    GT = Geotag()
    GT.extract()

    # print( GT.query("Paris"))
    # print( GT.query("London"))
    # print( GT.query("Rome"))
