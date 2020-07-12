from database import cursor, db
import mysql.connector
import json
from json2xml import json2xml
from json2xml.utils import readfromstring
from flask import jsonify
import os

try:
    if not os.path.exists('loc_sql'):
        os.makedirs('loc_sql')
except OSError:
    print ('Error: Creating directory of loc_sql')

class create_dict(dict): 
  
    # __init__ function 
    def __init__(self): 
        self = dict() 
          
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value

mydict = create_dict()
sql = """SELECT * FROM LOCATION"""
cursor.execute(sql)
rv = cursor.fetchall()

payload = []

content = {}

for row in rv:
    content = {'STOP_ID':row[0],'NAME':row[1],'ADDRESS':row[2],'LAT':row[3],'LNG':row[4],'TYPE':row[5]}
    payload.append(content)
    content = {}
print(json.dumps(payload))
stud_json = json.dumps(payload)
data = readfromstring(stud_json)
print(json2xml.Json2xml(data, wrapper="all", pretty=True, attr_type=False).to_xml())
xml_data = json2xml.Json2xml(data, wrapper="all", pretty=True, attr_type=False).to_xml()

#for loc in range():
loc = str(xml_data)
file_path = './loc_sql/loc'+'.xml'

file = open(file_path, 'w')

with open(file_path, 'w') as file:
    file.write(loc)

file.close()
