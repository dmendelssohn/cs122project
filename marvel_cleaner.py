import pandas as pd
#we had to deal with unicode encodings (ie \u00e9) manually because
#slashes were not written as escape characters

marveldf = pd.read_csv('marvel_sans_earth.csv')
identifiers = marveldf['name_no_earth'].str.extract(r'^([^(]+)(?:\(([^\)]+)\))*',
    expand=True)
identifiers.columns = ["hero_name","alias"]
fulldf = pd.concat([marveldf,identifiers["hero_name"].str.strip(),
    identifiers["alias"].str.strip()],axis=1)

fulldf.to_csv('marvel_split_names.csv',index=False)


rawdf = pd.read_csv('marvel-wikia-data.csv')
suffs = rawdf['name'].str.extract(r'^[^(]+(?:\([^\)]+\))?(?:\(([^\)]*Earth[^\)]*)\))',
    expand=True)

suffs = list(set(suffs[0]))
suffs = suffs[1:]
suffs = r"(" + r")|(".join(suffs) + r")"

suffs = r'\(Earth-61018\)|\(Earth-148611\)|\(Earth-9510\)|\(Earth-88194\)|' + \
    r'\(Earth-TRN361\)|\(Earth-TRN259\)|\(Earth-20476\)|\(Earth-41001\)|' + \
    r'\(Earth-11052\)|\(Earth-982\)|\(Earth-4096\)|\(Earth-5311\)|\(Earth-616\)|' + \
    r'\(Earth-20051)|(Earth-11418)|(Earth-98121)|(Earth-5106)|(Earth-941066)|(Earth-8410)|(Sub-Earth Men)|(Earth-1610)|(Earth-5012)|(Counter-Earth)'

name_no_earth = rawdf['name'].str.extract(r'^([.*]+) (?:' + suffs + ')')
