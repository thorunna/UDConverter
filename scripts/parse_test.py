from lib import DMII_data
from lib import features
from nltk.corpus.util import LazyCorpusLoader
from nltk.corpus.reader import CategorizedBracketParseCorpusReader
from nltk.data import path
from nltk.tree import *
from tokenizer import correct_spaces
from pprint import pprint
import os

import re


# path.extend(['/Users/hinrik/Documents/trjabankar'])
# path.extend(['./icepahc_nltk/'])
path.extend(['./testing/'])


# icepahc = LazyCorpusLoader(
#     'icepahc-v0.9/psd/', CategorizedBracketParseCorpusReader,
#     r'2008\.mamma\.nar-fic\.psd', cat_pattern=r'.*(nar|rel|sci|bio|law)\-.*'
# )

icepahc = LazyCorpusLoader(
    'icepahc-v0.9/psd/', CategorizedBracketParseCorpusReader,
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
        in the CONLLU format for UD:
            ID: Word index, integer starting at 1 for each new sentence.
            FORM: Word form or punctuation symbol.
            LEMMA: Lemma or stem of word form.
            UPOS: Universal part-of-speech tag.
            XPOS: Language-specific part-of-speech tag; underscore if not available.
            FEATS: List of morphological features from the universal feature inventory or from a defined language-specific extension; underscore if not available.
            HEAD: Head of the current word, which is either a value of ID or zero (0).
            DEPREL: Universal dependency relation to the HEAD (root iff HEAD = 0) or a defined language-specific subtype of one.
            DEPS: Enhanced dependency graph in the form of a list of head-deprel pairs.
            MISC: Any other annotation.
    '''
    sentence = []
    runner = 0
    # print(tree.leaves())
    sentence.append(sent_text(tree))
    sentence.append(['ID', 'FORM', 'LEMMA', 'UPOS', 'XPOS', 'FEATS', 'HEAD', 'DEPREL', 'DEPS', 'MISC'])
    for leaf in tree.pos():
        runner += 1 # runner updated for counting
        ID = str(runner) # ID: Word index, integer starting at 1 for each new sentence.
        if '-' in leaf[0]:  # if token and lemma present
            word = leaf[0].split('-') # token and lemma separated.
            FORM = word[0] # FORM: Word form or punctuation symbol (token).
            LEMMA = word[1]
        else:   # if no lemma present
            FORM = leaf[0]
            if FORM[0] not in ['*', '0']:
                DMII_combined = DMII_data.DMII_data('combined')
                LEMMA = DMII_data.get_lemma(DMII_combined, FORM)
                token_lemma = str(FORM+'-'+LEMMA)
                tag = leaf[1]
                leaf = token_lemma, tag
        if FORM[0] in ['*', '0']: continue
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


def print_data():
    '''
        Prints the CONllu data to command line or writes it to file, by
        specification.
    '''
    # fileids = icepahc.fileids() # leave uncommented for whole corpus use
    fileids = ['1150.homiliubok.rel-ser.psd'] # For debug use only
    total_sents = 0
    # CONLLU_log = open('out_test/is_test.02.conllu', 'w') # old debug
    for fileid in fileids:
        file_sents = 0
        # CONLLU_log = os.path.splitext(fileid)[0]
        # CONLLU_log = os.path.join('out_test', '03', CONLLU_log + '.conllu')
        # CONLLU_log = open(CONLLU_log, 'w')
        for tree in icepahc.parsed_sents(fileid):
            treeID = fileid + '_' + str(file_sents+1) + '_' + str(total_sents+1)
            try:
                print('# sent_id =', treeID)
                # CONLLU_log.write('# sent_id = ' + treeID)
                # CONLLU_log.write('\n')
                for line in word_info(tree):
                    if line[0] == '#':
                        print(line)
                        # CONLLU_log.write(line)
                        # CONLLU_log.write('\n')
                    else:
                        print('\t'.join(line))
                        # CONLLU_log.write('\t'.join(line))
                        # CONLLU_log.write('\n')
                # CONLLU_log.write('\n')
                total_sents += 1
                file_sents += 1
            except:
                raise
                print('\n# sent_id = ',  treeID)
                print('Failure')
                print(tree)
                # CONLLU_log.write('# sent_id = ' + treeID)
                # CONLLU_log.write('Failure\n\n')
                total_sents += 1
                file_sents += 1
                continue

# print(DMII_data.get_DMII()['flestum'])

print_data()
