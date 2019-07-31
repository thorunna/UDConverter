
'''
depender.py
Hinrik Hafsteinsson (hih43@hi.is)
Þórunn Arnardóttir (tha86@hi.is)
2019
Based on earlier work by
Örvar Kárason (ohk2@hi.is)
Part of UniTree project for IcePaHC
'''

#from lib import features as f
from lib import DMII_data
from lib.rules import head_rules, relation_NP, relation_IP, relation_CP

from nltk.tree import Tree
from nltk.parse import DependencyGraph
from sys import argv, stdin, stdout
import getopt
from collections import defaultdict
import re
import string

# DMII_combined = DMII_data.DMII_data('combined') # TODO: Move to features script

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

    def _select_head(self, tree):
        '''

        '''
        tag_orig = str(tree.label())
        tag = re.sub('-\d+', '', tag_orig)
        head_rule = head_rules.get(tag, {'dir':'r', 'rules':['.*']})  #default rule, first from left
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
        mod_tag = re.sub('-TTT', '', mod_tag)
        mod_tag = re.sub('-\d+', '', mod_tag)
        mod_tag = re.sub('=\d+|=XXX|=X', '', mod_tag)

        head_tag = re.sub('-TTT', '', head_tag)
        head_tag = re.sub('-\d+', '', head_tag)
        head_tag = re.sub('=\d+|=XXX|=X', '', head_tag)

        if '+' in mod_tag:
            mod_tag = re.sub('\w+\+', '', mod_tag)
        if '+' in head_tag:
            head_tag = re.sub('\w+\+', '', head_tag)

        #todo use head_tag and more info about the constituency to better select the relation label

        if '-' in mod_tag:
            mod_tag, mod_func = mod_tag.split('-', 1) #todo, handle more than one function label
#            if mod_tag == 'CP' and '-' in mod_func:
#                mod_func, mod_extra = mod_func.split('-', 1) 
        else:
            mod_func = None
#        if mod_func == r'[0123456]':     #TODO: virkar ekki, in {'0', '1', '2', '3', '4', '5', '6'}:
#            mod_func = None
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

#        if mod_func:        
#            if '-' in mod_func:
#                mod_func, mod_extra = mod_func.split('-', 1)    

#        if head_func:        
#            if '-' in head_func:
#                head_func, head_extra = head_func.split('-', 1)
        
#        if head_tag == 'NP' and head_func == 'SBJ-1':       #TODO: finna aðra lausn til að merkja expl
#            return 'expl'
#        elif mod_tag == 'NS':
#            return 'HALLO'
#        if mod_tag == 'NP' and mod_func == None:
#            return 'NP???'
        if mod_tag in ['NP', 'NX', 'WNX']:   #TODO: hvað ef mod_tag er bara NP?
            # -ADV, -CMP, -PRN, -SBJ, -OB1, -OB2, -OB3, -PRD, -POS, -COM, -ADT, -TMP, -MSR
            return relation_NP.get(mod_func, 'rel-'+mod_tag)
        elif mod_tag == 'WNP':
            return 'obj'
        elif mod_tag in ['NS', 'N', 'NPRS'] and head_tag in ['NP', 'NX', 'QTP', 'ADJP', 'CONJP', 'NPR']:    #seinna no. í nafnlið fær 'conj' og er háð fyrra no.
            return 'conj'
        elif mod_tag == 'NPR' and head_tag == 'CONJP':
            return 'conj'
        elif mod_tag == 'NPR' and head_tag in ['NP', 'NX', 'QTP']:
            return 'flat:name'
        elif mod_tag == 'ES':
            return 'expl'   #expletive
        elif mod_tag in ['PRO', 'WPRO']:
            return 'nmod?'
