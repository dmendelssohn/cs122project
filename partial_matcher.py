import pandas as pd
import jellyfish

def pieces_in(row, pieces):
    boolean = True
    for piece in pieces:
        pb = piece in row
        boolean = pb and boolean
    return boolean

def partial_matcher(name_from_ui, universe):
    pieces = name_from_ui.split()
    if universe == 0:
        df = pd.read_csv('marvel_split_names.csv', encoding='latin1')
        new = df['name_no_earth'].apply(lambda row: pieces_in(row, pieces))
    elif universe == 1:
        df = pd.read_csv('dc_split_names.csv', encoding='latin1')
        new = df['fullname'].apply(lambda row: pieces_in(row, pieces))

    s = set(list(df['hero_name'].ix[new]) + list(df['alias'].ix[new]) + 
        jaro_matcher(name_from_ui, universe))
    s = {x for x in s if x == x}

    return list(s)

def calculate_jaro_winkler(name, name_from_ui):
    return jellyfish.jaro_winkler(name, name_from_ui)

def jaro_matcher(name_from_ui, universe):
    if universe == 0:
        df = pd.read_csv('marvel_split_names.csv', encoding='latin1')
    if universe == 1:
        df = pd.read_csv('dc_split_names.csv', encoding='latin1')
    new_hn = df['hero_name'].apply(
        lambda row: calculate_jaro_winkler(row, name_from_ui))
    new_hn.name = 'scores'
    together_hn = pd.concat([df, new_hn], axis=1)
    sort_hn = together_hn.sort_values('scores', axis=0, ascending=False)

    lst = list(sort_hn.head(3)['hero_name']) + list(sort_hn.head(3)['alias'])

    new_al = df['alias'].dropna().apply(
        lambda row: calculate_jaro_winkler(row, name_from_ui))
    new_al.name = 'scores'
    together_al = pd.concat([df, new_al], axis=1)
    sort_al = together_al.sort_values('scores', axis=0, ascending=False)

    lst += list(sort_al.head(3)['hero_name']) + list(sort_al.head(3)['alias'])
    return lst
