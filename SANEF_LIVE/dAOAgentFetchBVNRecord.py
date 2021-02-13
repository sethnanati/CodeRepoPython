from time import sleep
import cx_Oracle
import config as dbconn
from datetime import datetime
import re

#RUN THIS SECOND TO FETCH OTHER DETAILS OF THE AGENT LIKE BVN

def getDAOConnectionAgency():
    # Get Date for Application and Database Timestamp
    datatime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    print(datatime)

    # Get the sql connection for AGENCY Database
    #misCon = dbconn.getDBConnectionBVN()
    misCon = dbconn.getDBConnectionBVNBkp()
    misCursor = misCon.cursor()

    # Get the sql connection for SANEF Database
    sanefCursor = dbconn.getSanefDBConnection()
    cursor2 = sanefCursor.cursor()

    #fetchBVNSQL = 'SELECT ADDITIONALINFO1 FROM SANEF.SANEFREQUEST WHERE  BVN IS NULL'
    #getAcctNoBVN = sanefCursor.execute(fetchBVNSQL)

    #countrow = 'SELECT MAX(AGENT_ID) FROM SANEFREQUEST'
    fetchBVNSQL = 'SELECT ROW_ID, ADDITIONALINFO1 FROM MCASH.SANEF_AGENT_RECORD WHERE  BVN IS NULL ORDER BY ROW_ID ASC'
    #cursor2.execute(countrow)
    cursor2.execute(fetchBVNSQL)
    row = cursor2.fetchall()
    for (agentDBrow) in row:
        #row = cursor2.fetchone()
        print(str(agentDBrow[0]), str(agentDBrow[1]))

        # Fetch agent data with no BVN from mobile and insert into SANEF Database.
        sql = 'SELECT A.CUSTOMER_NO, A.CUSTOMER_NAME1, A.UDF_2, B.CUST_AC_NO  FROM FCUBSNIG.STTM_CUSTOMER A, FCUBSNIG.STTM_CUST_ACCOUNT B WHERE ' \
              'A.CUSTOMER_NO = B.CUST_NO AND B.CUST_AC_NO = :min'

        #for agentDBrow in sql:
        #print('Agent Row:', agentDBrow)
        misCursor.prepare(sql)
        misCursor.execute(sql, {'min': agentDBrow[1]})
        getCustIDWitBVN = misCursor.fetchone()
        print('getBVN:', getCustIDWitBVN)
        if getCustIDWitBVN:
            print('getCustIDWitBVN:', getCustIDWitBVN[2], getCustIDWitBVN[3])

        try:
            if getCustIDWitBVN == None:
                continue
                qdata = [(getCustIDWitBVN[2], getCustIDWitBVN[3])]
                print(qdata)
                print('data_type', type(getCustIDWitBVN[2]))
                #bvncount = print(len(getCustIDWitBVN[2]))

        except:
            continue


        try:
            statement = "UPDATE MCASH.SANEF_AGENT_RECORD SET BVN = :min2 WHERE ADDITIONALINFO1 = :min3"
            cursor2.prepare(statement)
            # Execute the sql query
            cursor2.execute(statement, {'min2': getCustIDWitBVN[2], 'min3': getCustIDWitBVN[3]})

            # Commit the data
            sanefCursor.commit()
            print('Data Saved Successfully')

        except dbconn.getSanefDBConnection().DatabaseError as e:
            print('Something wrong, please check:', e)

            # Close the data connection
            misCursor.close()
            cursor2.close()
            sanefCursor.close()

getDAOConnectionAgency()

