import config as dbconn
import pandas.io.sql as psql
import pandas as pd
import numpy as np

agentDBConnection = dbconn.getDAOConnectionAgency()
cursor = agentDBConnection.cursor()

sanefDBConnection = dbconn.getSanefDBConnection()
cursor2 = sanefDBConnection.cursor()

# sql = """SELECT CASE WHEN LENGTH(MOBILE_NO) <= 10 THEN 234||MOBILE_NO WHEN LENGTH(MOBILE_NO) = 11 THEN 234||SUBSTR(MOBILE_NO, -0, 10)
# ELSE MOBILE_NO END AS MOBILE_NO , TO_CHAR(REQUEST_DATE, 'YYYY-MM-DD') AS transactionDate,
# COUNT(AGENT_CODE) AS cashInCount, SUM(AMOUNT) AS cashInValue, REQUEST_TYPE FROM (
# SELECT A.MOBILE_NO, B.REQUEST_DATE, B.AGENT_CODE, B.AMOUNT, B.REQUEST_TYPE,  B.BILLER_RSP_CODE
# FROM MESB_SADC.BIL_AGENT_INFO A, MESB_SADC.BIL_AGENT_LOG B WHERE A.AFFILIATE_CODE = 'ENG'
# AND A.AGENT_CODE = B.AGENT_CODE AND B.REQUEST_TYPE = 'CASHIN' UNION
# SELECT A.MOBILE_NO, B.REQUEST_DATE, B.AGENT_CODE, B.AMOUNT, B.REQUEST_TYPE,  B.BILLER_RSP_CODE
# FROM MESB_SADC.BIL_AGENT_INFO A, MESB_SADC.BIL_AGENT_LOG B WHERE A.AFFILIATE_CODE = 'ENG'
# AND A.agent_CODE = B.AGENT_CODE AND B.REQUEST_TYPE = 'CASHOUT') WHERE  BILLER_RSP_CODE = '000'
# AND TO_CHAR(REQUEST_DATE, 'YYYY-MM-DD') = TO_CHAR(SYSDATE-22, 'YYYY-MM-DD') AND MOBILE_NO = '2349036214350'
# GROUP BY MOBILE_NO, TO_CHAR(REQUEST_DATE, 'YYYY-MM-DD'), REQUEST_TYPE, BILLER_RSP_CODE
# ORDER BY MOBILE_NO DESC"""

sql = """SELECT  TRANSACTIONDATE AS TXNDATE, MOBILE_NO AS MOBNO, SUM(CASHOUTCOUNT) AS CONUM, SUM(CASHOUTVALUE) AS COVAL, SUM(CASHINCOUNT) AS CINUM, SUM(CASHINVALUE) CIVAL, REQUEST_TYPE RTYPE
FROM (SELECT CASE WHEN LENGTH(MOBILE_NO) <= 10 THEN 234||MOBILE_NO WHEN LENGTH(MOBILE_NO) = 11 THEN 234||SUBSTR(MOBILE_NO, -0, 10) ELSE MOBILE_NO END AS MOBILE_NO, 
TO_CHAR(REQUEST_DATE, 'YYYY-MM-DD') AS TRANSACTIONDATE, COUNT(CASHOUTVALUE) AS CASHOUTCOUNT, SUM(CASHOUTVALUE) AS CASHOUTVALUE, COUNT(CASHINVALUE) AS CashinCount, 
SUM(CASHINVALUE) AS CASHINVALUE, REQUEST_TYPE FROM (SELECT A.MOBILE_NO, B.REQUEST_DATE, B.AGENT_CODE, CASE WHEN B.REQUEST_TYPE = 'CASHOUT' THEN B.AMOUNT END AS CASHOUTVALUE, 
CASE WHEN B.REQUEST_TYPE = 'CASHIN' THEN B.AMOUNT END AS CASHINVALUE, B.REQUEST_TYPE,  B.BILLER_RSP_CODE  FROM MESB_SADC.BIL_AGENT_INFO A, MESB_SADC.BIL_AGENT_LOG B WHERE A.AFFILIATE_CODE = 'ENG' 
AND A.agent_CODE = B.AGENT_CODE) WHERE  BILLER_RSP_CODE = '000'  AND TO_CHAR(REQUEST_DATE, 'YYYY-MM-DD') = 
TO_CHAR(SYSDATE -29, 'YYYY-MM-DD') AND REQUEST_TYPE IN ('CASHOUT', 'CASHIN') ----AND MOBILE_NO = '2349036214350' 
GROUP BY MOBILE_NO, TO_CHAR(REQUEST_DATE, 'YYYY-MM-DD'), REQUEST_TYPE, BILLER_RSP_CODE  
ORDER BY MOBILE_NO DESC
) GROUP BY TRANSACTIONDATE, MOBILE_NO, CASHOUTCOUNT, CASHOUTVALUE, CASHINCOUNT, CASHINVALUE, REQUEST_TYPE"""
cursor.execute(sql)
rows = cursor.fetchmany()
print(type(rows))

