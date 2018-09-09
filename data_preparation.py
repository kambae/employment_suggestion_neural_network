from urllib.request import urlopen
import json
import pickle
import os
import csv


def dict_to_list_of_dicts(dict_list, relevant_properties):
    a = list()
    for i in range(0, len(dict_list)):
        a.append({j:dict_list[i][j] for j in relevant_properties})
    return a

def read_urls(path):
    urls = list()
    file = open(path, "r")
    for line in file:
        split_line = line.strip()
        split_line = split_line.split(";")
        urls.append((split_line[0], split_line[1], split_line[2]))
    return urls


#add dictionary to outide for dataset name
# def pickle_locations(url_location, path):
#     urls = read_urls(url_location)
#     PATH = path
#     if os.path.exists(PATH):
#         os.remove(PATH)
#     a = {}
#     file = open(PATH, "wb+")
#     for i in urls:
#         request = urlopen(i[0])
#         data = json.loads(request.read())
#         json_path = i[1].strip()
#         json_path = json_path.split(",")
#         id = data[json_path[0]][0]["id"]
#         id = id.split(".")[0]
#         request = urlopen(i[0])
#         data = json.loads(request.read())
#         json_path = i[1].strip()
#         json_path = json_path.split(",")
#         relevant_properties = i[2].strip()
#         relevant_properties = relevant_properties.split(",")
#         a.update({id: dict_to_list_of_dicts([j[json_path[1]] for j in data[json_path[0]]], relevant_properties)})
#         for j in a[id]:
#             if relevant_properties[0] == "coordinates":
#                 if type(j["coordinates"][0]) is list:
#                     if len(j["coordinates"]) == 1:
#                         j["coordinates"] = j["coordinates"][0]
#                     else:
#                         for k in range(1, len(j["coordinates"])):
#                             a[id].append({"coordinates": j["coordinates"][k]})
#                         j["coordinates"] = j["coordinates"][0]
#         print(str(id) + " " + str(a[id][:100]))
#     pickle.dump(a, file)
#     file.close()

def pickle_suburb_data(url_location, path):
    urls = read_urls(url_location)
    PATH = path
    if os.path.exists(PATH):
        os.remove(PATH)
    a = list()
    file = open(PATH, "wb+")
    for i in urls:
        request = urlopen(i[0])
        data = json.loads(request.read())
        json_path = i[1].strip()
        json_path = json_path.split(",")
        relevant_properties = i[2].strip()
        relevant_properties = relevant_properties.split(",")
        for j in range(0, len(data[json_path[0]])):
            j_temp = data[json_path[0]][j]
            for k in dict_to_list_of_dicts([j_temp[json_path[1]]], relevant_properties):
                if len(a) > j:
                    a[j].update({l: j_temp[json_path[1]][l] for l in k})
                else:
                    a.append({l: j_temp[json_path[1]][l] for l in k})
    pickle.dump(a, file)
    file.close()

def append_internet_location_data_pickle(a, csv_path, path, suburb_list):
    PATH = path
    if os.path.exists(PATH):
        os.remove(PATH)
    num_internets = dict()
    file = open(PATH, "wb+")
    with open(csv_path) as int_loc:
        reader = csv.reader(int_loc, delimiter = ",")
        for row in reader:
            if not row[3] in num_internets:
                num_internets[row[3]] = 1
            else:
                num_internets[row[3]] +=1
    for i in range(0, len(suburb_list)):
        if suburb_list[i] in num_internets:
            a[i]["number_internet_locations"] = num_internets[suburb_list[i]]
        else:
            a[i]["number_internet_locations"] = 0
    pickle.dump(a, file)
    file.close()

def get_suburb_list():
    a = list()
    request = urlopen("https://myvic-app-dev-gis.beta.vic.gov.au/geoserver/myvic/ows?service=WFS&version=1.0.0&request=GetFeature&outputFormat=application%2Fjson&typeName=myvic%3Aeducation_suburb")
    data = json.loads(request.read())
    for j in range(0, len(data["features"])):
        j_temp = data["features"][j]
        a.append(j_temp["properties"]["ssc_name"])
    return a

if __name__ == "__main__":
    PATH = "prepared_data.pkl"
    pickle_suburb_data("urls", PATH)
    file = open(PATH, "rb")
    a = pickle.load(file)
    file.close()
    suburb_list = get_suburb_list()
    append_internet_location_data_pickle(a, "public_internet_locations_vic.csv",PATH, suburb_list)