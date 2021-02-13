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
        #bvn = '2238458863156'
        # rdata = {"additionalInfo1": "", "additionalInfo2": "", "bvn": bvn, "city": "Lagos",
        #          "emailAddress": "tomny@gmail.com",
        #          "latitude": "6.6000", "longitude": "6.6000", "lga": "Agege", "state": "Lagos", "firstName": "Adeola",
        #          "lastName": "Ijisola", "middleName": "Babatope", "title": "Mr", "phoneList": ["07052233242"],
        #          "servicesProvided": ["CASH_IN", "CASH_OUT", "BVN_ENROLLMENT"], "username": "tommy44",
        #          "streetNumber": "21C", "streetName": "AhmaduBelloVictoriaIsland",
        #          "streetDescription": "BonnyCampLagos", "ward": "xxx", "password": "p@ssW0rd"}
        #
        rdata = {"additionalInfo1": "", "additionalInfo2": "", "bvn": "22172180083", "city": "Ogun",
                 "emailAddress": "Josephajayiseun06@gmail.com", "latitude": "6.6000", "longitude": "6.6000",
                 "lga": "DEFAULT", "state": "Ogun", "firstName": "AJAYI", "lastName": "Oluwaseun", "middleName": "Joseph",
                 "title": "Mr", "phoneList": ["2347033836645"], "servicesProvided": ["CASH_IN", "CASH_OUT"], "username": "Josephajayiseun06",
                 "streetNumber": "8", "streetName": "8OkeElaIpariodaStreetIlaro",
                 "streetDescription": "8OkeElaIpariodaStreetIlaro", "ward": "Ilaro", "password": "R@asnd0m"}


        # 99988182
        # bvn = '2238458863156'
        # rdata = {"additionalInfo1": "", "additionalInfo2": "", "bvn": bvn, "city": "Lagos", "emailAddress": "tomny@gmail.com",
        #          "latitude": "6.6000", "longitude": "6.6000", "lga": "Agege", "state": "Lagos", "firstName": "Adeola",
        #          "lastName": "Ijisola", "middleName": "Babatope", "title": "Mr", "phoneList": ["07052233242"],
        #          "servicesProvided": ["CASH_IN", "CASH_OUT", "BVN_ENROLLMENT"], "username": "tommy44",
        #          "streetNumber": "21C", "streetName": "AhmaduBelloVictoriaIsland",
        #          "streetDescription": "BonnyCampLagos", "ward": "xxx", "password": "p@ssW0rd"}

        # json.dumps(rdata)
        data = str(json.dumps(rdata)).encode('utf-8')
        serviceurl = endpoints()['creatAgent']
        print('requestdata:', data)
        print('url:', serviceurl)

        base_data = encrypt(data)
        print('request:', base_data)
        iLog(base_data)

        headers = {"Authorization":authorizationEncoding64.authdecoded, "Signature":encrypt_string(),
                   "Content-Type": 'application/json',"Signature_Meth":'SHA256'}

        #print('headers:', headers)
        serviceurl = requests.post(url=serviceurl, data=base_data, headers=headers)
        responsetext = serviceurl.text
        print('responsetext:', responsetext)
        iLog(responsetext)
        print('Status_Code:', serviceurl.status_code, 'Status_Text:', serviceurl.text, ErrorLog()[str(serviceurl.status_code)], 'Status_Reason:', serviceurl.reason)
    #
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
#print(ping.pingConnection())
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