#        elif mod_tag == 'PRO' and head_tag == 'NP' and head_func == 'PRN':  #TODO: skoða betur, hliðstæð NPR sem eru bæði dobj?
#            return 'obj'
        elif mod_tag in ['D', 'WD', 'ONE', 'ONES', 'OTHER', 'OTHERS', 'SUCH']:
            return 'det'
        elif mod_tag[:3] == 'ADJ' or mod_tag[:4] == 'WADJ' or mod_tag in ['Q', 'QR', 'QS', 'WQP']:
            # -SPR (secondary predicate)
            return 'amod'
        elif mod_tag in ['PP', 'WPP', 'PX']:
            # -BY, -PRN
            return 'obl'        #NP sem er haus PP fær obl nominal  #TODO: haus CP-ADV (sem er PP) á að vera merktur advcl
        elif mod_tag == 'P':
            return 'case'
        elif mod_tag[:3] == 'ADV' or mod_tag in ['NEG', 'FP', 'QP', 'ALSO', 'WADV', 'WADVP']:    #FP = focus particles  #QP = quantifier phrase - ATH.
            # -DIR, -LOC, -TP
            return 'advmod'
        elif mod_tag == 'NS' and head_tag == 'ADVP' and head_func == 'TMP':     #ath. virkar fyrir eitt dæmi, of greedy?
            return 'conj'
        elif mod_tag in ['RP', 'RPX']:
            return 'compound:prt'
        elif mod_tag == 'IP' and mod_func == 'SUB' and head_tag == 'CP' and head_func == 'FRL':
            return 'acl:relcl'
        elif mod_tag in ['IP', 'VP']:
            return relation_IP.get(mod_func, 'rel-'+mod_tag)
        elif mod_tag[:2] == 'VB' and head_tag == 'CP':
            return 'ccomp'
        elif mod_tag in ['VAN', 'DAN', 'HAN', 'BAN']:
            return 'aux:pass'
        elif mod_tag in ['VBN', 'DON', 'HVN', 'RDN']:   #ath. VBN getur verið rót
            return '?'
        elif mod_tag[:2] in ['VB', 'DO', 'HV', 'RD', 'MD']: #todo
            return 'aux'
        elif mod_tag[:2] == 'BE' or mod_tag == 'BAN':  #copular, TODO: ekki alltaf copular
            return 'cop'
        elif mod_tag == 'VAG':
            return 'amod?'
        elif mod_tag == 'RRC':
            return 'acl:relcl?'
        elif mod_tag == 'CONJ':
            return 'cc'
        elif mod_tag in ['CONJP', 'N'] and head_tag in ['NP', 'N', 'PP']:      #N: tvö N í einum NP tengd með CONJ
            return 'conj'
        elif mod_tag == 'CONJP' and head_tag == 'IP':
            return relation_IP.get(head_func, 'rel-'+mod_tag+head_tag+head_func)
        elif mod_tag == 'CONJP':
            return 'conj'
        elif mod_tag == 'CP':
            return relation_CP.get(mod_func, 'rel-'+mod_tag)
        elif mod_tag in ['C', 'CP', 'TO', 'WQ']:  #infinitival marker with marker relation
            return 'mark'
        elif mod_tag in ['NUM', 'NUMP']:
            return 'nummod'
        elif mod_tag == 'FRAG':
            return 'xcomp'
        elif mod_tag in string.punctuation or mod_tag == 'LB':
            return 'punct'
        elif mod_tag in ['FW', 'X', 'LATIN']:    #meira?
            return '_'
        elif mod_tag in ['INTJ', 'INTJP'] or head_tag == 'INTJP':
            return 'discourse'
        elif mod_tag in ['XXX', 'XP', 'FOREIGN', 'FW', 'QTP', 'REP', 'FS', 'LS', 'META', 'REF', 'ENGLISH']:      #XXX = annotator unsure of parse, LS = list marker
            return 'dep'    #unspecified dependency
        elif head_tag in ['META', 'CODE', 'REF', 'FRAG']:
            return 'dep'

        return 'rel-'+mod_tag+'+'+head_tag

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
                if t[i][0] in {'0', '*', '{'}:   #if t[1].pos()[0][0] in {'0', '*'}:
                    continue
                # If terminal node with no label (token-lemma)
                # e.g. tók-taka
                if '-' in t[i]:
                    FORM, LEMMA = t[i].split('-', 1)
                    tag = tag_list[nr]
                # If <dash/>, <dash> or </dash>
                elif t[i][0] in {'<dash/>', '<dash>', '</dash>'}:
                    FORM = LEMMA = '-'
                    tag = tag_list[nr]
                else: # If no lemma present
                    FORM = t[i][0]
                    #DMII_combined = f.DMII_data('combined')
                    # print(FORM)
                    # LEMMA = DMII_data.get_lemma(DMII_combined, FORM)    # LEMMA = '_'
                    LEMMA = DMII_data.get_lemma(FORM)
                    if LEMMA == None:
                        LEMMA = '_'
                    token_lemma = str(FORM+'-'+LEMMA)
                    tag = tag_list[nr]
                if '+' in tag:
                    tag = re.sub('\w+\+', '', tag)
                token_lemma = str(FORM+'-'+LEMMA)
                leaf = token_lemma, tag
                XPOS = tag
                # Feature Classes called here
                #leaf = f.Word(leaf).getinfo()
                #UPOS = leaf.UD_tag
                #FEATS = leaf.features.featString()
                self.dg.add_node({'address': nr,
                                  'word': FORM,
                                  'lemma': LEMMA,
                                  #'ctag': UPOS, # upostag
                                  'ctag': None, # upostag
                                  'tag': XPOS,   # xpostag
                                  #'feats': FEATS,
                                  'feats': None,
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
            if re.search(r'\w{1,5}(21|22|31|32|33)', head_tag):
                head_tag = re.sub('(21|22|31|32|33)', '', head_tag)
            for child in t[i]:
                mod_tag = child.label()
                if re.search(r'\w{1,5}(21|22|31|32|33)', mod_tag):
                    mod_tag = re.sub('(21|22|31|32|33)', '', mod_tag)
                mod_nr = child.id()
#                if head_nr == mod_nr and re.match("NP-PRD", head_tag):      #ath. virkar þetta rétt? Leið til að láta sagnfyllingu cop vera rót
#                    self.dg.get_by_address(mod_nr).update({'head': 0, 'rel': 'root'})
#                    self.dg.root = self.dg.get_by_address(mod_nr)
                if child:
                    if head_nr == mod_nr and re.match( "IP-MAT.*|INTJP|FRAG", head_tag):  #todo root phrase types from config
                        self.dg.get_by_address(mod_nr).update({'head': 0, 'rel': 'root'})  #todo copula not a head
                        self.dg.root = self.dg.get_by_address(mod_nr)
                    elif child[0] == '0' or '*' in child[0] or '{' in child[0] or '<' in child[0] or mod_tag == 'CODE':
                        continue
                    else:
                        self.dg.get_by_address(mod_nr).update({'head': head_nr, 'rel': self._relation(mod_tag, head_tag)})
                    if head_nr != mod_nr:
                        self.dg.add_arc(head_nr, mod_nr)

        return self.dg

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
