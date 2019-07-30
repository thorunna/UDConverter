
from lib_test.rules import DMII_map
from ast import literal_eval as make_tuple
from collections import defaultdict, Hashable
from sys import getsizeof
from pprint import pprint
import os
import csv
import time
import string
import json
import re

class DMII_word():
    '''
    Reads line in 'Sigrúnarsnið' DMII output and converts to DMII_word instance
    DMII_word.features is a dict of grammatical features for the given token
    as described in the DMII
    '''

    def __init__(self, line):
        self.token = line[4].lower()
        self.lemma = line[0].lower()
        self._class = line[2]
        self._featureString = line[5]
        self.subclass = None
        # self.features = None
        self.features = defaultdict(lambda:  { 'Case' : None,
                                    'Number' : None,
                                    'Definite' : None,
                                    'Gender' : None,
                                    'PronType' : None,
                                    'Degree' : None,
                                    'Mood' : None,
                                    'Tense' : None,
                                    'VerbForm' : None,
                                    'Voice' : None,
                                    'Person' : None,
                                    'NumType' : None,
                                    'AdpType' : None,
                                    'Clitic' : None,
                                   })

        def _populate_features(self):
            '''
            Sets relevant attributes for each instance based on information in
            Sigrúnarsnið line
            '''
            f = self._featureString
            if f[-1].isdigit():
                return self
            # nouns
            if self._class in {'hk', 'kk', 'kvk'}:
                self.features = {'Case' : DMII_map[0]['Case'][f[0:2]],
                                'Gender' : DMII_map[0]['Gender'][self._class],
                                'Definite' : DMII_map[0]['Definite'][f[-2:]],
                                }
                if len(f) > 5:
                    # print(line, f)
                    # self.features['Definite'] = DMII_map[0]['Definite'][f[-2:]]
                    self.features['Number'] = DMII_map[0]['Number'][f[-4:-2]],
                else:
                    self.features['Number'] = DMII_map[0]['Number'][f[-2:]]
            # adjectives
            elif self._class == 'lo':
                f = self._featureString.split('-')
                if len(f) < 3:
                    self.features = {'Case' : DMII_map[0]['Case'][f[1][0:2]],
                                    'Number' : DMII_map[0]['Number'][f[1][-2:]],
                                    'Gender' : DMII_map[0]['Gender'][f[0]]
                                    }
                else:
                    # print(f, line)
                    self.features = {'Case' : DMII_map[0]['Case'][f[2][0:2]],
                                    'Number' : DMII_map[0]['Number'][f[2][-2:]],
                                    'Gender' : DMII_map[0]['Gender'][f[1]]
                                    }
                if f[0][1:] in {'SB', 'VB'}:
                    self.features['Definite'] = DMII_map[0]['Definite'][f[0][1:]]
                else:
                    self.features['Definite'] = None

            # verbs
            elif self._class == 'so':
                f = self._featureString.split('-')
                # past participle
                if f[0] == 'LHÞT':
                    self.subclass = f[0]
                    self.features = {'Case' : DMII_map[0]['Case'][f[3][0:2]],
                                    'Number' : DMII_map[0]['Number'][f[3][-2:]],
                                    'Definite' : DMII_map[0]['Definite'][f[1]],
                                    'Gender' : DMII_map[0]['Gender'][f[2]],
                                    }
                # infinitives and supine
                elif f[-1] in {'SAGNB', 'NH'}:
                    self.subclass = f[-1]
                    self.features = None
                # infinitives
                elif 'NH' in f:
                    self.subclass = 'NH'
                    self.features = None
                # impersonals
                elif f[0] in {'OP'}: # ATH: Var þessu alltaf sleppt?
                    self.features = None
                # present participle
                elif self._featureString == 'LH-NT':
                    self.features = None
                # imperative
                elif f[1] == 'BH':
                    self.features = None
                # infinitives and subjunctives (rest)
                elif 'FN' in f:
                    self.features = None
                else:
                    # print(f, line)
                    self.features = {'Number' : DMII_map[0]['Number'][f[-1]],
                                    'Mood' : DMII_map[0]['Mood'][f[1]],
                                    'Tense' : DMII_map[0]['Tense'][f[2]],
                                    'Voice' : DMII_map[0]['Voice'][f[0]],
                                    'Person' : DMII_map[0]['Person'][f[3]],
                                    }
            # pronouns
            elif self._class in {'fn', 'pfn', 'afturbfn', 'sp', 'tv', 'ab', 'oakv'}:
                f = self._featureString.strip(' ')
                if '-' in f:
                    f = f.split('-')
                else:
                    f = f.split('_')
                if 'fn' in f:
                    f.remove('fn')
                # print(f, line)
                self.features = {'Case' : DMII_map[0]['Case'][f[-1][0:2]],
                                'PronType' : DMII_map[0]['PronType'].get(self._class),
                                }
                if len(f[-1]) > 2:
                    self.features['Number'] = DMII_map[0]['Number'][f[-1][-2:]]
                if len(f) == 2:
                    self.features['Gender'] = DMII_map[0]['Gender'][f[0]]
            # numerals
            elif self._class == 'to':
                # print(f, line)
                f = self._featureString.split('_')
                # print(f, line)
                self.features = {'Case' : DMII_map[0]['Case'][f[1][0:2]],
                                'Number' : DMII_map[0]['Number'][f[1][-2:]],
                                'Gender' : DMII_map[0]['Gender'][f[0]],
                                }
                # print(self.features)
            return self

        def _getUDtags(self):
            '''
            finds Universal Dependencies POS-tag for each word using rules module
            '''
            if self.features:
                try:
                    # print(self.lemma, self.features, self._featureString, 'before')
                    for key, DMII_tag in self.features.items():
                        self.features[key] = DMII_map[0][key][DMII_tag]
                    # print(self.lemma, self.features, 'after')
                    # print()
                except:
                    print(self.lemma, self.features, self._featureString, self.subclass, 'before')
                    raise
            return self

        _populate_features(self)
        # _getUDtags(self)




