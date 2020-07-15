from database import cursor, db
import mysql.connector
import json
from json2xml import json2xml
from json2xml.utils import readfromstring
from flask import jsonify
import os

try:
    if not os.path.exists('liv_loc'):
        os.makedirs('liv_loc')
except OSError:
    print ('Error: Creating directory of liv_loc')

class create_dict(dict): 

    # __init__ function 
    def __init__(self): 
        self = dict() 
        
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value

mydict = create_dict()
sql = """SELECT  longitude, latitude FROM traccar.tc_positions WHERE id = ( SELECT max(id) FROM traccar.tc_positions )"""
cursor.execute(sql)
rv = cursor.fetchall()

payload = []

content = {}

for row in rv:
    content = {'longitude':row[0],'latitude':row[1]}
    print(content)
    payload.append(content)
    content = {}
print(json.dumps(payload))
stud_json = json.dumps(payload)
print(stud_json)
data = readfromstring(stud_json)
print(json2xml.Json2xml(data, wrapper="all", pretty=True, attr_type=False).to_xml())
xml_data = json2xml.Json2xml(data, wrapper="all", pretty=True, attr_type=False).to_xml()

#for loc in range():
live = str(xml_data)
file_path = './loc_sql/live'+'.xml'
print(file_path)

file = open(file_path, 'w')

with open(file_path, 'w') as file:
    file.write(live)

file.close()

