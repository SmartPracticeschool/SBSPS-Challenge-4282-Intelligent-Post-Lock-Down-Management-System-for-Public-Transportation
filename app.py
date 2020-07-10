from __future__ import division, print_function

# Flask utils
from flask import Flask,flash, redirect, url_for, request, render_template,session,logging,jsonify
from werkzeug.utils import secure_filename


# coding=utf-8
import sys
import os
import glob

#MySQL
from database import cursor, db

#visual recognition
import json
from watson_developer_cloud import VisualRecognitionV3

import urllib
#SHA
from passlib.hash import sha256_crypt
from functools import wraps

#http request
import http.client
import mimetypes


from newsapi import NewsApiClient
newsapi = NewsApiClient(api_key='8e6f6b4477454be88b16d8e3313c137d')

# Define a flask app
app = Flask(__name__, static_url_path='/static')

@app.route('/register', methods=['GET','POST'])
def register():
    #form = RegisterForm(request.form)
    # Main page
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST': 
        name = request.form['name']         
        phone = request.form['phone']         
        email = request.form['email']
        hash = sha256_crypt.hash(str(request.form['password']))
        insert_user = "INSERT INTO USERS(NAME,EMAIL_ID,PHONE_NUMBER,PASSWORD) VALUES (%s, %s, %s,%s)"
        params = (name,email,phone,hash)
        # Insert new user
        cursor.execute(insert_user, params)
        db.commit()
        user_id = cursor.lastrowid   
        flash('You are now Resgistered','success')
        return redirect(url_for('login'))
    return render_template('register.html') 



@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        # Main page
        return render_template('login.html')
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        select_user = 'SELECT USER_ID,NAME, EMAIL_ID, PHONE_NUMBER, PASSWORD , IS_ADMIN FROM USERS WHERE EMAIL_ID = %s '
        cursor.execute(select_user,[email])
        result = cursor.fetchone() 
        if result != None:  
            user_id = result[0]
            name = result[1]          
            hash = result[4]
            isAdmin = result[5]         
            if sha256_crypt.verify(password,hash):
                session['logged_in'] = True
                session['email'] = email
                session['name'] = name
                session['user_id'] = user_id

                if(isAdmin == True):
                    return redirect(url_for('admins'))
                else:
                    flash('You are now logged in','success')
                    return redirect(url_for('home'))
            else:
                error = 'Invalid Login'
                return render_template('login.html',error=error)
        else:
            error ='User not found! Please Register'
            return render_template('login.html',error=error)   
    return render_template('login.html') 


# check if user logged in

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please Login','danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

@app.route('/home',methods=['GET','POST'])
@is_logged_in
def home():    
    if request.method == 'GET':
        bus_stop_names = 'SELECT DISTINCT ORIGIN FROM BUS_STOP'        
        cursor.execute(bus_stop_names)
        result = cursor.fetchall()
        return render_template('home.html',bus_stops = result)
    # if request.method == 'POST':
    #     origin = request.form['origin']
    #     destination =  request.form['destination']
    #     routes_db =  "SELECT BUS_NUMBER , ORIGIN  as 'FROM', 'NA' as 'VIA',  DESTINY as 'TO' ,'NA' as BUS_NUMBER, STOP_COUNT AS 'TOTAL' FROM BUS_TRAVEL WHERE ORIGIN = %s AND DESTINY = %s UNION ALL SELECT DISTINCT A.BUS_NUMBER , A.ORIGIN as 'FROM', B.ORIGIN as 'VIA' , B.DESTINY as 'TO', B.BUS_NUMBER, A.STOP_COUNT + B.STOP_COUNT as 'TOTAL' FROM BUS_TRAVEL A JOIN BUS_TRAVEL B ON A.DESTINY = B.ORIGIN WHERE A.ORIGIN = %s and B.DESTINY = %s ORDER BY 'TOTAL' ASC LIMIT 1"
    #     params = (origin,destination,origin,destination)
    #     print(routes_db)
    #     cursor.execute(routes_db,params)
    #     result = cursor.fetchall()
    #     print(result)
    #     return render_template('home.html')

@app.route('/admins',methods=['GET','POST'])
@is_logged_in
def admins():    
    if request.method == 'GET':
        bus_stop_names = 'SELECT DISTINCT ORIGIN FROM BUS_STOP'        
        cursor.execute(bus_stop_names)
        result = cursor.fetchall()
        return render_template('admins.html',bus_stops = result)

