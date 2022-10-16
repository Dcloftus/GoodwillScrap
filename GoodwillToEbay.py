#============================================================================================================
#============================================================================================================
# Daniel Loftus - Goodwill to eBay - RaaS
# Tool to gather list of Goodwill listing and determine if they are good buys on eBay
# July 1st 2022
#============================================================================================================
#============================================================================================================

from fileinput import close
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
debug_on = True
Goodwill_on = True
eBay_on = True

# CSV Headers
headers = ["Item Id", "Category Id", "Item Title", "Current Price", "Buy it Now Price", "Average eBay Price", "Good Buy?"]

# Shared File Vaiables
goodwillOutput = "goodwillOutput.csv"
ebayOutput = "ebayOutput.csv"

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
    data_file = open(goodwillOutput, 'a')

    # create the csv writer object
    csv_writer = csv.writer(data_file)

    for item in searchResults:
        if(debug_on): print([item["itemId"], item["categoryId"], item["title"], item["currentPrice"], item["buyNowPrice"]])
        
        # Creating Temp array to store what we want in a single row
        temp = [item["itemId"], item["categoryId"], item["title"], item["currentPrice"], item["buyNowPrice"]]

        csv_writer.writerow(temp)

    data_file.close()
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
    with open(goodwillOutput, 'r') as input:
        tempDict =[]
        datareader = csv.reader(input)
        for row in datareader:
            if(debug_on):
                print("---------------- Search Row ----------------")
                print("Name: " + row[2])
                print("Current Price: " + row[3])
                print("Buy it Now Price: " + row[4])

            #Call Search API with CSV Values
            response = ebay.search(accessToken, row[2])
            #print(json.dumps(response, indent=4))

            #Check if there is a response
            if(debug_on): print("Searching Ebay for: " + row[2])
            if(response["total"] != 0):
                # Gather Prices
                meanPrice = ebay.meanOfResultsPrice(response)

                # Check to see if its a good buy
                if(meanPrice > float(row[4])):
                    goodBuy = "Yes"
                else:
                    goodBuy = "No"

                if(debug_on):
                    print("Mean Ebay Price: " + str(meanPrice))
                    print("Good Buy? " + str(goodBuy))

                # Add Price to dict to be written later
                tempDict.append({"Item Id":row[0], "Category Id":row[1], "Item Title":row[2], "Current Price":row[3], "Buy it Now Price":row[4], "Average eBay Price":meanPrice, "Good Buy?":goodBuy})
            
            else:
                if(debug_on): print("eBay did not return any listings for: " + row[2])

                # Adding Original Goodwill result with a failed to get eBay data back
                tempDict.append({"Item Id":row[0], "Category Id":row[1], "Item Title":row[2], "Current Price":row[3], "Buy it Now Price":row[4], "Average eBay Price":"N/A", "Good Buy?":"N/A"})


    try:
        with open(ebayOutput, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            for data in tempDict:
                writer.writerow(data)
    except IOError:
        print("I/O error")
else:
    print("---------------- eBay Poriton Turned Off ----------------")