
'''
depender.py
Hinrik Hafsteinsson (hih43@hi.is)
Þórunn Arnardóttir (tha86@hi.is)
2019
Based on earlier work by
Örvar Kárason (ohk2@hi.is)
Part of UniTree project for IcePaHC
'''

from lib import features as f
# from lib import DMII_data
from lib.reader import IndexedCorpusTree
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
                                   'head': '_', # None, # TODO: find permanent fix!
                                   'deps': defaultdict(list),
                                   'rel': None,
                                   'misc': defaultdict(None),    # testing adding Misc column
                                   })
        self.nodes[0].update(
            {
                'ctag': 'TOP',
                'tag': 'TOP',
                'ID': 0,
            }
        )
        self.original_ID = None

    #todo _parse for CoNLL-U

    def _deps_str(self, deps_dict):
        #todo, format should be "4:nsubj|11:nsubj", see http://universaldependencies.github.io/docs/format.html
        return '_' #return ''.join('%s:%s,' % (dep, '+'.join(str(rel))) for (dep, rel) in deps_dict.items())[0:-1]

    def _misc_string(self, misc_dict):
        """17.03.20

        Returns:
                string: contents of MISC column for word.
                        ex. {'SpaceAfter' : 'No'} -> 'SpaceAfter=No'
                        If misc_dict is None returns '_'

        # TODO: implement

        """
        return '|'.join(f'{pair[0]}={pair[1]}' for pair in misc_dict.items())

    def addresses(self):
        """10.03.20
        Gets addresses of the dependency graph.

        Returns:
            tuple: all addresses in dependency graph of sentence.

        """

        return tuple(address for address in [node['address'] for node in self.nodes.values()] if address != None)


    def rels(self):
        '''
        Checks and counts the relations in the sentence

        Returns:
            defaultdict: Relations found in the sentence graph, counted.
        '''
        rels = defaultdict(int)
        rels['root'] = 0
        rels['ccomp/xcomp'] = 0
        for node in self.nodes.values():
            rels[node['rel']] += 1
        # return {rel for rel in [node['rel'] for node in self.nodes.values()]}
        return rels

    def num_roots(self):
        '''
        Method for checking the root relation in the graph.
        There must be one relation to the root node in each sentence, no more
        no less. This should return 1 if sentence is correctly parsed.

        Returns:
            int: Number of root relations found in sentence.
        '''
        return self.rels()['root']

    def num_verbs(self):
        '''09.03.20
        Checks by POS (IcePaHC PoS tag) how many verbs are in sent. graph.
        Used to estimate whether verb 'aux' UPOS is correct or wrong.
        Converter generalizes 'aux' UPOS for 'hafa' and 'vera'.

        Returns:
            int: Number of verb tags found in sentence.

        # TODO: Finish implementation
        '''

        verb_count = 0
        for node in self.nodes.values():
            if node['tag'][0:2] in  {'VB', 'BE', 'DO', 'HV', 'MD', 'RD',}:
                verb_count += 1

        return verb_count

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

        # TODO: _misc_string
        """

        # template = '{i}\t{word}\t{lemma}\t{ctag}\t{tag}\t{feats}\t{head}\t{rel}\t{deps_str}\t_\n'
        template = '{i}\t{word}\t{lemma}\t{ctag}\t{tag}\t{feats}\t{head}\t{rel}\t{deps_str}\t{misc_str}\n' # testing misc column

        return ''.join(template.format(i=i, **node, deps_str=self._deps_str(node['deps']), misc_str=self._misc_string(node['misc']))
                         for i, node in sorted(self.nodes.items()) if node['tag'] != 'TOP') \
               + '\n'

    def plain_text(self):
        """ 09.03.20
        Extracts text from dependency graph.
        - Removes '$' from conjoined words and joins word-parts using regex
        - Joins punctuation to previous word by adding '$' and removing with regex

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
        punctuation = '!"#$%&\'()*+, -./:;<=>?@[\\]^_`{|}~'
        text = []
        for address, info in self.nodes.items():
            if info['word']:
                if info['word'] in punctuation:
                    text.append('$'+info['word'])
                else:
                    text.append(info['word'])
        text = '# text = ' + ' '.join(text)
        text = re.sub('\$ \$', '', text)
        text = re.sub(' \$', '', text)
        text = re.sub('</?dash/?>', '-', text)
        return text

    def original_ID_plain_text(self, **kwargs):
        return '# '+kwargs.get('corpus_name', 'Original')+'_ID = '+ str(self.original_ID)



