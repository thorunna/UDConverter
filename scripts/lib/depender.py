
'''
depender.py
Hinrik Hafsteinsson (hih43@hi.is)
Þórunn Arnardóttir (tha86@hi.is)
2019
Based on earlier work by
Örvar Kárason (ohk2@hi.is)
'''

from nltk.tree import Tree
from nltk.parse import DependencyGraph
from sys import argv, stdin, stdout
import getopt
from lib import features
from collections import defaultdict
import re
import string

class UniversalDependencyGraph(DependencyGraph):
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

    def __init__(self, tree_str=None, cell_extractor=None, zero_based=False, cell_separator=None, top_relation_label='root'):
        DependencyGraph.__init__(self,tree_str, cell_extractor, zero_based, cell_separator, top_relation_label)

        self.nodes = defaultdict(lambda:  {'address': None,
                                   'word': None,
                                   'lemma': None,
                                   'ctag': None,    # upostag
                                   'tag': None,     # xpostag
                                   'feats': None,
                                   'head': None,
                                   'deps': defaultdict(list),
                                   'rel': None,
                                   })
        self.nodes[0].update(
            {
                'ctag': 'TOP',
                'tag': 'TOP',
                'ID': 0,
            }
        )
    #todo _parse for CoNLL-U

    def _deps_str(self, deps_dict):
        #todo, format should be "4:nsubj|11:nsubj", see http://universaldependencies.github.io/docs/format.html
        return '_' #return ''.join('%s:%s,' % (dep, '+'.join(str(rel))) for (dep, rel) in deps_dict.items())[0:-1]

    def to_conllU(self):
        """
        The dependency graph in CoNLL-U (Universal) format.

        Consist of one or more word lines, and word lines contain the following fields:

        ID: Word index, integer starting at 1 for each new sentence; may be a range for tokens with multiple words.
        FORM: Word form or punctuation symbol.
        LEMMA: Lemma or stem of word form.
        UPOSTAG: Universal part-of-speech tag drawn from our revised version of the Google universal POS tags.
        XPOSTAG: Language-specific part-of-speech tag; underscore if not available.
        FEATS: List of morphological features from the universal feature inventory or from a defined language-specific extension; underscore if not available.
        HEAD: Head of the current token, which is either a value of ID or zero (0).
        DEPREL: Universal Stanford dependency relation to the HEAD (root iff HEAD = 0) or a defined language-specific subtype of one.
        DEPS: List of secondary dependencies (head-deprel pairs).
        MISC: Any other annotation.

        :rtype: str
        """

        template = '{i}\t{word}\t{lemma}\t{ctag}\t{tag}\t{feats}\t{head}\t{rel}\t{deps_str}\t_\n'

        return ''.join(template.format(i=i, **node, deps_str=self._deps_str(node['deps']))
                         for i, node in sorted(self.nodes.items()) if node['tag'] != 'TOP') \
               + '\n'

        def plain_text(self):
            '''
            '''
            text = []
            for leaf in leaves:
                leaf = leaf.split('-')
                if leaf[0][0] in {'*', '0'}: continue
                text.append(leaf[0])
            text = '# text = ' + ' '.join(text)
            return text


class IndexedTree(Tree):

    def __init__(self, node, children=None):
        Tree.__init__(self, node, children)
        self._id = 0

    def id(self):
        """
        Returns the (leaf) index of the tree or leaf
        :return: (leaf) index of tree or leaf
        """
        return self._id

    def set_id(self, id):
        """
        Sets the (leaf) index of the tree or leaf
        """
        self._id = int(id)

    def phrases(self):
        """
        Return the "constituencies" of the tree.

        :return: a list containing this tree's "constituencies" in-order.
        :rtype: list
        """
        phrases = []
        for child in self:
            if isinstance(child, Tree):
                if len(child) > 1:
                    phrases.append(child)
                phrases.extend(child.phrases())
        return phrases



