import requests
import json
import time
from signatureEncoding256 import encrypt_string
import authorizationEncoding64
from cryptoAESLatest import encrypt
from config import endpoints
from ResponseErrorLog import ErrorLog
from iLogs import iLog

def createAgent():
    try:
        updateData = {"additionalInfo1": "", "additionalInfo2": "", "bvn": "22384588631", "city": "Lagos", "emailAddress": "iiyede@ecobank.com",
         "latitude": "6.6000", "longitude": "6.6000", "lga": "Agege", "state": "Lagos", "firstName": "Abiola",
         "lastName": "Ijisola", "middleName": "Babatope", "title": "Mr", "phoneList": ["07052233242"],
         "servicesProvided": ["CASH_IN", "CASH_OUT", "BVN_ENROLLMENT"], "username": "tomiwa42",
         "streetNumber": "21C", "streetName": "AhmaduBelloVictoriaIsland","agentCode": "99988182",
         "streetDescription": "BonnyCampLagos", "ward": "xxx"}

        json.dumps(updateData)
        data = str(json.dumps(updateData)).encode('utf-8')
        print(data)
        serviceurl = endpoints()['updateAgent']
        print('url:', serviceurl)

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
        try:
            errorDesc = ErrorLog()[json.loads(serviceurl.text)['responseCode']]
            result = 'Status_Code:', serviceurl.status_code, 'Status_Msg:', getErrorMessage, 'Response:', responsetext, errorDesc
        except KeyError:
            errorDesc = KeyError
            result = 'Status_Code:', serviceurl.status_code, 'Status_Msg:', getErrorMessage, 'Response:', responsetext, errorDesc
        print(result)
        iLog(result)
    except json.JSONDecodeError as e:
        print('JSON Error:', e)

createAgent()
# print('-----Initializing Create Agent-------')
# while True:
#     if ping.pingConnection()[0] == 200:
#         time.sleep(2)
#         createAgent()
#
#     else:
#         ping.pingConnection()
#         print('...Service is unavailable retrying in 60sec.....')
#         time.sleep(60)


# def createAgent(pingresp):