import json
import requests
import csv
import pandas as pd

goodwill_url = "https://buyerapi.shopgoodwill.com/api/Search/ItemListing"
csvFile = "test_api.csv"

#////////////////////////////
maxpages = 5
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
    "pageSize": "50",
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
#////////////////////////////
f = open(csvFile, 'w')
writer = csv.writer(f)
for i in range(1,maxpages):
  body["page"] = i
  httpresponse = requests.post(goodwill_url, json=body).json()
  response = pd.DataFrame(httpresponse.get('searchResults'))
  print(response)

  for item in response.values:
    #output = [item.title, item.buyNowPrice, item.endTime]
    writer.writerow(item)