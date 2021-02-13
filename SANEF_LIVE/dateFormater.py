from datetime import  date

def timing():
    dttimer = date.today()
    finetime = dttimer.strftime('%Y%m%d')
    #print('datetime:', finetime)
    return finetime

timing()