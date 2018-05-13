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



