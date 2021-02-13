import requests
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
        bulkdata = [ {"transactionDate":"2018-07-12",    "cashInCount":"1000",    "cashInValue":"20000",    "cashOutCount":"1000",
                      "cashOutValue":"2000",    "accountOpeningCount":"2000",    "accountOpeningValue":"4000",
                      "billsPaymentCount":"2000",    "billsPaymentValue":"3000",    "airtimeRechargeCount":"20000",
                      "airtimeRechargeValue":"4000",    "fundTransferCount":"2000",    "fundTransferValue":"3000",
                      "bvnEnrollmentCount":"1000",    "bvnEnrollmentValue":"3000",    "othersCount":"4000",    "othersValue":"30000",
                      "additionalService1Count":"",    "additionalService1Value":"",    "additionalService2Count":"",
                      "additionalService2Value":"",    "agentCode":"99988171" }, {"transactionDate":"2018-07-12",    "cashInCount":"1000",    "cashInValue":"20000",    "cashOutCount":"1000",
                      "cashOutValue":"2000",    "accountOpeningCount":"2000",    "accountOpeningValue":"4000",
                      "billsPaymentCount":"2000",    "billsPaymentValue":"3000",    "airtimeRechargeCount":"20000",
                      "airtimeRechargeValue":"4000",    "fundTransferCount":"2000",    "fundTransferValue":"3000",
                      "bvnEnrollmentCount":"1000",    "bvnEnrollmentValue":"3000",    "othersCount":"4000",    "othersValue":"30000",
                      "additionalService1Count":"",    "additionalService1Value":"",    "additionalService2Count":"",
                      "additionalService2Value":"",    "agentCode":"99988172" }, {"transactionDate":"2018-07-12",    "cashInCount":"1000",    "cashInValue":"20000",    "cashOutCount":"1000",
                      "cashOutValue":"2000",    "accountOpeningCount":"2000",    "accountOpeningValue":"4000",
                      "billsPaymentCount":"2000",    "billsPaymentValue":"3000",    "airtimeRechargeCount":"20000",
                      "airtimeRechargeValue":"4000",    "fundTransferCount":"2000",    "fundTransferValue":"3000",
                      "bvnEnrollmentCount":"1000",    "bvnEnrollmentValue":"3000",    "othersCount":"4000",    "othersValue":"30000",
                      "additionalService1Count":"",    "additionalService1Value":"",    "additionalService2Count":"",
                      "additionalService2Value":"",    "agentCode":"99988173" }, {"transactionDate":"2018-07-12",    "cashInCount":"1000",    "cashInValue":"20000",    "cashOutCount":"1000",
                      "cashOutValue":"2000",    "accountOpeningCount":"2000",    "accountOpeningValue":"4000",
                      "billsPaymentCount":"2000",    "billsPaymentValue":"3000",    "airtimeRechargeCount":"20000",
                      "airtimeRechargeValue":"4000",    "fundTransferCount":"2000",    "fundTransferValue":"3000",
                      "bvnEnrollmentCount":"1000",    "bvnEnrollmentValue":"3000",    "othersCount":"4000",    "othersValue":"30000",
                      "additionalService1Count":"",    "additionalService1Value":"",    "additionalService2Count":"",
                      "additionalService2Value":"",    "agentCode":"99988170" }, {"transactionDate":"2018-07-12",    "cashInCount":"1000",    "cashInValue":"20000",    "cashOutCount":"1000",
                      "cashOutValue":"2000",    "accountOpeningCount":"2000",    "accountOpeningValue":"4000",
                      "billsPaymentCount":"2000",    "billsPaymentValue":"3000",    "airtimeRechargeCount":"20000",
                      "airtimeRechargeValue":"4000",    "fundTransferCount":"2000",    "fundTransferValue":"3000",
                      "bvnEnrollmentCount":"1000",    "bvnEnrollmentValue":"3000",    "othersCount":"4000",    "othersValue":"30000",
                      "additionalService1Count":"",    "additionalService1Value":"",    "additionalService2Count":"",
                      "additionalService2Value":"",    "agentCode":"99988169" }, {"transactionDate":"2018-07-12",    "cashInCount":"1000",    "cashInValue":"20000",    "cashOutCount":"1000",
                      "cashOutValue":"2000",    "accountOpeningCount":"2000",    "accountOpeningValue":"4000",
                      "billsPaymentCount":"2000",    "billsPaymentValue":"3000",    "airtimeRechargeCount":"20000",
                      "airtimeRechargeValue":"4000",    "fundTransferCount":"2000",    "fundTransferValue":"3000",
                      "bvnEnrollmentCount":"1000",    "bvnEnrollmentValue":"3000",    "othersCount":"4000",    "othersValue":"30000",
                      "additionalService1Count":"",    "additionalService1Value":"",    "additionalService2Count":"",
                      "additionalService2Value":"",    "agentCode":"99988168" }, {"transactionDate":"2018-07-12",    "cashInCount":"1000",    "cashInValue":"20000",    "cashOutCount":"1000",
                      "cashOutValue":"2000",    "accountOpeningCount":"2000",    "accountOpeningValue":"4000",
                      "billsPaymentCount":"2000",    "billsPaymentValue":"3000",    "airtimeRechargeCount":"20000",
                      "airtimeRechargeValue":"4000",    "fundTransferCount":"2000",    "fundTransferValue":"3000",
                      "bvnEnrollmentCount":"1000",    "bvnEnrollmentValue":"3000",    "othersCount":"4000",    "othersValue":"30000",
                      "additionalService1Count":"",    "additionalService1Value":"",    "additionalService2Count":"",
                      "additionalService2Value":"",    "agentCode":"99988167" }, {"transactionDate":"2018-07-12",    "cashInCount":"1000",    "cashInValue":"20000",    "cashOutCount":"1000",
                      "cashOutValue":"2000",    "accountOpeningCount":"2000",    "accountOpeningValue":"4000",
                      "billsPaymentCount":"2000",    "billsPaymentValue":"3000",    "airtimeRechargeCount":"20000",
                      "airtimeRechargeValue":"4000",    "fundTransferCount":"2000",    "fundTransferValue":"3000",
                      "bvnEnrollmentCount":"1000",    "bvnEnrollmentValue":"3000",    "othersCount":"4000",    "othersValue":"30000",
                      "additionalService1Count":"",    "additionalService1Value":"",    "additionalService2Count":"",
                      "additionalService2Value":"",    "agentCode":"99988166" }, {"transactionDate":"2018-07-12",    "cashInCount":"1000",    "cashInValue":"20000",    "cashOutCount":"1000",
                      "cashOutValue":"2000",    "accountOpeningCount":"2000",    "accountOpeningValue":"4000",
                      "billsPaymentCount":"2000",    "billsPaymentValue":"3000",    "airtimeRechargeCount":"20000",
                      "airtimeRechargeValue":"4000",    "fundTransferCount":"2000",    "fundTransferValue":"3000",
                      "bvnEnrollmentCount":"1000",    "bvnEnrollmentValue":"3000",    "othersCount":"4000",    "othersValue":"30000",
                      "additionalService1Count":"",    "additionalService1Value":"",    "additionalService2Count":"",
                      "additionalService2Value":"",    "agentCode":"99988165" }, {"transactionDate":"2018-07-12",    "cashInCount":"1000",    "cashInValue":"20000",    "cashOutCount":"1000",
                      "cashOutValue":"2000",    "accountOpeningCount":"2000",    "accountOpeningValue":"4000",
                      "billsPaymentCount":"2000",    "billsPaymentValue":"3000",    "airtimeRechargeCount":"20000",
                      "airtimeRechargeValue":"4000",    "fundTransferCount":"2000",    "fundTransferValue":"3000",
                      "bvnEnrollmentCount":"1000",    "bvnEnrollmentValue":"3000",    "othersCount":"4000",    "othersValue":"30000",
                      "additionalService1Count":"",    "additionalService1Value":"",    "additionalService2Count":"",
                      "additionalService2Value":"",    "agentCode":"99988164" }, {"transactionDate":"2018-07-12",    "cashInCount":"1000",    "cashInValue":"20000",    "cashOutCount":"1000",
                      "cashOutValue":"2000",    "accountOpeningCount":"2000",    "accountOpeningValue":"4000",
                      "billsPaymentCount":"2000",    "billsPaymentValue":"3000",    "airtimeRechargeCount":"20000",
                      "airtimeRechargeValue":"4000",    "fundTransferCount":"2000",    "fundTransferValue":"3000",
                      "bvnEnrollmentCount":"1000",    "bvnEnrollmentValue":"3000",    "othersCount":"4000",    "othersValue":"30000",
                      "additionalService1Count":"",    "additionalService1Value":"",    "additionalService2Count":"",
                      "additionalService2Value":"",    "agentCode":"99988163" }]

        json.dumps(bulkdata)
        data = str(json.dumps(bulkdata)).encode('utf-8')
        print(data)
        serviceurl = endpoints()['transactionReportBulk']
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