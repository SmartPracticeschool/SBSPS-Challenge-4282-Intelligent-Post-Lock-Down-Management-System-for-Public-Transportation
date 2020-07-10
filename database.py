import mysql.connector

config = {
    'user': 'root',
    'password': 'password',
    'host': '34.93.19.32',
    'database': 'transport'
}

db = mysql.connector.connect(**config)

cursor = db.cursor()