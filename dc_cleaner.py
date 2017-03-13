import pandas as pd
#we had to deal with unicode encodings (ie \u00e9) manually because
#slashes were not written as escape characters

dcdf = pd.read_csv('dc-sans-earth.csv')
identifiers = dcdf['fullname'].str.extract(r'^([^(]+)(?:\(([^\)]+)\))*',
    expand=True)
identifiers.columns = ["hero_name","alias"]
fulldf = pd.concat([dcdf,identifiers["hero_name"].str.strip(),
    identifiers["alias"].str.strip()],axis=1)
fulldf.to_csv('dc_split_names.csv',index=False)

