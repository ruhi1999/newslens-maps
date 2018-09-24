with open("data/places_65923.json", "r") as f:
    places = json.load(f)
    print( len(places))
    print( places[0].keys())
    print(places[0]['place_name'])