# HolidayListV2
This is a second upload as there was an issue with the first one.
The aim of this project was to design and implement a text-based application to keep track of holidays, scraped from timeanddate.com.
The holidays were scraped from 2020 to 2024 and saved as data-class objects with attributes for name and date (the scraped dates were just the month and day,
the year was concatenated on later. There is some redundancy in the data values as there was also redundancies on the host site (the same holiday was mentioned
multiple times across different categories, but there was no simple or straight-forward way to isolate a unique holiday from the scraping) as a result some
data cleaning is still needed. 
Addionally, an API call was made to openweathermap, to get a seven day forecast (with the current day as well) for a feature where, if the dates of the holidays
veiwed matched the current week, the forecast would be applied to the holidays as well for an additional reference. There is some ironing-out that still needs to
be implemented in the design w.r.t this feature, but the connections are there in the general picture. 
It has a feature where the holidays can be saved as a .json, and an addional feature where it can be saved as a .csv (pending)
For the most part, the code deals with error-handling but due to time restrictions, it was not universally implemented.

A folder called plans is attached, with a .pdf and two other python files.
The .pdf goes over a very high-level overview of the flow of the application, as visualized in the pre-planning stages.
The two additonal python files are what I used for reference (from my own work and stackoverflow) to build some of my functions and test smaller bits of my main code.
They can be thought of aides to my thought-process.
