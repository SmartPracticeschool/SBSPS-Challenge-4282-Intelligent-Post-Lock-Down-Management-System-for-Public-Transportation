import ibm_db
import ibm_db_dbi
conn_str = 'DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-lon02-01.services.eu-gb.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=hfl44215;PWD=n53mz4wc9m0hl+z9'
ibm_db_conn = ibm_db.connect(conn_str,'','')

conn = ibm_db_dbi.Connection(ibm_db_conn)
# Insert 3 rows into the table
insert = "insert into mytable values(?,?)"
params=((4,'Raj'),(5,'Kedar'),(6,'Pranav'))
stmt_insert = ibm_db.prepare(ibm_db_conn, insert)
ibm_db.execute_many(stmt_insert,params)
ibm_db.close(ibm_db_conn)