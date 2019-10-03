#!/usr/bin/env python
# coding: utf-8

# In[34]:


from selenium import webdriver
import time
from bs4 import BeautifulSoup
from lxml import html
import requests
import os
import json


# In[38]:


def generate_sub_cat_list():
    with open('Subject_Categories.txt') as f:
        subject_categories_file = f.readlines()

    subject_list = []

    for line in subject_categories_file:
        cleaned_line = line.replace("\n", "").strip()
        subject_list.append('cc(' + cleaned_line[-4:] + ': ' + cleaned_line[:len(cleaned_line)-5] + ')')

    return subject_list


# In[36]:


driver = webdriver.Firefox(executable_path=r'/Users/chris/Data/Palakhfiles/Virginia_Tech/Digital_Libraries/geckodriver')
driver.get("https://search-proquest-com.ezproxy.lib.vt.edu/")
databasePageLink = driver.find_element_by_id("databasePageLink")
databasePageLink.click()

virginiaTechDb = driver.find_element_by_partial_link_text("Dissertations & Theses @ Virginia Polytechnic Institute and State University")
virginiaTechDb.click()

fullTextCheckbox = driver.find_element_by_id("fullTextLimit")
fullTextCheckbox.click()

time.sleep(2)

manuscriptTypeCheckbox = driver.find_element_by_id("allNotSelected_ManuscriptType")
manuscriptTypeCheckbox.click()

searchButton = driver.find_element_by_id("searchToResultPage")
searchButton.click()

time.sleep(10)

sub_cat_count_dict = {}

for category in generate_sub_cat_list():
    try:
        searchField = driver.find_element_by_id("searchTerm")
        searchField.clear()
        searchField.send_keys(category)
        driver.find_element_by_class_name("uxf-search").click()
        time.sleep(10)
        sub_cat_count_dict[category] = driver.find_element_by_id("pqResultsCount").get_attribute("innerHTML")
    except:
        driver.find_element_by_partial_link_text("return to previous result list").click()
        time.sleep(10)
    time.sleep(20)
    
with open("count_data.json",'w') as f: 
    f.write(json.dumps(sub_cat_count_dict, indent=2, sort_keys=True))

