# README
# As with collabs.py this script is not fully finished
# It will return a partially cleaned list but some data is lost in the process and isn't entirely accurate
# I would recommend using a more advanced tool like NLP/GenAI or string matching with a more powerful computer

import pandas as pd
import json
import matplotlib.pyplot as plt
import rapidfuzz
from unidecode import unidecode

df = pd.read_csv('collabs.csv')

university_words = ['University', 'Universidad', 'Université', 'Universitat', 'Organization', 'Polytechnique',
                    'Organisation', 'Universiteit', 'Ecole']
next_words = ['Institute', 'Laboratory', 'Institut', 'Laboratories']
next2_words = ['Center', 'Corporation', 'Research', 'Semiconductor', 'Technologies', 'Limited', 'Agency', 'Centre', 'Systems']
acronyms = ['CSIRO', 'GmbH', 'CERN', 'ETH', 'IBM']

lst_of_list = [university_words, next_words, next2_words, acronyms]


def remove_enclosed_text(text):
    # Find the index of the first opening parenthesis
    start_index = text.find('(')

    # Find the index of the corresponding closing parenthesis
    end_index = text.find(')', start_index)

    # Continue until there are no more parentheses
    while start_index != -1 and end_index != -1:
        # Remove the text enclosed in parentheses
        text = text[:start_index] + text[end_index + 1:]

        # Find the index of the next opening parenthesis
        start_index = text.find('(')

        # Find the index of the corresponding closing parenthesis
        end_index = text.find(')', start_index)

    return text


def cleaner(string, targetword):
    if isinstance(string, str):
        string = unidecode(remove_enclosed_text(string))
        if targetword not in string:
            return string
        str_list = string.split(',')
    else:
        return string
    str_list = [ele for ele in str_list if targetword in ele]
    s = str_list[0].strip()
    return ''.join(i for i in s if not i.isdigit())


for lst in lst_of_list:
    for word in lst:
        df['InstName'] = df['InstName'].apply(lambda x: cleaner(x, word))
df['InstName'] = df.InstName.apply(lambda x: unidecode(x))
# s2 = df.groupby(['Country', 'InstName'])['Article Citation Count'].sum()
# # print(s2)
df.to_csv('inst_pubs.csv')

