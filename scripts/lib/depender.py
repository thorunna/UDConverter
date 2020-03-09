
'''
depender.py
Hinrik Hafsteinsson (hih43@hi.is)
Þórunn Arnardóttir (tha86@hi.is)
2019
Based on earlier work by
Örvar Kárason (ohk2@hi.is)
Part of UniTree project for IcePaHC
'''

# from lib import features as f
# from lib import DMII_data
from lib.rules import head_rules
from lib import relations

from nltk.tree import Tree
from nltk.parse import DependencyGraph
from sys import argv, stdin, stdout
import getopt
from collections import defaultdict
import re
import string


class UniversalDependencyGraph(DependencyGraph):
    '''
    Takes in a nltk Tree object and returns an approximation of the tree
    sentence in the CONLLU format for UD:
        ID: Word index, integer starting at 1 for each new sentence.
        FORM: Word form or punctuation symbol.
        LEMMA: Lemma or stem of word form.
        UPOS: Universal part-of-speech tag.
        XPOS: Language-specific part-of-speech tag; underscore if not available.
        FEATS: List of morphological features from the universal feature
            inventory or from a defined language-specific extension; underscore
            if not available.
        HEAD: Head of the current word, which is either a value of ID or
            zero (0).
        DEPREL: Universal dependency relation to the HEAD (root iff HEAD = 0)
            or a defined language-specific subtype of one.
        DEPS: Enhanced dependency graph in the form of a list of head-deprel
            pairs.
        MISC: Any other annotation.
    '''

    def __init__(self, tree_str=None, cell_extractor=None, zero_based=False,
                cell_separator=None, top_relation_label='root'):
        DependencyGraph.__init__(self, tree_str, cell_extractor, zero_based,
                                cell_separator, top_relation_label)

        self.nodes = defaultdict(lambda:  {'address': None,
                                   'word': None,
                                   'lemma': None,
                                   'ctag': None,    # upostag
                                   'tag': None,     # xpostag
                                   'feats': None,
                                   'head': '_', # None, # NOTE: possible fix to None in head output........
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
        """ 09.03.20
        Extracts text from dependency graph.

        Returns:
            string: String representation of sentence text

        """
        # NOTE: Old method kept as comment
        # text = []
        # for leaf in leaves:
        #     leaf = leaf.split('-')
        #     if leaf[0][0] in {'*', '0'}: continue
        #     text.append(leaf[0])
        # text = '# text = ' + ' '.join(text)
        # return text
        text = []
        for address, info in self.nodes.items():
            if info['word']:
                text.append(info['word'])
        text = '# text = ' + ' '.join(text)
        text = re.sub('\$ \$', '', text)
        return text


class IndexedTree(Tree):
    """
    Contains a tree object with each leaf indexed by location within tree
    # TODO: finish/fix documentation

    Args:
        node (tree): leaf.
        children (tree?): constituents.

    Attributes:
        _id (int): Counter for index.

    """

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
    """
    Converts constituency tree to

    Attributes:
        t (type): NLTK.Tree object being converted.
        dg (type): NLTK.parse.DependencyGraph object.

    """
    def __init__(self):
        #todo read rules from config file
        self.t = None
        self.dg = None

    def _select_head(self, tree):
        """
        Selects dependency head of a tree object, specifically a constituency
        tree (i.e. small part) of a bigger sentence

        Args:
            tree (IndexedTree): IndexedTree object to have head selected
        """

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
                    #if '*' in child[0]: #or ' ' in child[0]: ATH. sturlunga 822 CODE tekið út og '' sett í staðinn - betra að hafa ' '
                    #    continue
                    #else:
                    tree.set_id(child.id())
                    return

        #no head-rules applicable: select either the first or last child as head
        if len(tree) == 0:
            tree.set_id(999) # For when there is no terminal node in head (text edit artifact)
        elif dir == 'l':
            tree.set_id(tree[-1].id())

        # NOTE: Þetta er mögulega þar sem None kemur inn í úttakið... HH
        else:
            tree.set_id(tree[1].id())  # first from left indicated or no head rule index found
            #TODO: frekar síðasta orð?

        # elif tree[1].id() is not None:
        #     tree.set_id(tree[1].id())  # first from left indicated or no head rule index found
        # else:
        #     tree.set_id('_')

    def _relation(self, mod_tag, head_tag):
        """
            Return a Universal Relation name given an IcePaHC/Penn phrase-type tag

            http://www.linguist.is/icelandic_treebank/Phrase_Types
            to
            http://universaldependencies.github.io/docs/u/dep/index.html

        :param mod_tag: str
        :param head_tag: str
        :return: str
        """

        mod_tag = re.sub('-TTT', '', mod_tag)
        mod_tag = re.sub('-\d+', '', mod_tag)
        #'=\d+|
        mod_tag = re.sub('=XXX|=X', '', mod_tag)

        head_tag = re.sub('-TTT', '', head_tag)
        head_tag = re.sub('-\d+', '', head_tag)
        #'=\d+|
        head_tag = re.sub('=XXX|=X', '', head_tag)

        if '+' in mod_tag:
            mod_tag = re.sub('\w+\+', '', mod_tag)
        if '+' in head_tag:
            head_tag = re.sub('\w+\+', '', head_tag)

        if '-' in mod_tag:
            mod_tag, mod_func = mod_tag.split('-', 1) #todo, handle more than one function label
        else:
            mod_func = None

        if '-' in head_tag:
            head_tag, head_func = head_tag.split('-', 1)
        else:
            head_func = None

        return relations.determine_relations(mod_tag, mod_func, head_tag, head_func)

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
                    #LEMMA = DMII_data.get_lemma(FORM)
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
                '''
                # NOTE: Features Classes rewritten, may be removed from here
                leaf = f.Word(leaf).getinfo()
                UPOS = leaf.UD_tag
                FEATS = leaf.features.featString()
                '''
                UPOS = '_'
                FEATS = '_'
                if FORM != None:
                    self.dg.add_node({'address': nr,
                                      'word': FORM,
                                      'lemma': LEMMA,
                                      #'lemma': '_',
                                      'ctag': UPOS, # upostag
                                      #'ctag': '_', # upostag
                                      'tag': XPOS,   # xpostag
                                      'feats': FEATS,
                                      #'feats': '_',
                                      'deps': defaultdict(list),
                                      'rel': '_'})
                    nr += 1

        print(t)
        # go through the constituencies (bottom up) and find their heads
        const.sort(key=lambda x: len(x), reverse=True)

        for i in const:
            print(i, t[i], t[i].label())
            input()
            self._select_head(t[i])

        for i in const:
            head_tag = t[i].label()
            head_nr = t[i].id()

            if re.search(r'\w{1,5}(21|22|31|32|33)', head_tag):
                head_tag = re.sub('(21|22|31|32|33)', '', head_tag)
            #if re.search(r'IP-MAT=\d+', head_tag):
            #    head_tag = re.sub('IP-MAT=\d+', 'IP-MAT', head_tag)
            for child in t[i]:
                mod_tag = child.label()
                if re.search(r'\w{1,5}(21|22|31|32|33)', mod_tag):
                    mod_tag = re.sub('(21|22|31|32|33)', '', mod_tag)
                mod_nr = child.id()

#                if head_nr == mod_nr and re.match("NP-PRD", head_tag):      #ath. virkar þetta rétt? Leið til að láta sagnfyllingu cop vera rót
#                    self.dg.get_by_address(mod_nr).update({'head': 0, 'rel': 'root'})
#                    self.dg.root = self.dg.get_by_address(mod_nr)
                if child:
                    #if child[0] == '0' or '*' in child[0] or '{' in child[0] or '<' in child[0] or mod_tag == 'CODE':
                    #    continue
                    #else:
                    #    if head_nr == mod_nr and re.match("IP-MAT.*|INTJP|FRAG|CP-QUE-SPE|IP-IMP-SPE|QTP", head_tag):  #todo root phrase types from config
                    #        self.dg.get_by_address(mod_nr).update({'head': 0, 'rel': 'root'})  #todo copula not a head
                    #        self.dg.root = self.dg.get_by_address(mod_nr)
                    #    else:
                    #        self.dg.get_by_address(mod_nr).update({'head': head_nr, 'rel': self._relation(mod_tag, head_tag)})
                    #    if head_nr != mod_nr:
                    #        self.dg.add_arc(head_nr, mod_nr)
                    #if head_nr == mod_nr and re.match("IP-MAT.*|CP.*|INTJP|FRAG", head_tag):  #todo root phrase types from config
                    if head_nr == mod_nr and re.match("IP-MAT|IP-MAT-[^=].*|INTJP|FRAG|CP-QUE-SPE|IP-IMP-SPE[^=1]|QTP|CODE|LATIN|TRANSLATION|META|IP-IMP|CP-QUE|CP-EXL|CP-THT", head_tag):  #todo root phrase types from config
                        self.dg.get_by_address(mod_nr).update({'head': 0, 'rel': 'root'})  #todo copula not a head
                        self.dg.root = self.dg.get_by_address(mod_nr)

                    elif child[0] == '0' or '*' in child[0] or '{' in child[0] or '<' in child[0] or mod_tag == 'CODE':
                        continue
                    else:
                        self.dg.get_by_address(mod_nr).update({'head': head_nr, 'rel': self._relation(mod_tag, head_tag)})
                    if head_nr != mod_nr:
                        self.dg.add_arc(head_nr, mod_nr)

        return self.dg


def test_case(infile):
    # NOTE: not used!!!
    '''05.03.20
    Test case for debugging head choice algorithm
    Prints output to command line

    Args:
        infile (string): Path to input file.

    '''
    psd = ''
    with open(infile) as file:
        for line in file:
            psd += line
            if len(line.strip()) == 0 and len(psd.strip()) > 0:
                dep = c.create_dependency_graph(psd)
                dep.to_conllU()


'''
# NOTE: Old main function
def main(argv):
    c = Converter()
    psd = ''
    infilename = outfilename = None

    opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])

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
'''

if __name__ == "__main__":
    # main(argv[1:])
    test_case(sys.argv[1])
