import datetime 
import time


# def getThedate():
#     try:
#         date_entry = input('Enter a date in YYYY-MM-DD format: ')
#         year, month, day = map(int, date_entry.split('-'))
#         thedate = datetime.date(year, month, day)
#         return thedate
#     except:
#         print('something went wrong, try again!')
#         getThedate()

# d1 = getThedate()
# print(d1)

def getThedate():
    badent = True
    while badent:
        try:
            udate = input('Enter a date as YYYY-MM-DD: ')
            year, month, day = map(int, udate.split('-'))
            thedate1 = datetime.date(year,month,day)
            thedate = thedate1
            badent = False
        except:
            print('something went wrong!')
            badent = True
        else: 
            return thedate

d1 = getThedate()
print(d1)
print(type(d1))