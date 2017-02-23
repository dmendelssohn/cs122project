import bs4
import json
import sys
import requests

r = requests.get('http://en.wikipedia.org/wiki/%s' % (arg))
soup = bs4.BeautifulSoup(r.text)
ths = soup.find_all('th')
lis = [th.next_sibling.next_sibling.find_all("li") for th in ths if th.text == "Abilities"]
if lis != []:
    abilities_list = [li.text for li in lis[0]]
else:
    abilities_list = ['No specific abilities']

if soup.find_all('a', class_='mw-redirect', title=arg) == 0:
    alter_ego = soup.find_all(
        'th', text='Alter ego')[0].next_sibling.next_sibling.text
else:
    alter_ego = ths[0].text

#Finding dopplegangers, probably belongs in another file
df = pd.read_csv('./fivethirtyeight_marvel.csv')
df2 = pd.read_csv('./marvel_sans_earth.csv')
joined = pd.concat([df, df2['name_no_earth']], axis=1)
test = joined['name_no_earth'].str.extract(
    r'^([^\(]*)(?: \((.*)\))*$', expand=True)