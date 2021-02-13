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
        # summaryData = {"transactionDate":"2018-07-10","cashInCount":"1000",    "cashInValue":"20000.00",    "cashOutCount":"1000",
        #                "cashOutValue":"2000.00",    "accountOpeningCount":"2000", "accountOpeningValue":"4000.00",
        #                "billsPaymentCount":"2000",    "billsPaymentValue":"3000.00",    "airtimeRechargeCount":"20000",
        #                "airtimeRechargeValue":"4000.00",    "fundTransferCount":"2000",    "fundTransferValue":"3000.00",
        #                "bvnEnrollmentCount":"1000",    "bvnEnrollmentValue":"3000.00",    "othersCount":"4000",
        #                "othersValue":"30000.00",    "additionalService1Count":"",    "additionalService1Value":"",
        #                "additionalService2Count":"",    "additionalService2Value":"" }

        summaryData = {"transactionDate":"2019-07-21",    "cashInCount":"43",    "cashInValue":"623200.00",    "cashOutCount":"0",
                        "cashOutValue":"0.00",    "accountOpeningCount":"0",    "accountOpeningValue":"0.00",
                        "billsPaymentCount":"0",    "billsPaymentValue":"0.00",    "airtimeRechargeCount": "1",
                        "airtimeRechargeValue":"200.00",    "fundTransferCount":"0",    "fundTransferValue": "0.00",
                        "bvnEnrollmentCount":"0",    "bvnEnrollmentValue":"0.00",    "othersCount": "0",
                        "othersValue":"0.00",    "additionalService1Count":"",    "additionalService1Value":"",
                        "additionalService2Count":"",    "additionalService2Value":""}

        json.dumps(summaryData)
        data = str(json.dumps(summaryData)).encode('utf-8')
        print(data)
        serviceurl = endpoints()['transactionSummaryReport']
        print('url:', serviceurl)

        base_data = encrypt(data)
        print('request:', base_data)
        iLog(base_data)

        headers = {"Authorization":authorizationEncoding64.authdecoded, "Signature":encrypt_string(),
                   "Content-Type": 'application/json', 'Signature_Meth':'SHA256'}
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