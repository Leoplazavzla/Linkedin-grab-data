import os
import random
import sys
import time
from urllib.parse import urlparse
from selenium.common.exceptions import ElementNotInteractableException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import pandas as pd

# Open Webdriver
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome('chromedriver.exe', options=options)
driver.set_window_size(800,800)

# LinkedIn login page
driver.get('https://www.linkedin.com/uas/login')

# Getting login details
file = open('config.txt')
lines = file.readlines()
username = lines[0]
password = lines[1]
globalPauseTime = 3

# Insert Username
elementID = driver.find_element_by_id('username')
elementID.send_keys(username)

# Insert Password
elementID = driver.find_element_by_id('password')
elementID.send_keys(password)
time.sleep(globalPauseTime)

# Submit
elementID.submit()

# Reading excel file with LinkedIn Accounts
dataLocation = "accounts.xlsx"
df = pd.read_excel(dataLocation)

# Check number of rows
rows = len(df)

# Looking for each account
for row in range(rows):
    studentAccount = df.loc[row][0]
    searchURL = studentAccount
    driver.get(searchURL)

    # scrolling to the bottom and top again
    scrollPauseTime = 3
    height = driver.execute_script("return document.documentElement.scrollHeight")
    for i in range(1):
        # Scroll to the middle of the page
        driver.execute_script("window.scrollTo(0, " + str(height/2) + ");")
        time.sleep(scrollPauseTime-1)
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, " + str(height) + ");")
        # Scroll to the top of the page
        time.sleep(scrollPauseTime+1)
        driver.execute_script("window.scrollTo(0, 0); ")
        


        wait= WebDriverWait(driver, 5)
        connection = driver.find_element_by_class_name('dist-value').get_attribute("innerHTML").strip()
        if(connection == '1st'):
            name = driver.find_element_by_class_name('text-heading-xlarge').get_attribute("innerHTML")
            job_title = driver.find_element_by_class_name('text-body-medium break-words'.replace(' ', '.')).get_attribute("innerHTML").strip()
            location = driver.find_element_by_class_name('text-body-small inline t-black--light break-words'.replace(' ', '.')).get_attribute("innerHTML").strip()
            time.sleep(scrollPauseTime+1)
            company_link = driver.find_element(By.XPATH, "//*[@data-field='experience_company_logo']").get_attribute("href")
            contactDetails = driver.find_element_by_link_text('Contact info')
            contactDetails.click()
            time.sleep(scrollPauseTime+2)
            email_section =  driver.find_element(By.XPATH, "//section[@class='pv-contact-info__contact-type ci-email']")
            email = email_section.find_element_by_class_name('pv-contact-info__contact-link link-without-visited-state t-14'.replace(' ', '.')).get_attribute("innerHTML").strip()
            print(company_link, " ", email)
            print(name, connection, job_title, location)
        else:
            name = driver.find_element_by_class_name('text-heading-xlarge').get_attribute("innerHTML")
            job_title = driver.find_element_by_class_name('text-body-medium break-words'.replace(' ', '.')).get_attribute("innerHTML").strip()
            location = driver.find_element_by_class_name('text-body-small inline t-black--light break-words'.replace(' ', '.')).get_attribute("innerHTML").strip()
            time.sleep(scrollPauseTime+1)
            company_link = driver.find_element(By.XPATH, "//*[@data-field='experience_company_logo']").get_attribute("href")
            print(company_link)
            print(name, connection, job_title, location)
        

        print(company_link)
        print(name, connection, job_title, location)

    

        
        
        
        """
        .get_attribute("innerHTML")
        connection = driver.find_element_by_xpath('.//*[@id="ember448"]/div[2]/div[2]/div[1]/div[1]/span/span[2]')
        job_title = driver.find_element_by_xpath('.//*[@id="ember448"]/div[2]/div[2]/div[1]/div[2]')
        address = driver.find_element_by_xpath('.//*[@id="ember448"]/div[2]/div[2]/div[2]/span[1]')
        connections = driver.find_element_by_xpath('.//*[@id="ember454"]/span/span')
        print(name, connection, job_title, address, connections)
        """

        # Getting connection type for student
        """
        sourceCode = BeautifulSoup(browser.page_source)
        connection = sourceCode.find(
            'span', {'class': 'dist-value'}).get_text()
        print(connection)

        # Extract data for each student
        
                # 1st CONNECTION
        if (connection == '1st'):

            



        
            # Get company Name
            companyName = sourceCode.find('span', {
                                          'class': 'text-align-left ml2 t-14 t-black t-bold full-width lt-line-clamp lt-line-clamp--multi-line ember-view'}).get_text()
            print(companyName)
            # Get job title
            jobTitle = sourceCode.find(
                'h3', {'class': 't-16 t-black t-bold'}).get_text()
            print(jobTitle)
            ####
            # Get student email
            contactDetails = browser.find_element_by_link_text('Contact info')
            contactDetails.click()
            time.sleep(scrollPauseTime)
            sourceCode2 = BeautifulSoup(browser.page_source)
            studentEmailSec = sourceCode2.find(
                'section', {'class': 'pv-contact-info__contact-type ci-email'})
            studentEmailDiv = studentEmailSec.find_all(
                'a', {'class': 'pv-contact-info__ci-container t-14'})
            studentEmail = studentEmailSec.a.get_text()
            print(studentEmail)
            browser.back()
            # Get company Link
            companyLink = sourceCode.find(
                'a', {'class': 'full-width ember-view'})
            fullLink = 'https://www.linkedin.com' + companyLink['href']
            print(companyLink['href'])
            time.sleep(scrollPauseTime)
            # Append data to Excell
            df.loc[row, 'company'] = companyName
            df.loc[row, 'email'] = studentEmail
            df.loc[row, 'companylink'] = fullLink
            df.loc[row, 'jobtitle'] = jobTitle
            df.to_excel(dataLocation, index=False)
        # 2nd CONNECTION
        elif (connection == '2nd'):
            # Get company Name
            companyName = sourceCode.find('span', {
                                          'class': 'text-align-left ml2 t-14 t-black t-bold full-width lt-line-clamp lt-line-clamp--multi-line ember-view'}).get_text()
            print(companyName)
            # Get company Link
            companyLink = sourceCode.find(
                'a', {'class': 'full-width ember-view'})
            fullLink = 'https://www.linkedin.com' + companyLink['href']
            print(companyLink['href'])
            time.sleep(scrollPauseTime)
            # Get job Title
            jobTitle = sourceCode.find(
                'h3', {'class': 't-16 t-black t-bold'}).get_text()
            print(jobTitle)
            
            # Append data to Excell
            time.sleep(scrollPauseTime)
            connected = 'yes'
            df.loc[row, 'company'] = companyName
            df.loc[row, 'companylink'] = fullLink
            df.loc[row, 'jobtitle'] = jobTitle
            df.to_excel(dataLocation, index=False)
        else:
            # Get company Name
            companyName = sourceCode.find('span', {
                                          'class': 'text-align-left ml2 t-14 t-black t-bold full-width lt-line-clamp lt-line-clamp--multi-line ember-view'}).get_text()
            print(companyName)
            # Get company Link
            companyLink = sourceCode.find(
                'a', {'class': 'full-width ember-view'})
            fullLink = 'https://www.linkedin.com' + companyLink['href']
            print(companyLink['href'])
            time.sleep(scrollPauseTime)
            # Get job Title
            jobTitle = sourceCode.find(
                'h3', {'class': 't-16 t-black t-bold'}).get_text()
            print(jobTitle)
            sourceCode4 = BeautifulSoup(browser.page_source)
            
            # Append data to Excell
            connected = 'yes'
            df.loc[row, 'company'] = companyName
            df.loc[row, 'companylink'] = fullLink
            df.loc[row, 'jobtitle'] = jobTitle
            df.to_excel(dataLocation, index=False)
            """
driver.close()