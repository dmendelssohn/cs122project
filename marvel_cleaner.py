import pandas as pd
#we had to deal with unicode encodings (ie \u00e9) manually because
#slashes were not written as escape characters

marveldf = pd.read_csv('marvel-wikia-data.csv')
suffs = marveldf['name'].str.extract(r'^[^(]+(?:\([^\)]+\))?(?:(\([^\)]*Earth[^\)]*\)))',
    expand=True)

suffs = list(set(suffs[0]))
suffs = suffs[1:]
suffs = [" " + x for x in suffs]

def earth_replace(s,suff):
    return s.replace(suff,"")

marveldf["name_no_earth"] = marveldf["name"]

for suff in suffs:
    marveldf["name_no_earth"] = marveldf["name_no_earth"].apply(lambda row: earth_replace(row,suff))

identifiers = marveldf['name_no_earth'].str.extract(r'^([^(]+)(?:\(([^\)]+)\))*',
    expand=True)
identifiers.columns = ["hero_name","alias"]
fulldf = pd.concat([marveldf,identifiers["hero_name"].str.strip(),
    identifiers["alias"].str.strip()],axis=1)

fulldf.to_csv('marvel_split_names.csv',index=False)