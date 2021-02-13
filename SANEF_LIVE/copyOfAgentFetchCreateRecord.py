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
from Validator import validateEmail, dataValidator

#RUN THIS THIRD FOR FETCHING THE AGENT RECORD FROM ESB SERVER


datatime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

def nameChecker(agentname, agentusername):
    getNameList = agentname.split(' ')

    try:
        getMail = agentusername.split('@')
        mail = getMail[0]
    except:
        mail = 'default@email.com'

    if len(getNameList) >= 3:
        fname = getNameList[0]
        lname = getNameList[-1]
        mname = getNameList[1]

    else:
        fname = getNameList[0]
        lname = getNameList[-1]
        mname = fname

    data = {}
    data['firstname'] = fname
    data['surname'] = lname
    data['middlename'] = mname
    data['email'] = mail
    json_data = data
    return json_data

def addressChecker(agentaddress):
    try:
        getaddress = int(re.search(r'\d+', agentaddress).group())
        print(getaddress)
        if getaddress:
            addressno = str(getaddress)
        else:
            addressno = '12C'
    except:
        addressno = '12C'
    return addressno

def emailChecker(value):
    if len(value) >= 5:
        if '@' in value:
            if '.com' in value:
                return True
            else:
                return 'None'
        else:
            return 'None'
    else:
        return 'None'