# rowcount = 0
#
# for transList in rows:
#         rowcount += 1
#         print('Next Agent:', transList[1], rowcount)
#         if len(transList[1]) == 2:
#             print(transList)

arow=rows
uniques=[]
dups=[]

for a in arow[1]:
    print(a)
    #for each in a:
    #   print(each)
    #     if each not in uniques:
    #         uniques.append(each)
    #     else:
    #         dups.append(each)
    # print("Unique values are below:")
    # print(uniques)
    # print("Duplicate values are below:")
    # print(dups)

# count = 0
# for row in rows:
#     count+= row
#     print(count)

#df = DataFrame(cursor.fetchall())
#df.columns = cursor.keys()
# pd.set_option('display.max_columns', 7)
#
# df = psql.read_sql_query(sql, agentDBConnection)
# df = df.applymap(str)
#print(df)
#print(df.replace('nan', '').groupby('MOBNO').agg({'TXNDATE': 'first', 'CINUM':'first','CIVAL': ', '.join, 'CONUM':'first','COVAL':'first','RTYPE':'first' }).reset_index())

#print('new_func:', pd.pivot_table(df, index=['MOBNO','TXNDATE'], aggfunc='sum')
#print('GroupBy_apply:', df.groupby("MOBNO")['CINUM'].apply(' '.join).reset_index(), sep=',')
#print('Group By Size:', df.groupby(['MOBNO']))
#rColmn = df.to_string(header=False)
#print(rColmn)
# getList = []
#
# grp = df.groupby('MOBNO')
# for mobNo, group in grp:
#     if len(group.index) == 2:
#         getTwoMore = group.to_string(header=False)
#         #print(type(getTwoMore))
#         #print('DoubleTrans:', '\n', getTwoMore)
#         print(getTwoMore[-1])

    # elif len(group.index) == 1:
    #     print(group.to_string(header=False))
    # else:
    #     print(group.to_string(header=False))

        #     getles = len(group.index) < 2
    #     group.to_string(header=False)
    #     print('singleTrans:', getles)
        #print('new_func:', group.pivot_table(group, index=['MOBNO','TXNDATE'], aggfunc='sum'))

        # res = getTwoMore.strip('][').split(', ')
        # print('res', res, sep= '==>', end=', ')




        #condata = '|'.join(group.index)
        #condata = pd.merge(group, on='MOBNO' )
        #print(group, end = ' | ')
    #print(group)
    #print()
#[CONUM"]["COVAL"]["CINUM"]["CIVAL"]["RTYPE"]).sum)
#print (grouped_df)

#grouped_pf = df.groupby("MOBNO").apply(lambda x: "%s" % ' '.join(x['CINUM']))
#print(grouped_pf)

## Select all duplicate rows based on one column
#duplicateRowsDF = df[df.duplicated(['MOBNO'])]

#print("Duplicate Rows based on a single column are:", duplicateRowsDF)
# rowcount = 0
#
# for agentDBrowResult in row:
#         rowcount += 1
#         #print('Next Agent:', agentDBrowResult)
#         data = agentDBrowResult
#         anoData = rowcount, data[0], data[1], data[2], data[3], data[4], '','',''
#         #print('data', anoData)
#         qData = [anoData]
#         print('Ano:,', anoData)
#
#         try:
#
#             #qData = [(1, '2349098697829', '2019-08-17', '2', '4400', 'CASHIN', ' ', ' ', ' ')]
#
#             insert = "INSERT INTO SANEF.SANEF_TRANS_SUMMARY(ROW_ID, MSISDN, TRANSDATE, TRANSCOUNT, TRANSAMOUNTSUMMARY, TRANSTYPE, ADDITIONAL1, " \
#             "ADDITIONAL2, ADDITIONAL3) values (:1, :2, to_date(:3, 'YYYY-mm-dd'), :4, :5, :6, :7,  :8, :9)"
#
#             cursor2.prepare(insert)
#
#             # Execute the sql query
#             cursor2.executemany(None, qData)
#
#             # Commit the data
#             sanefDBConnection.commit()
#             print('Data Saved Successfully')
#
#         except dbconn.getSanefDBConnection().DatabaseError as e:
#             print('Something wrong, please check:', e)
#
# # finally:
# clscursor = cursor2.close()
# print(clscursor)
# # Close the connection
# clsconnection = sanefDBConnection.close()
# print(clsconnection)
# #bvnConnection.close()



