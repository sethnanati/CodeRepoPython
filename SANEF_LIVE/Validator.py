import re

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

# Define a function for
# for validating an Email
def validateEmail(email):
    # pass the regualar expression
    # and the string in search() method
    if (re.search(regex, email)):
        print("Valid Email")
        return email


def dataValidator(attr):
    try:
        if attr == 'bvn':
            if len(str(attr)) == 0:
                return False
            else:
                return attr
        else:
            if str(attr) == 'None':
                return False

    except Exception as e:
        print('error:', e)

    return attr






# email =  '1@.com'
# validateEmail(email)