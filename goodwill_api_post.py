import json
import requests

def Pull_items():
  goodwill_url = "https://buyerapi.shopgoodwill.com/api/Search/ItemListing"
  payload = './lib/payload.json'
  responseData = "./data/results.json"

  #////////////////////////////
  maxpages = 1
  body = json.load(open(payload))
  #////////////////////////////
  file = open(responseData, 'w')
  response = []

  try:
    for i in range(1,maxpages+1):
      body["page"] = i
      httpresponse = requests.post(goodwill_url, json=body).json()['searchResults']['items']
      response += httpresponse
    file.writelines(json.dumps(response, indent=4))
  except Exception as e:
    print ("---------------- Failed Gathering Items - Quiting the Driver ----------------")
    print(e)
  file.close()  
  return json.dumps(response, indent=4)
  