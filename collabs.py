# README
# This script is only partially complete - it should run without error but the functionality isn't entirely finished
# since the project moved in a different direction

import pandas as pd
import json
from geopy.geocoders import Nominatim
from random import randint

file_path = 'official_names.json'
with open(file_path, 'r', encoding='cp1252') as file:
    official_names = json.load(file)
file_path2 = 'country_mapping.json'
with open(file_path2, 'r', encoding='cp1252') as file:
    country_mapping = json.load(file)

def country_converter(input_str):
    input_str_upper = input_str.upper()

    for abbreviation, full_name in country_mapping.items():
        if input_str_upper == abbreviation.upper():
            return full_name
    return input_str

def official_name_converter(input_str):
    input_str_upper = input_str.upper()

    for abbreviation, full_name in official_names.items():
        if input_str_upper == abbreviation.upper():
            return full_name
    return input_str


def combine_lists(list_of_lists):
    combined_list = []
    for sublist in list_of_lists:
        combined_list.extend(sublist)
    return combined_list


csv_path = 'data_processed.csv'

df = pd.read_csv(csv_path)
df['Author Affiliations'] = df['Author Affiliations'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
df['Author Affiliations'].fillna(value='', inplace=True)
df['Affiliated Institutions'] = df['Author Affiliations']

df.drop(columns=['Document Title', 'Authors', 'Publication Title', 'Publication Year', 'Abstract', 'ISSN', 'DOI',
                 'Funding Information', 'PDF Link', 'Reference Count',
                 'Online Date', 'Author Countries', 'Countries', 'Author Keywords', 'IEEE Terms'], inplace=True)
df = df.explode('Author Affiliations')

df['Affiliated Institutions'] = df.apply(lambda row: [inst for inst in row['Affiliated Institutions'] if inst != row['Author Affiliations']], axis=1)


# Combine duplicate entries by concatenating lists in column 'B'
df = df.groupby('Author Affiliations')['Affiliated Institutions'].agg(combine_lists).reset_index()
df['Country'] = df['Author Affiliations'].apply(lambda x: x.split(',')[-1].strip())
df['Country'] = df['Country'].apply(lambda x: official_name_converter(country_converter(x)))
df.to_csv('collabs.csv', index=False)
print(df)

