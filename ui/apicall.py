import hashlib
import requests
import time
from priv_key import priv
import csv
import os 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def apicall(name):
    '''
    Pulls information from the api and creates character image
    Inputs:
      name: (str) name provided by user
    Outputs tuple with description and bool for success of image pull
    '''
    m = hashlib.md5()
    pub = "a86a6cb4e0255630ae1eae723b451328"

    desc = ''
    t = time.time()
    m.update((str(t) + priv() + pub).encode('utf-8'))
    hashed = m.hexdigest()
    params = {"hash":hashed,"apikey":pub,"ts":t,"name":name}
    url = "https://gateway.marvel.com/v1/public/characters"
    req = requests.get(url,params=params)
    imgbool = 0
    if req.json()["code"] == 200:
        if len(req.json()["data"]["results"]) > 0:
            desc += req.json()["data"]["results"][0]["description"]

            img = requests.get(req.json()['data']['results'][0]['thumbnail']['path'] + 
                '/detail.' + req.json()['data']['results'][0]['thumbnail']['extension'],
                stream=True)
            if img.status_code == 200:
                imgbool = 1
                with open(os.path.join(BASE_DIR,'ui/static/character.jpg'), 'wb') as writer:
                    for piece in img:
                        writer.write(piece)

    if desc == '':
        return 'Sorry, no character description available', imgbool
    else:
        return desc, imgbool
