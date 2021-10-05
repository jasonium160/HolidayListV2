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

    #this dunder returns the holiday as the required output: name (date)
    def __str__(self):
        return '{} ({})'.format(self.name, self.date)

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
    hyr = hyear.split('/')[5]
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
#I didn't design removeHoliday with a decorator in mind, so the decorator is pretty
#useless here, but I included it because it was requried
#I think I have the gist of them, but I'll have to experiment more before I can
#do something useful with them
#------
def decorFn(f):
    def wrapperFn(*args, **kwargs):
        print("Let's delete or try to delete this record!")
        return f
    return wrapperFn

@decorFn
def fdel():
    print('Successfully Deleted!\n')
#------
#loops through hoilday list and removes input name if there, otherwise
#goes back to menu or try again
def removeHoliday(holidaylist):
    print("""
        Remove a Holiday
        ================
    """)
    
    #not a neat way of doing it, but it sort of works, not efficient though
    name1 = str(input("What's the name of the holiday you'd like to remove: "))
    for i in range(0,len(holidaylist)):
        if holidaylist[i].name == name1:
            del(holidaylist[i])
            fdel()
            print(name1, "has been removed from the holiday list!")
            break
        else:
            continue
    
    print("Not in here! or not in here anymore!")
    goback1 = str(input('Go back to main menu? [y/n]')).lower()
    if goback1 == 'y':
        mainMenu()
    else:
        removeHoliday(holidaylist)

#-------------------------------------------------------------------
#saves the list as a dictionary then as a .json
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
#handling my api call here 
def getForecast():
    import datetime
    from datetime import datetime
    import requests

    today = date.today()

    #for minneapolis, need to figure out how to hide on git, but it's a free key so not that sensitive
    lat = 44.98
    lon = -93.27
    exclude = "minutely,hourly,alerts"
    APIkey = '33290dce4656d6e45908955c2583cc6e'

    url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={exclude}&appid={APIkey}'
    req = requests.get(url)
    wdata = req.json()

    #got list to store the 7 day forecast including current day
    wforecast = [] #forecast saved in this list
    wfdate = [] #date saved in this list
    for day in wdata['daily']:
        wforecast.append(day['weather'][0]['description'])
        dt = int(day['dt'])
        dt = datetime.utcfromtimestamp(dt).strftime('%Y-%m-%d')
        wfdate.append(dt)

    wf = dict(zip(wfdate, wforecast)) #combined the two lists into a dictonary with date as key
    return wf

#-------------------------------------------------------------------
#view holidays within a given week and year
def viewHoliday(holidaylist):
    import datetime
    from datetime import date

    print("""
        View Holidays
        ==============
    """)
    try:
        year = int(input('What year in the range [2020-2024]? '))
        if year > 2024 or year < 2020:
            print('Outside range! try something between 2021 and 2024!')
            viewHoliday(holidaylist)
    except ValueError:
        print('what?? :<')
        viewHoliday(holidaylist)

    try:
        week = int(input('Which week? [1-52]? or 53 for current week: '))
        if week > 53 or week < 0:
            print('Outside range!, start again!!')
            viewHoliday(holidaylist)
    except ValueError:
        print(':/ back to the top!')
        viewHoliday(holidaylist)

    wf = getForecast()

    if week != 53:
        startweek = getSDate(year, week)
        endweek = startweek + datetime.timedelta(days=6.9)
        holidayhold = list(filter(lambda h: h.date > startweek and h.date < endweek, holidaylist))

        print('='*25)

        for h in holidayhold:
            print(h)

        print('='*25)

    else:
        startweek = date.today()
        endweek = startweek + datetime.timedelta(days=6.9)
        holidayhold = list(filter(lambda h: h.date > startweek and h.date < endweek, holidaylist))

        print('=0'*25)
        print('')

        for h in holidayhold:
            datestr = str(h.date)
            print(h, " ...... Expected weather in Minneapolis, for that day: ", wf[datestr])

        print('')
        print('=0'*25)
    
    print('')
    goback1 = str(input('Want to check out another time range? [y/n]')).lower()
    if goback1 == 'y':
        viewHoliday(holidaylist)
    else:
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
        exit()
    else:
        mainMenu()

#----------------------------------------------------------------------------------------------------

print("""
    ---|| Holiday Management ||---
    ==============================
""")
print('There are currently: ', len(holidaylist), ' holidays in the system, including duplicates :(')
mainMenu()

#----------------------------------------------------------------------------------------------------