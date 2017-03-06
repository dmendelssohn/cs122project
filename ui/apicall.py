import hashlib
import requests
import time
from priv_key import priv
import csv
import textwrap

def get_desc(name):
#name = arg

    m = hashlib.md5()
    pub = "a86a6cb4e0255630ae1eae723b451328"
    #Not-working private key extraction from home directory
    '''
    with open('../priv_key.csv', 'w') as keyfile:
        keyreader = csv.reader(keyfile)
        for row in keyreader:
            priv = row
    '''
    t = time.time()
    private_key = priv()
    m.update((str(t) + private_key + pub).encode('utf-8'))
    hashed = m.hexdigest()
    params = {"hash":hashed,"apikey":pub,"ts":t,"name":name}
    url = "https://gateway.marvel.com/v1/public/characters"
    req = requests.get(url,params=params)
    if req.json()["code"] == 200:
        desc = req.json()["data"]["results"][0]["description"]
        return desc
    else:
        desc = "No description found. Please try another character name."
        return desc
        #print("sorry, idiot")

# images get request
# img = requests.get(req.json()['data']['results'][0]['thumbnail']['path'] + 
#    'detail' + req.json()['data']['results'][0]['thumbnail']['extension'])