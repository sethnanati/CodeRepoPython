import config as dbconn
from datetime import datetime
import re
import json
import requests
from signatureEncoding256 import encrypt_string, rand_string
import authorizationEncoding64
from cryptoAESLatest import encrypt
from config import endpoints
from ResponseErrorLog import ErrorLog
from iLogs import iLog

#RUN THIS LAST FOR SENDING THE AGENT SINGLE TRANSACTION TO NIBSS

datatime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

def dAOConnectionFecthAgentRecord():

    # Get the sql connection for SANEF Database
    agentDBConnection = dbconn.getDAOConnectionAgency()
    cursor = agentDBConnection.cursor()

    sql = """SELECT TRANSACTIONDATE, MOBILE_NO, COUNT(cashInCount)cashInCount, SUM(cashInValue)cashInValue, COUNT(cashOutCount) cashOutCount, SUM(cashOutValue) cashOutValue, 
    COUNT(billsPaymentCount) billsPaymentCount, SUM(billsPaymentValue) billsPaymentValue, COUNT(airtimeRechargeCount) airtimeRechargeCount, 
    SUM(airtimeRechargeValue) airtimeRechargeValue, COUNT(fundTransferCount) fundTransferCount, SUM(fundTransferValue) fundTransferValue, AGENT_CODE, AGENT_ACCOUNT_NO  FROM (
    SELECT TO_CHAR(REQUEST_DATE, 'YYYY-MM-DD') AS TRANSACTIONDATE, CASE WHEN LENGTH(MOBILE_NO) = 11 THEN 234||SUBSTR(MOBILE_NO, -0, 10) WHEN LENGTH(MOBILE_NO) = '10' THEN 234||MOBILE_NO ELSE MOBILE_NO END AS MOBILE_NO , 
    CASE WHEN REQUEST_TYPE = 'CASHIN' THEN COUNT(AGENT_CODE) END AS cashInCount, CASE WHEN REQUEST_TYPE = 'CASHIN' THEN SUM(AMOUNT) END AS cashInValue, 
    CASE WHEN REQUEST_TYPE = 'CASHOUT' THEN COUNT(AGENT_CODE) END AS cashOutCount, CASE WHEN REQUEST_TYPE = 'CASHOUT' THEN SUM(AMOUNT) END AS cashOutValue,
    CASE WHEN REQUEST_TYPE = 'BILLSPAYMENT' THEN COUNT(AGENT_CODE) END AS billsPaymentCount, CASE WHEN REQUEST_TYPE = 'BILLSPAYMENT' THEN SUM(AMOUNT) END AS billsPaymentValue,
    CASE WHEN REQUEST_TYPE = 'AIRTIME' THEN COUNT(MOBILE_NO) END AS airtimeRechargeCount, CASE WHEN REQUEST_TYPE = 'AIRTIME' THEN SUM(AMOUNT) END AS airtimeRechargeValue,
    CASE WHEN REQUEST_TYPE = 'INTERBANK' THEN COUNT(AGENT_CODE) END AS fundTransferCount, CASE WHEN REQUEST_TYPE = 'INTERBANK' THEN SUM(AMOUNT) END AS fundTransferValue,
    REQUEST_TYPE, AGENT_CODE, TO_CHAR(REQUEST_DATE, 'YYYY-MM-DD'), AGENT_ACCOUNT_NO FROM (
    ---CASH IN AND CASH OUT-----
    SELECT A.MOBILE_NO, B.REQUEST_DATE, B.AGENT_CODE, B.AMOUNT, B.REQUEST_TYPE,  B.BILLER_RSP_CODE, A.AGENT_ACCOUNT_NO
    FROM MESB_SADC.BIL_AGENT_INFO A, MESB_SADC.BIL_AGENT_LOG B WHERE A.AFFILIATE_CODE = 'ENG'
    AND A.agent_CODE = B.AGENT_CODE AND B.REQUEST_TYPE IN ('CASHIN', 'CASHOUT') AND B.BILLER_RSP_CODE = '000' 
    UNION
     ----INTERBANK----
    SELECT A.MOBILE_NO AS MOBILE_NO, B.REQUEST_DATE, A.AGENT_CODE, B.AMOUNT, TO_CHAR('INTERBANK') AS REQUEST_TYPE,
    B.ACH_RSP_CODE AS BILLER_RSP_CODE, A.AGENT_ACCOUNT_NO 
    FROM MESB_SADC.BIL_AGENT_INFO A,  ESBUSER.MUL_IBT_LOG@esbdashboard1 B WHERE A.AFFILIATE_CODE = 'ENG' 
    AND A.AGENT_ACCOUNT_NO = B.SEND_ACCOUNT_NO AND B.ACH_RSP_CODE = '000'
    UNION
    -----AIRTIME TOPUP AND BILLSPAYMENT-----
    SELECT A.MOBILE_NO, B.REQUEST_DATE, A.AGENT_CODE, B.AMOUNT, CASE WHEN BILLER_CODE IN ('MTN TOPUP',  'Airtel TOPUP', 'Glo TOPUP', 'Etisalat TOPUP') 
    THEN 'AIRTIME' ELSE 'BILLSPAYMENT' END REQUEST_TYPE, BILLER_RSP_CODE, A.AGENT_ACCOUNT_NO
    FROM MESB_SADC.BIL_AGENT_INFO A, ESBUSER.BIL_TRAN_LOG@esbdashboard1 B WHERE A.AFFILIATE_CODE = 'ENG' AND A.AGENT_ACCOUNT_NO = B.CUSTOMER_ACCOUNT
    )  WHERE TO_CHAR(REQUEST_DATE, 'YYYY-MM-DD') between TO_CHAR(SYSDATE -14, 'YYYY-MM-DD') and TO_CHAR(SYSDATE -3, 'YYYY-MM-DD') 
    ---and mobile_no = '2348141994951'
    GROUP BY MOBILE_NO, TO_CHAR(REQUEST_DATE, 'YYYY-MM-DD'), REQUEST_TYPE, BILLER_RSP_CODE, AGENT_CODE, AGENT_ACCOUNT_NO )
    GROUP BY TRANSACTIONDATE, MOBILE_NO, AGENT_CODE, AGENT_ACCOUNT_NO ORDER BY MOBILE_NO DESC"""

    cursor.execute(sql)
    row = cursor.fetchmany()
    print(row)

    dataMsg = {}
    l = []

    for agentDBrowResult in row:

        #print('Next Agent:', agentDBrowResult)
        data = agentDBrowResult
        #print(data)

        # Get the sql connection for SANEF Database
        sanefDBConnection = dbconn.getSanefDBConnection()
        cursor2 = sanefDBConnection.cursor()

        sqlSelect = "SELECT PHONELIST, AGENT_ID, RESPCODE FROM MCASH.SANEF_CREATE_AGENT WHERE RESPCODE = '00' AND PHONELIST = :min ORDER BY PHONELIST"

        #print(sqlSelect)
        cursor2.execute(sqlSelect, {'min': data[1]})

        agentiddata = cursor2.fetchone()
        #print('agentiddata:', agentiddata)

        try:
            if agentiddata[1] != 'None':
                pushToNIBSS = [data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13], agentiddata[1]]
                getresult = pushToNIBSS
                #print('getresult', getresult)

                dataMsg['transactionDate'] = data[0]
                dataMsg['cashInCount'] = data[2]
                dataMsg['cashInValue'] = data[3]
                dataMsg['cashOutCount'] = data[4]
                dataMsg['cashOutValue'] = data[5]
                dataMsg['accountOpeningCount'] = ''
                dataMsg['accountOpeningValue'] = ''
                dataMsg['billsPaymentCount'] = data[6]
                dataMsg['billsPaymentValue'] = data[7]
                dataMsg['airtimeRechargeCount'] = data[8]
                dataMsg['airtimeRechargeValue'] = data[9]
                dataMsg['fundTransferCount'] = data[10]
                dataMsg['fundTransferValue'] = data[11]
                dataMsg['bvnEnrollmentCount'] = ''
                dataMsg['bvnEnrollmentValue'] = ''
                dataMsg["othersCount"] = ''
                dataMsg['othersValue'] = ''
                dataMsg['additionalService1Count'] = ''
                dataMsg['additionalService1Value'] = ''
                dataMsg['additionalService2Count'] = ''
                dataMsg['additionalService2Value'] = ''
                dataMsg['agentCode'] = agentiddata[1]

                # json_data = json.dumps(dataMsg)
                # print('jsondata', json_data)
                # sentRequest = 'request:', json_data
                # Log(sentRequest)

                sendingNibss = ('=======sending create data to NIBSS===============')
                print(sendingNibss)
                iLog(sendingNibss)
                try:
                    nipData = str(json.dumps(dataMsg)).encode('utf-8')
                    print(nipData)
                    serviceurl = endpoints()['transactionReportSingle']
                    print('requestdata:', nipData)
                    iLog(nipData)
                    print('url:', serviceurl)

                    base_data = encrypt(nipData)
                    print('request:', base_data)
                    iLog(base_data)

                    headers = {"Authorization": authorizationEncoding64.authdecoded, "Signature": encrypt_string(),
                               "Content-Type": 'application/json', "Signature_Meth": 'SHA256'}
                    serviceurl = requests.post(url=serviceurl, data=base_data, headers=headers)
                    print(serviceurl.url)
                    responsetext = json.loads(serviceurl.text)
                    iLog(responsetext)
                    try:
                        print('ErrorLog:', ErrorLog()[str(serviceurl.status_code)])
                        #iLog(ErrorLog()[str(serviceurl.status_code)])
                        print('Status_Code:', serviceurl.status_code, 'Status_Text:', responsetext, ErrorLog()[responsetext['responseCode']])
                        iLog(serviceurl.status_code, 'Status_Text:', responsetext, ErrorLog()[responsetext['responseCode']])
                    except:
                        pass

                except requests.ConnectionError as e:
                    print("OOPS! Connection Error:", e)

                except requests.RequestException as e:
                    print("OOPS! Request Error:", e)

                except requests.ConnectTimeout as e:
                    print("OOPS! Connect Timeout:", e)

        except Exception as e:
            continue
            print('Exception Error Log:', e)
            iLog(e)
