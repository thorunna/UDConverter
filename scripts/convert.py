from lib import DMII_data
from lib import features
from lib import depender

from nltk.corpus.util import LazyCorpusLoader
from nltk.corpus.reader import CategorizedBracketParseCorpusReader
from nltk.data import path
from nltk.tree import *
from tokenizer import correct_spaces
from pprint import pprint
from collections import defaultdict, OrderedDict
import os
import time
import re
import string

path.extend(['./testing/'])

DMII_combined = DMII_data.load_json('combined') # TODO: Move to features script

icepahc = LazyCorpusLoader(
    'icepahc-v0.9/psd/', CategorizedBracketParseCorpusReader,
    r'.*\.psd', cat_pattern=r'.*(nar|rel|sci|bio|law)\-.*'
)

class Converter():
    def __init__(self):
        #todo read rules from config file
        self.t = None
        self.dg = None
        self.head_rules = {
#            'IP-MAT'  : {'dir':'r', 'rules':['VB.*','RD.*','BE.*','N.*']},
#            'IP-SUB'  : {'dir':'r', 'rules':['BED.','.*']},
#            'NP-SBJ'  : {'dir':'r', 'rules':['N-N']},
#            'NP-OB1'  : {'dir':'r', 'rules':['N-A', 'NPR-A', 'ONE+Q-A']},
#            'NP'      : {'dir':'r', 'rules':['NS-.', 'N-.']},
#            'NP-MSR'  : {'dir':'r', 'rules':['NS-.', 'N-.']},
#            'ADJP'    : {'dir':'r', 'rules':['ADJ-N']},
#            'ADJP-SPR': {'dir':'r', 'rules':['ADJ-N']},
#            'PP'      : {'dir':'r', 'rules':['P']},
#            'CP-THT'  : {'dir':'r', 'rules':['IP-SUB','.*']},
            #'IP-INF'  : {'dir':'r', 'rules':['IP-INF']},  # óþarfi, er fyrsti frá vinstri
            #'CONJP'   : {'dir':'r', 'rules':['IP-INF']}   # óþarfi, er fyrsti frá vinstri
            
            'IP-INF'        : {'dir':'r', 'rules':['VB']},
            'IP-INF-1'      : {'dir':'r', 'rules':['VB']},
            'IP-INF-PRP'    : {'dir':'r', 'rules':['VB']},
            'IP-INF-PRP-PRN': {'dir':'r', 'rules':['VB']},
            'IP-MAT'        : {'dir':'r', 'rules':['VB.*','RD.*', 'DO.*','N.*']}, 
            'IP-MAT-PRN'    : {'dir':'r', 'rules':['VB.*']},
            'IP-SUB'        : {'dir':'r', 'rules':['VB.*', 'DO.*', '.*', 'ADVP']},    #meira?
            'IP-SUB-PRN'    : {'dir':'r', 'rules':['VB.*']},
            'IP-SUB-SPE'    : {'dir':'r', 'rules':['VB.*']},
            'IP-IMP'        : {'dir':'r', 'rules':['VB.*']},
            'IP-SMC'        : {'dir':'r', 'rules':['ADJP']},
            'IP-PPL'        : {'dir':'r', 'rules':[]},
            'CP-THT'        : {'dir':'r', 'rules':['IP-SUB.*','.*']},
            'CP-CAR'        : {'dir':'r', 'rules':['NP.*']},
            'CP-CLF'        : {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-CMP'        : {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-DEG'        : {'dir':'r', 'rules':[]},
            'CP-FRL'        : {'dir':'r', 'rules':[]},
            'CP-REL'        : {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-QUE'        : {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-ADV'        : {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-EOP'        : {'dir':'r', 'rules':['IP-INF']},
            'CP-TMC'        : {'dir':'r', 'rules':['IP-INF']},
            'NP'            : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NP.*', 'PRO-.']},
            'NP-1'          : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NP.*', 'PRO-.']},
            'NP-ADV'        : {'dir':'r', 'rules':['NP.*']},
            'NP-CMP'        : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.']},
            'NP-PRN'        : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'PRO-.']},
            'NP-SBJ'        : {'dir':'r', 'rules':['N-N', 'NS-N', 'NPR-N', 'PRO-N', 'ADJ-N', 'ES']},
            'NP-SBJ-1'      : {'dir':'r', 'rules':['N-N', 'NS-N', 'NPR-N', 'PRO-N', 'ADJ-N', 'ES']},
            'NP-OB1'        : {'dir':'r', 'rules':['N-A', 'NPR-A', 'NS-A', 'ONE+Q-A']},
            'NP-OB2'        : {'dir':'r', 'rules':['NP.*', 'PRO-.', 'N-D', 'NS-D', 'NPR-.', 'CP-FRL', 'MAN-.']},    #MEIRA?
            'NP-OB3'        : {'dir':'r', 'rules':['PRO-D', 'N-D', 'NS-D', 'NPR-D']},
            'NP-PRD'        : {'dir':'r', 'rules':['NP.*', 'NPR-N', 'N-.']},
            'NP-POS'        : {'dir':'r', 'rules':['N.*', 'PRO-.']},
            'NP-COM'        : {'dir':'r', 'rules':[]},  #bara spor, hafa með?
            'NP-ADT'        : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.']},
            'NP-TMP'        : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.']},
            'NP-MSR'        : {'dir':'r', 'rules':['NS-.', 'N-.']},
            'ADJP'          : {'dir':'r', 'rules':['ADJ.*', 'ADJR.*', 'ADJS.*', 'ADVR', 'ONE']},
            'ADJP-SPR'      : {'dir':'r', 'rules':['ADJ-.', 'ADJS-N']},
            'PP'            : {'dir':'r', 'rules':['NP.*', 'P']},
            'PP-BY'         : {'dir':'r', 'rules':['P']},
            'PP-PRN'        : {'dir':'r', 'rules':['P']},
            'ADVP'          : {'dir':'r', 'rules':['ADV', 'WADV']},
            'ADVP-DIR'      : {'dir':'r', 'rules':['ADV', 'WADV']},
            'ADVP-LOC'      : {'dir':'r', 'rules':['ADV', 'WADV']},
            'ADVP-TMP'      : {'dir':'r', 'rules':['ADV', 'WADV']},
            'RP'            : {'dir':'r', 'rules':[]},  #tagg fyrir orð en ekki phrase type?
            'CONJP'         : {'dir':'l', 'rules':['NP.*', 'NX' 'CONJ']},
            'WNP'           : {'dir':'r', 'rules':['WPRO-.', 'PRO-.']}, #MEIRA?
            'WPP'           : {'dir':'r', 'rules':['WNP', 'NP']},
            'NX'            : {'dir':'r', 'rules':['N-.']},
            'FRAG-LFD'      : {'dir':'r', 'rules':['IP-SMC']}
            }

    def _select_head(self, tree):
        '''

        '''
        tag = tree.label()
        head_rule = self.head_rules.get(tag, {'dir':'r', 'rules':['.*']})  #default rule, first from left
        rules = head_rule['rules']
        dir = head_rule['dir']
        head = None

        if dir == 'l':
            rules = reversed(rules)

        for rule in rules:
            for child in tree:
                if re.match(rule, child.label()):
                    tree.set_id(child.id())
                    return

        #no head-rules applicable: select either the first or last child as head
        if len(tree) == 0:
            tree.set_id(999) # For when there is no terminal node in head (text edit artifact)
        elif dir == 'l':
            tree.set_id(tree[-1].id())
        else:
            tree.set_id(tree[1].id()) # first from left indicated or no head rule index found

    def _relation(self, mod_tag, head_tag):
        """
            Return a Universal Relation name given an IcePaHC/Penn phrase-type tag

            http://www.linguist.is/icelandic_treebank/Phrase_Types
            to
            http://universaldependencies.github.io/docs/u/dep/index.html

        :param mod_tag: str
        :return: str
        """

        #todo use head_tag and more info about the constituency to better select the relation label

        if '-' in mod_tag:
            mod_tag, mod_func = mod_tag.split('-', 1) #todo, handle more than one function label
        else:
            mod_func = None

        if '-' in head_tag:
            head_tag, head_func = head_tag.split('-', 1)
        else:
            head_func = None

        if mod_tag == 'NP':
            # -ADV, -CMP, -PRN, -SBJ, -OB1, -OB2, -OB3, -PRD, -POS, -COM, -ADT, -TMP, -MSR
            return {
                'SBJ': 'nsubj',
                'OB1': 'dobj',
                'OB2': 'iobj',
                'OB3': 'iobj',
                'POS': 'nmod:poss',      #Örvar: 'POS': 'case'
            }.get(mod_func, 'rel')
        elif mod_tag == 'N' and head_tag == 'NP':
            return 'conj'
        elif mod_tag == 'NPR' and head_tag == 'NP':     #TODO: skoða betur, hliðstæð NPR sem eru bæði dobj? 
            return 'dobj'
        elif mod_tag == 'PRO' and head_tag == 'NP' and head_func == 'PRN':  #TODO: skoða betur, hliðstæð NPR sem eru bæði dobj? 
            return 'dobj'
        elif mod_tag == 'D' or mod_tag == 'ONE':
            return 'det'
        elif mod_tag == 'ADJP' or mod_tag == 'ADJ' or mod_tag == 'Q':
            # -SPR (secondary predicate)
            return 'amod'
        elif mod_tag == 'PP':
            # -BY, -PRN
            return 'obl'        #NP sem er haus PP fær obl nominal
        elif mod_tag == 'P':
            return 'case'
        elif mod_tag == 'ADVP' or mod_tag == 'NEG':
            # -DIR, -LOC, -TP
            return 'advmod'
        elif mod_tag[0:2] == 'VB' and head_tag == 'CP':
            return 'ccomp'
        elif mod_tag in ['VAN', 'DAN', 'HAN']:
            return 'aux:pass'
        elif mod_tag in ['VBN', 'DON', 'HVN', 'RDN']:
            return 'auxpass'
        elif mod_tag[0:2] in ['VB', 'DO', 'HV', 'RD', 'MD']: #todo
            return 'aux'
        elif mod_tag[0:2] == 'BE' or mod_tag == 'BAN':  #copular
            return 'cop'
        elif mod_tag == 'RP' or mod_tag == 'FP': #todo, adverbial particles
            return 'amod'
        elif mod_tag == 'CONJ':
            return 'cc'
        elif mod_tag == 'CONJP':
            return 'conj'
        elif mod_tag == 'C' or mod_tag == 'CP' or mod_tag == 'TO':  #infinitival marker with marker relation
            return 'mark'
        elif mod_tag == 'ES':
            return 'expl'
        elif mod_tag == 'NUM':
            return 'nummod'
        elif mod_tag in string.punctuation:
            return 'punct'
        elif mod_tag in ['FW', 'X', 'LATIN']:    #meira?
            return '_'
        elif mod_tag == 'INTJ':
            return 'discourse'

        return 'rel-'+mod_tag

    def create_dependency_graph(self, tree):
        """Create a dependency graph from a phrase structure tree."""
        const = []
        tag_list = {}
        nr = 1
        # Tree item read in as string and transferred to UD graph instance
        t = depender.IndexedTree.fromstring(tree)
        self.dg = depender.UniversalDependencyGraph()

        for i in t.treepositions():
            if isinstance(t[i], Tree):
                if len(t[i]) == 1:
                    # If terminal node with label
                    # e.g. (VBDI tók-taka) or (NP-SBJ (PRO-N hann-hann))
                    tag_list[nr] = t[i].label()
                    t[i].set_id(nr)
                    # print(t[i])
                else:
                    # If constituent / complex phrase
                    # e.g. (ADVP (ADV smám-smám) (ADV saman-saman))
                    t[i].set_id(0)
                    const.append(i)
            else:
                # If terminal node with no label (token-lemma)
                # e.g. tók-taka
                if '-' in t[i]:
                    FORM, LEMMA = t[i].split('-', 1)
                    tag = tag_list[nr]
                    # print(tag_list)
                # If <dash/>, <dash> or </dash>
                elif t[i][0] in {'<dash/>', '<dash>', '</dash>'}:
                    FORM = LEMMA = '-'
                    # token_lemma = str(FORM+'-'+LEMMA)
                    tag = tag_list[nr]
                    # leaf = token_lemma, tag
                else: # If no lemma present
                    FORM = t[i][0]
                    # DMII_combined = DMII_data.DMII_data('combined')
                    LEMMA = '_'# DMII_data.get_lemma(DMII_combined, FORM)
                    if LEMMA == None:
                        LEMMA = '_'
                    # token_lemma = str(FORM+'-'+LEMMA)
                    tag = tag_list[nr]
                    # leaf = token_lemma, tag
                token_lemma = str(FORM+'-'+LEMMA)
                leaf = token_lemma, tag
                # UPOS = '_'
                UPOS = features.get_UD_tag(tag, LEMMA)
                XPOS = tag
                # print(FORM, UPOS, XPOS)
                FEATS = '_'
                FEATS = features.get_feats(leaf)
                self.dg.add_node({'address': nr,
                                  'word': FORM,
                                  'lemma': LEMMA,
                                  'ctag': UPOS, # upostag
                                  'tag': XPOS,   # xpostag
                                  'feats': FEATS,
                                  'deps': defaultdict(list),
                                  'rel': None})
                nr += 1

        # go through the constituencies (bottom up) and find their heads
        const.sort(key=lambda x: len(x), reverse=True)

        for i in const:
            self._select_head(t[i])

        for i in const:
            head_tag = t[i].label()
            head_nr = t[i].id()
            for child in t[i]:
                mod_tag = child.label()
                mod_nr = child.id()
                if head_nr == mod_nr and re.match( "IP-.+|QTP|CP-.+|FRAG", head_tag):  #todo root phrase types from config
                    self.dg.get_by_address(mod_nr).update({'head': 0, 'rel': 'root'})  #todo copula not a head
                    self.dg.root = self.dg.get_by_address(mod_nr)
                else:
                    self.dg.get_by_address(mod_nr).update({'head': head_nr, 'rel': self._relation(mod_tag, head_tag)})
                if head_nr != mod_nr:
                    self.dg.add_arc(head_nr, mod_nr)

        #todo coordination, http://www.linguist.is/icelandic_treebank/Conjunction

        #todo gaps, http://www.linguist.is/icelandic_treebank/Empty_categories

        #todo ...

        return self.dg

if __name__ == '__main__':
    #fileids = icepahc.fileids() # leave uncommented for whole corpus use
    fileids = ['2008.ofsi.nar-sag.psd'] # For debug use only
    c = Converter() # Creates instance of Converter class
    total_sents = 0

    ''' Prints the dependency graph data in conllU format '''
    for fileid in fileids:
        error_num = 0
        start = time.time()
        file_sents = 0
        print('\nProcessing file: {0}...'.format(fileid))
        for tree in icepahc.parsed_sents(fileid):
            treeID = fileid + '_' + str(file_sents+1) + '_' + str(total_sents+1)
            try:
                dep = c.create_dependency_graph(str(tree))
                dep_c = dep.to_conllU()
                #print(dep_c)
                print('# sent_id =', treeID)
                print(dep.to_conllU())
            except:
                error_num += 1
            file_sents += 1
            total_sents += 1
        end = time.time()
        duration = '%.2f' % float(end - start)
        print('Finished! Time elapsed: {0} seconds'.format(duration))
        print('Number of sentences in file: {0}'.format(file_sents))
        print('Number of failed sentences: {0}'.format(error_num))
