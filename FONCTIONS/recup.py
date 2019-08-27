# -*- coding: latin-1 -*-

import os
import csv
import urllib
import xmltodict
import shutil
import pprint
import json
import glob
import pandas as pd


path_to_json = 'somedir/'
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
print(json_files)

path_to_json = 'json/'
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')];


jsons_data = pd.DataFrame(columns=['idArt', 'year', 'abstract'])


for index, js in enumerate(json_files):
with open(os.path.join(path_to_json, js)) as json_file:
json_text = json.load(article_1.json);

idArt = json_text['year'][0]['abstract']['idArt']
year = json_text['idArt'][0]['year']['abstract']
abstract = json_text['features'][0]['geometry']['coordinates']

jsons_data.loc[index] = [idArt, year, abstract]

print(jsons_data)


