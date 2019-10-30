import os, json, itertools
from pymongo import MongoClient
import xml.etree.ElementTree as ET

client = MongoClient()
cs5604_db = client.cs5604_db
metadata = cs5604_db.metadata


def get_dissertation(dissertation_handle):
    query = {"handle": dissertation_handle}
    cursor = metadata.find(query)
    for x in cursor:
        return x
    return {}


def find_issued_date(xml_tree):
    try:
        return xml_tree.getroot().findall(".//dcvalue[@element='date'][@qualifier='issued']")[0].text
    except:
        return ''


def read_json(font_file_name):
    with open(font_file_name) as f:
        return json.load(f)


dissertation_path = '/home/sampanna/dissertation'
dissertation_folders = [f for f in os.listdir(dissertation_path) if os.path.isdir(os.path.join(dissertation_path, f))]
count = 0
for dissertation_folder in dissertation_folders:
    # print(dissertation_folder)
    mongo_entry = get_dissertation(dissertation_folder)
    if not mongo_entry:
        print("No mongo entry found for {}. Skipped.".format(dissertation_folder))
        continue

    complete_dissertation_folder = os.path.join(dissertation_path, dissertation_folder)
    files = [os.path.join(complete_dissertation_folder, f) for f in os.listdir(complete_dissertation_folder) if
             os.path.isfile(os.path.join(complete_dissertation_folder, f))]

    all_fonts = []
    [all_fonts.append(read_json(file_name)) for file_name in files if "_fonts.json" in file_name]
    all_fonts = list(itertools.chain.from_iterable(all_fonts))
    print(all_fonts)
    fonts = {"fonts" : all_fonts}
    metadata.update_one({"handle": dissertation_folder}, {"$set": fonts}, upsert=False)

    count = count + 1
    print("------------------------------- Success counter: {} --------------------------------------".format(count))
    # dublin_core_path = os.path.join(complete_dissertation_folder, 'dublin_core.xml')
    # tree = ET.parse(dublin_core_path)
    # issued_date = find_issued_date(xml_tree=tree)
    # print(issued_date)
    # break
