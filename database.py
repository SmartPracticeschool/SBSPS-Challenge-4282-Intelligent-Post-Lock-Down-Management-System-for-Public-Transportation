import mysql.connector

config = {
    'user': 'root',
    'password': 'password',
    'host': '34.93.240.234',
    'database': 'ulka_public'
}

db = mysql.connector.connect(**config)

cursor = db.cursor()