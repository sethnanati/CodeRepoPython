import requests
import config as dbconn
from datetime import datetime


from time import sleep
import cx_Oracle
import config as dbconn
from datetime import datetime
import re

def dAOcreateState():
    response = requests.get('http://196.6.103.30:88/agencybankingservice/lga')
    data = response.json()

    insert = "INSERT INTO SANEF.SANEF_CREATE_STATE(STATE, LGA) VALUES(:1, :2)"

    for datum in data:
        qdata = (str(datum['state']).upper(), str(datum['lga']).upper())

        # Get the sql connection for SANEF Database
        sanefConnection = dbconn.getSanefDBConnection()
        cursor = sanefConnection.cursor()

        print('data:', qdata)
        try:

            # Execute the sql query
            cursor.execute(insert, qdata)

            # Commit the data
            sanefConnection.commit()
            print('Data Saved Successfully')

        except dbconn.getSanefDBConnection().DatabaseError as e:
            print('Something wrong, please check:', e)
    #finally:
    cursor.close()
    #Close the connection
    sanefConnection.close()
    #bvnConnection.close()

dAOcreateState()