def DMII_data(filename):
    print('Accessing DMII data for', filename+'.csv...')
    # bin_token = []
    # bin_lemma = []
    # bin_tags = []
    # bin_classes = []
    bin_all = {}
    # DMII_path = os.path.join('DMII_data', 'SHsnid.csv')
    DMII_path = os.path.join('DMII_data', 'split', filename+'.csv')
    DMII = csv.reader(open(DMII_path, encoding = 'UTF-8'), delimiter=';')
    start = time.time()
    for line in DMII:
        # print(line)
        word = DMII_word(line)
        # print(word.features)
        if word.features:
            # print(word.features)
            if word.lemma not in bin_all:
                bin_all[word.lemma] = {word}
            else:
                bin_all.get(word.lemma).add(word)
        else:
            continue
        # # print(line)
        # # bin_lemmas.append(line[0])
        # # print(line[4]+line[0], line[5])
        # bin_token.append(line[4])
        # bin_lemma.append(line[0])
        # bin_tags.append(line[5])
        # bin_classes.append(line[2])
    # bin_all = dict(zip(zip(bin_token, bin_lemma) , zip(bin_tags, bin_classes)))
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
        return dict[word]
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

def create_lemmaDict(filename):
    print('Compiling list of DMII lemmas from', filename+'.csv...')
    bin_all = {}
    DMII_path = os.path.join('DMII_data', 'split', filename+'.csv')
    DMII = csv.reader(open(DMII_path, encoding = 'UTF-8'), delimiter=';')
    start = time.time()
    for line in DMII:
        bin_all[line[4]] = line[0]
    end = time.time()
    print('DMII ready. Time elapsed:', end-start, 'seconds' )
    return bin_all

lemmaDict = create_lemmaDict('combined')

