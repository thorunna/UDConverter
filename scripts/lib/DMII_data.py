
from ast import literal_eval as make_tuple
import os
import csv
import time
import string
import json
import re

def DMII_data(filename):
    print('Accessing DMII data for', filename+'.csv...')
    bin_token = []
    bin_lemma = []
    bin_tags = []
    bin_classes = []
    # DMII_path = os.path.join('DMII_data', 'SHsnid.csv')
    DMII_path = os.path.join('DMII_data', 'split', filename+'.csv')
    DMII = csv.reader(open(DMII_path, encoding = 'UTF-8'), delimiter=';')

    for line in DMII:
        # print(line)
        # bin_lemmas.append(line[0])
        # print(line[4]+line[0], line[5])
        bin_token.append(line[4])
        bin_lemma.append(line[0])
        bin_tags.append(line[5])
        bin_classes.append(line[2])
    bin_all = dict(zip(zip(bin_token, bin_lemma) , zip(bin_tags, bin_classes)))
    end = time.time()
    print('DMII ready. Time elapsed:', end-start, 'seconds' )
    return bin_all

def load_json(filename):
    print('Accessing DMII data for', filename + '.json...')
    start = time.time()
    DMII_path = os.path.join('DMII_data', 'json', 'DMII_' + filename + '.json')
    with open(DMII_path) as file:
        data = json.load(file)
        # data = {make_tuple(k):v for k,v in data.items()}
        end = time.time()
        print('DMII ready. Time elapsed:', end-start, 'seconds')
        return data


def check_DMII(dict, token, lemma):
    # print('Finding word...')
    start = time.time()
    word = token, lemma
    try:
        end = time.time()
        # print('Time elapsed searching for word:', end-start, 'seconds' )
        # print(word, dict[word])
        return dict[make_tuple(word)]
    except:
        # print('Word "{0}" not present in DMII.'.format(word))
        end = time.time()
        # print('Time elapsed searching for word:', end-start, 'seconds' )
        return

def check_DMII_verb(thedict, token, lemma, IPtag):
    word = token, lemma
    tense = IPtag[2]
    mood = IPtag[3]
    if tense == 'P':
        bin_tense = 'NT'
    elif tense == 'D':
        bin_tense = 'ÞT'
    if mood == 'I':
        bin_mood = 'FH'
    elif mood == 'S':
        bin_mood = 'VH'
    for k, v in thedict.items():
        tag = v[0].split('-')
        if tag[0] == 'OP':
            del tag[0]
        if k[0] == token and k[1] == lemma and tag[1] == bin_mood and tag[2] == bin_tense:
            return thedict[word]

def get_lemma(thedict, token):
    if token.endswith('$'):
        token = re.sub('\$', '', token)
    # print('Finding lemma for "{0}"...'.format(token))
    try:
        for word, tag in thedict.items():
            if word[0] == token:
                return word[1]
    except:
        # print('Word "{0}" not present in DMII.'.format(token))
        return



'''
def get_gender(word_info, lemma, token):
    if lemma = word_info[1] and type == word_info[2]:
        return word_info[0]
    else:
        pass
'''

if __name__ == '__main__':
    get_DMII()
