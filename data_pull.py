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

