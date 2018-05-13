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


def attendence_record(base_url):
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
    data = data.drop[0, axis =1]
    data.columns = ['Team', 'Total Attendence', 'Number of Home Games' , 'Average Attendence']
    
    return(data)
    