dAOConnectionFecthAgentRecord()

        #
        #                             print('========== Inserting into DB ===============')
        #
        #                 print('re',responsetext)
        #                 respcode = responsetext['responseCode']
        #                 print('respcode:', respcode)
        #                 respmsg = ErrorLog()[responsetext['responseCode']]
        #                 print('respmsg:', respmsg)
        #
        #                 agentcode = ''
        #
        #                 try:
        #                     respAgentCode = responsetext['agentCode']
        #                     print('respAgetCode:', respAgentCode)
        #                     if 'agentCode' in responsetext:
        #                         agentcode = respAgentCode
        #                         print('respAgentCode:', respAgentCode)
        #                     else:
        #                         agentcode = 'null'
        #                         print(agentcode)
        #                 except KeyError:
        #                     print('keyerror')
        #
        #                 print(agentcode)
        #
        #                 countrow = 'SELECT MAX(row_id) FROM SANEF.SANEF_CREATE_AGENT'
        #                 cursor2.execute(countrow)
        #                 row = cursor2.fetchone()
        #
        #                 print('Row:', row)
        #
        #                 if row[0] == None:
        #                     row_id = 1
        #                 else:
        #                     row_id = row[0]
        #                     row_id += 1
        #                     print('next_id:', row_id)
        #
        #                 try:
        #                     qdata = [(str(row_id), str(datatime), dataMsg['additionalInfo1'], dataMsg['additionalInfo2'],
        #                               str(dataMsg['bvn']),
        #                               str(dataMsg['city']), str(dataMsg['emailAddress']), dataMsg['latitude'],
        #                               str(dataMsg['longitude']), str(dataMsg['lga']), str(dataMsg['state']),
        #                               str(dataMsg['firstName']), str(dataMsg['lastName']),
        #                               str(dataMsg['middleName']), str(dataMsg['title']),
        #                               dataMsg['phoneList'][0], 'Y', 'Y', 'N', str(dataMsg["username"]), str(dataMsg['streetNumber']),
        #                               str(dataMsg['streetName']),
        #                               str(dataMsg['streetDescription']), str(dataMsg['ward']), str(dataMsg['password']), str(agentcode),
        #                               str(respcode),
        #                               str(respmsg), '', '')]
        #
        #                     print(qdata)
        #
        #                     try:
        #                         insert = "Insert into Sanef.Sanef_Create_Agent(row_id, creation_date, additionalInfo1, additionalInfo2, bvn, city, " \
        #                                  "emailAddress, latitude, longitude, lga, state, firstName, lastName, middleName, title, phoneList, cash_in, cash_out, " \
        #                                  "bvn_enrollment, username, streetNumber, streetName, streetDescription, ward, password, agent_id, respcode, respmsg, " \
        #                                  "additionalinfo3, additionalinfo4) Values(:1, to_date(:2, 'YYYY/MM/DD, HH24:mi:ss'), :3, :4, :5, :6, :7, :8, :9, :10, :11, " \
        #                                  ":12, :13, :14, :15, :16, :17, :18, :19, :20, :21, :22, :23, :24, :25, :26, :27, :28, :29, :30)"
        #
        #                         cursor2.prepare(insert)
        #
        #                         # Execute the sql query
        #                         cursor2.executemany(None, qdata)
        #
        #                         # Commit the data
        #                         sanefConnection.commit()
        #                         print('Data Saved Successfully')
        #
        #                     except dbconn.getSanefDBConnection().DatabaseError as e:
        #                         print('Something wrong, please check:', e)
        #
        #                 except dbconn.getSanefDBConnection().DatabaseError as e:
        #                     print('Something wrong, please check:', e)
        #
        #                     try:
        #                         getErrorMessage = ErrorLog()[str(respcode.status_code)]
        #                         try:
        #                             errorDesc = ErrorLog()[json.loads(respcode.text)['responseCode']]
        #                             result = 'Status_Code:', respcode.status_code, 'Status_Msg:', getErrorMessage, 'Response:', respcode.text, errorDesc
        #                         except KeyError:
        #                             errorDesc = KeyError
        #                             result = 'Status_Code:', respcode.status_code, 'Status_Msg:', getErrorMessage, 'Response:', respcode.text, errorDesc
        #                         # print(result)
        #                         iLog(result)
        #                     except json.JSONDecodeError as e:
        #                         print('JSON Error:', e)
        #
        #                     # finally:
        #                     clscursor = cursor2.close()
        #                     print(clscursor)
        #                     # Close the connection
        #                     clsconnection = sanefConnection.close()
        #                     print(clsconnection)
        #                     # bvnConnection.close()
        #
        #
        #
        #
        #
        #
        # dataMsg = {}
        #
        # for agentDBrowResult in row:
        #     print('Next Agent:', agentDBrowResult)
        #     data = agentDBrowResult
        #     print('data', data)
        #     if data[4] == 'CASHIN':
        #         cashin = data[4]
        #         print('This is CASHIN:', cashin, '\n')
        #
        #     elif data[4] == 'CASHOUT':
        #         cashout = data[4]
        #         print('This is CASHOUT:', cashout, '\n')
        #         continue
        #
        # if data[4] == 'CASHIN':
        #     cashin = data[4]
        #     print('This is CASHIN:', cashin, '\n')
        #
        # elif data[4] == 'CASHOUT':
        #     cashout = data[4]
        #     print('This is CASHOUT:', cashout, '\n')
        #     continue
        #
        #
        #
        #             print('data:',data[22])
        #             agentName = nameChecker(data[11], data[6])
        #             agentAddress = addressChecker(data[22])
        #             email = str(data[6]).lower()
        #
        #
        #             try:
        #                 getErrorMessage = ErrorLog()[str(serviceurl.status_code)]
        #                 print('getErrorMessage:', getErrorMessage)
        #                 try:
        #                     errorDesc = ErrorLog()[json.loads(serviceurl.text)['responseCode']]
        #                     print('errorDesc:', errorDesc)
        #                     result = 'Status_Code:', serviceurl.status_code, 'Status_Msg:', getErrorMessage, 'Response:', responsetext, errorDesc
        #                     print('result:', result)
        #                 except KeyError:
        #                     errorDesc = KeyError
        #                     print('errorDesc:', errorDesc)
        #                     result = 'Status_Code:', serviceurl.status_code, 'Status_Msg:', getErrorMessage, 'Response:', responsetext, errorDesc
        #                     print('result:', result)
        #                 print(result)
        #                 iLog(result)
        #             except json.JSONDecodeError as e:
        #                 print('JSON Error:', e)
        #
        #         return True
        #
        #
        #     def insertCreatedAgentIntoTable(response):
        #         # get connection
        #         sanefConnection = dbconn.getSanefDBConnection()
        #         cursor2 = sanefConnection.cursor()
        #
        #         respcode = response['responseCode']
        #         print('respcode:', respcode)
        #         respmsg = ErrorLog()[response['responseCode']]
        #         print('respmsg:', respmsg)
        #
        #         try:
        #             respAgentCode = response['agentCode']
        #             print('respAgetCode:', respAgentCode)
        #             if 'agentCode' in response:
        #                 agentcode = respAgentCode
        #                 print('respAgentCode:', respAgentCode)
        #             else:
        #                 agentcode = 'null'
        #                 print(agentcode)
        #         except KeyError:
        #             print('keyerror')
        #
        #         #agentcode = respAgentCode
        #
        #
        #         #if response.status_code == "00":
        #         dataMsg = dAOConnectionFecthAgentRecord()
        #
        #         countrow = 'SELECT MAX(row_id) FROM SANEF.SANEF_CREATE_AGENT'
        #         cursor2.execute(countrow)
        #         row = cursor2.fetchone()
        #
        #         print('Row:', row)
        #
        #         if row[0] == None:
        #             row_id = 1
        #         else:
        #             row_id = row[0]
        #             row_id += 1
        #             print('next_id:', row_id)
        #
        #         try:
        #             qdata = [(str(row_id), str(datatime), dataMsg['additionalInfo1'], dataMsg['additionalInfo2'], str(dataMsg['bvn']),
        #                       str(dataMsg['city']), str(dataMsg['emailAddress']), dataMsg['latitude'], str(dataMsg['longitude']), str(dataMsg['lga']),
        #                       str(dataMsg['state']), str(dataMsg['firstName']), str(dataMsg['lastName']), str(dataMsg['middleName']), str(dataMsg['title']),
        #                       dataMsg['phoneList'][0], 'Y', 'Y', 'N', str(dataMsg["username"]), str(dataMsg['streetNumber']), str(dataMsg['streetName']),
        #                       str(dataMsg['streetDescription']), str(dataMsg['ward']), str(dataMsg['password']), str(agentcode), str(respcode),
        #                       str(respmsg), '','')]
        #
        #             print(qdata)
        #
        #             try:
        #                 insert = "Insert into Sanef.Sanef_Create_Agent(row_id, creation_date, additionalInfo1, additionalInfo2, bvn, city, " \
        #                          "emailAddress, latitude, longitude, lga, state, firstName, lastName, middleName, title, phoneList, cash_in, cash_out, " \
        #                          "bvn_enrollment, username, streetNumber, streetName, streetDescription, ward, password, agent_id, respcode, respmsg, " \
        #                          "additionalinfo3, additionalinfo4) Values(:1, to_date(:2, 'YYYY/MM/DD, HH24:mi:ss'), :3, :4, :5, :6, :7, :8, :9, :10, :11, " \
        #                          ":12, :13, :14, :15, :16, :17, :18, :19, :20, :21, :22, :23, :24, :25, :26, :27, :28, :29, :30)"
        #
        #                 cursor2.prepare(insert)
        #
        #                 # Execute the sql query
        #                 cursor2.executemany(None, qdata)
        #
        #                 # Commit the data
        #                 sanefConnection.commit()
        #                 print('Data Saved Successfully')
        #
        #             except dbconn.getSanefDBConnection().DatabaseError as e:
        #                 print('Something wrong, please check:', e)
        #
        #         except dbconn.getSanefDBConnection().DatabaseError as e:
        #             print('Something wrong, please check:', e)
        #
        #             try:
        #                 getErrorMessage = ErrorLog()[str(response.status_code)]
        #                 try:
        #                     errorDesc = ErrorLog()[json.loads(response.text)['responseCode']]
        #                     result = 'Status_Code:', response.status_code, 'Status_Msg:', getErrorMessage, 'Response:', response.text, errorDesc
        #                 except KeyError:
        #                     errorDesc = KeyError
        #                     result = 'Status_Code:', response.status_code, 'Status_Msg:', getErrorMessage, 'Response:', response.text, errorDesc
        #                 # print(result)
        #                 iLog(result)
        #             except json.JSONDecodeError as e:
        #                 print('JSON Error:', e)
        #
        #             # finally:
        #             clscursor = cursor2.close()
        #             print(clscursor)
        #             # Close the connection
        #             clsconnection = sanefConnection.close()
        #             print(clsconnection)
        #             # bvnConnection.close()
        #
        #
        #
        #
        #
        #
        #
        #
