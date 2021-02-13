
import config as dbconn

def dAOConnectionFecthAgentRecord():

    # Get the sql connection for SANEF Database
    sanefConnection = dbconn.getSanefDBConnection()
    cursor2 = sanefConnection.cursor()

    sql = """SELECT bvn FROM(SELECT * FROM SANEF.SANEF_AGENT_RECORD WHERE 
    BVN NOT IN(SELECT BVN FROM SANEF.SANEF_CREATE_AGENT))"""
    cursor2.execute(sql)

    rows = cursor2.fetchmany()

    dataMsg = {}
    count = 0
    for row in rows:
        count+= 1
        data = row
        dataMsg['bvn'] = (data[4])
        print(count, dataMsg['bvn'])

    # dataMsg = {}
    # increser = 0
    #
    # for agentDBrowResult in row:
    #      print('Next Agent:', agentDBrowResult)
    #      data = agentDBrowResult
    #      print('data',data)
    #
    #      for row in data:
    #          print('roq:',row)

         # dataMsg['bvn'] = (data[4])
         # count = 0
         # for row in (dataMsg['bvn']):
         #     count+= int(row)
         #     print(count, dataMsg['bvn'], sep='==>')

dAOConnectionFecthAgentRecord()