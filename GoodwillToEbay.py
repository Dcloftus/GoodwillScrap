#============================================================================================================
#============================================================================================================
# Daniel Loftus - Goodwill to eBay - RaaS
# Tool to gather list of Goodwill listing and determine if they are good buys on eBay
# July 1st 2022
#============================================================================================================
#============================================================================================================

import Functions.goodwill as goodwill
import Functions.ebay as ebay

import csv
import json
import platform
from statistics import mean

#============================================================================================================
#============================================================================================================
#= Variables
#============================================================================================================
#============================================================================================================
#OS Determination
os = platform.platform()

# Switches
debug_on = False
UserInput_on = False
Goodwill_on = True
eBay_on = False


# Shared File Vaiables
csvFile = "test.csv"

#============================================================================================================
#============================================================================================================
#= Main
#============================================================================================================
#============================================================================================================

#============================================================================================================
#= GoodWill Portion
#============================================================================================================
if(Goodwill_on):
    searchResults = goodwill.search(1)

    # Write Products to csv file
    data_file = open(csvFile, 'w')

    # create the csv writer object
    csv_writer = csv.writer(data_file)

    for item in searchResults:
        if(debug_on): print([item["title"]], [item["currentPrice"]], [item["buyNowPrice"]])
        
        # Creating Temp array to store what we want in a single row
        temp = [item["title"], item["currentPrice"], item["buyNowPrice"]]

        csv_writer.writerow(temp)

else:
    print("---------------- Goodwill Poriton Turned Off ----------------")
#============================================================================================================
#= EBAY PORTION
#============================================================================================================
if(eBay_on):
    #============================================================================================================
    #= Call to get Access Token for eBay API calls
    #============================================================================================================
    accessToken = ebay.auth()

    #============================================================================================================
    #= Main eBay calls based on the csv file created above
    #============================================================================================================
    with open(csvFile, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            if(debug_on):
                print("---------------- Search Row ----------------")
                print("Name: " + row[0])
                print("Price: " + row[1])
                print("Time Left: " + row[2])
            #Call Search API with CSV Values
            response = ebay.search(accessToken, row[0])
            #print(json.dumps(response, indent=4))

            #Check if there is a response
            if(debug_on): print("Searching Ebay for: " + row[0])
            if(response["total"] != 0):
                # Gather Prices
                priceArray = []
                for thing in response["itemSummaries"]:
                    priceArray.append(float(thing["price"]["value"]))

                if(debug_on):
                    print("All Prices: " + str(priceArray))
                    print("Mean: " + str(mean(priceArray)))
                    print("")
            else:
                if(debug_on): print("eBay did not return any listings for: " + row[0])
else:
    print("---------------- eBay Poriton Turned Off ----------------")