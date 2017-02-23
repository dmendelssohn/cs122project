import bs4
import json
import sys
import requests

r = requests.get('http://en.wikipedia.org/wiki/%s' % (arg))
soup = bs4.BeautifulSoup(r.text)
ths = soup.find_all('th')
abilities_list = [li.text for li in [th.next_sibling.next_sibling.find_all("li") for th in ths if th.text == "Abilities"][0]]
if soup.find_all('a', class_='mw-redirect', title=arg) == 0:
    alter_ego = soup.find_all(
        'th', text='Alter ego')[0].next_sibling.next_sibling.text
else:
    alter_ego = ths[0].text