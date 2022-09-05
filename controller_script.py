#----------------------------------------------------IMPORT RELEVANT LIBRARIES----------------------------------------------#
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from bs4.element import Tag
from time import sleep
import csv
from parsel import Selector
import parameters_real
import numpy
from random import seed
from random import randint

### SET SEED - MAKE SURE YOU SET TO A DIFFERENT NUMBER EVERY TIME YOU RUN THE PROGRAM
seed(123432)

###------------------------------------------------------HELPER FUNCTIONS---------------------------------------------------------------##
# Function call extracting title and linkedin profile iteratively
def find_profiles():
    for r in result_div:
        # Checks if each element is present, else, raise exception
        try:
            link = r.find('a', href=True)
            title = None
            title = r.find('h3')
            
            # returns True if a specified object is of a specified type; Tag in this instance 
            if isinstance(title,Tag):
                title = title.get_text()
    
            description = None
            description = r.find('span', attrs={'class': 'st'})
    
            if isinstance(description, Tag):
                description = description.get_text()
    
            # Check to make sure everything is present before appending
            if link != '' and title != '' and description != '':
                links.append(link['href'])
                titles.append(title)
                descriptions.append(description)
        # Next loop if one element is not present
        except Exception as e:
            print(e)
            continue
        
# This function iteratively clicks on the "Next" button at the bottom right of the search page. 
def profiles_loop():
    
    find_profiles()
    
    next_button = driver.find_element_by_xpath('//*[@id="pnnext"]') 
    next_button.click()
def repeat_fun(times, f):
    for i in range(times): f()

#--------------------------------------------------------LINKEDIN SCRAPE-----------------------------------------------------#
# specifies the path to the chromedriver.exe
driver = webdriver.Chrome(r"C:\Users\tanis\Downloads\chromedriver_win32\chromedriver.exe")

# driver.get method() will navigate to a page given by the URL address
driver.get('https://www.linkedin.com')

# locate email form by_class_name
username = driver.find_element_by_id('session_key')

# send_keys() to simulate key strokes
username.send_keys('user')
sleep(randint(5, 15))

# locate password form by_class_name
password = driver.find_element_by_id('session_password')

# send_keys() to simulate key strokes
password.send_keys('password')
sleep(randint(5, 15))

# locate submit button by_class_name
log_in_button = driver.find_element_by_class_name('sign-in-form__submit-button')

# .click() to mimic button click
log_in_button.click()
sleep(randint(0, 2))
#----------------------------------GOOGLE SCRAPE -------------------------------------------------------------#

# driver.get method() will navigate to a page given by the URL address
driver.get('https://www.google.com')
sleep(randint(3, 10))

# locate search form by_name
search_query = driver.find_element_by_name('q')

# send_keys() to simulate the search text key strokes
search_query.send_keys(parameters_real.search_query)
sleep(randint(5, 15))

# .send_keys() to simulate the return key 
search_query.send_keys(Keys.RETURN)

#---------------------------------------------------------BEAUTIFUL SOUP TIME----------------------------------------------------------------#
soup = BeautifulSoup(driver.page_source,'lxml')
result_div = soup.find_all('div', attrs={'class': 'g'})
    
# initialize empty lists
links, titles , descriptions = [], [], []

# Function call x10 of function profiles_loop; you can change the number to as many pages of search as you like. 
repeat_fun(10, profiles_loop)
print(titles)
print(links)
print(descriptions)
# Separates out just the First/Last Names for the titles variable
titles01 = [i.split()[0:2] for i in titles].reverse()
# The function below stores scraped data into a .csv file
from itertools import zip_longest
# Load titles and links data into csv
d = [titles01, links]
export_data = zip_longest(*d, fillvalue = '')
with open(parameters_real.file_name, 'w', encoding="ISO-8859-1", newline='') as myfile:
      wr = csv.writer(myfile)
      wr.writerow(("Titles", "Links", "Current_Job", "Current_Location" ))
      wr.writerows(export_data)
myfile.close()
