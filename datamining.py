#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 12:56:47 2018

@author: prabhpahul
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv, json, os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import pickle
import time
import pandas as pd
import re



#soup_child = BeautifulSoup(soup_div,'html.parser')

cwd = os.getcwd()
print(cwd)
dataset =pd.read_csv('subtype1.csv',header = 0)
dataset = dataset.iloc[:, 0].values
for values in dataset:
    values = values.split("|")
    print(values)
    final_strings = []
    for val in values[1:]:
        stringToSearch = values[0] + " "+ val
        final_strings.append(stringToSearch)
    print(final_strings)  
    anchor=[]
    directory=[]
    for i in final_strings: 
        print(i)
        driver = webdriver.Chrome("/Users/prabhpahul/Downloads/chromedriver")
        driver.get("https://www.ncbi.nlm.nih.gov/pubmed/")
        inputElement = driver.find_element_by_id("term")
        inputElement.send_keys(i)
        driver.find_element_by_id('search').click()
        driver.implicitly_wait(30)
        URL = driver.page_source
        bsoup = BeautifulSoup(URL,'html.parser')
        get_details = bsoup.find_all(id='pageno')
        get_values = bsoup.find_all(id="resultcount")
        try:
            number = int(get_details[0]['last'])
            print(get_details[0]['last'])
        except IndexError:
            number = 1  
        try:
            countResult = int(get_values[0]['value'])
            print(countResult)
        except IndexError:
            countResult = 0      
        if countResult > 0:
            for x in range(0, (number)):
                print("We're achieving something big ", x)
                URL = driver.page_source
                soup = BeautifulSoup(URL,'html.parser')
                driver.implicitly_wait(10)
                soup_div = soup.find_all("p","title")
                for a in soup_div:
                    print(a.a["href"])
                    prefix = "https://www.ncbi.nlm.nih.gov"
                    link = prefix + a.a["href"]
                    print(link)
                    anchor.append(link)
                 
                try:
                    driver.find_element_by_link_text('Next >').click()
                except NoSuchElementException:  #spelling error making this code not work as expected
                    pass    
            for anc in anchor:
                result={}
                result.clear()
                result["link"] = anc
                try:
                    f = urlopen(anc)
                except:
                   print(anc)
                   continue
                    
                soupLink = BeautifulSoup(f, 'html.parser')
                abstract = soupLink.find_all("div", class_="rprt_all")
                heading = abstract[0].find_next("h1")
                #heading = abstract.find_all("h1")
                result["heading"] = heading.get_text()
                abstractDiv = abstract[0].find_all("div",class_="abstr")
                print(anc)
                try:
                     result["abstract"] = abstractDiv[0].find_next("div").text
                except IndexError:
                    result["abstract"] = 'null'  
                directory.append(result)
                print("still on")
        else:
                result = {}
                result['result'] = "Not Result Found"
                directory.append(result)    
                print('no result') 
    filename = re.findall(r"[\w']+", i)
    filename = filename[0]+'_'+filename[-1]    
    print(filename)       
    with open(filename+'.txt', 'w') as file:
        for item in directory: 
           for key, value in item.items():
                file.write("---"+key+":: "+value+"\n")
    print('downloaded file', i)            
    driver.close()            
print("done go download")
    #element = driver.find_element_by_class_name('gs_ico_nav_next')
    #driver.execute_script("arguments[0].click();", element)
    #driver.find_element_by_link_text('Next').click()
    #element = driver.find_element_by_link_text('Next')
    #driver.execute_script("arguments[0].click();", element)
    #driver.find_element_by_link_text('Next').click()
#  
#with open("resultpitx1.json", "w") as writeJSON:
     #json.dump(anchor, writeJSON)   
#    if l is None:
#        print(link)
#    else:
#        print(l)