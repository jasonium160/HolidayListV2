from bs4 import BeautifulSoup as bs
import requests
from dataclasses import dataclass
from datetime import date, datetime
import json

#some stuff might be residual from my testing, didn't have enough time to 
# clean up properly
#==========================================================================

#the dataclass for holidays, i'm storing them as a list of objects in 
#holidaylist
@dataclass
class Holidays:
    name: str
    date: datetime.date

#--------------------------------------------------------------------------
#storage variables for scraping
startyr = 2020 #start year
endyr = 2024 #end year
#these are intermediate, holding in-between values until i make my final list
hyears = [] #store each page from the site correspoding to a year of holidays
hdates =[] #store the scraped dates month and day
hnames = [] #store thes scraped holidays <--wasted a lot of time trying to remove duplicates
hspecyr = [] #stored the year of the page so i can concat it to my dates

#------scraping for holidays from the given site
for i in range(startyr, endyr+1):
    url = ('https://www.timeanddate.com/holidays/us/{}').format(i)
    hyears.append(url)

#---for each year i scrape for dates and holidays
for hyear in hyears:
    hyr = str(i)
    holidayinfo = requests.get(hyear)
    hsoup = bs(holidayinfo.text, 'html.parser')

    table = hsoup.find('tbody').find_all('tr')
    for tr in table:
        hdate = tr.find_all('th')
        for hd in hdate:
            hdates.append(hd.getText())
            hspecyr.append(hyr)
        
        hname = tr.find_all('a')
        for hn in hname:
            hnames.append(hn.getText())

#another intermiedate - will store combined dates here (month + date)
combdate = []
d2 = []# will store combined dates with year (year + combdate)
combdate = list(zip(hdates,hspecyr))
for i in range(0,len(combdate)):
    dte, yr = combdate[i]
    d = dte + " " + yr
    d = (datetime.strptime(d, '%b %d %Y')).date()
    d2.append(d)
#now that i have a proper date with the year, i make my holiday list using
#objects from the holidays class to store the values i scraped (name and date)
holidaylist = []
for i in range(0, len(d2)):
    holidaylist.append(Holidays(hnames[i],d2[i]))
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
def mainMenu():
    print("""
        Holiday Menu
        =============
        [1]. Add a Holiday
        [2]. Remove a Holiday
        [3]. Save Holiday List
        [4]. View Holidays
        [5]. Exit
    """)
    try:
        selection = int(input("Choose an option: "))
        if selection == 1:
            addHoliday(holidaylist)
        elif selection == 2:
            removeHoliday(holidaylist)
        elif selection == 3:
            saveHoliday(holidaylist)
        elif selection == 4:
            viewHoliday(holidaylist)
        elif selection == 5:
            exitMenu()
        else:
            print('wait, what? choose an option from 1 to 5!')
            mainMenu()
    except ValueError:
        print('Huh? :^/')
        mainMenu()       
#-------------------------------------------------------------------
#used to get the check and get the date in the addholiday method
def getThedate():
    import datetime
    badent = True
    while badent:
        try:
            udate = input('Enter a date as YYYY-MM-DD: ')
            year, month, day = map(int, udate.split('-'))
            thedate1 = datetime.date(year,month,day)
            thedate = thedate1
            badent = False
        except:
            print("That's not a valid date! Try again.")
            badent = True
        else: 
            return thedate
#-------------------------------------------------------------------
#adds a holiday if the date is good
def addHoliday(holidaylist):
    print("""
        Add a Holiday
        =============
    """)

    hname = str(input("What's the name of this holiday?: "))
    hdate = getThedate()
    print('previous list size: ', len(holidaylist))
    holidaylist.append(Holidays(hname,hdate))
    print('new list size: ', len(holidaylist))
    print(hname, ", observed on: (", hdate, ") has been successfully added!")
    print('\n----------->Returning to main menu!')
    mainMenu()

