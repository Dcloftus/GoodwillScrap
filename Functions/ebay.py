#============================================================================================================
#============================================================================================================
# Daniel Loftus - Goodwill to eBay - RaaS
# Common eBay Functions
# October 14st 2022
#============================================================================================================
#============================================================================================================

import requests

#===========================================================================================================
#= Variables
#===========================================================================================================
# eBay API - Authentication Variables
accessTokenUrl = "https://api.sandbox.ebay.com/identity/v1/oauth2/token"
accessToken = ""

# eBay API - Browse Variables
searchUrl = "https://api.sandbox.ebay.com/buy/browse/v1/item_summary/search"
limit = 5
offset = 0


#===========================================================================================================
#= Functions
#===========================================================================================================
def auth():
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

    return accessToken

def search(accessToken, searchString):
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