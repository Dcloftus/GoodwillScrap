#============================================================================================================
#============================================================================================================
# Justin Solitro - Goodwill to eBay - RaaS
# Common Goodwill Functions
# October 14st 2022
#============================================================================================================
#============================================================================================================
import requests
import pandas as pd


#===========================================================================================================
#= Variables
#===========================================================================================================
goodwill_url = "https://buyerapi.shopgoodwill.com/api/Search/ItemListing"

body = {
    "isSize": "false",
    "isWeddingCatagory": "false",
    "isMultipleCategoryIds": "false",
    "isFromHeaderMenuTab": "false",
    "layout": "list",
    "isFromHomePage": "false",
    "searchText": "",
    "selectedGroup": "New",
    "selectedCategoryIds": "",
    "selectedSellerIds": "",
    "lowPrice": "0",
    "highPrice": "99999",
    "searchBuyNowOnly": "1",
    "searchPickupOnly": "false",
    "searchNoPickupOnly": "false",
    "searchOneCentShippingOnly": "false",
    "searchDescriptions": "false",
    "searchClosedAuctions": "false",
    "closedAuctionEndingDate": "7/6/2022",
    "closedAuctionDaysBack": "7",
    "searchCanadaShipping": "false",
    "searchInternationalShippingOnly": "false",
    "sortColumn": "1",
    "page": 1,
    "pageSize": "1",
    "sortDescending": "false",
    "savedSearchId": 0,
    "useBuyerPrefs": "true",
    "searchUSOnlyShipping": "false",
    "categoryLevelNo": "1",
    "categoryLevel": 1,
    "categoryId": 0,
    "partNumber": "",
    "catIds": ""
}

#===========================================================================================================
#= Functions
#===========================================================================================================
def search(page):
    # Modify Payload based on input arguments
    body["page"] = page

    # Make POST request to the search API
    response = requests.post(goodwill_url, json=body).json()

    # Trim out just the 40 Items of the page
    response = response["searchResults"]["items"]

    return response