class Converter():
    def __init__(self):
        #todo read rules from config file
        self.t = None
        self.dg = None
        self.head_rules = {
            'IP-INF'        : {'dir':'r', 'rules':['VB', 'DO']},
            'IP-INF-1'      : {'dir':'r', 'rules':['VB']},
            'IP-INF=3'      : {'dir':'r', 'rules':['VB']},
            'IP-INF-PRP'    : {'dir':'r', 'rules':['VB']},      #tilgangsnafnháttur
            'IP-INF-PRP-PRN': {'dir':'r', 'rules':['VB']},
            'IP-INF-SPE'    : {'dir':'r', 'rules':['VB']},      #spe = direct speech
            'IP-INF-PRN'    : {'dir':'r', 'rules':['VB']},
#            'IP-INF-PRN-ELAB'
#            'IP-INF-PRN-ELAB=2'
            'IP-INF-SBJ'    : {'dir':'r', 'rules':['VB']},
            'IP-INF-DEG'    : {'dir':'r', 'rules':['VB']},  #degree infinitive
            'IP-INF-ADT'    : {'dir':'r', 'rules':['VB']},
            'IP-INF-ADT-SPE': {'dir':'r', 'rules':['VB']},
            'IP-MAT'        : {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'NP-1', 'ADJP', 'VAN', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT-1']},
            'IP-MAT-1'      : {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'NP-1', 'VAN', 'NP-PRD', 'ADJP', 'N.*', 'IP-SMC', 'IP-MAT-1']},
            'IP-MAT=1'      : {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'NP-1', 'ADJP', 'VAN', 'NP-PRD', 'N.*', 'IP-SMC']}, 
            'IP-MAT-PRN'    : {'dir':'r', 'rules':['VB.*']},
            'IP-MAT-SPE'    : {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'NP-1', 'ADJP', 'VAN', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT-1']},
#            'IP-SUB'        : {'dir':'r', 'rules':['IP-INF.*', 'VB', 'VB.*', 'DO.*', 'DAN', 'NP-PRD', 'RD.*', 'ADVP', 'ADJP', 'IP-SUB', 'NP-PRD']},    #meira?
            'IP-SUB'        : {'dir':'r', 'rules':['ADJP', 'IP-INF.*', 'VB', 'VB.*', 'DO.*', 'DAN', 'NP-PRD', 'RD.*', 'ADVP', 'IP-SUB', 'NP-2', 'HVN']},
            'IP-SUB-4'      : {'dir':'r', 'rules':['ADJP', 'IP-INF.*', 'VB', 'VB.*', 'DO.*', 'DAN', 'VAN', 'NP-PRD', 'RD.*', 'ADVP', 'IP-SUB', 'NP-2', 'HVN']},
            'IP-SUB-PRN'    : {'dir':'r', 'rules':['VB.*']},
            'IP-SUB-PRN=4'  : {'dir':'r', 'rules':['VB.*', 'VAN']},
            'IP-SUB-SPE'    : {'dir':'r', 'rules':['VB.*']},
            'IP-IMP'        : {'dir':'r', 'rules':['VB.']},    #imperative
            'IP-IMP-SPE'    : {'dir':'r', 'rules':['VB.']},
            'IP-SMC'        : {'dir':'r', 'rules':['IP-INF-SBJ', 'ADJP', 'NP.*', 'NP-PRD']},    #small clause
            'IP-PPL'        : {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG']},  #lýsingarháttarsetning
            'CP-THT'        : {'dir':'r', 'rules':['IP-SUB.*','.*']},   #að
            'CP-THT-1'      : {'dir':'r', 'rules':['IP-SUB.*','.*']},
            'CP-THT-SBJ'    : {'dir':'r', 'rules':['IP-SUB.*','.*']},   #extraposed subject
            'CP-THT-PRN'    : {'dir':'r', 'rules':['IP-SUB.*','.*']},
            'CP-THT-PRN-1'  : {'dir':'r', 'rules':['IP-SUB.*','.*']},
            'CP-THT-PRN-2'  : {'dir':'r', 'rules':['IP-SUB.*','.*']},
            'CP-CAR'        : {'dir':'r', 'rules':['IP-SUB.*']},    #clause-adjoined relatives
            'CP-CLF'        : {'dir':'r', 'rules':['IP-SUB.*']},    #it-cleft
            'CP-CMP'        : {'dir':'r', 'rules':['IP-SUB.*']},    #comparative clause
            'CP-DEG'        : {'dir':'r', 'rules':['IP-SUB.*']},  #degree complements
            'CP-DEG-1'      : {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-DEG-2'      : {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-FRL'        : {'dir':'r', 'rules':['IP-SUB.*']},  #free relative
            'CP-REL'        : {'dir':'r', 'rules':['IP-SUB.*']},    #relative
            'CP-REL-1'      : {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-QUE'        : {'dir':'r', 'rules':['IP-SUB.*']},    #question
            'CP-QUE-1'      : {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-QUE-SPE'    : {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-QUE-ADV'    : {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-ADV'        : {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-EOP'        : {'dir':'r', 'rules':['IP-INF']},  #empty operator
            'CP-EOP-1'      : {'dir':'r', 'rules':['IP-INF']},
            'CP-EOP-2'      : {'dir':'r', 'rules':['IP-INF']},
            'CP-TMC'        : {'dir':'r', 'rules':['IP-INF']},  #tough-movement
            'CP-TMC-3'      : {'dir':'r', 'rules':['IP-INF']},
            'NP'            : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NP.*', 'PRO-.', 'Q.*', 'MAN-.', 'OTHER-.']},
            'NP-1'          : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NP.*', 'PRO-.', 'Q.*', 'MAN-.', 'OTHER-.']},
            'NP-2'          : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NP.*', 'PRO-.', 'Q.*', 'MAN-.', 'OTHER-.']},
            'NP-4'          : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NP.*', 'PRO-.', 'Q.*', 'MAN-.', 'OTHER-.']},
            'NP-ADV'        : {'dir':'r', 'rules':['NP.*']},
            'NP-CMP'        : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'MAN-.', 'OTHER-.']},
            'NP-PRN'        : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'PRO-.', 'MAN-.', 'OTHER-.']},   #viðurlag, appositive
            'NP-PRN-3'      : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'PRO-.', 'MAN-.', 'OTHER-.']},
            'NP-SBJ'        : {'dir':'r', 'rules':['N-N', 'NS-N', 'NPR-N', 'PRO-.', 'ADJ-N', 'MAN-N', 'OTHER-.']},
            'NP-SBJ-1'      : {'dir':'r', 'rules':['N-N', 'NS-N', 'NPR-N', 'PRO-.', 'ADJ-N', 'MAN-N', 'OTHER-.']},
            'NP-SBJ-2'      : {'dir':'r', 'rules':['N-N', 'NS-N', 'NPR-N', 'PRO-.', 'ADJ-N', 'MAN-N', 'OTHER-.']},
            'NP-SBJ-4'      : {'dir':'r', 'rules':['N-N', 'NS-N', 'NPR-N', 'PRO-.', 'ADJ-N', 'MAN-N', 'OTHER-.']},
            'NP-OB1'        : {'dir':'r', 'rules':['N-.', 'NPR-A', 'NS-.', 'ONE+Q-A', 'MAN-A', 'OTHER-.', 'PRO-.']},
            'NP-OB2'        : {'dir':'r', 'rules':['NP.*', 'PRO-.', 'N-D', 'NS-D', 'NPR-.', 'CP-FRL', 'MAN-.', 'OTHER-.']},    #MEIRA?
            'NP-OB3'        : {'dir':'r', 'rules':['PRO-D', 'N-D', 'NS-D', 'NPR-D', 'MAN-.', 'OTHER-.']},
            'NP-PRD'        : {'dir':'r', 'rules':['N-.', 'NS.*', 'NP.*', 'OTHER-.']},     #sagnfylling copulu
            'NP-SPR'        : {'dir':'r', 'rules':['N-.', 'NS-.']},   #secondary predicate
            'NP-POS'        : {'dir':'r', 'rules':['N.*', 'PRO-.', 'MAN-.', 'OTHER-.']},
            'NP-COM'        : {'dir':'r', 'rules':['N.*', 'NP.*', 'OTHER-.']},  #fylliliður N sem er ekki í ef.
            'NP-ADT'        : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'MAN-.', 'OTHER-.']},    #instrumental NP
            'NP-TMP'        : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'ADJ-.', 'NUM-.', 'OTHER-.']},    #temporal NP
            'NP-MSR'        : {'dir':'r', 'rules':['NS-.', 'N-.', 'Q-.', 'QS-.', 'QR-.', 'OTHER-.', 'ADV']},
            'NP-VOC'        : {'dir':'r', 'rules':['N-N', 'NS-N', 'MAN-N', 'OTHER-.']},
            'ADJP'          : {'dir':'r', 'rules':['ADJ.*', 'ADJR.*', 'ADJS.*', 'ADVR', 'ONE', 'ONES']},
            'ADJP-1'        : {'dir':'r', 'rules':['ADJ.*', 'ADJR.*', 'ADJS.*', 'ADVR', 'ONE', 'ONES']},
            'ADJP-SPR'      : {'dir':'r', 'rules':['ADJ-.', 'ADJS-N']},
            'PP'            : {'dir':'r', 'rules':['NP.*', 'CP-ADV', 'ADVP', 'ADJP', 'CP-.*', 'P']},
            'PP-1'          : {'dir':'r', 'rules':['NP.*', 'CP-ADV', 'ADVP', 'ADJP', 'P']},
            'PP-2'          : {'dir':'r', 'rules':['NP.*', 'CP-ADV', 'ADVP', 'ADJP', 'P']},
            'PP-BY'         : {'dir':'r', 'rules':['P']},
            'PP-PRN'        : {'dir':'r', 'rules':['CP-ADV', 'P']},
            'PP-LFD'        : {'dir':'r', 'rules':['CP-ADV']},
            'ADVP'          : {'dir':'r', 'rules':['ADV', 'WADV']},
            'ADVP-DIR'      : {'dir':'r', 'rules':['ADV', 'WADV']},
            'ADVP-LOC'      : {'dir':'r', 'rules':['ADV', 'WADV']},
            'ADVP-TMP'      : {'dir':'r', 'rules':['ADV', 'WADV']},
            'ADVP-RSP'      : {'dir':'r', 'rules':['ADV', 'WADV']},
            'ADVP-TMP-RSP'  : {'dir':'r', 'rules':['ADV', 'WADV']},
            'WADVP'         : {'dir':'r', 'rules':['WADV']},
            'WADVP-1'       : {'dir':'r', 'rules':['WADV']},
            'WADVP-2'       : {'dir':'r', 'rules':['WADV']},
            'WADVP-3'       : {'dir':'r', 'rules':['WADV']},
            'CONJP'         : {'dir':'l', 'rules':['NP.*', 'NX' 'CONJ']},
            'WNP'           : {'dir':'r', 'rules':['WPRO-.', 'PRO-.']}, #MEIRA?
            'WNP-1'         : {'dir':'r', 'rules':['WPRO-.', 'PRO-.']},
            'WNP-2'         : {'dir':'r', 'rules':['WPRO-.', 'PRO-.']},
            'WNP-3'         : {'dir':'r', 'rules':['WPRO-.', 'PRO-.']},
            'WNP-4'         : {'dir':'r', 'rules':['WPRO-.', 'PRO-.']},
            'WPP'           : {'dir':'r', 'rules':['WNP', 'NP']},
            'NX'            : {'dir':'r', 'rules':['N-.']},
            'FRAG-LFD'      : {'dir':'r', 'rules':['IP-SMC']},
            'FRAG'          : {'dir':'r', 'rules':['NP']},
            'QP'            : {'dir':'r', 'rules':['Q-.', 'QS-.', 'QR-.']}
            }

    def _select_head(self, tree):
        '''

        '''
        tag_orig = str(tree.label())
        tag = re.sub('-\d\+', '', tag_orig)     #TODO: virkar ekki
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
        if mod_func in {'0', '1', '2', '3', '4', '5', '6'}:     #TODO: virkar ekki
            mod_func = None
