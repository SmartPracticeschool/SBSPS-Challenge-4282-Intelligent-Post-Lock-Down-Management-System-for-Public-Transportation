from __future__ import division, print_function

# Flask utils
from flask import Flask,flash, redirect, url_for, request, render_template,session,logging
from werkzeug.utils import secure_filename


# coding=utf-8
import sys
import os
import glob

#IBM DB
import ibm_db_dbi 
import ibm_db 

#visual recognition
import json
from watson_developer_cloud import VisualRecognitionV3

#SHA
from passlib.hash import sha256_crypt
from functools import wraps


# Define a flask app
app = Flask(__name__)


conn_str='DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-lon02-01.services.eu-gb.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=hfl44215;PWD=n53mz4wc9m0hl+z9'
ibm_db_conn = ibm_db.connect(conn_str,'','')

conn = ibm_db_dbi.Connection(ibm_db_conn)

cursor = conn.cursor()

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
        password = sha256_crypt.encrypt(str(request.form['password']))
        home = 'i m home honey'
        work = 'it sucks here'
        insert = "INSERT into USERS  VALUES (?,?,?,?,?,?)"
        params = ((name, phone, email,password, home ,work))
        stmt_insert = ibm_db.prepare(ibm_db_conn, insert)
        ibm_db.execute(stmt_insert,params)        
        
        cursor.close()
        ibm_db.close(ibm_db_conn)
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
        password_user = request.form['password']        
        result =  cursor.execute('SELECT "NAME", "PHONE_NO", "EMAIL_ID", "PASSWORD", "HOME", "WORK" FROM "HFL44215"."USERS" WHERE "EMAIL_ID" = ? FETCH FIRST 1 ROWS ONLY ',[email])
        if result == True:
            data = cursor.fetchone() 
            password = data[3] 

            if sha256_crypt.verify(password_user,password):
                #app.logger.info('Passwords Matched')
                session['logged_in'] = True
                session['email'] = email

                flash('You are now logged in','success')
                return redirect(url_for('home'))
            else:
                error = 'Invalid Login'
                #app.logger.info('Passwords Not matched')
                return render_template('login.html',error=error)
            # close connection
            cursor.close()            
            ibm_db.close(ibm_db_conn)
            
        else:
            #app.logger.info('No user')
            error:'Username not found'
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


@app.route('/home', methods=['GET'])
def home():
    # Gesture page
    if 'email' in session:
      email = session['email']
    return render_template('home.html')
        
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


if __name__ == '__main__':
    app.secret_key = 'KomalTai'
    app.run(debug=True)

