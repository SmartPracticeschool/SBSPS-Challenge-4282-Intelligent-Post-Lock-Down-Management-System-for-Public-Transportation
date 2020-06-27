import ibm_db_dbi as db
conn = db.connect("DATABASE=name;HOSTNAME=host;PORT=60000;PROTOCOL=TCPIP;UID=username;PWD=password;", "", "")   
for t in conn.tables():
    print(t)