import bs4
import json
import sys
import requests

r = requests.get('http://en.wikipedia.org/wiki/%s' % (arg))
soup = bs4.BeautifulSoup(r.text)
ths = soup.find_all('th')
ab_lis = [th.next_sibling.next_sibling.find_all('li') for th in ths if th.text == 'Abilities']
if ab_lis != []:
    abilities_list = [li.text for li in ab_lis[0]]
else:
    abilities_list = ['No specific abilities']

ta_lis = [th.next_sibling.next_sibling.find_all('li') for th in ths if th.text == 'Team affiliations']
if ta_lis != []:
    team_list = [li.text for li in ta_lis[0]]
else:
    team_list = ['No team affiliations']

sp_lis = [th.next_sibling.next_sibling.find_all('li') for th in ths if th.text == 'Species']
if sp_lis != []:
    species_list = [li.text for li in sp_lis[0]]
else:
    species_list = ['No known species']

publisher_list = ['No publisher information available']
for th in ths[:20]:
    if th.text == 'Publisher':
        publisher_list = [th.next_sibling.next_sibling.text]

first_appearance_list = ['No first appearance information available']
for th in ths[:20]:
    if th.text == 'First appearance':
        first_appearance_list = [th.next_sibling.next_sibling.text]

cr_as = [th.next_sibling.next_sibling.find_all('a') for th in ths if th.text == 'Created by']
if cr_as != []:
    creator_list = [a.text for a in cr_as[0]]
else:
    creator_list = ['No creator information available']

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