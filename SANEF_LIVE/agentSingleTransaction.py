import requests
import json
from signatureEncoding256 import encrypt_string
import authorizationEncoding64
from cryptoAESLatest import encrypt
from config import endpoints
from ResponseErrorLog import ErrorLog
from iLogs import iLog



def createAgent():
    try:
        singleData = {"transactionDate":"2019-12-27", "cashInCount":"", "cashInValue":"",
        "cashOutCount":"", "cashOutValue":"", "accountOpeningCount":"", "accountOpeningValue":"",
        "billsPaymentCount":"", "billsPaymentValue":"", "airtimeRechargeCount":"", "airtimeRechargeValue":"",
        "fundTransferCount":"6", "fundTransferValue":"45200", "bvnEnrollmentCount":"", "bvnEnrollmentValue":"",
        "othersCount":"", "othersValue":"", "additionalService1Count":"", "additionalService1Value":"",
        "additionalService2Count":"", "additionalService2Value":"", "agentCode":"90159806" }
        # 2348134281702    2019-07-24    1    5000    CASHIN  2348134281702    90159639    00

        json.dumps(singleData)
        data = str(json.dumps(singleData)).encode('utf-8')
        iLog(data)
        print(data)
        serviceurl = endpoints()['transactionReportSingle']
        print('url:', serviceurl)

        base_data = encrypt(data)
        #print('request:', base_data)
        iLog(base_data)

        headers = {"Authorization":authorizationEncoding64.authdecoded, "Signature":encrypt_string(),
                   "Content-Type": 'application/json', 'Signature_Meth':'SHA256'}
        serviceurl = requests.post(url=serviceurl, data=base_data, headers=headers)
        responsetext = serviceurl.text
        print(responsetext)
        iLog(responsetext)
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
