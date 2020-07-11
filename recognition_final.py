import cv2
import numpy as np
import requests
import json
import os
from watson_developer_cloud import VisualRecognitionV3
from database import cursor, db
import sched, time

## DETAILS OF VISUAL RECOGNITION MODEL
visual_recognition = VisualRecognitionV3('2018-03-19',iam_apikey='YgNSrJcWFSrLlIkng2XsEmY6k-HIer3DShnSNeop8Fue')

## SCHEDULAR FOR RUNNING THE NEXT LINE
s = sched.scheduler(time.time, time.sleep)

## TO CREATE PATH FOR SAVING THE IMAGES
try:
    if not os.path.exists('data'):
        os.makedirs('data')
except OSError:
    print ('Error: Creating directory of data')

## UPDATE FUNCTION
def autoupdate (sc):

    ## SELECT THE URL AND ID FROM DATABASE
    cctv_url = 'SELECT CCTV_URL, CCTV_ID FROM SCHEDULE'
    cursor.execute(cctv_url)
    result = cursor.fetchall()

    ## i DECLARED AS 0 , IT REPRESENTS THE ROWS
    i = 0

    ## WHILE LOOP 
    while i < 41 :
        url_out = result[i][0]
        _id = result[i][1]
        print (url_out)
        print (_id)
        url = url_out
        print (url)
        img_request = requests.get(url)
        img_arr = np.array(bytearray  (img_request.content), dtype= np.uint8)
        img = cv2.imdecode(img_arr,-1)
        name = './data/img' + '.jpg'
        cv2.imwrite(name,img)
        ## IMAGE IS CAPTURED

        ## OPENED IN FILE FORMAT
        with open(name, 'rb') as images_file:

            ## PUT IN OKAY OR NOT OKAY MODEL
            classes = visual_recognition.classify( images_file, threshold='0.6', classifier_ids='Bus_View_932757643').get_result()
            visual =json.loads(json.dumps(classes, indent=2))
            preds=visual['images'][0]['classifiers'][0]['classes'][0]['class']

            ## IF NOT OKAY DECLARED AS CROWED
            if (preds) == 'Not Okay':
                count = -1
                print(count)

            ## IF OKAY PUT INTO HUMAN DETECTION TO GET THE HUMAN COUNT
            else:
                url1 = "https://gateway.watsonplatform.net/visual-recognition/api/v4/analyze?version=2019-02-11"
                payload = {'features': 'objects','collection_ids': '465fd7ad-785a-4dab-b64b-08a937c9adcb','threshold': '0.15'}
                files = [('images_file', open(name,'rb'))]
                headers = {'Authorization': 'Basic YXBpa2V5OllnTlNySmNXRlNyTGxJa25nMlhzRW1ZNmstSEllcjNEU2huU05lb3A4RnVl'}
                response = requests.request("POST", url1, headers=headers, data = payload, files = files)
                json_con = json.loads(response.text.encode('utf8'))
                detect = json_con['images'][0]['objects']['collections'][0]['objects']
                count = len(detect)
                print(count)
        
        ## TAKES TO THE NEXT ROW
        i += 1
        print ('loop'+ str(i))

        ## UPDATE THE COUNT TO SQL DATABASE
        update_stat = "UPDATE SCHEDULE SET COUNT = %s WHERE CCTV_ID = %s"
        params = (count,_id)
        print(params)
        cursor.execute(update_stat,params)
        db.commit()
        print('Upadting SQL')

    ## EXIST WHEN THE ROWS ARE COMPLTED
    print('exist')

    ## AFTER EVERY 30 SECS THE PROGRAM IS RUN AGAIN
    s.enter(30, 1, autoupdate, (sc,))

## AFTER 0 SECS NEXT ROW OF THE TABLE IS EXCECUTED
s.enter(0, 1, autoupdate, (s,))
s.run()