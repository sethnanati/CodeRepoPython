import json
import requests

from ResponseErrorLog import ErrorLog
from config import endpoints, credentials, headers
import time

from iLogs import iLog


def resetApi():
    servicePing = str(endpoints()['ping'])
    print(servicePing)
    pingresponse = requests.get(url=servicePing)
    print('Ping Response:', pingresponse.text)
    iLog('===PingResult:==== ' + pingresponse.text)

    while True:
        if (pingresponse.text == 'Service is available'):
            print('Yipee.... Connected to SANEF')

            try:
                serviceUrl = str(endpoints()['reset'])
                payload = {'institutionCode': str(credentials()['institutionCode']), 'email': str(credentials()['email'])}
                validJsonData = json.dumps(payload)
                response = requests.post(url=str(serviceUrl), json=payload, headers=headers())
                setresponse = (response.text)
                with open('prodPrivateConfig.ini', 'w+') as f:
                    f.write(setresponse)
                print('request', response.url)
                print('requestdata:', validJsonData)
                print('response:', setresponse)
                print(setresponse.responseCode)
                print(ErrorLog()[str(setresponse.responseCode)])
                #getErrorMessage = ErrorLog()[str(serviceurl.status_code)]
            except:
                 print('finished')
            break

        else:
            print(pingresponse.text, '...retrying service connection with NIBSS.....')
            time.sleep(20)
        continue

    return setresponse

getstatus = resetApi()
