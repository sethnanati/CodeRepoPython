from time import sleep
import cx_Oracle
import config as dbconn
from datetime import datetime
import re

#RUN THIS FIRST FOR FETCHING THE AGENT RECORD FROM ESB SERVER

def dAOConnectionFecthAgentRecord():

    #Get Date for Application and Database Timestamp
    datatime = datetime.today().strftime('%Y/%m/%d %H:%M:%S')
    #print(datatime)

    #Get the sql connection for AGENCY Database
    agentConnection = dbconn.getDAOConnectionAgency()
    cursor = agentConnection.cursor()


    # Get the sql connection for SANEF Database
    sanefConnection = dbconn.getSanefDBConnection()
    cursor2 = sanefConnection.cursor()

    #Fetch agent data with no BVN from mobile and insert into SANEF Database.
    sql = cursor.execute("""SELECT TRADING_ACC_NO AS AGENT_ACCOUNT_NO, TO_CHAR('') BVN, CITY, EMAIL_ID, GEO_LOCATION, GEO_LOCATION, AREA, 
    AGENT_STATE AS STATE, AGENT_NAME AS FIRSTNAME, AGENT_NAME AS LASTNAME, AGENT_NAME AS MIDDLENAME, TO_CHAR('') TITLE, 
    MOBILE_NO, TO_CHAR('CASH_IN, CASH_OUT') SERVICESPROVIDED, MOBILE_NO AS USERNAME, ADDRESS AS STREETNUMBER, 
    ADDRESS AS STREETNAME, ADDRESS, TO_CHAR('') WARD, TO_CHAR('') PASSWORD FROM MESB_SADC.AG_AGENT_INFO WHERE AFFILIATE_CODE = 'ENG'""")
    # sql = cursor.execute("""SELECT A.AGENT_ACCOUNT_NO, TO_CHAR('') BVN, A.CITY, A.EMAIL_ID, A.GEO_LOCATION, A.GEO_LOCATION, A.AREA,
    # A.STATE, B.ACCOUNT_NAME AS FIRSTNAME, B.ACCOUNT_NAME AS LASTNAME, B.ACCOUNT_NAME AS MIDDLENAME, TO_CHAR('') TITLE,
    # A.MOBILE_NO, TO_CHAR('CASH_IN, CASH_OUT') SERVICESPROVIDED, A.MOBILE_NO AS USERNAME, A.ADDRESS AS STREETNUMBER,
    # A.ADDRESS AS STREETNAME, A.ADDRESS, TO_CHAR('') WARD, TO_CHAR('') PASSWORD FROM MESB_SADC.BIL_AGENT_INFO A,
    # MESB_SADC.MV_MERCHANTS B WHERE A.AFFILIATE_CODE = 'ENG' AND A.AGENT_CODE = B.MERCHANT_CODE AND B.CATEGORY = 'A'""")

    #Fetch the maximum id on SANEF Database and assign the next number as ID
    for agentDBrowResult in sql:
        print('Next Agent:', agentDBrowResult)
        data = agentDBrowResult

        sqlinsertSelect = "SELECT COUNT(ADDITIONALINFO1) FROM MCASH.SANEF_AGENT_RECORD WHERE ADDITIONALINFO1 = :min"
        # print(sqlinsertSelect)
        cursor2.execute(sqlinsertSelect, {'min': data[0]})
        existingdata = cursor2.fetchone()

        for custExistCheckResult in existingdata:
            if custExistCheckResult != 0:
                print('Exist Check Result:', custExistCheckResult)
                print(custExistCheckResult, 'Customer already Exist......unable to insert Data', )
                break

            else:
                print('Customer does not exist inserting Data', )
                countrow = 'SELECT MAX(row_id) FROM MCASH.SANEF_AGENT_RECORD'
                cursor2.execute(countrow)
                row = cursor2.fetchone()
                print('Row:', row)

                if row[0] == None:
                    row_id = 1
                else:
                    row_id = row[0]
                    row_id += 1
                    print('next_id:', row_id)

                qdata = [(str(row_id), str(datatime), data[0], '', data[1], data[2], data[3], data[4], data[5], data[6],
                  data[7], data[8], data[9], data[10], data[11], re.sub("\W", '', str(data[12])), 'Y', 'Y', 'Y', '','',
                  data[15], data[16], data[17], data[18])]

                print('data:', qdata)

                try:

                    insert = "Insert Into MCASH.SANEF_AGENT_RECORD(row_id, creation_date, additionalInfo1, additionalInfo2, bvn, city, emailAddress, " \
                     "latitude, longitude, lga, state, firstName, lastName, middleName, title, phoneList, cash_in, cash_out, bvn_enrollment, " \
                     "username, streetNumber, streetName, streetDescription, ward, password)" \
                     "Values(:1, to_date(:2, 'YYYY/MM/DD, HH24:mi:ss'), :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15, :16, :17, :18," \
                     ":19, :20, :21, :22, :23, :24, :25)"

                    cursor2.prepare(insert)

                    # Execute the sql query
                    cursor2.executemany(None, qdata)

                    # Commit the data
                    sanefConnection.commit()
                    print('Data Saved Successfully')

                except dbconn.getSanefDBConnection().DatabaseError as e:
                    print('Something wrong, please check:', e)
    #finally:
    cursor2.close()
    #Close the connection
    sanefConnection.close()
    #bvnConnection.close()

dAOConnectionFecthAgentRecord()
