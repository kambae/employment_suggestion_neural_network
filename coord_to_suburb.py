import pickle
from urllib.request import urlopen
import numpy as np
from geopy.geocoders import Nominatim
import geopy
import json
import coord_scrapes
import os


def coord_to_suburb(coords):
    geolocator = Nominatim(user_agent="To Employ or Not To Employ")
    try:
        location = geolocator.reverse(coords[1] + ", " + coords[0])
    except geopy:
        return None
    if location.address is None:
        return None
    if "town" in location.raw["address"]:
        return location.raw["address"]["town"]
    elif "suburb" in location.raw["address"]:
        return location.raw["address"]["suburb"]
    else:
        return None


def locations_to_suburb_count(all_coords: dict):
    suburbs = get_suburb_list()
    result = [{} for suburb in suburbs]
    for feature in all_coords.keys():
        locations = {}
        for loc in all_coords[feature]:
            suburb = coord_to_suburb(coord_string_to_list(loc['coordinates']))
            if suburb is None or suburb not in suburbs:
                continue
            if suburb in locations:
                locations[suburb] += 1
            else:
                locations[suburb] = 1
        for i in range(len(locations.keys())):
            key = sorted(locations.keys())[i]
            result[i][feature] = locations[key]
    return result


def coord_string_to_list(coord_string: str):
    coords = coord_string.split(" ")[0]
    return coords.split(",")


def get_suburb_list():
    a = list()
    request = urlopen("https://myvic-app-dev-gis.beta.vic.gov.au/geoserver/myvic/ows?service=WFS&version=1.0.0&request=GetFeature&outputFormat=application%2Fjson&typeName=myvic%3Aeducation_suburb")
    data = json.loads(request.read())
    for j in range(0, len(data["features"])):
        j_temp = data["features"][j]
        a.append(j_temp["properties"]["ssc_name"])
    return a


if __name__ == "__main__":
    data = {}
    coordinates = []
    for file in os.listdir("data/xmls"):
        filename = str(os.fsdecode(file))
        coordinates.append(coord_scrapes.scrape_coords(filename))
        coordinates = np.array(coordinates)
    np.save("coords.csv", np.array(coordinates))