#        elif '-' in mod_func:
#            mod_func, mod_3 = mod_func.split('-', 1)
#            if mod_3 in {'0', '1', '2', '3', '4', '5', '6'}:
#                mod_3 = None
#        else:
#            mod_3 = None

        if '-' in head_tag:
            head_tag, head_func = head_tag.split('-', 1)
        else:
            head_func = None

#        if mod_tag == 'NP' and mod_func == 'SBJ-1':
#            return 'expl'
        if head_tag == 'NP' and head_func == 'SBJ-1':       #TODO: finna aðra lausn til að merkja expl
            return 'expl'
        elif mod_tag == 'NP':   #TODO: hvað ef mod_tag er bara NP?
            # -ADV, -CMP, -PRN, -SBJ, -OB1, -OB2, -OB3, -PRD, -POS, -COM, -ADT, -TMP, -MSR
            return {
                'SBJ': 'nsubj',
                'SBJ-1' : 'nsubj:pass?',
                'SBJ-2' : 'nsubj:pass?',
                'SBJ-4' : 'nsubj:pass?',
                'OB1': 'obj',
                'OB2': 'iobj',
                'OB3': 'iobj',
                'POS': 'nmod:poss',      #Örvar: 'POS': 'case'
                'VOC': 'vocative',
                'PRD': 'acl?',    #sagnfylling, predicate
                'SPR': 'xcomp?',
                'PRN': 'appos',
                'PRN-3': 'appos',
                'COM': 'nmod',
                'ADT': 'obl',    #ATH. rétt?
                'TMP': 'advmod',  #ATH. rétt?
                '1'  : '?',
                '2': '?',
                '4': '?',
                'MSR': 'amod',   #measure phrase
                'ADV': '?'
            }.get(mod_func, 'rel')
