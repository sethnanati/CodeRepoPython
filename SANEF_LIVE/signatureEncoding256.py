import hashlib
from dateFormater import timing
from config import oauth, credentials
import string
import random

def encrypt_string():
    curdate = str(timing())
    hash_string = credentials()['agentManagerCode']+curdate+oauth()['password']
    #print(hash_string)
    sha_signature = hashlib.sha256(hash_string.encode('utf-8')).hexdigest()
    #print(sha_signature)
    return sha_signature

#encrypt_string()

def rand_string():
    size = 10
    chars = string.ascii_letters + string.digits + string.punctuation
    password = random.choice(string.ascii_lowercase)
    password += random.choice(string.ascii_uppercase)
    password += random.choice(string.digits)
    password += random.choice(string.punctuation)
    for i in range(6):
        password += random.choice(chars)
    passwordList = list(password)
    random.SystemRandom().shuffle(passwordList)
    psswd = ''.join(passwordList)
    #print(psswd)
    return psswd

#rand_string()



