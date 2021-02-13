import requests
from config import endpoints
import time
import json

def pingConnection():
    try:
        servicePing = str(endpoints()['ping'])
        print('servicePingURL:', servicePing)
        pingresponse = requests.get(url=servicePing)
        print('Ping Response:', pingresponse.status_code, pingresponse.text)
        getPingStatus = pingresponse.status_code
        getPingResultText = pingresponse.text
        try:
            getPingJsonResult = pingresponse.json
        except json.JSONDecodeError as e:
            print('JSON Error:', e)
    except requests.ConnectionError as e:
        print("OOPS! Connection Error:", e)

    except requests.ConnectTimeout as e:
        print("OOPS! Connect Timeout:", e)
    # while True:
    #     if (pingresponse.text == 'Service is available'):
    #         print('Yipee.... Connected to SANEF')
    #     else:
    #         print(pingresponse.text, '...Service is unavailable retrying in 60sec.....')
    #         time.sleep(60)
    #     continue

    return getPingStatus, getPingResultText, getPingJsonResult

getstatus = pingConnection()