#        elif mod_tag == 'N' and head_tag == 'NP':
#            return 'conj'
        elif mod_tag == 'NS' or mod_tag == 'N' and head_tag == 'NP':    #seinna no. í nafnlið fær 'conj' og er háð fyrra no.
            return 'conj'
        elif mod_tag == 'NPR' and head_tag == 'NP':
            return 'flat:name'
#        elif mod_tag == 'PRO' and head_tag == 'NP' and head_func == 'PRN':  #TODO: skoða betur, hliðstæð NPR sem eru bæði dobj?
#            return 'obj'
        elif mod_tag == 'D' or mod_tag == 'ONE' or mod_tag == 'ONES' or mod_tag == 'OTHER' or mod_tag == 'OTHERS' or mod_tag == 'SUCH':
            return 'det'
        elif mod_tag == 'ADJP' or mod_tag == 'ADJ' or mod_tag == 'Q' or mod_tag == 'QR' or mod_tag == 'QS':
            # -SPR (secondary predicate)
            return 'amod'
        elif mod_tag == 'PP':
            # -BY, -PRN
            return 'obl'        #NP sem er haus PP fær obl nominal  #TODO: haus CP-ADV (sem er PP) á að vera merktur advcl
        elif mod_tag == 'P':
            return 'case'
        elif mod_tag == 'ADVP' or mod_tag == 'ADV' or mod_tag == 'ADVR' or mod_tag == 'ADVS' or mod_tag == 'NEG' or mod_tag == 'FP' or mod_tag == 'QP' or mod_tag == 'ALSO':    #FP = focus particles  #QP = quantifier phrase - ATH.
            # -DIR, -LOC, -TP
            return 'advmod'
        elif mod_tag == 'RP':
            return 'compound:prt'
        elif mod_tag == 'IP':
            return {
                'INF': 'ccomp', #?
                'INF-1': '',
                'INF-PRP': 'advcl',
                'INF-PRP-PRN': '',
                'INF-PRN': 'xcomp', #ADVCL?
                'INF-SPE': 'xcomp',  #ATH. réttur merkimiði?
                'PPL': 'advcl',  #?
                'SUB-PRN=4': 'aux:pass'     #sérstakt dæmi
            }.get(mod_func, 'rel')
        elif mod_tag[0:2] == 'VB' and head_tag == 'CP':
            return 'ccomp'
        elif mod_tag in ['VAN', 'DAN', 'HAN']:
            return 'aux:pass'
        elif mod_tag in ['VBN', 'DON', 'HVN', 'RDN']:   #ath. VBN getur verið rót
            return '?'
        elif mod_tag[0:2] in ['VB', 'DO', 'HV', 'RD', 'MD']: #todo
            return 'aux'
        elif mod_tag[0:2] == 'BE' or mod_tag == 'BAN':  #copular, TODO: ekki alltaf copular
            return 'cop'
        elif mod_tag == 'CONJ':
            return 'cc'
        elif mod_tag == 'CONJP' or mod_tag == 'N':      #N: tvö N í einum NP tengd með CONJ
            return 'conj'
