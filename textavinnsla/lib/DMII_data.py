
import os
import csv
import time

def DMII_data():
    print('Accessing DMII data...')
    bin_keys = []
    bin_tags = []
    bin_classes = []
    # DMII_path = os.path.join('DMII_data', 'SHsnid.csv')
    DMII_path = os.path.join('DMII_data', 'split', 'no.csv')
    DMII = csv.reader(open(DMII_path, encoding = 'UTF-8'), delimiter=';')
    start = time.time()
    for line in DMII:
        # print(line)
        # bin_lemmas.append(line[0])
        bin_keys.append(line[4]+line[0])
        bin_tags.append(line[5])
        bin_classes.append(line[2])
    bin_all = dict(zip(bin_keys, zip(bin_tags, bin_classes)))
    end = time.time()
    print('DMII ready. Time elapsed:', end-start, 'seconds' )
    return bin_all

def check_DMII(dict, word):
    print('Finding word...')
    start = time.time()
    try:
        end = time.time()
        print('Time elapsed searching for word:', end-start, 'seconds' )
        return dict[word]
    except:
        print('Word "{0}" not present in DMII.'.format(word))
        end = time.time()
        print('Time elapsed searching for word:', end-start, 'seconds' )
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
