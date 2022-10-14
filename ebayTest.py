#============================================================================================================
#============================================================================================================
# Daniel Loftus - Test of eBay APIs in a Python Script
# Testing out Sandbox eBay APIs
# September 10th 2022
#============================================================================================================
#============================================================================================================

import json
from statistics import mean, median
import requests

#============================================================================================================
#============================================================================================================
#= Global Variables
#============================================================================================================
#============================================================================================================
debug_on = False

sandBoxAuthUrl = "https://api.sandbox.ebay.com/identity/v1/oauth2/token"

# eBay API - Browse Variables
searchUrl = "https://api.sandbox.ebay.com/buy/browse/v1/item_summary/search"
limit = 5
offset = 10

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
    response = requests.post(sandBoxAuthUrl, data=body, headers=headers)
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
#= Set up API calls
#============================================================================================================
accessToken = ebayAuth()

print(accessToken)

response = ebaySearch(accessToken, "Shoes")

print(json.dumps(response, indent=4))

#print(response["itemSummaries"][0]["price"]["value"])

priceArray = []
for thing in response["itemSummaries"]:
    priceArray.append(float(thing["price"]["value"]))
print(priceArray)
print(mean(priceArray))