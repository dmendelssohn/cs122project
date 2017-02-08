import hashlib
import requests
import time

name = arg

m = hashlib.md5()
pub = "a86a6cb4e0255630ae1eae723b451328"
priv = ""
t = time.time()
m.update((str(t)+priv + pub).encode('utf-8'))
hashed = m.hexdigest()
params = {"hash":hashed,"apikey":pub,"ts":t,"name":name}
url = "https://gateway.marvel.com/v1/public/characters"
req = requests.get(url,params=params)
if req.json()["code"] == 200:
    desc = req.json()["data"]["results"][0]["description"]
else:
    print("sorry, idiot")
