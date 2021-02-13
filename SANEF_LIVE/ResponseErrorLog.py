def ErrorLog():
     return {'00': 'Successful response', '04': 'Invalid Agent Request', '05': 'Invalid LGA','07': 'Invalid Service Provided',
             '08': 'Invalid BVN', '10': 'Invalid Agent', '11': 'Invalid Transaction Date Format', '12': 'Database Error',
             '13': 'Transaction Report Threshold Exceeded','14': 'Invalid Bulk Transaction Report', '15': 'Invalid Amount',
             '16': 'Invalid Value Number', '17': 'Invalid Transaction Report','18': 'Invalid Transaction Summary Report',
             '19': 'Invalid Reset Request', '20': 'Invalid Institution', '21': 'No Services','22': 'System Error',
             '23': 'Unable to generate credentials', '24': 'Invalid Latitude (must be four decimal places)',
             '25': 'Invalid Longitude (must be four decimal places)', '26': 'Invalid Transaction Month', '27': 'Invalid Transaction Day',
             '28': 'Password Policy Violation (The password MUST contain small letters, capital letters, special characters and numbers. It must not exceed fifteen characters and not less than eight characters)',
             '29': 'BVN exists', '30': 'Invalid e-mail address', '31': 'Unable to generate  code', '32': 'Agent already exist',
             '33': 'Agent does not exist', '34': 'Agent username exist', '35': 'Unable to create user', '36': 'Unable to create agent',
             '37': 'User email exist', '38': 'Invalid agent request', '051': 'Invalid State', '200':'Request successfully executed',
            '415':'Unsupported media type. Media type must be application/json',
            '401':'Unauthorized', '500':'Internal Server error', '400':'Invalid request'}

#print( ErrorLog()['28'])

def URLError():
    return {'200':'Request successfully executed',
            '415':'Unsupported media type. Media type must be application/json',
            '401':',Unauthorized', '500':',Internal Server error', '400':',Invalid request'}
