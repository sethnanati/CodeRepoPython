import requests
import json
import time
from signatureEncoding256 import encrypt_string
import authorizationEncoding64
from cryptoAESLatest import encrypt
from config import endpoints
from ResponseErrorLog import ErrorLog
from iLogs import iLog
import config as dbconn

def createAgent():

    sanefCon = dbconn.getSanefDBConnection()
    sanefCursor = sanefCon.cursor()

    fetchNewAgents = 'SELECT * FROM SANEF.SANEFREQUEST WHERE respmsg is null and respcode is null and BVN IS NOT NULL'
    getNewAgents = sanefCursor.execute(fetchNewAgents)

    for row in getNewAgents:
        try:
            # function to take lag and return states
            # function to get latitude and longitude
            rdata = {"additionalInfo1": row[2], "additionalInfo2":row[3], "bvn": row[4], "city": row[5], "emailAddress": row[6],
                     "latitude": "6.6000", "longitude": "6.6000", "lga": row[9], "state": row[10], "firstName": row[11],
                     "lastName": row[12], "middleName": row[13], "title": "Mr", "phoneList": [row[15]],
                     "servicesProvided": ["CASH_IN", "CASH_OUT", "BVN_ENROLLMENT"], "username": row[11],
                     "streetNumber": row[20], "streetName": row[21],"streetDescription": row[22],
                     "ward": row[23], "password": row[24]}

            print(rdata)

            json.dumps(rdata)
            data = str(json.dumps(rdata)).encode('utf-8')
            serviceurl = endpoints()['creatAgent']
            #print('url:', serviceurl)

            base_data = encrypt(data)
            print('request:', base_data)
            iLog(base_data)

            headers = {"Authorization":authorizationEncoding64.authdecoded, "Signature":encrypt_string(),
                       "Content-Type": 'application/json', 'HTTP method':'POST', 'Signature_Meth':'SHA256'}
            serviceurl = requests.post(url=serviceurl, data=base_data, headers=headers)
            responsetext = serviceurl.text
            print(responsetext)
            #iLog(responsetext)
            #print('Status_Code:', serviceurl.status_code, 'Status_Text:', responsetext, ErrorLog()[str(serviceurl.status_code)], 'Status_Reason:', serviceurl.reason)

        except requests.ConnectionError as e:
            print("OOPS! Connection Error:", e)

        except requests.RequestException as e:
            print("OOPS! Request Error:", e)

        except requests.ConnectTimeout as e:
             print("OOPS! Connect Timeout:", e)

        try:
            getErrorMessage = ErrorLog()[str(serviceurl.status_code)]
            result = 'Status_Code:', serviceurl.status_code, 'Status_Msg:', getErrorMessage, 'Response:', responsetext, ErrorLog()[json.loads(serviceurl.text)['responseCode']]
            #print(result)
            iLog(result)
        except json.JSONDecodeError as e:
            print('JSON Error:', e)
        break

createAgent()
