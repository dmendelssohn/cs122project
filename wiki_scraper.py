import re
import bs4
import json
import sys
import requests

r = requests.get('http://en.wikipedia.org/wiki/%s' % (arg))
soup = bs4.BeautifulSoup(r.text)
ths = soup.find_all('th')
abilities_list = [li.text for li in [th.next_sibling.next_sibling.find_all("li") for th in ths if th.text == "Abilities"][0]]
alter_ego = 