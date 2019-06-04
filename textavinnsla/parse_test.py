from nltk.corpus.util import LazyCorpusLoader
from nltk.corpus.reader import CategorizedBracketParseCorpusReader
from nltk.data import path
from nltk.tree import *
import string

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

tree = icepahc.parsed_sents()[6]

ptree = ParentedTree.convert(tree)

cconj = {'og', 'eða', 'en', 'heldur', 'enda', 'ellegar',
        'bæði','hvorki','annaðhvort','hvort', 'ýmist'}

tags = {
    # ipsd_tag : UD_tag
    'N' : 'NOUN',   # generalized nouns tagged as NOUN
    'D' : 'DET',    # generalized determiners tagged as DET
    'P' : 'ADP',    # generalized prepositions tagged as ADP
    'Q' : 'ADJ',    # quantifiers tagged as ADJ - ATH ÞETTA ÞARF AÐ ENDURSKOÐA
    'NPR' : 'POPN', # proper nouns tagged as POPN
    'ADJ' : 'ADJ',
    'PRO' : 'PRON',
    'NUM' : 'NUM',
    'ADV' : 'ADV',
    'NEG' : 'ADV',
    'ALSO' : 'ADV'
}

def get_UD_tag(tag, word):
    # if ipsd_tag.beginswith('NPR'):
    #     return tags['NPR']
    try:
        return tags[tag]
    except:
        if tag == 'NEG':
            return tags[tag]
        elif tag.startswith('PRO'):
            return tags['PRO']
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

print()
for word in word_info(tree):
    print('\t'.join(word))


# print(tree.pformat_latex_qtree())
