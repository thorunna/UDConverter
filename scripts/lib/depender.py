
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
from collections import defaultdict, OrderedDict
import re
from sys import argv, stdin, stdout
import getopt

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
            'IP-MAT'  : {'dir':'r', 'rules':['VB.*','RD.*','BE.*','N.*']},
            'IP-SUB'  : {'dir':'r', 'rules':['BED.','.*']},
            'NP-SBJ'  : {'dir':'r', 'rules':['N-N']},
            'NP-OB1'  : {'dir':'r', 'rules':['N-A', 'NPR-A', 'ONE+Q-A']},
            'NP'      : {'dir':'r', 'rules':['NS-.', 'N-.']},
            'NP-MSR'  : {'dir':'r', 'rules':['NS-.', 'N-.']},
            'ADJP'    : {'dir':'r', 'rules':['ADJ-N']},
            'ADJP-SPR': {'dir':'r', 'rules':['ADJ-N']},
            'PP'      : {'dir':'r', 'rules':['P']},
            'CP-THT'  : {'dir':'r', 'rules':['IP-SUB','.*']},
            #'IP-INF'  : {'dir':'r', 'rules':['IP-INF']},  # óþarfi, er fyrsti frá vinstri
            #'CONJP'   : {'dir':'r', 'rules':['IP-INF']}   # óþarfi, er fyrsti frá vinstri
        }

    def _select_head(self, tree):
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
        if dir == 'l':
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

        if mod_tag == 'NP':
            # -ADV, -CMP, -PRN, -SBJ, -OB1, -OB2, -OB3, -PRD, -POS, -COM, -ADT, -TMP, -MSR
            return {
                'SBJ': 'nsubj',
                'OB1': 'dobj',
                'OB2': 'iobj',
                'OB3': 'iobj',
                'POS': 'case',
            }.get(mod_func, 'rel')
        elif mod_tag == 'D':
            return 'det'
        elif mod_tag == 'ADJP':
            # -SPR (secondary predicate)
            return 'amod'
        elif mod_tag == 'PP':
            # -BY, -PRN
            return 'case'
        elif mod_tag == 'ADVP':
            # -DIR, -LOC, -TP
            return 'amod'
        elif mod_tag in ['VAN', 'BAN', 'DAN', 'HAN']:
            return 'aux'
        elif mod_tag in ['VBN', 'BEN', 'DON', 'HVN', 'RDN']:
            return 'auxpass'
        elif mod_tag[0:2] in ['VB', 'BE', 'DO', 'HV', 'RD']: #todo
            return 'aux'
        elif mod_tag == 'RP': #todo, adverbial particles
            return 'amod'
        elif mod_tag in ['.', ',', ';', ':', '!', '?']:
            return 'punc'

        return 'rel-'+mod_tag

    @staticmethod
    def _conllU_tag(tag):
        return '_'

    def create_dependency_graph(self, psd):
        """Create a dependency graph from a phrase structure tree."""
        const = []
        tag_list = {}
        nr = 1
        t = IndexedTree.fromstring(psd)
        # t = IndexedTree(psd)


        self.dg = UniversalDependencyGraph()


        #remove id node and trim tree
        # if t[1].label() == 'ID':
        #     self.dg.sent_id = t[1][0]
        #     t = t[0]

        for i in t.treepositions():
            if isinstance(t[i], Tree):
                if len(t[i]) == 1:
                    #tag + lemma
                    tag_list[nr] = t[i].label()
                    t[i].set_id(nr)
                else:
                    #phrase
                    t[i].set_id(0)
                    const.append(i)

            else:
                #form-lemma
                if '-' in t[i]:
                    form, lemma = t[i].split('-', 1)
                else:
                    form = lemma = t[i]
                self.dg.add_node({'address': nr,
                                  'word': form,
                                  'lemma': lemma,
                                  'ctag': '_',
                                  'tag': tag_list[nr],
                                  'feats': '_',
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
