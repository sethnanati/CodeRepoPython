import re

# def emailChecker(value):    



regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

# Define a function for# for validating an Email
def validateEmail(email):    
    # # pass the regualar expression    
    # # and the string in search() method    
    if (re.search(regex, email)):        
        return True
    else:
        if len(email) >= 5:        
            if '@' in email:            
                if '.com' in email:                
                    if '.co' in email:                    
                        return True                
                    else:                    
                        return False            
                else:                
                    return False        
            else:            
                return False    
        else:        
            return False        
    
    return email

validateEmail('adeyemi@yahoo.')
    
#idowutoye@yahoo.co.uk None 2348033244815

