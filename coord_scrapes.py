import xml.etree.ElementTree as ET


def scrape_coords(file_name):
    coords = []
    root = ET.parse("data/xmls/{}".format(file_name)).getroot()
    for coord in root.iter():
        if "coordinates" in coord.tag:
            coords.append([coord.text])
    return coords
