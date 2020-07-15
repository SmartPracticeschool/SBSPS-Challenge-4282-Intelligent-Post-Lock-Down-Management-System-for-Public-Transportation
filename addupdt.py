from database import cursor, db
import mysql.connector
import sched, time

s = sched.scheduler(time.time, time.sleep)

def autoupdate(sc):

    sql = 'SELECT  longitude, latitude FROM traccar.tc_positions WHERE id = ( SELECT max(id) FROM traccar.tc_positions )'
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)

    update_add = "UPDATE SCHEDULE SET LOCATION = '%s' WHERE FACILITY = 'BUS'"
    params = (result)
    print(params)
    cursor.execute(update_add,params)
    db.commit()
    print('Upadting SQL')

    s.enter(5, 1, autoupdate, (sc,))

## AFTER 0 SECS NEXT ROW OF THE TABLE IS EXCECUTED
s.enter(0, 1, autoupdate, (s,))
s.run()