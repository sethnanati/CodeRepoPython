import random

import requests
from Crypto.Cipher import AES
from cryptoAESLatest import encrypt
#from configReadWrite import readPrivateConfig
from signatureEncoding256 import encrypt_string
import authorizationEncoding64

#passwordkey = readPrivateConfig()[3]
#print(passwordkey)

base_data = encrypt()
print(base_data)
#base_data2 = 'DA1476BD0EE5384635CDAB5402C2AA551AD439CF276A7CA4AA0EE53CA7183FFB645D73F6702641D610A5570671EE31C757756FDE68EB164C0C1536ED91DFE31EAC5C7D6AC15A9867574564CC1B7EC86BB2E9587625A8C63386CF7324CA1F8576B5A810347738BECDE12BE5B144B981C2BA1BA94F5F15DADEEE21D32123894B16A9A01F4EA2E40956870C85D33FB05403DB1398BFA0B65016FF06AFA9764287F23FECFB77B873BA72ABC974456A86BAC4CCE5C4BA7D0FC473EEB9E18F94A777A7E6BE5306D593B5F3222E55CC4B15E51FEEA14C00963B367ACE3120F18D8540C6811B0A2B48588AF5EFD2F4AD28C7D3CF98C28F08AB2DF7ABDE8C97335EB580066558D38C566E69D2007DF0291C9612A43AD490BB2728F7E046DC8A0EA98212449564F00DA8E1455A5DE5E292AFC1168AE16296F17390B791BE7744255BAEAB9AD8D2E8D8D443CF315DEBDBB0E514B59A8A3D185FAFEBB7892E3F7AC05A5AAEF7139B4EFFB856543D7E4AA2B2245753D440C0229673412E99080DC4497962A76CA8DE62C5154949CE6C5B8F1F4CD96A7DD292B86903F2098B7D979D00AF0084F43F1DBF38F390B8F9227BB2B3C2F4787A182EE941B81661B19BEB60FE5934968B1925C364DB93C763B90C35F2B9EB45DFF126CB2D0C02013BEEE7FB1D92320DFF753BF977B70210F60E697B7687189B557B13655698756446033D82ADF4BD4A114B7E5B62ED5D60C672D55690F51365E8616B0E222F75D3D7BF9630F81EE5DEE6'
headers = {'Authorization':'MDAwMTM6UWdseWwxcUNsUA==', 'Signature':'93faba9c49a02b78df0b5c0bbc5d3f40e4ae11dc6b1bf20a508fc627c87915fc', 'Content-Type': 'application/json', 'HTTP method':'POST', 'Signature_Meth':'SHA256'}
serviceurl = requests.post('http://196.6.103.58:8080/agencybankingservice/api/agents/create/', data=base_data, headers=headers)

print(base_data,'\n', serviceurl.url,'\n','status code:', serviceurl.status_code, '\n', 'response:', serviceurl.text)

# print('Request', serviceurl.request, serviceurl.encoding)

# sendingmsg = serviceurl,base_data2,headers
# #print(sendingmsg)
# print('serviceurl:', serviceurl)
# # plainmessage = (base_data2, headers)
# print('plainmessage:',  plainmessage )
# print(headers)
# print('request:',serviceurl,base_data2.strip(""),headers)
#response = serviceurl(url=serviceurl, json=base_data2,headers=headers)
#print('response:', response.json())

# InitVector = 'ramgTPLVZVf8aFgK'
# key = 'U2m2snJoAPFbDJZ1'
#
# getlen = len(InitVector) % 16 != 0
# print(getlen)
# finalIV = (InitVector += ' ' * (16 - (len(InitVector) % 16)))
#
# for i in range(16):
#     InitVector += chr(random.randint(0, 0xFF))
#
# encryptor = AES.new(key, AES.MODE_CBC, InitVector)
# print(encryptor)
#
#