def dAOConnectionFecthAgentRecord():

    # Get the sql connection for SANEF Database
    sanefConnection = dbconn.getSanefDBConnection()
    cursor2 = sanefConnection.cursor()

    sql = """SELECT * FROM(SELECT * FROM MCASH.SANEF_AGENT_RECORD WHERE 
    BVN NOT IN(SELECT BVN FROM MCASH.SANEF_CREATE_AGENT))"""
    cursor2.execute(sql)
    row = cursor2.fetchall()

    dataMsg = {}

    for agentDBrowResult in row:
        print('Next Agent:', agentDBrowResult)
        data = agentDBrowResult
        print('data',data)

        if not dataValidator(str(data[4])):
            print('failed BVN validation')
            continue
        if not dataValidator(str(data[5])):
            print('failed City validation')
            continue
        if not dataValidator(str(data[10])):
            print('failed State validation')
            continue
        if not dataValidator(str(data[15])):
            print('failed BVN validation')
            continue
        if not dataValidator(str(data[21])):
            print('failed BVN validation')
            continue
        if not dataValidator(str(data[22])):
            print('failed BVN validation')
            continue

        print('data:',data[22])
        agentName = nameChecker(data[11], data[6])
        agentAddress = addressChecker(data[22])
        email = validateEmail(str(data[6]).lower())

        dataMsg['additionalInfo1'] = ''
        dataMsg['additionalInfo2'] = ''
        dataMsg['bvn'] = (data[4])
        dataMsg['city'] = dataValidator(str(data[5]).capitalize())
        dataMsg['emailAddress'] = str(email).lower()
        dataMsg['latitude'] = '6.6000'
        dataMsg['longitude'] = '6.6000'
        dataMsg['lga'] = 'DEFAULT'  # data[9]
        state = dataValidator(str(data[10]).capitalize())#dataValidator(str(data[10]).capitalize())  # data[10]
        if state == 'Abuja':
            dataMsg['state'] = 'Abuja (FCT)'
        else:
            dataMsg['state'] = dataValidator(str(data[10]).capitalize())
        dataMsg['firstName'] = str(agentName['firstname']).capitalize()
        dataMsg['lastName'] = str(agentName['surname']).capitalize()
        dataMsg['middleName'] = str(agentName['middlename']).capitalize()
        dataMsg['title'] = 'Mr'
        dataMsg['phoneList'] = dataValidator([data[15]])
        dataMsg['servicesProvided'] = ["CASH_IN", "CASH_OUT"]
        dataMsg["username"] = str(agentName['email']).lower()
        dataMsg['streetNumber'] = str(agentAddress)
        dataMsg['streetName'] = dataValidator(str(data[21]).title().replace(' ', ''))
        dataMsg['streetDescription'] = dataValidator(str(data[22]).title().replace(' ', ''))

        if len(str(data[22])) == 0:
            print(len(str(data[22])) > 0)
            dataMsg['ward'] = str(data[22])
        else:
            str(data[22])
            print(str(data[22]))
            dataMsg['ward'] = str('DEFAULT')

        dataMsg['password'] = rand_string()
        json_data = json.dumps(dataMsg)
        print('jsondata', json_data)

        print('=======sending create data to NIBSS===============')
        try:
            # json.dumps(rdata)
            data = str(json.dumps(dataMsg)).encode('utf-8')
            serviceurl = endpoints()['creatAgent']
            print('requestdata:', data)
            print('url:', serviceurl)

            base_data = encrypt(data)
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
                print('Status_Code:', serviceurl.status_code, 'Status_Text:', responsetext, ErrorLog()[responsetext['responseCode']])
            except:
                pass

        except requests.ConnectionError as e:
            print("OOPS! Connection Error:", e)

        except requests.RequestException as e:
            print("OOPS! Request Error:", e)

        except requests.ConnectTimeout as e:
            print("OOPS! Connect Timeout:", e)

        print('========== Inserting into DB ===============')

        try:
            print('re',responsetext)
            respcode = responsetext['responseCode']
            print('respcode:', respcode)
            respmsg = ErrorLog()[responsetext['responseCode']]
            print('respmsg:', respmsg)


            agentcode = ''


            respAgentCode = responsetext['agentCode']
            print('respAgetCode:', respAgentCode)
            if 'agentCode' in responsetext:
                agentcode = respAgentCode
                print('respAgentCode:', respAgentCode)
            else:
                agentcode = 'null'
                print(agentcode)
        except KeyError:
            print('keyerror')

        print(agentcode)

        countrow = 'SELECT MAX(row_id) FROM MCASH.SANEF_CREATE_AGENT'
        cursor2.execute(countrow)
        row = cursor2.fetchone()

        print('Row:', row)

        if row[0] == None:
            row_id = 1
        else:
            row_id = row[0]
            row_id += 1
            print('next_id:', row_id)

        try:
            qdata = [(str(row_id), str(datatime), dataMsg['additionalInfo1'], dataMsg['additionalInfo2'],
                      str(dataMsg['bvn']),
                      str(dataMsg['city']), str(dataMsg['emailAddress']), dataMsg['latitude'],
                      str(dataMsg['longitude']), str(dataMsg['lga']), str(dataMsg['state']),
                      str(dataMsg['firstName']), str(dataMsg['lastName']),
                      str(dataMsg['middleName']), str(dataMsg['title']),
                      dataMsg['phoneList'][0], 'Y', 'Y', 'N', str(dataMsg["username"]), str(dataMsg['streetNumber']),
                      str(dataMsg['streetName']),
                      str(dataMsg['streetDescription']), str(dataMsg['ward']), str(dataMsg['password']), str(agentcode),
                      str(respcode),
                      str(respmsg), '', '')]

            print(qdata)

            try:
                insert = "Insert into MCASH.Sanef_Create_Agent(row_id, creation_date, additionalInfo1, additionalInfo2, bvn, city, " \
                         "emailAddress, latitude, longitude, lga, state, firstName, lastName, middleName, title, phoneList, cash_in, cash_out, " \
                         "bvn_enrollment, username, streetNumber, streetName, streetDescription, ward, password, agent_id, respcode, respmsg, " \
                         "additionalinfo3, additionalinfo4) Values(:1, to_date(:2, 'YYYY/MM/DD, HH24:mi:ss'), :3, :4, :5, :6, :7, :8, :9, :10, :11, " \
                         ":12, :13, :14, :15, :16, :17, :18, :19, :20, :21, :22, :23, :24, :25, :26, :27, :28, :29, :30)"

                cursor2.prepare(insert)

                # Execute the sql query
                cursor2.executemany(None, qdata)

                # Commit the data
                sanefConnection.commit()
                print('Data Saved Successfully')

            except dbconn.getSanefDBConnection().DatabaseError as e:
                print('Something wrong, please check:', e)

        except dbconn.getSanefDBConnection().DatabaseError as e:
            print('Something wrong, please check:', e)

            try:
                getErrorMessage = ErrorLog()[str(respcode.status_code)]
                try:
                    errorDesc = ErrorLog()[json.loads(respcode.text)['responseCode']]
                    result = 'Status_Code:', respcode.status_code, 'Status_Msg:', getErrorMessage, 'Response:', respcode.text, errorDesc
                except KeyError:
                    errorDesc = KeyError
                    result = 'Status_Code:', respcode.status_code, 'Status_Msg:', getErrorMessage, 'Response:', respcode.text, errorDesc
                # print(result)
                iLog(result)
            except json.JSONDecodeError as e:
                print('JSON Error:', e)

            # finally:
            clscursor = cursor2.close()
            print(clscursor)
            # Close the connection
            clsconnection = sanefConnection.close()
            print(clsconnection)
            # bvnConnection.close()

        try:
            getErrorMessage = ErrorLog()[str(serviceurl.status_code)]
            print('getErrorMessage:', getErrorMessage)
            try:
                errorDesc = ErrorLog()[json.loads(serviceurl.text)['responseCode']]
                print('errorDesc:', errorDesc)
                result = 'Status_Code:', serviceurl.status_code, 'Status_Msg:', getErrorMessage, 'Response:', responsetext, errorDesc
                print('result:', result)
            except KeyError:
                errorDesc = KeyError
                print('errorDesc:', errorDesc)
                result = 'Status_Code:', serviceurl.status_code, 'Status_Msg:', getErrorMessage, 'Response:', responsetext, errorDesc
                print('result:', result)
            print(result)
            iLog(result)
        except json.JSONDecodeError as e:
            print('JSON Error:', e)

    return True