class Converter():
    """
    Converts constituency tree to

    # TODO: finish documentation

    Attributes:
        t (type): IndexedCorpusTree object being converted.
        dg (type): UnviersalDependencyGraph object.

    """
    def __init__(self):
        #todo read rules from config file
        self.t = None
        self.dg = None

    def _select_head(self, tree, main_clause=None):
        """
        Selects dependency head of a tree object, specifically a constituency
        tree (i.e. small part) of a bigger sentence

        Args:
            tree (IndexedCorpusTree): IndexedCorpusTree object to have head selected
        """

        # tag_orig = str(tree.label())
        # tag = re.sub('-\d+', '', tag_orig)
        tag = str(tree.label())

        # print(tag)

        # if re.match(tag[:2], r'IP') \
        # or re.match(tag[:2], r'CP') \
        # or re.match(tag[:2], r'WNP'):
            # NOTE: if the IP... tag is indexed, the index is removed in the
            #       tag variable, as the tag is used to look up in the head
            #       rules, where the indexes don't matter.
            # NOTE: r'IP|CP' regex doesn't work here for some reason.

            # # DEBUG
            # print('\nMatch IP/CP\n')


        # apparently this it's better to generalize this over all tags
        tag = re.sub(r'[=-]\d+', '', tag)



            # if tree.num_verbs() == 1:
            #     tag = 'IP-aux'
            #     tree.set_label(tag)
            #     # return self._select_head(tree)

            # if re.match('-\d', tag[-2:]):
            #
            #     # print(tree.id())
            #
            #     tag = re.sub('-\d+', '', tag)
            #     # tree.set_label(tag)
            #     # return self._select_head(tree)
            #
            # elif re.match('=\d', tag[-2:]):
            #     tag = re.sub('-\d+', '', tag)


        # # DEBUG:
        # print(f'Tree: ({tree.label()}), length: {len(tree)}, height: {tree.height()}\n', tree, tag)
        # input()

        new_rules = []
        head_rule = head_rules.get(tag, {'dir':'r', 'rules':['.*']})  #default rule, first from left
        rules = head_rule['rules']
        dir = head_rule['dir']
        head = None # NOTE: er þetta eitthvað?

        if not main_clause:
            main_clause = tree

        # # DEBUG
        # else:
        #     print('\nMain Clause indicated\n')

        # # DEBUG:
        # if tag[:2] == 'IP':
        #     print(len(head_rule['rules']))
        # input()

        # if tree.num_verbs() > 1:
        #     for rule in rules:
        #         if rule in {'BE.*', 'HV.*', 'MD.*', 'RD.*', 'BE', 'HV', 'MD', 'RD'}:
        #             rules.remove(rule)

        # Somewhat efficient fix for aux verbs
        if tree.num_verbs() == 1 or main_clause.num_verbs() == 1:
            new_rules[0:0] = rules
            # new_rules[4:4] = ['BE.*', 'HV.*', 'MD.*', 'RD.*']
            new_rules[4:4] = ['HV.*', 'MD.*', 'RD.*']
            rules = new_rules

        # TEMP: testing for 3 verb sentences where the 'first' verb is 'vera', e.g. 'En það var eftir að hann var farinn sem mér varð ljóst að ég yrði'
        elif tree.num_verbs() > 2 or main_clause.num_verbs() > 2:
            # print('\n3 verb sentence\n')
            new_rules[0:0] = rules
            new_rules[4:4] = [ 'IP-INF', 'HV.*', 'MD.*', 'RD.*']
            new_rules.append('BE.*')
            rules = new_rules

        # # DEBUG:
        # print(len(new_rules))
        # input()

        if dir == 'l':
            rules = reversed(rules)

        # For catching relation to main clause verb

        # # DEBUG
        # print('MC:\n',main_clause)
        # print('Verb num:\n',tree.num_verbs())


        for rule in rules:
            for child in main_clause:

                # # DEBUG:
                # print(rule, child.label())
                # print(child,'\n')

                if re.match(rule, child.label()):

                    # # DEBUG:
                    # print('Head rules:', rules)
                    # input()

                    #if '*' in child[0]: #or ' ' in child[0]: ATH. sturlunga 822 CODE tekið út og '' sett í staðinn - betra að hafa ' '
                    #    continue
                    #else:
                    tree.set_id(child.id())

                    # # DEBUG
                    # print('Head:\n',child)
                    # input()

                    return

        #no head-rules applicable: select either the first or last child as head
        if len(tree) == 0:
            # print('==no_head==')
            tree.set_id(999) # For when there is no terminal node in head (text edit artifact)
        elif dir == 'l':
            tree.set_id(tree[-1].id())

        else:
            # print('\tNo head rule found\n')
            tree.set_id(tree[0].id())  # first from left indicated or no head rule index found
            #TODO: frekar síðasta orð?

            # # DEBUG:
            # print('Head rules:', rules)
            # input()
            # # DEBUG:
            # print('Head:\n',child)
            # input()

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
        mod_tag = re.sub(r'[=-]\d+', '', mod_tag)
        #'=\d+|
        mod_tag = re.sub('=XXX|=X', '', mod_tag)

        head_tag = re.sub('-TTT', '', head_tag)
        head_tag = re.sub(r'[=-]\d+', '', head_tag)
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

    def _fix_root_relation(self):
        """09.03.20
        Fixes buggy root relations in filled out sentence graph by checking
        number of root relations and verb POS tags.

        # TODO: Finish implementation / documentation
        """
        # print(graph.nodes.items())

        # If there is no root in sentence
        # print('\n@ _fix_root_relation()\n')
        if self.dg.num_roots() < 1:

            # NOTE: catches sentences with only one word and marks it as root
            if len(self.dg.nodes) == 2:
                self.dg.get_by_address(1).update({'head': 0, 'rel': 'root'})

            # NOTE: when no verb in sentence and no root
            if self.dg.num_verbs() == 0:

                # print('No root relation found in sentence.')
                for address, info in self.dg.nodes.items():
                    # print(address, info['head'])
                    if address == info['head']:

                        # # DEBUG:
                        # print('Node to fix:')
                        # print(self.dg.get_by_address(address))
                        # print()

                        self.dg.get_by_address(address).update({'head': 0, 'rel': 'root'})

            # NOTE: when one verb in sent but no root
            elif self.dg.num_verbs() == 1:

                # TODO: Hér þarf sögnin að vera valin sem rót en vensl annarra
                #       orða við sögnina haldist rétt / séu lagfærð í leiðinni.
                # pass
                for address, info in self.dg.nodes.items():
                    # print(address, info['head'])
                    if address == info['head']:
                        self.dg.get_by_address(address).update({'head': 0, 'rel': 'root'})

            # NOTE: when more than one verb in sent but no root
            #       E.g. "Má ég klappa honum aftur á eftir?", where Klappa
            #       should get the root relation but not "Má"
            elif self.dg.num_verbs() > 1:
                # TODO: Passa að rétt sögn (umsögn aðalsetningar) sé valin sem
                #       rót og ekki aðrar sagnir.
                for address, info in self.dg.nodes.items():
                    # print(address, info['head'])
                    if address == info['head']:

                        # # DEBUG:
                        # print('Node to fix:')
                        # print(self.dg.get_by_address(address))
                        # print()

                        self.dg.get_by_address(address).update({'head': 0, 'rel': 'root'})
                pass

        # If there is more than one root in sentence
        elif self.dg.num_roots() > 1:

            # # DEBUG:
            # print('\nNo. of verbs in sentence:\n', self.dg.num_verbs())
            # print()

            if self.dg.num_verbs() == 1:
                pass


    def _fix_ccomp(self):
        """
        finds all nodes in graph with the relation 'ccomp/xcomp' and fixes them

        checks where ccomp can appear and should leave only xcomp nodes

        Returns:
            None

        """
        for address, info in self.dg.nodes.items():
            if info['rel'] == 'ccomp/xcomp':

                self.dg.get_by_address(address).update({'rel': 'xcomp'})
                # # DEBUG:
                # print('\nccomp/xcomp error node:')
                # print(address, info)

                for other_address, other_info in self.dg.nodes.items():
                    # check if nsubj node has ccomp/xcomp node as head
                    if other_info['head'] == address and other_info['rel'] == 'nsubj':


                        # # DEBUG:
                        # print('\n=> check for nsubj relation to error node\n')
                        # print(other_address, other_info)
                        # input()

                        self.dg.get_by_address(address).update({'rel': 'ccomp'})
                    elif other_info['address'] == info['head'] and self.dg.get_by_address(other_info['head'])['ctag'] in {'AUX', 'VERB'}:
                        # checks if error node head is verb and whether that verb has a nsubj node attached
                        # NOTE: likely be too greedy
                        for other_other_address, other_other_info in self.dg.nodes.items():
                            if other_other_info['head'] == other_info['head'] and other_other_info['rel'] == 'nsubj':

                                # # DEBUG:
                                # print('\n=> check if error node head is verb and verb has nsubj\n')
                                # print(other_address, other_info)
                                # print(other_other_address, other_other_info)
                                # input()

                                self.dg.get_by_address(address).update({'rel': 'ccomp'})
                    elif other_info['head'] == info['head'] and other_info['rel'] == 'nsubj':

                        if other_info['ctag'] == 'PRON' and re.search('(-A|-D|-G)', other_info['tag']):
                            # accusative and dative pronouns as subject may indicate no real subject, thus xcomp relation
                            # print('\n=> MAYBE NOT TOO GREEDY? (xcomp)')
                            # self.dg.get_by_address(address).update({'rel': 'xcomp'})
                            continue
                        else:
                            # This chould also be ccomp but is too greedy
                            # print('\n=> TOO GREEDY\n')
                            self.dg.get_by_address(address).update({'rel': 'ccomp'})
                            # continue

                # else:
                #     print('\n=> NO FIX\n')


                    # else:
                    #     self.dg.get_by_address(address).update({'rel': 'xcomp'})

    def _fix_cop(self):
        pass

    def _fix_aux_tag(self):
        """
        UD convention
        Fixes UPOS tag for verbs that have relation 'aux' but not UPOS tag AUX.
        """

        for address, info in self.dg.nodes.items():
            if info['rel'] == 'aux' and info['tag'] != 'AUX':
                self.dg.get_by_address(address).update({'ctag': 'AUX'})

    def _fix_acl_advcl(self):
        """
        finds all nodes in graph with the relation 'acl/advcl' and fixes them

        checks where ccomp can appear and should leave only xcomp nodes

        Returns:
            None

        """
        for address, info in self.dg.nodes.items():
            if info['rel'] == 'acl/advcl':
                # If the head is a verb
                if self.dg.get_by_address(info['head'])['ctag'] == 'VERB':

                    # # DEBUG
                    # print('=> Head is verb\n', self.dg.get_by_address(address))

                    self.dg.get_by_address(address).update({'rel': 'advcl'})
                # If the head has a cop attached
                elif self.dg.get_by_address(info['head'])['ctag'] in {'NOUN', 'PROPN', 'PRON', 'ADJ'}:

                    # # DEBUG
                    # print('=> Head seems to be nominal\n', self.dg.get_by_address(address))

                    for other_address, other_info in self.dg.nodes.items():
                        if other_info['head'] == info['head'] and other_info['rel'] == 'cop':
                            self.dg.get_by_address(address).update({'rel': 'advcl'})
                        # Should have acl relation if not caught above
                        else:
                            self.dg.get_by_address(address).update({'rel': 'acl'})
                # All cases not yet caught ~should~ have relation acl
                else:
                    self.dg.get_by_address(address).update({'rel': 'acl'})
            else:
                continue

    def _fix_punct_heads(self):
        for address, info in self.dg.nodes.items():
            if info['ctag'] == 'PUNCT':
                if address+1 in self.dg.nodes \
                and self.dg.get_by_address(address+1)['rel'] == 'conj':
                    self.dg.get_by_address(address).update({'head': address+1})



    def _add_space_after(self):
        """10.03.20
        Fills in Space_after feature in misc column.

        """

        for address in self.dg.addresses():
            if self.dg.get_by_address(address)['ctag'] == 'PUNCT':
                id_to_fix = int(address) - 1
                if id_to_fix < 0:
                    continue
                elif self.dg.get_by_address(address)['ctag'] == '„':
                    self.dg.get_by_address(address)['misc']['SpaceAfter'] = 'No'
                elif self.dg.get_by_address(id_to_fix)['lemma'] in {'„', ':'} or address == '1':
                    continue
                else:
                    self.dg.get_by_address(id_to_fix)['misc']['SpaceAfter'] = 'No'


    def create_dependency_graph(self, tree):
        """Create a dependency graph from a phrase structure tree.

        Returns:
            type: .

        """
        const = []
        tag_list = {}
        nr = 1
        # Tree item read in as string and transferred to UD graph instance
        if isinstance(tree, (IndexedCorpusTree)):
            t = tree.remove_code_nodes()
        else:
            t = IndexedCorpusTree.fromstring(tree).remove_code_nodes()
        self.dg = UniversalDependencyGraph()
        self.dg.original_ID = t.corpus_id

        for i in t.treepositions():
            if isinstance(t[i], Tree):

                if len(t[i]) == 1:
                    # If terminal node with label or tree with single child
                    # e.g. (VBDI tók-taka) or (NP-SBJ (PRO-N hann-hann))
                    tag_list[nr] = t[i].label()
                    t[i].set_id(nr)
                    # print(t[i],'\n', t[i].height(), len(t[i]))
                else:
                    # print(t[i])
                    # If constituent / complex phrase
                    # e.g. (ADVP (ADV smám-smám) (ADV saman-saman))
                    t[i].set_id(0)
                    const.append(i)


            else:

                # If trace node, skip (preliminary, may result in errors)
                # e.g. *T*-3 etc.
                if t[i][0] in {'0', '*', '{'}:   #if t[1].pos()[0][0] in {'0', '*'}:
                    continue

                # # catches e.g. <heading>
                # if re.search(r'\<.*\>', t[i][0]):
                #     print(t[i])
                #     input()
                #     FORM = LEMMA = '-'
                #     tag = tag_list[nr]

                # If terminal node with no label (token-lemma)
                # e.g. tók-taka
                if '-' in t[i]:
                    FORM, LEMMA = t[i].split('-', 1)
                    tag = tag_list[nr]
                # # If <dash/>, <dash> or </dash>
                # elif t[i][0] in {'<dash/>', '<dash>', '</dash>'}:
                #     print('DASH')
                #     FORM = LEMMA = '-'
                #     tag = tag_list[nr]
                else: # If no lemma present
                    continue
                    # print(t[i])
                    # input()
                    FORM = t[i][0]
                    LEMMA = None
                    # if LEMMA == None:
                    #     LEMMA = '_'
                    # token_lemma = str(FORM+'-'+LEMMA)
                    tag = tag_list[nr]
                if '+' in tag:
                    tag = re.sub('\w+\+', '', tag)
                # token_lemma = str(FORM+'-'+LEMMA)
                # leaf = token_lemma, tag
                XPOS = tag
                # Feature Classes called here
                UPOS = f.Features.get_UD_tag_external(tag)
                FEATS = '_'
                if FORM != None or FORM != 'None':
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

        # # DEBUG:
        # print(tag_list)

        # trees with single child
        singles = [i for i in set(t.treepositions()).difference(const) if isinstance(t[i], Tree)]

        # go through the constituencies (bottom up) and find their heads
        const.sort(key=lambda x: len(x), reverse=True)

        # # DEBUG:
        # print(t.tags())
        # print(t.num_verbs())
        # input()

        # head selection
        for i in const:

            # # DEBUG:
            # print(i, t[i], t[i].label(), len(t[i]))
            # input()

            # Catch index referenced sentences in treebank
            if re.match('=\d', t[i].label()[-2:]):# or t[i].label() == 'CONJP
                clause_index = t[i].label()[-1]
                # re.match('\d', t[i].label()[-2:])
                for j in const + singles:
                    if re.match(f'-{clause_index}', t[j].label()[-2:]):
                        if isinstance(t[j][0], str):
                            t[i].set_id(t[j].id())
                        else:
                            self._select_head(t[i], main_clause=t[j])

            else:
                self._select_head(t[i])

        # fixes subtrees with 1 child but wrong id
        for i in singles:
            if isinstance(t[i][0], Tree) and t[i].id() != t[i][0].id():

                # # DEBUG:
                # print()
                # print('Tree ID:', t[i].id(), 'Child ID:', t[i][0].id())
                # print('Tree:', t[i])
                # # print()
                # print('Child:', t[i][0])

                if re.match('=\d', t[i].label()[-2:]):
                    # print('\nMain Clause indicated\n')
                    clause_index = t[i].label()[-1]
                    # re.match('\d', t[i].label()[-2:])
                    for j in const:
                        if re.match(f'-{clause_index}', t[j].label()[-2:]):
                            self._select_head(t[i][0], main_clause=t[j])
                # else
                else:
                    t[i].set_id(t[i][0].id())

                # print('Tree ID:', t[i].id(), 'Child ID:', t[i][0].id())

        # runs various subtrees that are likely to have root errors after
        # last block back through head selection
        for i in const:
            if re.match('(IP-MAT|IP-SUB-SPE|FRAG|QTP|IP-IMP|CONJP|META|LATIN)', t[i].label()):
                self._select_head(t[i])

        for i in list(set(t.treepositions()).difference(const)):
            if isinstance(t[i][0], Tree) and t[i].label() == 'CONJP':
                t[i].set_id(t[i][0].id())

        # for i in const:
        #     # Catch index referenced sentences run back through head selection
        #     if re.match('=\d', t[i].label()[-2:]):# or t[i].label() == 'CONJP
        #         clause_index = t[i].label()[-1]
        #         # re.match('\d', t[i].label()[-2:])
        #         for j in const:
        #             if re.match(f'-{clause_index}', t[j].label()[-2:]):
        #                 self._select_head(t[i], main_clause=t[j])


        # relations set
        for i in const:

            head_tag = t[i].label()
            head_nr = t[i].id()

            # if re.search(r'\w{1,5}(21|22|31|32|33)', head_tag):
            head_tag = re.sub('(21|22|31|32|33)', '', head_tag)

            for child in t[i]:

                # block to catch explatives inside e.g. NP-SBJ nodes
                if len(child) == 1 and not isinstance(child[0], str) and child[0].label() == 'ES':
                    mod_tag = child[0].label()
                else:
                    mod_tag = child.label()

                # if re.search(r'\w{1,5}(21|22|31|32|33)', mod_tag):
                mod_tag = re.sub('(21|22|31|32|33)', '', mod_tag)
                mod_nr = child.id()