def get_lemma(token):
    if token.endswith('$'):
        token = re.sub('\$', '', token)
    # print('Finding lemma for "{0}"...'.format(token))
    # try:
    lemma = lemmaDict.get(token)
    return lemma
    # except:
    #     # print('Word "{0}" not present in DMII.'.format(token))
    #     return



'''
def get_gender(word_info, lemma, token):
    if lemma = word_info[1] and type == word_info[2]:
        return word_info[0]
    else:
        pass
'''

def test1():
    DMII_path = os.path.join('DMII_data', 'split', 'so.csv')
    dmii_so = csv.reader(open(DMII_path, encoding = 'UTF-8'), delimiter=';')

    lines = ['köttur;416784;kk;alm;kattarins;EFETgr;',
            'köttur;416784;kk;alm;kötturinn;NFETgr;',
            'köttur;416784;kk;alm;kött;ÞFET;',
            'köttur;416784;kk;alm;köttinn;ÞFETgr;',
            'mús;12269;kvk;alm;mýsnar;NFFTgr',
            'góður;412191;lo;alm;bestir;ESB-KK-NFFT',
            'auðvelda;419421;so;alm;auðveldaði;GM-VH-ÞT-1P-ET',
            'auðvelda;419421;so;alm;auðvelddfsfai;GM-VH-ÞT-1P-ET',
            'auðvelda;419421;so;alm;auðvei;GM-VH-ÞT-1P-ET',
            'auðvelda;419421;so;alm;auði;GM-VH-ÞT-1P-ET',
            ]
    bin_all = {}
    for line in dmii_so:
        # line = line.split(';')
        # print(line)
        word = DMII_word(line)
        # print(line)
        # print(isinstance(word, Hashable))
        # print('\t',word.lemma, word.features['Number'])
        if word.lemma not in bin_all:
            bin_all[word.lemma] = {word}
        else:
            bin_all.get(word.lemma).add(word)
        # print(bin_all)
    for k,v in bin_all.items():
        for item in v:
            print(item.token)
    # pprint(bin_all)

def test2():

    DMII_no = DMII_data('no')
    no_size = getsizeof(DMII_no)
    print(no_size)
    # del DMII_no
    DMII_lo = DMII_data('lo')
    lo_size = getsizeof(DMII_lo)
    print(lo_size)
    # del DMII_lo
    DMII_fn = DMII_data('fn')
    fn_size = getsizeof(DMII_fn)
    print(fn_size)
    # del DMII_fn
    DMII_to = DMII_data('to')
    to_size = getsizeof(DMII_to)
    print(to_size)
    # del DMII_to
    # DMII_ao = DMII_data('ao')
    DMII_so = DMII_data('so')
    so_size = getsizeof(DMII_so)
    print(so_size)
    # del DMII_so
    total_size = no_size + lo_size + fn_size + to_size + so_size
    print('Total size:', total_size)
    # for word in data:
    #     print(word.features.get('Case'))

def test3():
    DMII_combined = DMII_data('combined')
    combined_size = getsizeof(DMII_combined)
    print(combined_size)
    del DMII_combined

if __name__ == '__main__':
    test1()

# lv13-dw11:trjabankar hinrik$ python3 scripts/lib/DMII_data.py
# Accessing DMII data for no.csv...
# DMII ready. Time elapsed: 48.75069785118103 seconds
# 134217952
# Accessing DMII data for lo.csv...
# DMII ready. Time elapsed: 35.324458837509155 seconds
# 67109088
# Accessing DMII data for fn.csv...
# DMII ready. Time elapsed: 0.020704030990600586 seconds
# 131296
# Accessing DMII data for to.csv...
# DMII ready. Time elapsed: 0.0009129047393798828 seconds
# 2272
# Accessing DMII data for so.csv...
# DMII ready. Time elapsed: 9.257171869277954 seconds
# 33554656
# Total size: 235015264
# lv13-dw11:trjabankar hinrik$ python3 scripts/lib/DMII_data.py
# Accessing DMII data for combined.csv...
# DMII ready. Time elapsed: 166.30201697349548 seconds
# 268435680
