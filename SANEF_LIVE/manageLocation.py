import config as dbconn

sanefConnection = dbconn.getSanefDBConnection()
cursor2 = sanefConnection.cursor()

sql = """SELECT * FROM state"""
cursor2.execute(sql)

rows = cursor2.fetchmany()

for getinput in rows:
    print(getinput)