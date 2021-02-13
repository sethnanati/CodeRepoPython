import base64
from config import oauth, credentials

passwordkey = str(oauth()['password'])
#print(passwordkey)


amCode = str(credentials()['agentManagerCode'])
signatureformat = (amCode+':'+passwordkey)
#print(signatureformat)

data = (signatureformat.encode('utf-8'))
authencoded = base64.b64encode(data)
authdecoded = authencoded.decode('utf-8')
#print(authencoded)