#        elif mod_tag == 'CP' and mod_func == 'ADV':
#            return 'VIRKAR'
        elif mod_tag == 'CP':
            return {
                'THT': 'ccomp',
                'THT-1': 'ccomp',
                'THT-PRN': 'ccomp',
                'THT-PRN-1': 'ccomp',
                'ADV': 'advcl',
                'REL': 'acl:relcl',
                'CAR': 'acl:relcl',
                'CLF': 'acl:relcl',
                'CMP': 'advcl',      #ATH. rétt?
                'DEG': 'ccomp',      #ATH. rétt?
                'FRL': 'ccomp',      #ATH. rétt?
                'QUE': 'ccomp'
            }.get(mod_func, 'rel')
#        elif mod_func == 'THT':     #TODO: too greedy
#            return 'ccomp'
        elif mod_tag == 'C' or mod_tag == 'CP' or mod_tag == 'TO' or mod_tag == 'WQ':  #infinitival marker with marker relation
            return 'mark'
        elif mod_tag == 'NUM':
            return 'nummod'
        elif mod_tag == 'FRAG':
            return 'xcomp'
        elif mod_tag in string.punctuation:
            return 'punct'
        elif mod_tag in ['FW', 'X', 'LATIN']:    #meira?
            return '_'
        elif mod_tag == 'INTJ' or mod_tag == 'INTJP':
            return 'discourse'

        return 'rel-'+mod_tag

    def create_dependency_graph(self, tree):
        """Create a dependency graph from a phrase structure tree."""
        const = []
        tag_list = {}
        nr = 1
        # Tree item read in as string and transferred to UD graph instance
        t = IndexedTree.fromstring(tree)
        self.dg = UniversalDependencyGraph()

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
                # If trace node, skip (preliminary, may result in errors)
                # e.g. *T*-3 etc.
                if t[i][0] in {'0', '*'}:
                    continue
                # If terminal node with no label (token-lemma)
                # e.g. tók-taka
                elif '-' in t[i]:
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
                if '+' in tag:
                    tag = re.sub('\w+\+', '', tag)
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
#                if head_nr == mod_nr and re.match("NP-PRD", head_tag):      #ath. virkar þetta rétt? Leið til að láta sagnfyllingu cop vera rót
#                    self.dg.get_by_address(mod_nr).update({'head': 0, 'rel': 'root'})
#                    self.dg.root = self.dg.get_by_address(mod_nr)
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


"""
Example usage of the Converter class:

psd = "( (IP-MAT (NP-SBJ (N-N Himinn$-himinni) (D-N $inn-hinn)) (BEDI var-vera) (ADJP (ADV alveg-alveg) \
       (ADJ-N blár-blár)) (. .-.)) (ID 2008.MAMMA.NAR-FIC,.9))"

c = Converter()
dep = c.toDep(psd)
print(dep.to_conllU())
tree = dep.tree()
tree.draw()
"""

def main(argv):
    c = Converter()
    psd = ''
    infilename = outfilename = None

    opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])

    for opt, arg in opts:
        if opt == '-h':
            print('converter.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            infilename = arg
        elif opt in ("-o", "--ofile"):
            outfilename = arg

    with open(infilename) if infilename else stdin as infile, \
         open(outfilename, 'w') if outfilename else stdout as outfile:
        for line in infile:
            psd += line
            if len(line.strip()) == 0 and len(psd.strip()) > 0:
                dep = c.create_dependency_graph(psd)
                outfile.write(dep.to_conllU())
                psd = ''
                cnt = 0

        dep = c.create_dependency_graph(psd)
        outfile.write(dep.to_conllU())

if __name__ == "__main__":
    main(argv[1:])
