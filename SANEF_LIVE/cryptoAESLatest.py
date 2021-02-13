import json


from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from config import oauth

BLOCK_SIZE = 16

def encrypt(data):
    obj = AES.new(oauth()['apiKey'], AES.MODE_CBC, oauth()['ivKey'])
    encdata = obj.encrypt(pad(data, BLOCK_SIZE))
    cipherhexdata = (encdata.hex())
    #print('cipherhexdata:', cipherhexdata)
    return cipherhexdata

# data =  {"additionalInfo1": "", "additionalInfo2": "", "bvn": "22172180083", "city": "Ogun",
#                  "emailAddress": "Josephajayiseun06@gmail.com", "latitude": "6.6000", "longitude": "6.6000",
#                  "lga": "Ilaro", "state": "Ogun", "firstName": "AJAYI", "lastName": "Oluwaseun", "middleName": "Joseph",
#                  "title": "Mr", "phoneList": "2347033836645", "servicesProvided": "CASH_IN,CASH_OUT", "username": "Josephajayiseun06",
#                  "streetNumber": "8", "streetName": "8OkeElaIpariodaStreetIlaro",
#                  "streetDescription": "8OkeElaIpariodaStreetIlaro", "ward": "Ilaro", "password": "R@asnd0m"}

# data = {"additionalInfo1": "", "additionalInfo2": "", "bvn": "22172180083", "city": "Ogun",
#                  "emailAddress": "JOSEPHAJAYISEUN06@GMAIL.COM", "latitude": "6.6000", "longitude": "6.6000",
#                  "lga": "Ilaro", "state": "Ogun", "firstName": "AJAYI", "lastName": "OLUWASEUN", "middleName": "JOSEPH",
#                  "title": "Mr", "phoneList": "2347033836645", "servicesProvided": "CASH_IN,CASH_OUT", "username": "JOSEPHAJAYISEUN06",
#                  "streetNumber": "8", "streetName": "8 OKE ELA IPARIODA STREET ILARO",
#                  "streetDescription": "8 OKE ELA IPARIODA STREET ILARO", "ward": "8 OKE ELA IPARIODA STREET ILARO", "password": "R@asnd0m"}
#encodedata = str(data).encode('utf-8')
#encrypt(encodedata)
#8df5f83f15000c59fd3384355117cb9ad495989b91063623bf67af3bea6cdf96637ed5e6cb96f5fa3ad3f09cae7e98db28ca322a8cec74f24d68ca21b5785a56dd828e34a3d46f38fa6615d5ff3e98de57d20d9c20fd7e44bed4e554801f042946e5b9bd1b129ff15d8cbedc3500c6995ea84ba426385b39dfa93cb26075ed358bb191f0ce3013f9ff3f4b3a213b7ee7df052ff1ad0ab99937d6228ddd417778f6d0df255e2e6775d659e4ea434064c2144681ff50b0f7c9bdccc47c22e82963b2fda8700dae4a30561368812272ee3e9891537fb286cb7723d4ba5b7910bb7e0e6340660e52053c40e22b3b5fc6cee5ef9fff622f6e01df08c8fc360e1adde4748b8f7df1f6222390e78269d3a54b90445defdbe139a370e80acc85ea4d607ecb66ea63dacaaf136224f0e24fdcee6b5bbb24c23c42c2c2e9790a891723ed8c0ad6b443d5e465f08f972891ab646e21c6c3824b0774e50eb6eacb2531deb2c2b99cf0099b0893435be1b178131b27c62a91518c21cfea626dce29ca2ca524aba6dabe427bcd13ac7c9888d6e8638bfc831c5be6fc5d68c5b87aa851a38a20ae424933266a23e5bc939f83ebde0dc26a3a7f6f51846868e76c36fc849b5ebe6656004995adc318c8ca77a69640ba4b2d4a72f3f8cf1b39d073da8abca1276d6bd35f568d5e52290dad1c0a371778599977607553614cb54af528978409b2454017cb2dafbbfc8363434d1ff4cab820c5606a3448fd8e7c8b3ad5873e32b92ccad38246238a69816104e4d0301336b27c90a1f0bad14dc122821ec53ed3530e0112cb08ae30b3b1c6456930273f1543de