import cv2
import numpy as np
import requests
import json
import os
from watson_developer_cloud import VisualRecognitionV3
from database import cursor, db

try:
    if not os.path.exists('data'):
        os.makedirs('data')
except OSError:
    print ('Error: Creating directory of data')

cctv_url = 'SELECT CCTV_URL FROM SCHEDULE'

cursor.execute(cctv_url)
result = cursor.fetchall()
print(result)
i = 0
x = result[0][i]
while i < 42 :
    url = x
    i += 1
    print(url)
    img_request = requests.get(url)
    img_arr = np.array(bytearray  (img_request.content), dtype= np.uint8)
    img = cv2.imdecode(img_arr,-1)
    name = './data/img' + '.jpg'
    print ('Creating...' + name)
    cv2.imwrite(name,img)
    if cv2.waitKey(0):
         break