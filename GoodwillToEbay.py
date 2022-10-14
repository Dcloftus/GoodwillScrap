#============================================================================================================
#============================================================================================================
# Daniel Loftus - Goodwill to eBay - RaaS
# Tool to gather list of Goodwill listing and determine if they are good buys on eBay
# July 1st 2022
#============================================================================================================
#============================================================================================================

import csv
import time
import requests

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
# Switches
debug_on = True
UserInput_on = False
Goodwill_on = True
eBay_on = False

# Goodwill - Scrapiong Vairables
pageToSearch = 1
numberOfItemsPerPage = 40

# Shared File Vaiables
csvFile = "test.csv"

# eBay API - Authentication Variables
accessTokenUrl = "https://api.sandbox.ebay.com/identity/v1/oauth2/token"
accessToken = ""

# eBay API - Browse Variables
searchUrl = "https://api.sandbox.ebay.com/buy/browse/v1/item_summary/search"
limit = 5
offset = 0

#============================================================================================================
#= Ask the User to input custom variables
#============================================================================================================
if(UserInput_on):
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
    if(debug_on):
        print('---------------- User input not requested, using default values  ----------------')
        print('Number of pages to search - ' + str(pageToSearch))
        print('Number of records per page - ' + str(numberOfItemsPerPage))




#============================================================================================================
#============================================================================================================
#= Functions
#============================================================================================================
#============================================================================================================
def ebayAuth():
    #Set up Headers and body
    headers =  {
        "Content-Type":"application/x-www-form-urlencoded",
        "Authorization":"Basic RGFuaWVsTG8tcmFhc3NhbmQtU0JYLTkzOWJjY2MzNS0yOWJkNmQ3YjpTQlgtMzliY2NjMzU4MTQxLTU0MzktNDU1Yi05MThhLWUxZjQ="
        }
    body = {
        'grant_type':'client_credentials',
        'scope':'https://api.ebay.com/oauth/api_scope'
    }

    #Make POST request to the auth API
    response = requests.post(accessTokenUrl, data=body, headers=headers)
    accessToken = response.json()['access_token']
    if(debug_on): print(accessToken)

    return accessToken

def ebaySearch(accessToken, searchString):
    #Set up Headers and params
    headers =  {
        "Authorization":"Bearer " + accessToken
        }
    params = {
        'q':searchString,
        'limit':limit,
        'offset':offset
    }

    #Make GET Request
    response = requests.get(searchUrl, params=params, headers=headers)

    return response.json()


#============================================================================================================
#============================================================================================================
#= Main
#============================================================================================================
#============================================================================================================

#============================================================================================================
#= GoodWill Portion
#============================================================================================================

#============================================================================================================
#= Set Up Selenum to reach out to Goodwill
#============================================================================================================
if(Goodwill_on):
    options = Options()
    options.headless = False
    options.add_argument("--window-size=1920,1200")

    DRIVER_PATH = './chromedriver'
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    driver.get("https://shopgoodwill.com/categories/new?st=&sg=New&c=&s=&lp=0&hp=999999&sbn=&spo=false&snpo=false&socs=false&sd=false&sca=false&caed=7%2F6%2F2022&cadb=7&scs=false&sis=false&col=1&p=1&ps=40&desc=false&ss=0&UseBuyerPrefs=true&sus=false&cln=1&catIds=&pn=&wc=false&mci=false&hmt=false&layout=list")
    time.sleep(5)

    #============================================================================================================
    #= Gather Certian data from the site into memory
    #============================================================================================================
    # listingNames = driver.find_element_by_xpath("//a[@class='feat-item_name']")
    try:
        f = open(csvFile, 'w')
        writer = csv.writer(f)
        # Based on the "pageToSearch" loop through Goodwill results pages and write results
        for pagination in range(pageToSearch):
            # Move on to the next page (If its not the first iteration since we load the first results page immediately)
            if pagination != 0:
                # Click next page button
                driver.find_element('xpath', "//button[@class='p-paginator-next p-paginator-element p-link p-ripple']").click()
                driver.implicitly_wait(60) # seconds
                element = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//a[@class='feat-item_name']")))
                print("---------------- Moving to Next Page ----------------")
                time.sleep(5)
                print("---------------- After Waiting 5 Seconds ----------------")
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
                if(debug_on):
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
else:
    print("---------------- Goodwill Poriton Turned Off ----------------")
#============================================================================================================
#============================================================================================================
#= EBAY PORTION
#============================================================================================================
#============================================================================================================
if(eBay_on):
    #============================================================================================================
    #= Call to get Access Token for eBay API calls
    #============================================================================================================
    accessToken = ebayAuth()

    #============================================================================================================
    #= Main eBay calls based on the csv file created above
    #============================================================================================================
    with open(csvFile, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            if(debug_on):
                print("---------------- Print CSV Rows cells at a time ----------------")
                print("Name: " + row[0])
                print("Price: " + row[1])
                print("Time Left: " + row[2])
            
