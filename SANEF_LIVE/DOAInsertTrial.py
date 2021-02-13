import config as dbconn
from datetime import datetime

def daoConnFetchBVN():
    datatime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
#8008093334, 3703066923, 1193067196, 2523062782, 3663066544
    try:
        sanefCon = dbconn.getSanefDBConnection()
        sanefCursor = sanefCon.cursor()

        misCon = dbconn.getDBConnectionBVN()
        misCursor = misCon.cursor()

        fetchBVNSQL = 'SELECT ADDITIONALINFO1 FROM SANEF.SANEFREQUEST WHERE  BVN IS NULL'
        getAcctNoBVN = sanefCursor.execute(fetchBVNSQL)

        for row in getAcctNoBVN:
            accountno = row[0]
            #print('accountno:', accountno)
            if accountno:
               # print(accountno)

                sql = "SELECT A.CUSTOMER_NO, A.CUSTOMER_NAME1, A.UDF_2, B.CUST_AC_NO  FROM FCUBSNIG.STTM_CUSTOMER A, " \
                  "FCUBSNIG.STTM_CUST_ACCOUNT B WHERE A.CUSTOMER_NO = B.CUST_NO AND B.CUST_AC_NO = :min"
                misCursor.prepare(sql)
                misCursor.execute(sql, {'min': accountno})
                getCustIDWitBVN = misCursor.fetchmany()
                #print(getCustIDWitBVN)
                if getCustIDWitBVN:
                    accountdet = getCustIDWitBVN[0]
                    #print('accountdet:', accountdet)
                    for accountdet in getCustIDWitBVN:
                        qdata = [(str(datatime), accountdet[0], accountdet[1], accountdet[2], accountdet[3])]
                        print('qdata:', qdata)
                        # print(qdata[2])

                        insert = "Insert Into SanefBVN(creation_date, cust_id, customer_name, account_no, bvn)" \
                        "Values(to_date(:1, 'YYYY/MM/DD, HH24:mi:ss'), :2, :3, :4, :5)"

                        sanefCursor.prepare(insert)
                        sanefCursor.executemany(None, qdata)
                        sanefCon.commit()
                        print('insert:', )#
                        #     #insert = "Insert Into SanefBVN(creation_date, cust_id, customer_name, account_no, bvn)" \
                        #      #         "Values(to_date(:1, 'YYYY/MM/DD, HH24:mi:ss'), :2, :3, :4, :5)"
                        #     sanefCursor.prepare(insert)
                        #
                        #     #Execute the sql query
                        #     sanefCursor.executemany(None, qdata)
                        #
                        #     #Commit the data
                        #     sanefCon.commit()
                        #
                        # except dbconn.getSanefDBConnection().DatabaseError as e:
                        #     print('Something wrong, please check:', e)




            # i
            # #if getCustIDWitBVN:
            # for rowBVN in getCustIDWitBVN:
            #     bvn = rowBVN[2]
            #     print('BVN:', bvn)
            #
            #     for bvndata in bvn:
            #         print('bvndata:', bvndata)
            #         sqlvalidate = "SELECT COUNT(BVN) FROM SANEFBVN WHERE BVN = :min3"
            #         sanefCursor.prepare(sqlvalidate)
            #         sanefCursor.execute(sqlvalidate, {'min3':bvndata})
            #         print(sqlvalidate)
            #         existingdata = sanefCursor.fetchmany()
            #         for rowexistingdata in existingdata:
            #             if rowexistingdata:
            #                 break
            #             else:
            #                 continue
            #                 print('existingdata:', rowexistingdata)
            #     #if existingdata:

                   #bvnDetails = (str(datatime), rowBVN[0], rowBVN[1], rowBVN[2], rowBVN[3])
                    #print('bvnDetails:', bvnDetails)

                #
                #print(sqlinsertSelect)

                #for bvnDetailsrow in bvnDetails[3]:
                 #   print('bvnDetailsrow:', bvnDetailsrow)
                    #
                    #
                    #
                    # # for existingdatarow in existingdata:
                    #     print('existingdata:', existingdatarow)
                    #
                    # for custExistCheckResult in existingdata:
                    #     if custExistCheckResult != 0:
                    #         print('Exist Check Result:', custExistCheckResult)
                    #         print(custExistCheckResult, 'Customer already Exist......unable to insert Data', )
                    #         break
                    #
                    #     else:
                    #          print('Customer BVN does not exist inserting Data', )
                    #
                    #         insert = "Insert Into SanefBVN(creation_date, cust_id, customer_name, bvn, account_no)" \
                    #              "Values(to_date(:1, 'YYYY/MM/DD, HH24:mi:ss'), :2, :3, :4, :5)"
                    #         insertQuery = sanefCursor.prepare(insert)
                    #         print('insertQuery:',insertQuery)
                    #         # Execute the sql query
                    #         sanefCursor.executemany(None, bvnDetails)
                            # Commit the data
                #sanefCon.commit()
                #print('Data Saved Successfully')

            #else:
             ##continue

    except dbconn.getSanefDBConnection().DatabaseError as e:
        print('Something wrong, please check:', e)

    finally:
        sanefCursor.close()
        misCursor.close()
        #print('Closing Cursor')
        # Close the connection
        misCon.close()
        sanefCon.close()
        #print('Closing Connection')

        #return getCustIDWitBVN

daoConnFetchBVN()