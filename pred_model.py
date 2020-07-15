import urllib3
import requests
import json
from database import cursor, db
from datetime import datetime
import sched, time

## SCHEDULAR FOR RUNNING THE NEXT LINE
s = sched.scheduler(time.time, time.sleep)

def autoupdate (sc):

    datetime.today().strftime('%Y-%m-%d')
    print(datetime.today().strftime('%Y-%m-%d'))
    date_now = datetime.today().strftime('%Y-%m-%d')


    model_detail = 'SELECT URL_EMPTY_SEAT, URL_STOP_CROWD, ROUTE_ID FROM BUS_STOP'
    cursor.execute(model_detail)
    result = cursor.fetchall()

    ## i DECLARED AS 0 , IT REPRESENTS THE ROWS
    i = 0

    ## WHILE LOOP 
    while i < 2666:
        model_url_seat = result[i][0]
        model_url_stop = result[i][1]
        _id = result[i][2]
        
        # NOTE: generate iam_token and retrieve ml_instance_id based on provided documentation	
        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + "eyJraWQiOiIyMDIwMDYyNDE4MzAiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJpYW0tU2VydmljZUlkLTkxNDYzMTlhLWNkNTMtNGRiNi05ODE4LTM0NmRlMjQxOGM3NCIsImlkIjoiaWFtLVNlcnZpY2VJZC05MTQ2MzE5YS1jZDUzLTRkYjYtOTgxOC0zNDZkZTI0MThjNzQiLCJyZWFsbWlkIjoiaWFtIiwiaWRlbnRpZmllciI6IlNlcnZpY2VJZC05MTQ2MzE5YS1jZDUzLTRkYjYtOTgxOC0zNDZkZTI0MThjNzQiLCJuYW1lIjoiU2VydmljZSBjcmVkZW50aWFscy0xIiwic3ViIjoiU2VydmljZUlkLTkxNDYzMTlhLWNkNTMtNGRiNi05ODE4LTM0NmRlMjQxOGM3NCIsInN1Yl90eXBlIjoiU2VydmljZUlkIiwiYWNjb3VudCI6eyJ2YWxpZCI6dHJ1ZSwiYnNzIjoiNzdjNmZhNzgxNzNkNGU3OWIwNWJiYmZmOTVkNzhhOGEifSwiaWF0IjoxNTk0NzYxNjExLCJleHAiOjE1OTQ3NjUyMTEsImlzcyI6Imh0dHBzOi8vaWFtLmJsdWVtaXgubmV0L2lkZW50aXR5IiwiZ3JhbnRfdHlwZSI6InVybjppYm06cGFyYW1zOm9hdXRoOmdyYW50LXR5cGU6YXBpa2V5Iiwic2NvcGUiOiJpYm0gb3BlbmlkIiwiY2xpZW50X2lkIjoiZGVmYXVsdCIsImFjciI6MSwiYW1yIjpbInB3ZCJdfQ.pHBGLUFeZbdWeBFWNzQJgQwIiLXZ_ferEtZ7Pealw3ltnZpn7i1-2Jjybp7EByORud-9MqC7yvjZpGmK2fIgyjAPng3jzRbNlz2_JEiDQlX5NgcT8UiFFgUbSlym35us_lJoB1ZrRpbziOfLuYaiF_r6y1EsncwYccWqSLyjKayAWpKHlAWjwSiNK8aqpIZmz667AsU6U1s1517cFQ2R-bOH9i-Plbqf4QrXhuVo8Nkv0OAYXzRTSnLKIR-oY6Z73OFnY1EYUKRcnuVuskNkbSd39pm4rKQIQW7HjuSflGPhX4NrbIl7VNp6MmS-EUFhIMDZHEexoLSqgENkmGgphg", 'ML-Instance-ID': "f072af13-d309-42b8-9718-617d23a56d2a"}

        # NOTE: manually define and pass the array(s) of values to be scored in the next line
        payload_scoring = {"input_data":[{"fields":["Date"],"values":[[date_now]]}]}

        response_scoring_seat = requests.post(model_url_seat, json=payload_scoring, headers=header)
        seat = json.loads(response_scoring_seat.text)
        score_seat = seat['predictions'][0]['values'][0][-1]
        pred_seat = round(score_seat)

        response_scoring_stop = requests.post(model_url_stop, json=payload_scoring, headers=header)
        stop = json.loads(response_scoring_stop.text)
        score_stop = stop['predictions'][0]['values'][0][-1]
        pred_stop = round(score_stop)
        i +=1
        update_stat = "UPDATE BUS_STOP SET EMPTY_SEATS = %s, STOP_CROWD = %s WHERE ROUTE_ID = %s"
        params = (pred_seat, pred_stop,_id)
        cursor.execute(update_stat,params)
        db.commit()
    print('EXIST')
    ## AFTER EVERY 30 SECS THE PROGRAM IS RUN AGAIN
    s.enter(1, 1, autoupdate, (sc,))


## AFTER 0 SECS NEXT ROW OF THE TABLE IS EXCECUTED
s.enter(0, 1, autoupdate, (s,))
s.run()