#                if head_nr == mod_nr and re.match("NP-PRD", head_tag):      #ath. virkar þetta rétt? Leið til að láta sagnfyllingu cop vera rót
#                    self.dg.get_by_address(mod_nr).update({'head': 0, 'rel': 'root'})
#                    self.dg.root = self.dg.get_by_address(mod_nr)
                if child:
                    # NOTE: This is where the root is selected


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
                    if head_nr == mod_nr:
                        # print(self.dg.get_by_address(mod_nr))
                        if re.match("IP-MAT|IP-MAT-[^=].*|INTJP|FRAG|CP-QUE-SPE|IP-IMP-SPE[^=1]|QTP|CODE|LATIN|TRANSLATION|META|IP-IMP|CP-QUE|CP-EXL|CP-THT", head_tag):  #todo root phrase types from config
                            self.dg.get_by_address(mod_nr).update({'head': 0, 'rel': 'root'})  #todo copula not a head
                            self.dg.root = self.dg.get_by_address(mod_nr)
                        else:
                            # Unknown dependency relation (things to fix)
                            # self.dg.get_by_address(mod_nr).update({'head': head_nr, 'rel': '***'})
                            self.dg.get_by_address(mod_nr).update({'head': head_nr, 'rel': 'dep'})
                            self.dg.root = self.dg.get_by_address(mod_nr)

                            # print(self.dg.get_by_address(mod_nr))

                        # elif head_tag.endswith('=1'):
                            # # DEBUG:
                            # print(head_tag)
                            # print(self.dg.root)
                            # input()

                    elif child[0] == '0' or '*' in child[0] or '{' in child[0] or '<' in child[0] or mod_tag == 'CODE':
                        continue
                    else:

                        # # DEBUG:
                        # print('head_nr:', head_nr, 'mod_nr:', mod_nr)
                        # print('head_tag', head_tag, 'mod_tag', mod_tag)
                        # print(self.dg.get_by_address(mod_nr))
                        # # input()

                        self.dg.get_by_address(mod_nr).update({'head': head_nr, 'rel': self._relation(mod_tag, head_tag)})

                        # # DEBUG:
                        # print(self.dg.get_by_address(mod_nr))
                        # input()

                    if head_nr != mod_nr:
                        self.dg.add_arc(head_nr, mod_nr)

        self._add_space_after()

        # NOTE: Here call method to fix dependency graph if needed?
        if self.dg.num_roots() != 1:

            # # DEBUG:
            # print(self.dg.to_conllU())
            # input()

            self._fix_root_relation()

        rel_counts = self.dg.rels()

        if rel_counts['ccomp/xcomp'] > 0:
            self._fix_ccomp()
        if rel_counts['aux'] > 0:
            self._fix_aux_tag()
        if rel_counts['acl/advcl'] > 0:
            self._fix_acl_advcl()
        if rel_counts['punct'] > 0:
            self._fix_punct_heads()
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
