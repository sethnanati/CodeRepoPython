from time import sleep
import cx_Oracle
import config as dbconn
from datetime import datetime
import re
import json
from signatureEncoding256 import rand_string

datatime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

def nameChecker(agentname, agentusername):
    getNameList = agentname.split(' ')
    getMail = agentusername.split('@')
    if len(getNameList) >= 3:
        fname = getNameList[0]
        lname = getNameList[-1]
        mname = getNameList[1]
        mail = getMail[0]
    else:
        fname = getNameList[0]
        lname = getNameList[-1]
        mname = fname
        mail = 'default@email.com'

    data ={}
    data['firstname'] = fname
    data['surname'] = lname
    data['middlename'] = mname
    data['email'] = mail
    json_data = data
    return json_data


def addressChecker(agentaddress):
    getaddress = int(re.search(r'\d+', agentaddress).group())
    print(getaddress)
    if getaddress:
        addressno = str(getaddress)
    else:
        addressno = '12C'
    return addressno

def dAOConnectionFecthAgentRecord():
    # Get the sql connection for SANEF Database
    sanefConnection = dbconn.getSanefDBConnection()
    cursor2 = sanefConnection.cursor()
    #22176649869
    #Fetch agent data with no BVN from mobile and insert into SANEF Database.
    sql = cursor2.execute("""SELECT * FROM(SELECT * FROM SANEF.SANEF_AGENT_RECORD WHERE BVN NOT IN
    (SELECT BVN FROM SANEF.SANEF_CREATE_AGENT))""")

    #Fetch the maximum id on SANEF Database and assign the next number as ID
    for agentDBrowResult in sql:
        print('Next Agent:', agentDBrowResult)

    data = agentDBrowResult
    agentName = nameChecker(data[11], data[6])
    agentAddress = addressChecker(data[22])
    #
    # countrow = 'SELECT MAX(row_id) FROM SANEF.SANEF_CREATE_AGENT'
    # cursor2.execute(countrow)
    # row = cursor2.fetchone()
    # print('Row:', row)
    #
    # if row[0] == None:
    #     row_id = 1
    # else:
    #     row_id = row[0]
    #     row_id += 1
    #     print('next_id:', row_id)
    #
    # #print(agentName)
    # #print(agentAddress)
    #
    # dataMsg = {}
    # dataMsg['additionalInfo1'] = ''
    # dataMsg['additionalInfo2'] = ''
    # dataMsg['bvn'] = data[4]
    # dataMsg['city'] = str(data[5]).capitalize()
    # dataMsg['emailAddress'] = str(data[6]).capitalize()
    # dataMsg['latitude'] = str('6.6000')
    # dataMsg['longitude'] = str('6.6000')
    # dataMsg['lga'] = 'DEFAULT'#data[9]
    # dataMsg['state'] = 'Ogun'#data[10]
    # dataMsg['firstName'] = str(agentName['firstname']).capitalize()
    # dataMsg['lastName'] = str(agentName['surname']).capitalize()
    # dataMsg['middleName'] = str(agentName['middlename']).capitalize()
    # dataMsg['title'] = 'Mr'
    # dataMsg['phoneList'] = data[15]
    # dataMsg['servicesProvided'] = ["CASH_IN","CASH_OUT"]
    # dataMsg["username"] = str(agentName['email']).capitalize()
    # dataMsg['streetNumber'] = str(agentAddress)
    # dataMsg['streetName'] = str(data[21]).title().replace(' ','')
    # dataMsg['streetDescription'] = str(data[22]).title().replace(' ','')
    #
    # if len(str(data[22])) == 0:
    #     print(len(str(data[22])) > 0)
    #     dataMsg['ward'] = str(data[22])
    # else:
    #     str(data[22])
    #     print(str(data[22]))
    #     dataMsg['ward'] = str('DEFAULT')
    #
    # dataMsg['password'] = rand_string()
    # json_data = json.dumps(dataMsg)
    # print(json_data)
    #
    # qdata = [(str(row_id), str(datatime), dataMsg['additionalInfo1'], dataMsg['additionalInfo2'], dataMsg['bvn'], dataMsg['city'],
    #         dataMsg['emailAddress'], dataMsg['latitude'], dataMsg['longitude'], dataMsg['lga'], dataMsg['state'],
    #         dataMsg['firstName'], dataMsg['lastName'], dataMsg['middleName'], dataMsg['title'], dataMsg['phoneList'],
    #         'Y', 'Y', 'N', dataMsg["username"], dataMsg['streetNumber'], str(data[21]), dataMsg['streetDescription'],
    #         dataMsg['ward'] ,dataMsg['password'], '', '', '', '', '')]
    #
    # try:
    #     insert = "Insert into Sanef.Sanef_Create_Agent(row_id, creation_date, additionalInfo1, additionalInfo2, bvn, city, " \
    #     "emailAddress, latitude, longitude, lga, state, firstName, lastName, middleName, title, phoneList, cash_in, cash_out, " \
    #     "bvn_enrollment, username, streetNumber, streetName, streetDescription, ward, password, agent_id, respcode, respmsg, " \
    #     "additionalinfo3, additionalinfo4) Values(:1, to_date(:2, 'YYYY/MM/DD, HH24:mi:ss'), :3, :4, :5, :6, :7, :8, :9, :10, :11, " \
    #     ":12, :13, :14, :15, :16, :17, :18, :19, :20, :21, :22, :23, :24, :25, :26, :27, :28, :29, :30)"
    #
    #     cursor2.prepare(insert)
    #
    #     # Execute the sql query
    #     cursor2.executemany(None, qdata)
    #
    #     # Commit the data
    #     sanefConnection.commit()
    #     print('Data Saved Successfully')
    #
    # except dbconn.getSanefDBConnection().DatabaseError as e:
    #     print('Something wrong, please check:', e)
    #
    # # finally:
    # clscursor = cursor2.close()
    # print(clscursor)
    # # Close the connection
    # clsconnection = sanefConnection.close()
    # print(clsconnection)
    # # bvnConnection.close()

    #return json_data

dAOConnectionFecthAgentRecord()




