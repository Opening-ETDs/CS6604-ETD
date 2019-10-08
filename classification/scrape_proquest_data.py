#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from bs4 import BeautifulSoup
from lxml import html
import requests
import os
import json


# In[2]:


def write_metadata_file(abstract_link, subjectTitle):
    metadata_dict = {}
    session_requests = requests.session()
    source_code_text = session_requests.get(abstract_link).text
    soup = BeautifulSoup(source_code_text, "html.parser")
    for div in soup.findAll('div', {'class', 'display_record_indexing_row'}):
        key = div.find('div', {'class', 'display_record_indexing_fieldname'}).text.strip()
        for inner_div in div.findAll('div', {'class', 'display_record_indexing_data'}):
            if key == 'Identifier / keyword':
                value_list = []
                for span in inner_div.findAll('span'):
                    value_list.append(span.text.replace(';','').strip())
                metadata_dict[key] = value_list
                break
            if len(inner_div.findChildren()) > 0:
                value_list = []
                for child in inner_div.findChildren():
                    if child.text != '':
                        value_list.append(child.text.strip())
                metadata_dict[key] = value_list
            else:
                metadata_dict[key] = inner_div.text.strip()
    page_index = metadata_dict['ProQuest document ID'][0]
    doc_output_path = 'VT_ProQuest_Data/' + subjectTitle + '/' + str(page_index) + '/'
    if not os.path.exists(doc_output_path):
        os.mkdir(doc_output_path)
    with open(doc_output_path + str(page_index) + "_metadata.json",'w') as f: 
        f.write(json.dumps(metadata_dict, indent=2, sort_keys=True))


# In[3]:


def generate_sub_cat_list():
    with open('results/top_subject_categories.txt') as f:
        subject_categories_file = f.readlines()

    subject_list = []

    for line in subject_categories_file:
        cleaned_line = line.replace("\n", "").strip()
        subject_list.append(cleaned_line)

    return subject_list[12:13]


# In[4]:


def create_folders_for_top_sub_cat():
    for subjectTitle in generate_sub_cat_list():
        subjectTitle = subjectTitle[9:].replace(")", "").replace(" ","_")
        print(subjectTitle)
        folder_output_path_subject = 'VT_ProQuest_Data/' + subjectTitle + '/' 
        if not os.path.exists(folder_output_path_subject):
            os.mkdir(folder_output_path_subject)
            
create_folders_for_top_sub_cat()


# In[5]:


def scrape_page_data(page_source, subjectTitle):
    subjectTitle = subjectTitle.replace(" ","_")
    soup = BeautifulSoup(page_source, "html.parser")
    for abstract_link in soup.findAll('a', {'id', 'addFlashPageParameterformat_abstract'}):
        print(abstract_link.get('href'))
        print('\n')
        write_metadata_file(abstract_link.get('href'), subjectTitle)
        time.sleep(20)


# In[ ]:


driver = webdriver.Firefox(executable_path=r'/Users/palakhjude/Documents/Virginia_Tech/Digital_Libraries/Code/CS6604-ETD/classification/geckodriver')
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

selectSortTypeBtn = Select(driver.find_element_by_id('sortType'))
selectSortTypeBtn.select_by_value("DateDesc")

for category in generate_sub_cat_list():
    try:
        searchField = driver.find_element_by_id("searchTerm")
        searchField.clear()
        searchField.send_keys(category)
        driver.find_element_by_class_name("uxf-search").click()
        time.sleep(10)
        page_source = driver.page_source
        scrape_page_data(page_source, category[9:].replace(")", ""))
    except:
        print('Issue with category: ' + category)
    time.sleep(5)

