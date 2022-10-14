import json
import requests

goodwill_url = "https://shopgoodwill.com/categories/new?st=&sg=New&c=&s=&lp=0&hp=999999&sbn=&spo=false&snpo=false&socs=false&sd=false&sca=false&caed=7%2F6%2F2022&cadb=7&scs=false&sis=false&col=1&p=1&ps=40&desc=false&ss=0&UseBuyerPrefs=true&sus=false&cln=1&catIds=&pn=&wc=false&mci=false&hmt=false&layout=list&ihp="

response = requests.get(goodwill_url)
print