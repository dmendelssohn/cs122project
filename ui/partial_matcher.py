import pandas as pd
import jellyfish

def pieces_in(row, pieces):
    '''
    Determines if the separate words supplied by the user are contained in a
    given entry of the database
    Inputs:
      row: (str) database entry
      pieces: (list of strings) words given to the interface
    Outputs True if it is a match, False if not
    '''
    boolean = True
    for piece in pieces:
        pb = piece.lower() in row.lower()
        boolean = pb and boolean
    return boolean

def partial_matcher(name_from_ui, universe):
    '''
    Finds and aggregates all hard matches containing all of the words supplied
    by the user and the top partial matches by jaro-winkler distance
    Inputs:
      name_from_ui: (str) name supplied by user interface
      universe: (int) 0 for Marvel 1 for DC
    Outputs combined list of strings of hard and partial matches
    '''
    pieces = name_from_ui.split()
    if universe == 0:
        df = pd.read_csv('marvel_split_names.csv', encoding='latin1')
        new = df['name_no_earth'].apply(lambda row: pieces_in(row, pieces))
    elif universe == 1:
        df = pd.read_csv('dc_split_names.csv', encoding='latin1')
        new = df['fullname'].apply(lambda row: pieces_in(row, pieces))

    s = set(list(df['hero_name'].ix[new]) + list(df['alias'].ix[new]))
    s = {x for x in s if x == x}
    s = list(s)
    if len(s) > 15:
        s = s[:15]
    s += jaro_matcher(name_from_ui, universe)
    s = {x for x in s if x == x}
    
    return list(s)

def calculate_jaro_winkler(name, name_from_ui):
    '''
    Finds the score between two names
    Inputs:
      name: (str) name in database
      name_from_ui: (str) name supplied by user interface
    Outputs a float for the jaro-winkler score
    '''
    return jellyfish.jaro_winkler(name, name_from_ui)

def jaro_matcher(name_from_ui, universe):
    '''
    Matches list of best matches by jaro-winkler score
    Inputs:
      name_from_ui: (str) name to be searched for
      universe: (int) 0 for Marvel 1 for DC
    Outputs a list of strings containing searchable names
    '''
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
