import cx_Oracle

def create_data(conn):
    cursor = conn.cursor()
    print('inserting data......')
    for i in range(1,5):
        insert_response = ('INSERT INTO SANEFREPORT (response)' 'VALUES (%s)')
        cursor.execute(insert_response)

        conn.commit()
        cursor.close()
        print('done')


# def get_data(conn):
#     cursor = conn.cursor()
#     print('fetching data......')
#     for i in range(1,5):
#         fetch_response = ('select * from sanef.sanefreport (response)' 'VALUES (%s)')
#         cursor.execute(fetch)
#
#         conn.commit()
#         cursor.close()
#         print('done')


dsn_tns = cx_Oracle.makedsn(host='localhost', port='1521', sid='sanef') #if needed, place an 'r' before any parameter in order to address any special character such as '\'.
conn = cx_Oracle.connect(user='SANEF', password='password12$', dsn=dsn_tns) #if needed, place an 'r' before any parameter in order to address any special character such as '\'. For example, if your user name contains '\', you'll need to place 'r' before the user name: user=r'User Name'

create_data(conn)

#
#         c = conn.cursor()
#         # run the query
#
#         #accountno = '0443000329'
#
#         query = """select requestdate, sessionid, BeneficiaryAccountnumber, Accountname as BeneficiaryAccountname, amount,
#         Originatoraccountnumber as SenderAccount, originatorname as Sendername,
#         Narration paymentreference, responsecode from compass.Fp_Fundtransferrequest
#         where TO_DATE(requestdate) = to_date(sysdate) and BeneficiaryAccountnumber = '0443000329'"""
#
#         c.execute(query) # use triple quotes if you want to spread your query across multiple lines
#         for row in c:
#             print(row[0],',',row[1],',',row[2],',',row[3],',',row[4],',',row[5],',',row[6],',',row[7],',',row[8])
#     # this only shows the first two columns, to add an additional column yo'll need to add , '-', row[2], etc.
#     except:
#         print(conn.close())
#         print(c.close())
#
# daoConnection()
