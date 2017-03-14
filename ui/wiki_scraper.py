import bs4
import json
import sys
import requests


def scraper(arg):
    '''
    Crawls through infobox and compiles relevant information
    Inputs:
      arg: (str) name of character supplied by user
    Outputs dictionary containing lists of strings for relevant information
    '''
    info_dict = {}
    r = requests.get('http://en.wikipedia.org/wiki/%s' % (arg))
    soup = bs4.BeautifulSoup(r.text)
    ths = soup.find_all('th')

    if soup.find_all('table', id='disambigbox') !=[]:
        atags = soup.find_all('a')
        for a in atags:
            if 'comics' in a.text or 'Comics' in a.text:
                return scraper(a.text)

    ab_lis = [th.next_sibling.next_sibling.find_all('li') for th in ths \
        if th.text == 'Abilities']
    if ab_lis != []:
        abilities_list = [li.text for li in ab_lis[0]]
        if abilities_list == []:
            th = soup.find_all('th', text='Abilities')
            abilities_list = th[0].next_sibling.next_sibling.text.split('\n')
    else:
        abilities_list = ['No specific abilities information available']
    info_dict['Abilities'] = abilities_list

    ta_lis = [th.next_sibling.next_sibling.find_all('a') for th in ths \
        if th.text == 'Team affiliations']
    if ta_lis != []:
        team_list = [li.text for li in ta_lis[0]]
    else:
        team_list = ['No team affiliations']
    info_dict['Teams'] = team_list

    species_list = ['No species information available']
    for th in ths[:20]:
        if th.text == 'Species':
            species_list = [th.next_sibling.next_sibling.text]
    info_dict['Species'] = species_list

    publisher_list = ['No publisher information available']
    for th in ths[:20]:
        if th.text == 'Publisher':
            publisher_list = [th.next_sibling.next_sibling.text]
    info_dict['Publisher'] = publisher_list

    first_appearance_list = ['No first appearance information available']
    for th in ths[:20]:
        if th.text == 'First appearance':
            first_appearance_list = [th.next_sibling.next_sibling.text]
        if '\n' in first_appearance_list[0]:
            first_appearance_list = th.next_sibling.next_sibling.text.split('\n')
    info_dict['First appearance'] = first_appearance_list

    cr_as = [th.next_sibling.next_sibling.find_all('a') for th in ths \
        if th.text == 'Created by']
    if cr_as != []:
        creator_list = [a.text for a in cr_as[0]]
    else:
        creator_list = ['No creator information available']
    info_dict['Creators'] = creator_list

    partnership_list = ['No partnership information available']
    for th in ths[:20]:
        if th.text == 'Partnerships':
            partnership_list = [a.text for a in th.next_sibling.next_sibling.find_all('a')]
    info_dict['Partnerships'] = partnership_list

    aliases_list = ['No alias information available']
    for th in ths[:20]:
        if th.text == 'Notable aliases':
            aliases_list = [li.text for li in th.next_sibling.next_sibling.find_all('li')]
        if aliases_list == []:
            aliases_list = th.next_sibling.next_sibling.text.split(', ')
    info_dict['Aliases'] = aliases_list

    alter_ego = ['No alter ego information available']
    if ths == []:
        pass
    elif ths[0].text in arg and soup.find_all(
        'th', text='In-story information') != []:
        a_e = [soup.find_all('th', text='Alter ego')]
        if a_e !=[[]]:
            alter_ego = [a_e[0][0].next_sibling.next_sibling.text]
    elif soup.find_all('th', text='In-story information') != []:
        alter_ego = [ths[0].text]
    info_dict['Alter ego'] = alter_ego

    for key in info_dict:
        for index, entry in enumerate(info_dict[key]):
            if entry[-3] == '[':
                info_dict[key][index] = info_dict[key][index][:-3]

    return info_dict