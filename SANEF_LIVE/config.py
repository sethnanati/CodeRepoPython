from readConfig import keyConfig
import cx_Oracle

def oauth():
    return keyConfig()

def endpointsUAT():
    return {"ping":"http://196.6.103.58:8080/agencybankingservice/ping/",
            "reset":"http://196.6.103.58:8080/agencybankingservice/reset/",
            "creatAgent":"http://196.6.103.58:8080/agencybankingservice/api/agents/create/",
            "transactionSummaryReport":"http://196.6.103.58:8080/agencybankingservice/api/transactions/summary/",
            "updateAgent":"http://196.6.103.58:8080/agencybankingservice/api/agents/update/",
            "transactionReportSingle":"http://196.6.103.58:8080/agencybankingservice/api/transactions/single/",
            "transactionReportBulk":"http://196.6.103.58:8080/agencybankingservice/api/transactions/bulk/"}

def endpoints():
    return {"ping":"http://196.6.103.30:88/agencybankingservice/ping/",
            "reset":"http://196.6.103.30:88/agencybankingservice/reset/",
            "creatAgent":"http://196.6.103.30:88/agencybankingservice/api/agents/create/",
            "transactionSummaryReport":"http://196.6.103.30:88/agencybankingservice/api/transactions/summary/",
            "updateAgent":"http://196.6.103.30:88/agencybankingservice/api/agents/update/",
            "transactionReportSingle":"http://196.6.103.30:88/agencybankingservice/api/transactions/single/",
            "transactionReportBulk":"http://196.6.103.30:88/agencybankingservice/api/transactions/bulk/"}

def credentialsUAT():
    return{"agentManagerCode":"00013", "institutionCode":"00050", "email":"CBNAgencyReport@ecobank.com"}

def credentials():
    return{"agentManagerCode":"00141", "institutionCode":"00050", "email":"AllENG-Agencybanking@ecobank.com"}

def headers():
    return{"Content-Type": "application/json"}


# SQL Server Database Connection Properties
def getSanefDBConnection():
    dsn_tns = cx_Oracle.makedsn(host='10.4.184.8', port='1521', sid='mcash1')
    #dsn_tns = cx_Oracle.makedsn(host='localhost', port='1521', sid='sanef')
    conn = cx_Oracle.connect(user='mcash', password='mcash12#', dsn=dsn_tns)
    conn.autocommit=1
    return conn
#jdbc:sqlserver://EQN-SQLNCDB-SQL:1436;user=cbnbvnuser@ecobank.group;password=1234@password;database=BVN_UPDATE_SERVICE;integratedSecurity=true
# def getSanefDBConnection():
#     dsn_tns = cx_Oracle.makedsn(host='localhost', port='1521', sid='sanef')
#     conn = cx_Oracle.connect(user='SANEF', password='1234@support', dsn=dsn_tns)
#     conn.autocommit=1
#     return conn

def getDBConnectionBVN():
    dsn_tns = cx_Oracle.makedsn(host='10.4.184.57', port='1521', sid='FCUBSNIG')
    conn = cx_Oracle.connect(user='misuser', password='Passw0rd012', dsn=dsn_tns)
    conn.autocommit=1
    return conn

def getDBConnectionBVNBkp():
    dsn_tns = cx_Oracle.makedsn(host='10.4.184.29', port='1521', service_name='FCUBSNIGLG3')
    conn = cx_Oracle.connect(user='misuser', password='Passw0rd012', dsn=dsn_tns)
    conn.autocommit=1
    return conn

def getDAOConnectionAgency():
    dsn_tns = cx_Oracle.makedsn(host='ADC-entint-SCAN', port='1521', service_name='SRVESB')
    conn = cx_Oracle.connect(user='misuser', password='P$sswd999', dsn=dsn_tns)
    conn.autocommit = 1
    return conn




