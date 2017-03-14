import pandas as pd
#we had to deal with unicode encodings (ie \u00e9) manually because
#slashes were not written as escape characters

dcdf = pd.read_csv('dc-wikia-data.csv')
suffs = dcdf['name'].str.extract(r'^.*(\(.+\))')
suffs2 = set(suffs)
suffs2 = list(suffs2)[1:]
suffs3 = []
for suf in suffs2:
    print(suf)
    if 'Earth' in suf or 'Hour' in suf or 'verse' in suf:
        suffs3.append(suf)
suffs4 = [' ' + x for x in suffs3]

def replacer(s, suf):
    '''
    Deletes the irrelevant suffices
    Inputs:
      s: (str) string containing full name to be cleaned
      suf: (str) suffix being dropped
    Outputs string with name without the suffix
    '''
    return s.replace(suf, "")

dcdf['fullname'] = dcdf['name']

for suf in suffs4:
    dcdf['fullname'] = dcdf['fullname'].apply(
        lambda row: replacer(row, suf))

identifiers = dcdf['fullname'].str.extract(r'^([^(]+)(?:\(([^\)]+)\))*',
    expand=True)
identifiers.columns = ["hero_name","alias"]
fulldf = pd.concat([dcdf,identifiers["hero_name"].str.strip(),
    identifiers["alias"].str.strip()],axis=1)
fulldf.to_csv('dc_split_names.csv',index=False)