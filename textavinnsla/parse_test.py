from lib import BIN_data
from lib import features
from nltk.corpus.util import LazyCorpusLoader
from nltk.corpus.reader import CategorizedBracketParseCorpusReader
from nltk.data import path
from nltk.tree import *
from tokenizer import correct_spaces
from pprint import pprint

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

def sent_text(sentence):
    '''
    Takes in a nltk Tree object and returns the sentence text in string form
    '''
    text = []
    leaves = sentence.leaves()
    for leaf in leaves:
        leaf = leaf.split('-')
        if leaf[0][0] in {'*', '0'}: continue
        text.append(leaf[0])
    text = '# text = ' + correct_spaces(' '.join(text))
    return text

def word_info(tree):
    '''
    Takes in a nltk Tree object and returns an approximation of the tree sentence
    in the CONLLU format for UD
    '''
    sentence = []
    runner = 0
    # print(tree.leaves())
    sentence.append(sent_text(tree))
    sentence.append(['ID', 'FORM', 'LEMMA', 'UPOS', 'XPOS', 'FEATS', 'HEAD', 'DEPREL', 'DEPS', 'MISC'])
    for leaf in tree.pos():
        # print(leaf)
        runner += 1 # runner updated for counting
        ID = str(runner) # ID: Word index, integer starting at 1 for each new sentence.
        word = leaf[0].split('-') # token and lemma seperated.
        FORM = word[0] # FORM: Word form or punctuation symbol (token).
        if FORM[0] in ['*', '0']: continue
        LEMMA = word[1] # LEMMA: Lemma or stem of word form.
        XPOS = leaf[1] # XPOS: Language-specific part-of-speech tag (IcePaHC)
        UPOS = features.get_UD_tag(XPOS, LEMMA) # UPOS: Universal part-of-speech tag.
        FEATS = features.get_feats(leaf) # FEATS: List of morphological features from the universal feature inventory
        HEAD = '_' # HEAD: Head of the current word, which is either a value of ID or zero (0).
        DEPREL = '_' # DEPREL: Universal dependency relation to the HEAD (root iff HEAD = 0)
        DEPS = '_' # DEPS: Enhanced dependency graph in the form of a list of head-deprel pairs.
        MISC = '_' # MISC: Any other annotation.
        line = [str(runner), FORM, LEMMA, UPOS, XPOS, FEATS, HEAD, DEPREL, DEPS, MISC]
        sentence.append(line)
    return sentence

# ID: Word index, integer starting at 1 for each new sentence.
# FORM: Word form or punctuation symbol.
# LEMMA: Lemma or stem of word form.
# UPOS: Universal part-of-speech tag.
# XPOS: Language-specific part-of-speech tag; underscore if not available.
# FEATS: List of morphological features from the universal feature inventory or from a defined language-specific extension; underscore if not available.
# HEAD: Head of the current word, which is either a value of ID or zero (0).
# DEPREL: Universal dependency relation to the HEAD (root iff HEAD = 0) or a defined language-specific subtype of one.
# DEPS: Enhanced dependency graph in the form of a list of head-deprel pairs.
# MISC: Any other annotation.

fileids = icepahc.fileids() # TODO: Get fileid info per tree for tree ids
# trees = icepahc.parsed_sents()[0:10]

# tree = trees[0]

# for s in trees:
#     print(s)

def print_data():
    current_sentence = 0
    with open('out_test/is_test.02.conllu', 'w') as file:
        while current_sentence <= 100:
            try:
                # file.write('hello')
                print('\n# sent_id = ', current_sentence + 1)
                tree = icepahc.parsed_sents()[current_sentence]
                # file.write('# sent_id = ' + str(current_sentence + 1))
                # file.write('\n')
                for line in word_info(tree):
                    if line[0] == '#':
                        print(line)
                        # file.write(line)
                        # file.write('\n')
                    else:
                        print('\t'.join(line))
                        # file.write('\t'.join(line))
                        # file.write('\n')
                # file.write('\n')
                current_sentence += 1
            except:
                raise
                print('\n# sent_id = ', current_sentence)
                print('Failure')
                current_sentence += 1
                continue

# BIN_data.get_BIN()

print_data()