@app.route('/routes', methods=['POST'])
def routes():
    origin =  request.form['origin']
    destination = request.form['destination']
    routes_db =  "(SELECT BUS_NUMBER as 'BUS_NUMBER_1' , ORIGIN  as 'FROM', 'NA' as 'VIA',  DESTINY as 'TO' ,'NA' as 'BUS_NUMBER_2', STOP_COUNT AS 'TOTAL' FROM BUS_STOP WHERE ORIGIN = %s AND DESTINY = %s ) UNION ALL ( SELECT DISTINCT A.BUS_NUMBER as 'BUS_NUMBER_1', A.ORIGIN as 'FROM', B.ORIGIN as 'VIA' , B.DESTINY as 'TO', B.BUS_NUMBER as 'BUS_NUMBER_2', A.STOP_COUNT + B.STOP_COUNT as 'TOTAL' FROM BUS_STOP A JOIN BUS_STOP B ON A.DESTINY = B.ORIGIN WHERE A.ORIGIN = %s and B.DESTINY = %s ORDER BY 'TOTAL' ASC LIMIT 1)"
    params = (origin,destination,origin,destination)    
    cursor.execute(routes_db,params)
    rv = cursor.fetchall()
    payload = []
    content = {}
    for result in rv:
        content = {'BUS_NUMBER_1': result[0], 'FROM': result[1],'VIA': result[2] ,'TO': result[3],'BUS_NUMBER_2': result[4],'TOTAL' : result[5]}
        payload.append(content)
        content = {}
    return jsonify(payload)

@app.route('/route_time_dist')
def route_time_dist():
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    conn = http.client.HTTPSConnection("maps.googleapis.com")
    payload = ''
    headers = {
    'Content-Type': 'application/json'
    }
    conn.request("GET","/maps/api/distancematrix/json?origins="+ urllib.parse.quote(origin,safe='')+"&destinations="+ urllib.parse.quote(destination,safe='')+"&key=AIzaSyA45Lb9EP7uuJiGLnOW1cPpsgwvx0ByqKc&units=metric&mode=transit" , payload, headers)
    res = conn.getresponse()
    data = res.read()
    return jsonify(data.decode("utf-8"))

@app.route('/profile', methods=['GET','POST'])
def profile():
    if request.method == 'GET':
        user_id = session["user_id"]
        select_user = 'SELECT NAME, EMAIL_ID,PHONE_NUMBER, PASSWORD FROM USERS WHERE USER_ID = %s'
        # update user
        cursor.execute(select_user, (user_id,))
        result = cursor.fetchone()
        db.commit()
        return render_template('profile.html', user = result)
    if request.method == 'POST': 
        name = request.form['name']

        phone = request.form['phone_number']         
        email = request.form['email_id']
        user_id = session["user_id"]
        hash = sha256_crypt.hash(str(request.form['password']))
        update_user = "UPDATE USERS SET NAME=%s , EMAIL_ID =%s ,PHONE_NUMBER =%s,PASSWORD = %s WHERE USER_ID = %s"
        params = (name,email,phone,hash,user_id)
        # update user
        cursor.execute(update_user, params)
        db.commit()
        user_id = cursor.lastrowid   
        flash('Profile updated','success')
        return redirect(url_for('profile'))


@app.route('/news', methods=['GET'])
def news():
    top_headlines = newsapi.get_top_headlines(q='covid',
                                          category='health',
                                          language='en',
                                          country='in',
                                          page_size=90)
    articles = top_headlines['articles']    
    return render_template('news.html',data = articles)


@app.route('/gesture', methods=['GET'])
def gesture():
    # Gesture page
    return render_template('base.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['image']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        visual_recognition = VisualRecognitionV3('2018-03-19',iam_apikey='YgNSrJcWFSrLlIkng2XsEmY6k-HIer3DShnSNeop8Fue')
        with open(file_path, 'rb') as images_file:
            classes = visual_recognition.classify(images_file,threshold='0.6',classifier_ids='DefaultCustomModel_918288861').get_result()
            a=json.loads(json.dumps(classes, indent=2))
            preds=a['images'][0]['classifiers'][0]['classes'][0]['class']
        return preds
    return None

app.secret_key = 'KomalTai'
app.config["CACHE_TYPE"] = "null"

if __name__ == '__main__':
    app.secret_key = 'KomalTai'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run()
    #app.run(debug=True)