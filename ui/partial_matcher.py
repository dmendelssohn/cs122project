import pandas as pd


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

    return new