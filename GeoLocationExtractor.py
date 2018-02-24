from nltk.tag import StanfordNERTagger
import argparse
from nltk.tokenize import RegexpTokenizer
from geopy import geocoders
import json
import os

nlp = StanfordNERTagger('resources/english.all.3class.distsim.crf.ser.gz', "resources/stanford-ner.jar")


def get_full_locations(l):
    """
    iterates on all tagged data, append all consecutive locations to get address
    for example data:[["I", O}, ["drove", O], ["to", O], ["Eilat", LOCATION], ["via", O], ["Rager", LOCATION], ["Be'er Sheva",LOCATION]]
    should result ["Eilat", "Rager Be'er Sheva"]
    :param l:all tagged data
    :return:list of full locations
    """
    full_locations = []
    full_location = ""
    i = 0
    while i < len(l):
        if l[i][1] == "LOCATION":
            full_location += l[i][0] + " "
            j = i+1
            while j < len(l) and l[j][1] == "LOCATION":
                full_location += l[j][0] + " "
                j += 1
            i = j
            full_locations.append(full_location[:-1]) if full_location[:-1] not in full_locations else None
            full_location = ""
        else:
            i += 1

    return full_locations


def tag_locations_from_text(text):
    """
    Tokenize and tag all text and then filter the locations
    :param text: file text
    :return: list of locations
    """

    # print("dfsalkjfdladfjslfdjasdafsjldkfadafs" + text)
    tokenizer = RegexpTokenizer(r'\w+')
    print("Tokenizing text")
    tokenized_text = tokenizer.tokenize(text)
    print("Tagging tokenized Text")
    l = nlp.tag(tokenized_text)
    locations = get_full_locations(l)
    # return locations
    return json.dumps({"locations": locations})


def tag_locations_from_file(file_name):
    """
    reads ${file_name} and extract the locations from it
    :param file_name: text file
    :return: list of locations
    """

    print("Reading book...")
    file_text = open(file_name, encoding="utf-8").read()
    return tag_locations_from_text(file_text)


def build_geo_locations_from_list(locations):
    """
    takes {locations} list and uses {geo.geocode} to gat latitude and longitude of the location
    :param locations: list of locations
    :param file_name: name of the original file to use it for json name
    :return: None
    """
    print("Retrieving all geolocations of all locations tagged words")
    geo_locations_json = []
    geo = geocoders.GoogleV3(api_key='AIzaSyA_UBzU2-Wk3047IfY7pe2G4WGK-iuFiRw')

    for location in locations:
        location_details = geo.geocode(location, timeout=10)
        if location_details is not None and len(location_details) > 0:
            geo_locations_json.append({"name": location_details.address, "lat": location_details.latitude, "lng": location_details.longitude})
    print("Done.")

    return json.dumps({"locations": geo_locations_json})


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--file", type=str, required=True, help="get tagged locations from a file")

    args = parser.parse_args()
    locations = tag_locations_from_file(args.file)

    build_geo_locations_from_list(locations, args.file)


if __name__ == '__main__':
    main()
