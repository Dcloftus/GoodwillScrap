#============================================================================================================
#============================================================================================================
# Daniel Loftus - Goodwill to eBay - RaaS
# Tool to gather list of Goodwill listing and determine if they are good buys on eBay
# July 1st 2022
#============================================================================================================
#============================================================================================================

import csv
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#============================================================================================================
#============================================================================================================
#= Variables
#============================================================================================================
#============================================================================================================
askForUserInput = False
pageToSearch = 2
numberOfItemsPerPage = 40

#============================================================================================================
#= Ask the User to input custom variables
#============================================================================================================
if(askForUserInput):
    # Gather number of pages to search
    pageToSearchInput = int(input('How many pages to search? (Default is set to - ' + str(pageToSearch) + ')'))
    if(pageToSearchInput != pageToSearch):
        print('You want to search ' + str(pageToSearchInput) + ' pages.')
        pageToSearch = pageToSearchInput
    else:
        print('Using default number of pages to search (' + str(pageToSearch) + ')')
    
    # Gather number of records to retreive from the each page
    numberOfItemsPerPageInput = int(input('How many numbers per page? (Default is set to - ' + str(numberOfItemsPerPage) + ')'))
    if(numberOfItemsPerPageInput != numberOfItemsPerPage):
        print('You want to gather  ' + str(numberOfItemsPerPageInput) + ' record per page.')
        numberOfItemsPerPage = numberOfItemsPerPageInput
    else:
        print('Using default number records per page (' + str(numberOfItemsPerPageInput) + ')')
else:
    print('User input not requested, using default values.')
    print('Number of pages to search - ' + str(pageToSearch))
    print('Number of records per page - ' + str(numberOfItemsPerPage))
#============================================================================================================
#============================================================================================================
#= GoodWill Portion
#============================================================================================================
#============================================================================================================

#============================================================================================================
#= Set Up Selenum to reach out to Goodwill
#============================================================================================================
options = Options()
options.headless = False
options.add_argument("--window-size=1920,1200")

DRIVER_PATH = '/Users/danielloftus/bin/chromedriver'
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get("https://shopgoodwill.com/categories/new?st=&sg=New&c=&s=&lp=0&hp=999999&sbn=&spo=false&snpo=false&socs=false&sd=false&sca=false&caed=7%2F6%2F2022&cadb=7&scs=false&sis=false&col=1&p=1&ps=40&desc=false&ss=0&UseBuyerPrefs=true&sus=false&cln=1&catIds=&pn=&wc=false&mci=false&hmt=false&layout=list")

#============================================================================================================
#= Gather Certian data from the site into memory
#============================================================================================================
# listingNames = driver.find_element_by_xpath("//a[@class='feat-item_name']")
try:
    f = open('test.csv', 'w')
    writer = csv.writer(f)
    # Based on the "pageToSearch" loop through Goodwill results pages and write results
    for pagination in range(pageToSearch):
        # Move on to the next page (If its not the first iteration since we load the first results page immediately)
        if pagination != 0:
            # Click next page button
            driver.find_element('xpath', "//button[@class='p-paginator-next p-paginator-element p-link p-ripple']").click()
            driver.implicitly_wait(60) # seconds
            element = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//a[@class='feat-item_name']")))
            print("------------------------- Moving to Next Page ------------------------")
            time.sleep(5)
            print("---------------------- After Waiting 5 Seconds -----------------------")
        # Locating the Interested data on the page
        listingNames = driver.find_elements('xpath', "//a[@class='feat-item_name']")
        listingPrice = driver.find_elements('xpath', "//h3[@class='feat-item_price']")
        listingTimeLeft = driver.find_elements('xpath', "//li[@class='d-none d-md-inline-block ng-star-inserted']/span")

#============================================================================================================
#= Write certian screen data to a CSV File
#============================================================================================================
        # Loop through the "numberOfItemsPerPage" and write to a CSV
        timeRemainingIndex = 0
        for index in range(numberOfItemsPerPage):
            print([listingNames[index].text])
            print([listingPrice[index].text.split(": ",1)[1]])
            print([listingTimeLeft[timeRemainingIndex + 1].text])
            item = [listingNames[index].text,listingPrice[index].text.split(": ",1)[1],listingTimeLeft[timeRemainingIndex + 1].text]
            writer.writerow(item)

            # Increment the Time Remaining Index to skip the "Ending:" String
            timeRemainingIndex = timeRemainingIndex + 2

except Exception as e:
    print ("---------------- Failed Gathering Items - Quiting the Driver ----------------")
    print(e)
    driver.quit()
    f.close()

#============================================================================================================
#= Shut Down Selnium
#============================================================================================================
#print(driver.page_source)
driver.quit()
f.close()

#============================================================================================================
#============================================================================================================
#= EBAY PORTION
#============================================================================================================
#============================================================================================================