#-------------------------------------------------------------------
#loops through hoilday list and removes input name if there, otherwise
#goes back to menu or try again
def removeHoliday(holidaylist):
    print("""
        Remove a Holiday
        ================
    """)
    name1 = str(input("What's the name of the holiday you'd like to remove: "))
    for i in range(0,len(holidaylist)):
        if holidaylist[i].name == name1:
            del(holidaylist[i])
            print('Success!:\n')
            print(name1, "has been removed from the holiday list!")
            break
        else:
            continue
    
    print('not here!')
    goback1 = str(input('go back to menu? or try again? [y/n]')).lower()
    if goback1 == 'y':
        mainMenu()
    else:
        removeHoliday(holidaylist)

#-------------------------------------------------------------------
#saves the list as a .json, the format's a bit off though
def saveHoliday(holidaylist):
    import json
    print("""
        Save Holiday List?
        ==================
    """)
    save = str(input('Are you sure you want to save your changes? [y/n]')).lower()
    if save == 'n':
        print('OK, taking you back to the Main Menu!')
        mainMenu()
    else:
        with open('holidays.json', 'w') as f:
            for i in range(0, len(holidaylist)):
                json.dump(holidaylist[i].__dict__, f, indent=4, default=str)
    print("Somewhat successfully saved as .json")
    print("--------> Returning to main menu!")
    mainMenu()

#-------------------------------------------------------------------
#gets the year and week for viewholiday
#adapted from stackoverflow, takes a year and week and returns a date to iso standard
def getSDate(year, week):
    import datetime
    startweek = datetime.datetime.strptime(f'{year}-W{int(week)-1}-1', "%Y-W%W-%w").date()
    return startweek

#-------------------------------------------------------------------

today = date.today()
print(today.day)

#for minneapolis
lat = 44.98
lon = -93.27
exclude = "minutely,hourly,alerts"
APIkey = '33290dce4656d6e45908955c2583cc6e'

url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={exclude}&appid={APIkey}'
req = requests.get(url)
wdata = req.json()

wforecast = []

for day in wdata['daily']:
    wforecast.append(day['weather'][0]['description'])

print(wforecast)
#-------------------------------------------------------------------
#view holidays within a given week and year
#not fool-proof! be careful with values, didn't have enough time to fix!
def viewHoliday(holidaylist):
    import datetime
    from datetime import date
    import requests

    #handling my api call here as it's only relevant here
    today = date.today()

    #for minneapolis
    lat = 44.98
    lon = -93.27
    exclude = "minutely,hourly,alerts"
    APIkey = '33290dce4656d6e45908955c2583cc6e'

    url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={exclude}&appid={APIkey}'
    req = requests.get(url)
    wdata = req.json()

    #got list to store the 7 day forecast including current day
    wforecast = []
    for day in wdata['daily']:
        wforecast.append(day['weather'][0]['description'])

    #sort of works, I need more time to fix it, blank entry for week was giving me some looping errors
    #so i set it to 53 for current week instead; it calls the weather list from the api, but i still have to
    #pair the values in the print statement so it looks better and makes more sense
    print("""
        View Holidays
        ==============
    """)
    year = int(input('What year in the range [2020-2024]? '))
    week = int(input('Which week? [1-52]? or 53 for current week: '))
    if week != 53:
        startweek = getSDate(year, week)
        endweek = startweek + datetime.timedelta(days=6.9)
        holidayhold = list(filter(lambda h: h.date > startweek and h.date < endweek, holidaylist))

        for h in holidayhold:
            print(h.name, ":", h.date)

    else:
        startweek = date.today()
        endweek = startweek + datetime.timedelta(days=6.9)
        holidayhold = list(filter(lambda h: h.date > startweek and h.date < endweek, holidaylist))

        for h in holidayhold:
            print(h.name, ":", h.date)
        
        print('\nweather for that week: ')
        for weather in wforecast:
            print(weather)

    print('--------->Returning to main menu!')
    mainMenu()

#-------------------------------------------------------------------

def exitMenu():
    print("""
        Exit
        =====
        Any unsaved changes will be lost.
    """)
    goBack = str(input('Are you sure you want to leave? [y/n]: '))
    if goBack == 'y':
        print('Goodbye!')
        return 0
    else:
        mainMenu()

#-------------------------------------------------------------------

print("""
    ---|| Holiday Management ||---
    ==============================
""")
print('There are currently: ', len(holidaylist), ' holidays in the system, including duplicates :(')
mainMenu()

#----------------------------------------------------------------------------------------------------