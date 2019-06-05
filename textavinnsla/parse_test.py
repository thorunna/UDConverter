from nltk.corpus.util import LazyCorpusLoader
from nltk.corpus.reader import CategorizedBracketParseCorpusReader
from nltk.data import path
from nltk.tree import *
from pprint import pprint
import string
import re

# path.extend(['/Users/hinrik/Documents/trjabankar'])
# path.extend(['./icepahc_nltk/'])
path.extend(['./testing/'])


# icepahc = LazyCorpusLoader(
#     'icepahc-v0.9/psd/', CategorizedBracketParseCorpusReader,
#     r'2008\.mamma\.nar-fic\.psd', cat_pattern=r'.*(nar|rel|sci|bio|law)\-.*'
# )

icepahc = LazyCorpusLoader(
    'icepahc-v0.9/psd_orig/', CategorizedBracketParseCorpusReader,
    r'.*\.psd', cat_pattern=r'.*(nar|rel|sci|bio|law)\-.*'
)

trees = icepahc.parsed_sents()[0:20]
# tree = icepahc.parsed_sents()[0]
# tree = trees[0]

# pprint(tree.__dir__())
# print(tree)
# pprint(icepahc.fileids())

# ptree = ParentedTree.convert(tree)

cconj = {'og', 'eða', 'en', 'heldur', 'enda', 'ellegar',
        'bæði','hvorki','annaðhvort','hvort', 'ýmist'}

tags = {
    # ipsd_tag : UD_tag
    'N' : 'NOUN',   # generalized nouns tagged as NOUN
    'D' : 'DET',    # generalized determiners tagged as DET (determiner)
    'P' : 'ADP',    # generalized prepositions tagged as ADP
    'Q' : 'ADJ',    # quantifiers tagged as ADJ - ATH ÞETTA ÞARF AÐ ENDURSKOÐA
    'C' : 'SCONJ',  # complimentizer tagged as SCONJ (subordinate conjunction)
    'V' : 'VERB',
    'W' : 'DET',    # WH-determiner tagged as DET (determiner)
    'R' : 'VERB',   # All forms of "verða" tagged as VERB
    'TO' : 'PART',  # Infinitive marker tagged as PART (particle)
    'NPR' : 'POPN', # proper nouns tagged as POPN
    'PRO' : 'PRON',
    'NUM' : 'NUM',
    'ONE' : 'NUM',
    'ADJ' : 'ADJ',  # Adjectives tagged as ADV
    'ADJR' : 'ADJ', # Comparative adjectives tagged as ADV
    'ADJS' : 'ADJ', # Superlative adjectives tagged as ADV
    'ADV' : 'ADV',  # Adverbs tagged as ADV
    'NEG' : 'ADV',
    'ADVR' : 'ADV', # Comparative adverbs tagged as ADV
    'ADVS' : 'ADV', # Superlative adverbs tagged as ADV
    'ALSO' : 'ADV',
    'OTHER' : 'PRON',
    'OTHERS' : 'PRON'
}

def get_UD_tag(tag, word):
    # if ipsd_tag.beginswith('NPR'):
    #     return tags['NPR']
    tag = tag.split('-')[0]
    try:
        return tags[tag]
    except:
        if tag == 'NEG':
            return tags[tag]
        # elif tag.startswith('PRO'):
        #     return tags['PRO']
        # elif tag.startswith('NUM') or tag.startswith('ONE'):
        #     return 'NUM'
        elif tag == 'CONJ' and word in cconj:
            return 'CCONJ'
        elif tag in string.punctuation:
            return 'PUNCT'
        else:
            try:
                return tags[tag[0]]
            except:
                return '_'

def word_info(sentence):

    sentence = []
    runner = 0
    sentence.append(['nr.', 'token', 'lemma', 'UD_tag', 'ice_tag', 'feats', 'rel', 'rel_type'])
    for leaf in tree.pos():
        word = leaf[0].split('-')
        token = word[0]
        if token[0] in ['*', '0']: continue
        lemma = word[1]
        ipsd_tag = leaf[1]
        runner += 1
        UD_tag = get_UD_tag(ipsd_tag, lemma)
        feats = '_'
        rel = '_'
        rel_type = '_'
        line = [str(runner), token, lemma, UD_tag, ipsd_tag, feats, rel, rel_type]
        sentence.append(line)
    return sentence

for tree in trees:
    print()
    for word in word_info(tree):
        print('\t'.join(word))


# print(tree.pformat_latex_qtree())
