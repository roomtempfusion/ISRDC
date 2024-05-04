import pandas as pd
import json

df = pd.read_csv('data.csv')

df['Authors'] = df['Authors'].apply(lambda x: x.split('; ') if isinstance(x, str) else x)
df['Author Affiliations'] = df['Author Affiliations'].apply(lambda x: x.split('; ') if isinstance(x, str) else x)
df['Author Keywords'] = df['Author Keywords'].apply(lambda x: x.split(';') if isinstance(x, str) else x)
df['IEEE Terms'] = df['IEEE Terms'].apply(lambda x: x.split(';') if isinstance(x, str) else x)
df.drop(columns=['Date Added To Xplore', 'Volume', 'Issue', 'Start Page', 'End Page', 'ISBNs', 'Mesh_Terms', 'License',
                 'Patent Citation Count', 'Issue Date','Meeting Date','Publisher','Document Identifier'], inplace=True)

with open('countrydict.json', 'r') as file:
    country_dict = json.load(file)

def replace_country_name(input_str):

    input_str_upper = input_str.upper()

    for abbreviation, full_name in country_dict.items():
        if input_str_upper == abbreviation.upper():
            return full_name
    return input_str


def countries(list_of_affiliations):
    country_list = []
    for institution in list_of_affiliations:
        # print(institution)
        country = institution.split(', ')[-1]

        # check for abbreviations
        country = replace_country_name(country)

        country_list.append(country)
    return country_list


df['Author Countries'] = df['Author Affiliations'].apply(lambda x: countries(x) if isinstance(x, list) else '')
df['Author Affiliations'] = df['Author Affiliations'].apply(lambda x: list(set(x)) if isinstance(x, list) else '')
df['Funding Information'] = df['Funding Information'].apply(lambda x: x.split('; ') if isinstance(x, str) else x)
df = df.dropna(subset=['Author Countries', 'Authors', 'Author Affiliations'])
df['IEEE Terms'] = df['IEEE Terms'].fillna(value='z')
df['Author Keywords'] = df['Author Keywords'].fillna(value='z')
df['IEEE Terms'] = df['IEEE Terms'].apply(lambda x: [] if x == 'z' else x)
df['Author Keywords'] = df['Author Keywords'].apply(lambda x: [] if x == 'z' else x)


df = df[df['Author Countries'].apply(lambda x: x != ['NA'] if isinstance(x, list) else True)]
df = df[df['Author Countries'].apply(lambda x: x != [''] if isinstance(x, list) else True)]

df['Author Countries'] = df['Author Countries'].apply(lambda x: [item for item in x if item != 'NA'])

df['Author Countries'] = df['Author Countries'].apply(lambda x: x if x else None)
df['Countries'] = df['Author Countries'].apply(lambda x: list(set(x)) if x else None)

df['Author Keywords'].fillna('', inplace=True)
df['IEEE Terms'].fillna('', inplace=True)
json_col = ['Author Keywords', 'Authors', 'Author Affiliations', 'IEEE Terms', 'Author Countries', 'Countries', 'Funding Information']
df[json_col] = df[json_col].applymap(lambda x: json.dumps(x) if isinstance(x, list) else x)
df.to_csv('data_processed.csv', index=False)

