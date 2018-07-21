#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 13 14:22:22 2018

@author: adamwarner
"""

import pandas as pd 
import numpy as np 
from bs4 import BeautifulSoup
import urllib
import seaborn as sns

headers = { 'User-Agent' : 'Mozilla/5.0' }


def attendance_record(base_url):
    ''' This function is going to attempt to retrieve a table and its results to get the 
    attendance records for the proper season''' 
    try:
        req = urllib.request.Request(base_url, None, headers)
        r = urllib.request.urlopen(req).read()
        
        soup = BeautifulSoup(r)
        
        
        rows = soup.find("table",attrs={'class':'standard_tabelle'}).find_all('tr')
        data = []
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
            
        data = pd.DataFrame(data)
        data = data.drop([0,len(data)-1],axis= 0)
        data = data.drop([0], axis =1)
        data.columns = ['Team', 'Total Attendence', 'Number of Home Games' , 'Average Attendence']
        
        return(data)
    except:
        return('Something went wrong please check the url')


def url_list(start_year):
    
    ''' Only goes back 10 years to start ''' 
    
    base = "http://www.worldfootball.net/attendance/eng-premier-league-"
    end_year = start_year + 1
    end_base = "/1/"
    url_list = [base + str(start_year-i) + str("-") + str(end_year-i) + end_base 
                for i in range(0,10)]
    return(url_list)


def combine_years(urls):
    ''' List Comprehension Is Amazing ''' 
    
    df_list = [attendance_record(j) for j in urls]    
    return(pd.concat(df_list))

attendance_ten_years = combine_years(urls = url_list(2017))
attendance_ten_years.index = range(len(attendance_ten_years))
attendance_ten_years["Total Attendence"] = [x.replace('.', '') for x in 
                    attendance_ten_years["Total Attendence"]]

attendance_ten_years["Average Attendence"] = [x.replace('.', '') for x in 
                    attendance_ten_years["Average Attendence"]]


''' Ideas... Get the stadiums, match the stadiums with the teams  from 

https://simple.wikipedia.org/wiki/List_of_English_football_stadiums_by_capacity 

'''


def stadium_capcity(wikipedia_url):
    
    try:
        req = urllib.request.Request(wikipedia_url, None, headers)
        r = urllib.request.urlopen(req).read()
        
        soup = BeautifulSoup(r)
    
        rows = soup.find("table", attrs = {'class': 'wikitable sortable'})
        data = []
        for row in rows:
            try: 
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele])
            except AttributeError:
                pass            
        data = pd.DataFrame(data)
        return(data)
    except: return("Error please check url")

stadiums = stadium_capcity("https://simple.wikipedia.org/wiki/List_of_English_football_stadiums_by_capacity")
    
stadiums.columns = ["Overall Rank", "Stadium", "Town/City", "Capacity" , "Club", 
                           "League (Tier)", "Rank Within League", "Notes"]

def clean_capacity(df): 
    try:
        if int(df.Capacity[20]) >= 0:
            return(df.Capacity[20:26])
        else: 
            return(df.Capacity)
    except: return(df.Capacity)
stadiums['Clean Capacity'] = stadiums.apply(clean_capacity, axis =1)

Premier_League = stadiums[stadiums["League (Tier)"] == "Premier League"]
Premier_League["Clean Capacity"] = [x.replace(',', '') for x in 
                    Premier_League["Clean Capacity"]]

Premier_League['Clean Capacity'] = Premier_League['Clean Capacity'].astype(int)

Premier_League['Clean Capacity'].describe()


## Alright well this is cool, but what about the best league in world... the MLS #### 

### Can we create some sort of visual that shows distance traveled and the result based on the color #### 
### Does the distance away from home have an affect on the result??? #### 


def Schedule(base_url):
    ''' This function is going to attempt to retrieve a table and its results to get the 
    attendance records for the proper season''' 
    try:
        req = urllib.request.Request(base_url, None, headers)
        r = urllib.request.urlopen(req).read()
        
        soup = BeautifulSoup(r)
        
        
        rows = soup.find("table",attrs={'class':'standard_tabelle'}).find_all('tr')
        data = []
        for row in rows:
                cols = row.find_all('td')
                cols = [ele.text for ele in cols]
                data.append([ele for ele in cols])
        data = pd.DataFrame(data)
        data = data.drop([3, 6, 7],axis= 1)
        data.columns = ['Date', 'Time', 'Home Team', 'Away Team', 'Score']
        data = data.drop([0], axis = 0)        
        return(data)
    
    except:
        return('Something went wrong please check the url')
    
### Date_extension ### 

def Clean_Data(Data): 
    
    Data['Date'] = pd.to_datetime(Data['Date'])
    j = pd.to_datetime(Data['Date'])[1]
    date = []
    for i in pd.to_datetime(Data['Date']):
        if pd.isnull(i): 
            date.append(j)
        else: 
            date.append(i)
            j = i
    
    Data['Date'] = date
    Data = Data.drop(Data[pd.isnull(Data['Score'])].index, axis = 0)
    Data["FT Score"] = [x.strip()[0:3] for x in Data["Score"]]
    Data["HT Score"] = [x.strip()[5:8] for x in Data["Score"]]
    
    return(Data)

MLS = Schedule('http://www.worldfootball.net/all_matches/usa-major-league-soccer-2017/')
EPL = Schedule('http://www.worldfootball.net/all_matches/eng-premier-league-2017-2018/')

MLS = Clean_Data(MLS)
EPL = Clean_Data(EPL)

def Count_Plot_HT_Scores(Data):
 return(sns.countplot(x="HT Score", data=Data))

def Count_Plot_FT_Scores(Data):
 return(sns.countplot(x="FT Score", data=Data))

def Team_Specific_HT_Score(Team, Data, Home):
    if Home == "Yes":
        return(sns.countplot("HT Score", data  = Data[Data['Home Team'] == Team]))
    else: 
        return(sns.countplot("HT Score", data  = Data[Data['Away Team'] == Team]))






    
    