def insertCreatedAgentIntoTable(response):
    # get connection
    sanefConnection = dbconn.getSanefDBConnection()
    cursor2 = sanefConnection.cursor()

    respcode = response['responseCode']
    print('respcode:', respcode)
    respmsg = ErrorLog()[response['responseCode']]
    print('respmsg:', respmsg)

    try:
        respAgentCode = response['agentCode']
        print('respAgetCode:', respAgentCode)
        if 'agentCode' in response:
            agentcode = respAgentCode
            print('respAgentCode:', respAgentCode)
        else:
            agentcode = 'null'
            print(agentcode)
    except KeyError:
        print('keyerror')

    #agentcode = respAgentCode


    #if response.status_code == "00":
    dataMsg = dAOConnectionFecthAgentRecord()

    countrow = 'SELECT MAX(row_id) FROM MCASH.SANEF_CREATE_AGENT'
    cursor2.execute(countrow)
    row = cursor2.fetchone()

    print('Row:', row)

    if row[0] == None:
        row_id = 1
    else:
        row_id = row[0]
        row_id += 1
        print('next_id:', row_id)

    try:
        qdata = [(str(row_id), str(datatime), dataMsg['additionalInfo1'], dataMsg['additionalInfo2'], str(dataMsg['bvn']),
                  str(dataMsg['city']), str(dataMsg['emailAddress']), dataMsg['latitude'], str(dataMsg['longitude']), str(dataMsg['lga']),
                  str(dataMsg['state']), str(dataMsg['firstName']), str(dataMsg['lastName']), str(dataMsg['middleName']), str(dataMsg['title']),
                  dataMsg['phoneList'][0], 'Y', 'Y', 'N', str(dataMsg["username"]), str(dataMsg['streetNumber']), str(dataMsg['streetName']),
                  str(dataMsg['streetDescription']), str(dataMsg['ward']), str(dataMsg['password']), str(agentcode), str(respcode),
                  str(respmsg), '','')]

        print(qdata)

        try:
            insert = "Insert into MCASH.Sanef_Create_Agent(row_id, creation_date, additionalInfo1, additionalInfo2, bvn, city, " \
                     "emailAddress, latitude, longitude, lga, state, firstName, lastName, middleName, title, phoneList, cash_in, cash_out, " \
                     "bvn_enrollment, username, streetNumber, streetName, streetDescription, ward, password, agent_id, respcode, respmsg, " \
                     "additionalinfo3, additionalinfo4) Values(:1, to_date(:2, 'YYYY/MM/DD, HH24:mi:ss'), :3, :4, :5, :6, :7, :8, :9, :10, :11, " \
                     ":12, :13, :14, :15, :16, :17, :18, :19, :20, :21, :22, :23, :24, :25, :26, :27, :28, :29, :30)"

            cursor2.prepare(insert)

            # Execute the sql query
            cursor2.executemany(None, qdata)

            # Commit the data
            sanefConnection.commit()
            print('Data Saved Successfully')

        except dbconn.getSanefDBConnection().DatabaseError as e:
            print('Something wrong, please check:', e)

    except dbconn.getSanefDBConnection().DatabaseError as e:
        print('Something wrong, please check:', e)

        try:
            getErrorMessage = ErrorLog()[str(response.status_code)]
            try:
                errorDesc = ErrorLog()[json.loads(response.text)['responseCode']]
                result = 'Status_Code:', response.status_code, 'Status_Msg:', getErrorMessage, 'Response:', response.text, errorDesc
            except KeyError:
                errorDesc = KeyError
                result = 'Status_Code:', response.status_code, 'Status_Msg:', getErrorMessage, 'Response:', response.text, errorDesc
            # print(result)
            #iLog(result)
        except json.JSONDecodeError as e:
            print('JSON Error:', e)

        # finally:
        clscursor = cursor2.close()
        print(clscursor)
        # Close the connection
        clsconnection = sanefConnection.close()
        print(clsconnection)
        # bvnConnection.close()
    return True

dAOConnectionFecthAgentRecord()









