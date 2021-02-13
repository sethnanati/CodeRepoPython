import config as dbconn
import re
from datetime import datetime

#class Create:
def func_CreateData():
    datatime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    print(datatime)

    # Get the sql connection
    connection = dbconn.getSanefDBConnection()
    cursor = connection.cursor()

    data = ('005998546', 'AMIRAKPA GRACE OGONYE', '22224359793', '5743067355')

    qdata = [(str(datatime), data[0], data[1], data[2], data[3])]
    print(qdata)

    try:
        insert = """Insert Into SanefBVN(creation_date, CUST_ID, CUSTOMER_NAME, BVN, ACCOUNT_NO)Values
        (to_date(:1, 'YYYY/MM/DD, HH24:mi:ss'), :2, :3, :4, :5)"""
        print('insert:', insert)
        cursor.prepare(insert)

        # Execute the sql query
        cursor.executemany(None, qdata)

            # Commit the data
        connection.commit()
        print('Data Saved Successfully')

    except dbconn.getSanefDBConnection().DatabaseError as e:
        print('Something wrong, please check:', e)

    finally:
        cursor.close()
        # Close the connection
        connection.close()

func_CreateData()