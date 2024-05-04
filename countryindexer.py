import pandas as pd
import json

file_path = 'official_names.json'
with open(file_path, 'r', encoding='cp1252') as file:
    official_names = json.load(file)
file_path2 = 'country_mapping.json'
with open(file_path2, 'r', encoding='cp1252') as file:
    country_mapping = json.load(file)

df = pd.read_csv('data_processed.csv')
SCA_list = ['Afghanistan', 'Bangladesh', 'Bhutan', 'India', 'Kazakhstan', 'Kyrgyzstan',
            'Maldives', 'Nepal', 'Pakistan', 'Sri Lanka', 'Tajikistan', 'Turkmenistan','Uzbekistan']
NEA_list = ['Qatar', 'Saudi Arabia', 'Syria', 'Tunisia', 'United Arab Emirates', 'Yemen']
WHA_list = ['Antigua and Barbuda', 'Argentina', 'The Bahamas', 'Barbados', 'Belize', 'Bolivia', 'Brazil',
            'Canada', 'Chile', 'Colombia',
            'Costa Rica', 'Cuba', 'Dominican Republic', 'Ecuador', 'El Salvador', 'Grenada', 'Guatemala',
            'Guyana', 'Haiti', 'Honduras', 'Jamaica', 'Mexico', 'Nicaragua', 'Panama', 'Paraguay', 'Peru',
            'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Suriname', 'Trinidad and Tobago',
            'Uruguay', 'Venezuela']
EAP_list = ['Australia', 'Indonesia', 'Japan', 'Malaysia', 'New Zealand', 'Philippines', 'Singapore',
            'South Korea', 'Taiwan', 'Thailand', 'Vietnam']
EURAFR_list = [
    "Albania", "Andorra", "Armenia", "Austria", "Azerbaijan",
    "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia",
    "Cyprus", "Czechia", "Denmark", "Estonia", "Finland", "France", "Georgia",
    "Germany", "Greece", "Hungary", "Iceland", "Ireland", "Italy", "Kosovo",
    "Latvia", "Liechtenstein", "Lithuania", "Luxembourg", "Malta", "Moldova",
    "Monaco", "Montenegro", "Netherlands", "North Macedonia", "Norway", "Poland",
    "Portugal", "Romania", "Russia", "San Marino", "Serbia", "Slovakia", "Slovenia",
    "Spain", "Sweden", "Switzerland", "Turkey", "Ukraine", "United Kingdom",
    "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cabo Verde",
    "Cameroon", "Central African Republic", "Chad", "Comoros", "Côte d’Ivoire",
    "Democratic Republic of the Congo", "Djibouti", "Equatorial Guinea", "Eritrea",
    "Eswatini", "Ethiopia", "Gabon", "The Gambia", "Ghana", "Guinea", "Guinea-Bissau",
    "Kenya", "Lesotho", "Liberia", "Madagascar", "Malawi", "Mali", "Mauritania",
    "Mauritius", "Mozambique", "Namibia", "Niger", "Nigeria", "Republic of the Congo",
    "Rwanda", "Sao Tome and Principe", "Senegal", "Seychelles", "Sierra Leone",
    "Somalia", "South Africa", "South Sudan", "Sudan", "Tanzania", "Togo", "Uganda",
    "Zambia", "Zimbabwe"
]

region_list = EURAFR_list


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


def country_searcher(row, country):
    if country in row['Countries']:
        return True
    return False


def country_parser(df_to_search, country):
    mask = df_to_search.apply(lambda row: country_searcher(row, country), axis=1)
    df = df_to_search[mask]
    return df


countries_list = []
for country in region_list:
    countries_list.append(official_name_converter(country_converter(country)))
print(countries_list)

df.fillna('', inplace=True)
for country in countries_list:
    outdf = country_parser(df, country)
    if outdf.empty:
        continue
    outdf.to_csv(f'{country}_papers.csv',index=False)
    print(country, len(outdf))
