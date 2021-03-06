from lib import DMII_data
from lib import features
# from lib import depender
import nltk >= 3.4.5
from nltk.corpus.util import LazyCorpusLoader
from nltk.corpus.reader import CategorizedBracketParseCorpusReader
from nltk.data import path
from nltk.tree import *
# from pprint import pprint
import os
import time

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
        elif leaf[0] == '<dash/>' or leaf[0] == '<dash>' or leaf[0] == '</dash>':
            FORM = '-'
            LEMMA = '-'
            token_lemma = str(FORM+'-'+LEMMA)
            tag = leaf[1]
            leaf = token_lemma, tag
        else:   # if no lemma present
            FORM = leaf[0]
            if FORM[0] not in ['*', '0']:
                # DMII_combined = DMII_data.DMII_data('combined')
                LEMMA = DMII_data.get_lemma(DMII_combined, FORM)
                if LEMMA == None:
                    LEMMA = '_'
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

# No. Filename No. of sents. Errors
# 1 1150.firstgrammar.sci-lin.psd    182 0
# 2 1150.homiliubok.rel-ser.psd     2103 0
# 3 1210.jartein.rel-sag.psd         822 0
# 4 1210.thorlakur.rel-sag.psd       540 0
# 5 1250.sturlunga.nar-sag.psd      2225 0
# 6 1250.thetubrot.nar-sag.psd       246 0
# 7 1260.jomsvikingar.nar-sag.psd   1532 0
# 8 1270.gragas.law-law.psd          346 0
# 9 1275.morkin.nar-his.psd         2186 0
# 10 1300.alexander.nar-sag.psd     1383 1
# 11 1310.grettir.nar-sag.psd       2057 0
# 12 1325.arni.nar-sag.psd          1125 0
# 13 1350.bandamennM.nar-sag.psd    1222 0
# 14 1350.finnbogi.nar-sag.psd      2342 2
# 15 1350.marta.rel-sag.psd          977 1
# 16 1400.gunnar.nar-sag.psd         935 0
# 17 1400.gunnar2.nar-sag.psd        340 0
# 18 1400.viglundur.nar-sag.psd     1288 0
# 19 1450.bandamenn.nar-sag.psd     1034 0
# 20 1450.ectorssaga.nar-sag.psd    1950 0
# 21 1450.judit.rel-bib.psd          491 0
# 22 1450.vilhjalmur.nar-sag.psd    2414 0
# 23 1475.aevintyri.nar-rel.psd     1200 2
# 24 1480.jarlmann.nar-sag.psd      1282 0
            # Bad tree detected; trying to recover...
            #   Recovered by returning a flat parse.
# 25 1525.erasmus.nar-sag.psd        461 1
# 26 1525.georgius.nar-rel.psd      1060 0
# 27 1540.ntacts.rel-bib.psd        1183 0
# 28 1540.ntjohn.rel-bib.psd        1685 0
# 29 1593.eintal.rel-oth.psd        1553 0
# 30 1611.okur.rel-oth.psd           629 0
# 31 1628.olafuregils.bio-tra.psd    906 0
# 32 1630.gerhard.rel-oth.psd        701 0
# 33 1650.illugi.nar-sag.psd        1929 0
# 34 1659.pislarsaga.bio-aut.psd     324 0
# 35 1661.indiafari.bio-tra.psd     1388 0
# 36 1675.armann.nar-fic.psd        1018 0
# 37 1675.magnus.bio-oth.psd         204 0
# 38 1675.modars.nar-fic.psd         373 0
# 39 1680.skalholt.nar-rel.psd       869 0
# 40 1720.vidalin.rel-ser.psd       1112 0
# 41 1725.biskupasogur.nar-rel.psd  1105 0
# 42 1745.klim.nar-fic.psd           873 0
# 43 1790.fimmbraedra.nar-sag.psd   1602 1
            # Bad tree detected; trying to recover...
            #   Recovered by returning a flat parse.
# 44 1791.jonsteingrims.bio-aut.psd 1517 1
# 45 1830.hellismenn.nar-sag.psd    1411 0
# 46 1835.jonasedli.sci-nat.psd      163 0
# 47 1850.piltur.nar-fic.psd        1440 1
# 48 1859.hugvekjur.rel-ser.psd     1110 0
# 49 1861.orrusta.nar-fic.psd       1804 0
            # Bad tree detected; trying to recover...
            #   Recovered by returning a flat parse.
# 50 1882.torfhildur.nar-fic.psd    1999 3
# 51 1883.voggur.nar-fic.psd         130 0
# 52 1888.grimur.nar-fic.psd         625 0
# 53 1888.vordraumur.nar-fic.psd     756 0
# 54 1902.fossar.nar-fic.psd        1659 0
# 55 1907.leysing.nar-fic.psd       1521 0
# 56 1908.ofurefli.nar-fic.psd      1743 0
# 57 1920.arin.rel-ser.psd          1149 0
# 58 1985.margsaga.nar-fic.psd      1705 0
# 59 1985.sagan.nar-fic.psd         2008 0
# 60 2008.mamma.nar-fic.psd         1845 0
# 61 2008.ofsi.nar-sag.psd          1210 0
# Total:                           72992 13

def print_data():
    '''
        Prints the CONllu data to command line or writes it to file, by
        specification.
    '''
    fileids = icepahc.fileids()[5:10] # leave uncommented for whole corpus use
    # fileids = ['1250.sturlunga.nar-sag.psd'] # For debug use only
    total_sents = 0
    # CONLLU_log = open('out_test/is_test.02.conllu', 'w') # old debug
    for fileid in fileids:
        error_num = 0
        start = time.time()
        file_sents = 0
        print('\nProcessing file: {0}...'.format(fileid))
        CONLLU_log = os.path.splitext(fileid)[0]
        CONLLU_log = os.path.join('out_test', '03', CONLLU_log + '.err.conllu')
        CONLLU_log = open(CONLLU_log, 'w')
        for tree in icepahc.parsed_sents(fileid):
            treeID = fileid + '_' + str(file_sents+1) + '_' + str(total_sents+1)
            try:
                # print('# sent_id =', treeID)
                # CONLLU_log.write('# sent_id = ' + treeID)
                # CONLLU_log.write('\n')
                for line in word_info(tree):
                    pass
                    # if line[0] == '#':
                        # print(line)
                        # CONLLU_log.write(line)
                        # CONLLU_log.write('\n')
                    # else:
                        # print('\t'.join(line))
                        # CONLLU_log.write('\t'.join(line))
                        # CONLLU_log.write('\n')
                # CONLLU_log.write('\n')
                total_sents += 1
                file_sents += 1
            except Exception as ex:
                # raise
                error_num += 1
                print('\n# sent_id = ',  treeID)
                print('Failure - {0}. Arguments:\n{1!r}'.format(type(ex).__name__, ex.args))
                print(tree)
                # CONLLU_log.write('# sent_id = ' + treeID) # leave commented
                # CONLLU_log.write('\nFailure - {0}. Arguments:\n{1!r}\n\n'.format(type(ex).__name__, ex.args))
                total_sents += 1
                file_sents += 1
                # continue
        end = time.time()
        duration = '%.2f' % float(end - start)
        print('Finished! Time elapsed: {0} seconds'.format(duration))
        print('Number of sentences in file: {0}'.format(file_sents))
        print('Number of failed sentences: {0}'.format(error_num))

DMII_combined = DMII_data.load_json('combined')

if __name__ == '__main__':
    print_data()
