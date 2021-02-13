import cx_Oracle

def daoConnection():

    try:
        dsn_tns = cx_Oracle.makedsn(host='10.4.185.44', port='1521', sid='compassd1') #if needed, place an 'r' before any parameter in order to address any special character such as '\'.
        conn = cx_Oracle.connect(user='dashboard', password='dashboard12$', dsn=dsn_tns) #if needed, place an 'r' before any parameter in order to address any special character such as '\'. For example, if your user name contains '\', you'll need to place 'r' before the user name: user=r'User Name'

        c = conn.cursor()
        # run the query

        #accountno = '0443000329'

        query = """select requestdate, sessionid, BeneficiaryAccountnumber, Accountname as BeneficiaryAccountname, amount, 
        Originatoraccountnumber as SenderAccount, originatorname as Sendername, 
        Narration paymentreference, responsecode from compass.Fp_Fundtransferrequest
        where TO_DATE(requestdate) = to_date(sysdate) and BeneficiaryAccountnumber = '0443000329'"""

        c.execute(query) # use triple quotes if you want to spread your query across multiple lines
        for row in c:
            print(row[0],',',row[1],',',row[2],',',row[3],',',row[4],',',row[5],',',row[6],',',row[7],',',row[8])
    # this only shows the first two columns, to add an additional column yo'll need to add , '-', row[2], etc.
    except:
        print(conn.close())
        print(c.close())

daoConnection()

