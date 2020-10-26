
'''
depender.py
Hinrik Hafsteinsson (hih43@hi.is)
Þórunn Arnardóttir (tha86@hi.is)
2019
Based on earlier work by
Örvar Kárason (ohk2@hi.is)
Part of UniTree project for IcePaHC
'''

from lib.features import *
# from lib import DMII_data
from lib.reader import IndexedCorpusTree
from lib.rules import head_rules
from lib.tools import determine_relations, decode_escaped
from lib.joiners import NodeJoiner

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
                                   'feats': defaultdict(lambda: None),
                                   'head': '_', # None, # TODO: find permanent fix!
                                   'deps': defaultdict(list),
                                   'rel': None,
                                   'misc': defaultdict(lambda: None),    # testing adding Misc column
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

    def _dict_to_string(self, dict):
        """17.03.20

        Returns:
                string: contents of column column for word from defaultdict.
                        ex. {'SpaceAfter' : 'No'} -> 'SpaceAfter=No'
                        If dict is None returns '_'

        """
        return '|'.join(f'{pair[0]}={pair[1]}' for pair in sorted(dict.items(), key=lambda s: s[0].lower()) if pair[1] is not None) if dict and len(dict) != 0 else '_'

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

    def ctags(self):
        '''
        Checks and counts the IcePaHC tags in the sentence

        Returns:
            defaultdict: IcePaHC tags found in the sentence graph, counted.
        '''
        ctags = defaultdict(int)
        for node in self.nodes.values():
            ctags[node['ctag']] += 1
        # return {rel for rel in [node['rel'] for node in self.nodes.values()]}
        return ctags

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
            if node['tag'] == None:
                continue
            elif node['tag'][0:2] in  {'VB', 'BE', 'DO', 'HV', 'MD', 'RD',}:
                verb_count += 1

        return verb_count

    def num_subj(self):
        '''
        Returns a set of the words whose deprel is 'nsubj' and whose head is the same.
        '''
        from itertools import chain

        if self.rels()['nsubj'] > 1:
            subjs = {}
            for node in self.nodes.items():
                if node[1]['rel'] == 'nsubj':
                    subjs[node[1]['word']] = node[1]['head']

            rev_dict = {}
            for key, value in subjs.items():
                rev_dict.setdefault(value, set()).add(key)

            result = set(chain.from_iterable(values for key, values in rev_dict.items() if len(values) > 1))
        
            return result

    def join_output_nodes(self, conllU):
        '''
        Joins clitics in CoNLLU string output with NodeJoiner class
        '''
        nj = NodeJoiner(conllU.split('\n'))
        for n in reversed(nj.indexes):
            # Various clitics processed
            nj.join_clitics(n)
            nj.join_other_nodes(n)
        conllU = '\n'.join(nj.lines)
        return conllU
      
    def to_conllU(self):
        """
        The dependency graph in CoNLL-U (Universal) format.

        Consists of one or more word lines, and word lines contain the following fields:

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

        template = '{i}\t{word}\t{lemma_str}\t{ctag}\t{tag}\t{feats_str}\t{head}\t{rel}\t{deps_str}\t{misc_str}\n'

        return self.join_output_nodes(''.join(template.format(i=i, **node,
                                       lemma_str=node['lemma'] if node['lemma'] else '_',
                                       deps_str=self._deps_str(node['deps']),
                                       feats_str=self._dict_to_string(node['feats']),
                                       misc_str=self._dict_to_string(node['misc']))
                                    for i, node in sorted(self.nodes.items()) \
                                    if node['tag'] != 'TOP' and node['word'] not in {'None', None} ) \
                                    + '\n')

    def plain_text(self):
        """ 09.03.20
        Extracts text from dependency graph.
        - Removes '$' from conjoined words and joins word-parts using regex

        # TODO: Fix spacing ambiguous quotation marks: ",\'

        Returns:
            string: String representation of sentence text

        """
        # p_space_after = '!),.:;?\\]>^_`„”}'
        # p_space_before = '“([<{'
        # p_isolate = '*+=/|~#%-$&'
        # p_nospace = '@'
        # p_amb_quotes = '"\''
        # text = []
        # for address, node in self.nodes.items():
        #     if node['word']:
        #         if node['word'] in p_space_after:
        #             text.append('$'+node['word'])
        #         elif node['word'] in p_space_before:
        #             text.append(node['word']+'$')
        #         elif node['word'] in p_isolate:
        #             text.append('$'+node['word']+'$')
        #         elif node['word'] in p_amb_quotes:
        #             # needs proper fixing
        #             text.append(node['word'])
        #         else:
        #             text.append(node['word'])
        # text = '# text = ' + ' '.join(text)
        # text = re.sub('\$ \$', '', text)
        # text = re.sub(' \$', '', text)
        # text = re.sub('\$ ', '', text)
        # text = re.sub('</?dash/?>', '-', text)
        text = []
        for address, node in self.nodes.items():
            if node['word'] == None:
                continue
            elif 'SpaceAfter' in node['misc'] or address == len(self.nodes):
                text.append(decode_escaped(node['word']))
            else:
                text.append(decode_escaped(node['word']+' '))
        text = ''.join(text)
        # print(text)
        text = re.sub(r'(?<=\S)\$(?=\S)', '', text)
        # print(text)
        text = re.sub(r'\$ \$', '', text)
        text = re.sub(r'\$\$', '', text)
        text = re.sub(r' \$', ' ', text)
        text = re.sub(r'\$ ', ' ', text)
        text = re.sub(r' $', '', text)
        text = re.sub(r' \.', '.', text)
        text = re.sub(r' ,', ',', text)
        return '# text = ' + text

    def original_ID_plain_text(self, **kwargs):
        """Short summary.

        Returns:
            type: .

        """

        if isinstance(self.original_ID, list):
            return '# '+kwargs.get('corpus_name', 'X')+'_IDs = '+' ; '.join(self.original_ID)
        else:
            return '# '+kwargs.get('corpus_name', 'X')+'_ID = '+ str(self.original_ID)



class Converter():
    """
    Converts constituency tree to

    # TODO: finish documentation

    Attributes:
        t (type): IndexedCorpusTree object being converted.
        dg (type): UnviersalDependencyGraph object.

    """
    def __init__(self, auto_tags=False, faroese=False):
        #todo read rules from config file
        self.t = None
        self.dg = None
        self.auto_tags = auto_tags
        self.tagged_sentences = None
        self.faroese = faroese

    def set_tag_dict(self, tag_dict):
        self.tagged_sentences = tag_dict

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
        #     print(f'\nMain Clause indicated: {main_clause.label()} \n')

        # # DEBUG:
        # if tag[:2] == 'IP':
        #     print(len(head_rule['rules']))
        # input()

        # if tree.num_verbs() > 1:
        #     for rule in rules:
        #         if rule in {'BE.*', 'HV.*', 'MD.*', 'RD.*', 'BE', 'HV', 'MD', 'RD'}:
        #             rules.remove(rule)

        # Somewhat efficient fix for aux verbs
        # print(tree.num_verbs())
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
                try:
                    if child.height() == 2 and child[0][0] == '*':
                        continue

                # # DEBUG:
                # print(rule, child.label())
                # print(child,'\n')

                    elif re.match(rule, child.label()):

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
                except AttributeError:
                    print(child)
                    raise

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

        return determine_relations(mod_tag, mod_func, head_tag, head_func)

    def _get_tag_dict(self, tree):
        if self.auto_tags == 'single_sentence':
            try:
                text = re.sub('\$ \$', '', ' '.join([tree[i].split('-')[0] for i in tree.treepositions() if isinstance(tree[i], str) ]))
                # print(text)
                tag_pairs = Features.tagged_sent(text)
                # print(tag_pairs)
                return tag_pairs
            except FeatureExtractionError:
                raise
        elif self.auto_tags == 'corpus':
            return self.tagged_sentences.get(tree.corpus_id, defaultdict(None))
    # def _features(self):
    #     if self.auto_tags == True:
    #         TAG_PAIRS = []
    #         try:
    #             text = re.sub(r'# text = ', '', self.dg.plain_text()) + ' '
    #             text = re.sub(r'"', '\\"', text)
    #             TAG_PAIRS = Features.tagged_sent(text)
    #             print(TAG_PAIRS)
    #         except FeatureExtractionError:
    #             raise
    #         for address, node in self.dg.nodes:
    #             self.dg.get_by_address(address)['misc'].update({'IFD_tag' : TAG_PAIRS.get(node['word'], 'missing')})
    #     else:
    #         pass



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
                for address, node in self.dg.nodes.items():
                    # print(address, node['head'])
                    if address == node['head']:

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
                for address, node in self.dg.nodes.items():
                    # print(address, node['head'])
                    if address == node['head']:
                        self.dg.get_by_address(address).update({'head': 0, 'rel': 'root'})

            # NOTE: when more than one verb in sent but no root
            #       E.g. "Má ég klappa honum aftur á eftir?", where Klappa
            #       should get the root relation but not "Má"
            elif self.dg.num_verbs() > 1:
                # TODO: Passa að rétt sögn (umsögn aðalsetningar) sé valin sem
                #       rót og ekki aðrar sagnir.
                for address, node in self.dg.nodes.items():
                    # print(address, node['head'])
                    if address == node['head']:

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
        for address, node in self.dg.nodes.items():
            if node['rel'] == 'ccomp/xcomp':

                self.dg.get_by_address(address).update({'rel': 'xcomp'})
                # # DEBUG:
                # print('\nccomp/xcomp error node:')
                # print(address, node)

                for other_address, other_node in self.dg.nodes.items():
                    # check if nsubj node has ccomp/xcomp node as head
                    if other_node['head'] == address and other_node['rel'] == 'nsubj':


                        # # DEBUG:
                        # print('\n=> check for nsubj relation to error node\n')
                        # print(other_address, other_node)
                        # input()

                        self.dg.get_by_address(address).update({'rel': 'ccomp'})
                    elif other_node['address'] == node['head'] and self.dg.get_by_address(other_node['head'])['ctag'] in {'AUX', 'VERB'}:
                        # checks if error node head is verb and whether that verb has a nsubj node attached
                        # NOTE: likely be too greedy
                        for other_other_address, other_other_node in self.dg.nodes.items():
                            if other_other_node['head'] == other_node['head'] and other_other_node['rel'] == 'nsubj':

                                # # DEBUG:
                                # print('\n=> check if error node head is verb and verb has nsubj\n')
                                # print(other_address, other_node)
                                # print(other_other_address, other_other_node)
                                # input()

                                self.dg.get_by_address(address).update({'rel': 'ccomp'})
                    elif other_node['head'] == node['head'] and other_node['rel'] == 'nsubj':

                        if other_node['ctag'] == 'PRON' and re.search('(-A|-D|-G)', other_node['tag']):
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
        """
        Fixes a copula verb's argument
        """

        for address, node in self.dg.nodes.items():
            if node['rel'] == 'cop':
                self.dg.get_by_address(address+1).update({'rel': 'root'})

    def _fix_aux_tag(self):
        """
        UD convention
        Fixes UPOS tag for verbs that have relation 'aux' but not UPOS tag AUX.
        """

        for address, node in self.dg.nodes.items():
            if node['rel'] == 'aux' and node['tag'] != 'AUX' and node['ctag'] != 'RD':
                self.dg.get_by_address(address).update({'ctag': 'AUX'})

    def _fix_acl_advcl(self):
        """
        finds all nodes in graph with the relation 'acl/advcl' and fixes them

        checks where ccomp can appear and should leave only xcomp nodes

        Returns:
            None

        """
        for address, node in self.dg.nodes.items():
            if node['rel'] == 'acl/advcl':
                # If the head is a verb
                if self.dg.get_by_address(node['head'])['ctag'] == 'VERB':

                    # # DEBUG
                    # print('=> Head is verb\n', self.dg.get_by_address(address))

                    self.dg.get_by_address(address).update({'rel': 'advcl'})
                # If the head has a cop attached
                elif self.dg.get_by_address(node['head'])['ctag'] in {'NOUN', 'PROPN', 'PRON', 'ADJ'}:

                    # # DEBUG
                    # print('=> Head seems to be nominal\n', self.dg.get_by_address(address))

                    for other_address, other_node in self.dg.nodes.items():
                        if other_node['head'] == node['head'] and other_node['rel'] == 'cop':
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
        for address, node in self.dg.nodes.items():
            if node['ctag'] == 'PUNCT':
                if address+1 in self.dg.nodes \
                and self.dg.get_by_address(address+1)['rel'] == 'conj':
                    self.dg.get_by_address(address).update({'head': address+1})
                if self.dg.get_by_address(address-1)['head'] == address:
                    self.dg.get_by_address(address-1).update({'head': node['head']})
                #if node['head'] < int(self.dg.get_by_address(address+1)['head']) and self.dg.get_by_address(address+1)['ctag'] == 'ADV':
                #    self.dg.get_by_address(address).update({'head': self.dg.get_by_address(address+1)['head']})
                #else:
                #    new_head = self.dg.get_by_address(address+1)['head']
                #    self.dg.get_by_address(address).update({'head': new_head})
                #elif not address+1 in self.dg.nodes:
                #    new_head = self.dg.get_by_address(address-1)['head']
                #    self.dg.get_by_address(address).update({'head': new_head})
                #if node['head'] > address:
                #    next_heads = []
                #    for x in range(6):
                #        next_heads.append(self.dg.get_by_address(address+x+1)['head'])
                #    fix = False
                #    for y in next_heads:
                #        if y < address:
                #            fix = True
                #            break
                #    if fix == True:
                #        if self.dg.get_by_address(address+1)['head'] < address \
                #            and self.dg.get_by_address(address+2)['head'] < address \
                #                and self.dg.get_by_address(address+3)['head'] < address \
                #                    and self.dg.get_by_address(address+6)['head'] < address:
                #                    self.dg.get_by_address(address+1).update({'head': address+3})
                #                    self.dg.get_by_address(address+2).update({'head': address+3})
                #                    self.dg.get_by_address(address+3).update({'head': node['head']})
                #                    self.dg.get_by_address(address+6).update({'head': address+3})
                #                    if self.dg.get_by_address(address+1)['ctag'] == 'ADV':
                #                        self.dg.get_by_address(address+1).update({'rel': 'advmod'})
                #                    if self.dg.get_by_address(address+2)['ctag'] == 'DET':
                #                        self.dg.get_by_address(address+1).update({'rel': 'obl'})
                #                    if self.dg.get_by_address(address+3)['ctag'] == 'ADV':
                #                        self.dg.get_by_address(address+1).update({'rel': 'advmod'})
                #                    if self.dg.get_by_address(address+6)['ctag'] == 'N-D':
                #                        self.dg.get_by_address(address+1).update({'rel': 'obl'})

                if node['rel'] != 'punct':
                    self.dg.get_by_address(address).update({'rel': 'punct'})

    def _fix_empty_node(self):
        last_index = len(self.dg.nodes)-1
        for address, node in self.dg.nodes.items():
            if node['head'] == last_index:
                node['head'] = self.dg.get_by_address(last_index)['head']
        del self.dg.nodes[last_index]

    def _fix_advmod_tag(self):
        """
        A word with the deprel 'advmod' must be tagged ADV
        """

        for address, node in self.dg.nodes.items():
            if node['rel'] == 'advmod' and node['ctag'] != 'ADV':
                self.dg.get_by_address(address).update({'ctag': 'ADV'})

    def _fix_nummod_tag(self):
        """
        A word with the deprel 'nummod' must be tagged NUM
        """

        for address, node in self.dg.nodes.items():
            if node['rel'] == 'nummod' and node['ctag'] != 'NUM':
                self.dg.get_by_address(address).update({'ctag': 'NUM'})

    def _fix_mark_tag(self):
        """
        A word tagges PART must have the deprel 'mark'
        """

        for address, node in self.dg.nodes.items():
            if node['ctag'] == 'PART' and node['rel'] != 'mark':
                self.dg.get_by_address(address).update({'rel': 'mark'})

    def _fix_cconj_rel(self):

        for address, node in self.dg.nodes.items():
            if node['word'] == 'og' and node['ctag'] == 'CCONJ' and node['rel'] == 'amod':
                self.dg.get_by_address(address).update({'rel': 'cc'})

    def _fix_cc_tag(self):
        """
        A word with the deprel 'cc' cannot be tagged 'PRON' and a word cannot be dependent on it
        ie. annað hvort
        """

        for address, node in self.dg.nodes.items():
            if node['rel'] == 'cc' and node['ctag'] == 'PRON':
                self.dg.get_by_address(address).update({'ctag': 'CCONJ'}) 
                if self.dg.get_by_address(address+1)['head'] == address:
                    self.dg.get_by_address(address+1).update({'head': node['head']})

    def _fix_cc_rel(self):

        for address, node in self.dg.nodes.items():
            if node['rel'] == 'cc' and node['head'] == address-1 and self.dg.get_by_address(address+1)['head'] == address-1:
                self.dg.get_by_address(address).update({'head': address+1})
                if self.dg.get_by_address(address+1)['rel'] != 'conj':
                    self.dg.get_by_address(address+1).update({'rel': 'conj'})
                if self.dg.get_by_address(address-1)['rel'] == 'conj' and self.dg.get_by_address(address-1)['ctag'] == 'ADJ':
                    self.dg.get_by_address(address-1).update({'rel': 'amod'})
            elif node['rel'] == 'cc' and node['head'] == address+1 and self.dg.get_by_address(address+1)['head'] > address+1 and self.dg.get_by_address(address-1)['rel'] == 'amod':
                self.dg.get_by_address(address+1).update({'head': address-1}) 

    def _fix_conj_rel(self):

        try:
            for address, node in self.dg.nodes.items():
                if node['rel'] == 'conj' and node['head'] == address+1: 
                    if self.dg.get_by_address(address+1)['rel'] == 'obl': 
                        if node['ctag'] == 'NOUN':
                            self.dg.get_by_address(address).update({'rel': 'nummod'})
                        elif node['ctag'] == 'ADJ':
                            self.dg.get_by_address(address).update({'rel': 'amod'})
                        elif node['ctag'] == 'PRON':
                            self.dg.get_by_address(address).update({'rel': 'det'})
                    elif self.dg.get_by_address(address+1)['rel'] == 'nsubj':
                        if node['ctag'] == 'ADJ':
                            self.dg.get_by_address(address).update({'rel': 'amod'})
                    elif self.dg.get_by_address(address+1)['rel'] == 'amod':
                        if node['ctag'] == 'NOUN':
                            self.dg.get_by_address(address).update({'rel': 'nmod'})
                    elif self.dg.get_by_address(address+1)['rel'] == 'nmod:poss':
                        if node['ctag'] == 'ADJ':
                            self.dg.get_by_address(address).update({'rel': 'amod'})
                    elif self.dg.get_by_address(address+1)['rel'] == 'advcl':
                        if node['ctag'] == 'CCONJ':
                            self.dg.get_by_address(address).update({'rel': 'cc'})
                    elif self.dg.get_by_address(address-6)['rel'] == 'nsubj' and self.dg.get_by_address(address-6)['head'] == node['head']:
                        self.dg.get_by_address(address).update({'head': address-6})
                elif node['rel'] == 'conj' and node['head'] == address+2:
                    if self.dg.get_by_address(address+2)['rel'] in {'root', 'obl'} and self.dg.get_by_address(address+2)['ctag'] == 'NOUN':
                        if node['ctag'] == 'ADV':
                            self.dg.get_by_address(address).update({'rel': 'advmod'})
                    elif self.dg.get_by_address(address+2)['rel'] == 'ccomp':
                        if node['ctag'] == 'CCONJ':
                            self.dg.get_by_address(address).update({'rel': 'cc'})
                        elif self.dg.get_by_address(address-9)['rel'] == 'nsubj' and self.dg.get_by_address(address-9)['head'] == node['head']:
                            self.dg.get_by_address(address).update({'head': address-9})
                elif node['rel'] == 'conj' and node['head'] == address+3:
                    if self.dg.get_by_address(address+3)['rel'] == 'obl':
                        if node['ctag'] == 'VERB':
                            self.dg.get_by_address(address).update({'rel': 'amod'})
                    elif self.dg.get_by_address(address+3)['rel'] == 'nsubj':
                        if node['ctag'] == 'NOUN':
                            self.dg.get_by_address(address).update({'rel': 'nmod'})
                    elif self.dg.get_by_address(address+3)['rel'] == 'advcl':
                        if node['ctag'] == 'NOUN':
                            self.dg.get_by_address(address).update({'rel': 'nmod'})
                    elif self.dg.get_by_address(address+3)['rel'] == 'ccomp':
                        if self.dg.get_by_address(address-5)['rel'] == 'nsubj':
                            self.dg.get_by_address(address).update({'head': address-5})
                elif node['rel'] == 'conj' and node['head'] == address+4:
                    if self.dg.get_by_address(address+4)['rel'] == 'obl':
                        if node['ctag'] == 'ADV':
                            self.dg.get_by_address(address).update({'rel': 'advmod'})
                    elif self.dg.get_by_address(address+4)['rel'] == 'ccomp':
                        if self.dg.get_by_address(address-3)['rel'] == 'nsubj' and self.dg.get_by_address(address-3)['head'] == node['head']:
                            self.dg.get_by_address(address).update({'head': address-3})
                elif node['rel'] == 'conj' and node['head'] == address+5:
                    if self.dg.get_by_address(address+5)['rel'] == 'obl' and self.dg.get_by_address(address-4)['rel'] == 'nsubj' and self.dg.get_by_address(address-4)['head'] == node['head']:
                        self.dg.get_by_address(address).update({'head': address-4})
                elif node['rel'] == 'conj' and node['head'] == address+6:
                    if self.dg.get_by_address(address+6)['rel'] == 'ccomp' and self.dg.get_by_address(address-5)['rel'] == 'nsubj' and self.dg.get_by_address(address-5)['head'] == node['head']:
                        if node['ctag'] == 'NOUN':
                            self.dg.get_by_address(address).update({'head': address-5})
                elif node['rel'] == 'conj' and node['head'] == address+7:
                    if self.dg.get_by_address(address+7)['rel'] == 'ccomp' and self.dg.get_by_address(address-3)['rel'] == 'nsubj' and self.dg.get_by_address(address-3)['head'] == node['head']:
                        self.dg.get_by_address(address).update({'head': address-3})
                elif node['rel'] == 'conj' and node['head'] == address+13:
                    if self.dg.get_by_address(address+13)['rel'] == 'root' and self.dg.get_by_address(address-7)['word'] == 'þegar' and self.dg.get_by_address(address-7)['head'] == address:
                        self.dg.get_by_address(address).update({'rel': 'advcl'})
                elif node['rel'] == 'conj' and node['head'] > address+13:
                    if node['ctag'] == 'NOUN':
                        self.dg.get_by_address(address).update({'rel': 'dislocated'})
        except RuntimeError:
            print(node)
            raise

    def _fix_punct_tag(self):
        """
        A word with the deprel 'punct' must be tagged PUNCT
        """

        for address, node in self.dg.nodes.items():
            if node['rel'] == 'punct' and node['ctag'] != 'PUNCT':
                self.dg.get_by_address(address).update({'ctag': 'PUNCT'})

    def _fix_punct_rel(self):
        """
        A word with the tag PUNCT must have the deprel 'punct'
        """

        for address, node in self.dg.nodes.items():
            if node['ctag'] == 'PUNCT' and node['rel'] != 'punct':
                self.dg.get_by_address(address).update({'rel': 'punct'})

    def _fix_flatname_dep(self):
        """
        Finds and fixes a fixed phrase, flat:name
        """

        for address, node in self.dg.nodes.items():
            if node['ctag'] == 'PROPN' and self.dg.get_by_address(address-1)['ctag'] == 'PROPN' and node['head'] == address-1 \
            and node['rel'] != 'flat:name':
                self.dg.get_by_address(address).update({'rel': 'flat:name'})
                #if self.dg.get_by_address(address+1)['ctag'] == 'PROPN' and self.dg.get_by_address(address+1)['rel'] == 'dep' and self.dg.get_by_address(address+1)['head'] == node['head']:
                #    self.dg.get_by_address(address+1).update({'rel': 'flat:name'})

    def _fix_mark_dep(self):
        """
        Finds a fixed phrase and fixes its deprel
        """

        for address, node in self.dg.nodes.items():
            if node['rel'] == 'mark' and node['ctag'] == 'SCONJ' and self.dg.get_by_address(address+1)['rel'] == 'mark' and self.dg.get_by_address(address+1)['ctag'] == 'SCONJ':
                self.dg.get_by_address(address+1).update({'rel': 'fixed'})
                if self.dg.get_by_address(address+1)['head'] != address:
                    self.dg.get_by_address(address+1).update({'head':address})
                if self.dg.get_by_address(address+2)['rel'] == 'mark' and self.dg.get_by_address(address+2)['ctag'] == 'SCONJ' and self.dg.get_by_address(address+2)['head'] == address+1:
                    self.dg.get_by_address(address+2).update({'rel': 'fixed'})
                    self.dg.get_by_address(address+2).update({'head': address})
            elif node['rel'] == 'mark' and node['ctag'] == 'SCONJ' and node['word'] == 'sem' and self.dg.get_by_address(address-1)['word'] == 'svo':
                self.dg.get_by_address(address).update({'head':address-1})
                self.dg.get_by_address(address).update({'rel':'fixed'})
                #if self.dg.get_by_address(address+1)['word'] == 'að' and self.dg.get_by_address(address+1)['ctag'] == 'PART'

    def _fix_dep(self):
        """
        Fixes the second noun's deprel in a CONJP
        """

        for address, node in self.dg.nodes.items():
            if node['rel'] == 'dep':
                if self.dg.get_by_address(address-1)['ctag'] == 'CCONJ' and self.dg.get_by_address(address-2)['ctag'] == r'N[PRS-NADG]':
                    self.dg.get_by_address(address).update({'rel': 'conj'})

    def _fix_root_tag(self):
        """
        Changes a verb's tag from AUX to VERB if it is the root of the sentence
        """

        for address, node in self.dg.nodes.items():
            if node['rel'] == 'root' and node['ctag'] == 'AUX':
                self.dg.get_by_address(address).update({'ctag': 'VERB'})

    def _fix_head_id_same(self):
        """
        Changes a node's head if it is dependent on itself
        """
        
        try:
            for address, node in self.dg.nodes.items():
                    if node['address'] == node['head']:
                        if self.dg.get_by_address(address-12)['ctag'] == 'VERB':
                            self.dg.get_by_address(address).update({'head': address-12})
                        elif self.dg.get_by_address(address-4)['ctag'] == 'VERB':
                            self.dg.get_by_address(address).update({'head': address-4})
                        elif self.dg.get_by_address(address-3)['ctag'] == 'VERB':
                            self.dg.get_by_address(address).update({'head': address-3})
                        elif self.dg.get_by_address(address-2)['ctag'] == 'VERB':
                            self.dg.get_by_address(address).update({'head': address-2})
                        elif self.dg.get_by_address(address-1)['ctag'] == 'VERB':
                            self.dg.get_by_address(address).update({'head': address-1})
                        elif self.dg.get_by_address(address+1)['ctag'] == 'VERB':
                            self.dg.get_by_address(address).update({'head': address+1})
                        elif self.dg.get_by_address(address+2)['ctag'] == 'VERB':
                            self.dg.get_by_address(address).update({'head': address+2})
                        elif self.dg.get_by_address(address+3)['ctag'] == 'VERB':
                            self.dg.get_by_address(address).update({'head': address+3})
                        elif self.dg.get_by_address(address+4)['ctag'] == 'VERB':
                            self.dg.get_by_address(address).update({'head': address+4})
        except RuntimeError:
            pass
            #print(self.dg.nodes.items())
            #raise

    def _fix_flat_foreign(self):

        try:
            for address, node in self.dg.nodes.items():
                if node['ctag'] == 'X': 
                    if self.dg.get_by_address(address+1)['head'] == address and self.dg.get_by_address(address+1)['ctag'] == 'PROPN':
                        self.dg.get_by_address(address+1).update({'rel': 'flat:foreign'})
                    elif node['head'] > address:
                        self.dg.get_by_address(address).update({'rel': 'dep'})
                    elif self.dg.get_by_address(address-1)['head'] == address and self.dg.get_by_address(address-1)['ctag'] == 'ADP':
                        self.dg.get_by_address(address-1).update({'rel': 'dep'})
                
        except RuntimeError:
            pass
            #print(self.dg.nodes.items())
            #raise

    def _fix_left_right_alignments(self):

        #rels = {'conj', 'fixed', 'flat:name', 'flat:foreign', 'goesWith'}

        for address, node in self.dg.nodes.items():
            if node['rel'] == 'conj' and node['head'] > address:
                #if self.dg.get_by_address(address-2)['ctag'] in {'ADJ', 'N.*'} and self.dg.get_by_address(address-1)['ctag'] == 'CCONJ':
                #    self.dg.get_by_address(address).update({'head': address-2})
                if self.dg.get_by_address(address-5)['rel'] == 'nsubj' and self.dg.get_by_address(address-5)['head'] == node['head']:
                    self.dg.get_by_address(address).update({'head': address-5})
                elif self.dg.get_by_address(address-9)['rel'] == 'nsubj' and self.dg.get_by_address(address-5)['head'] == node['head']:
                    self.dg.get_by_address(address).update({'head': address-9})

                #self.dg.get_by_address(address).update({'rel': 'HALLO'})

  #def _fix_foreign_rels(self):

#        for address, node in self.dg.nodes.items():
#            if node['rel'] == 'flat:foreign' and node['head'] > address:

    def _fix_appos_lr(self):

        for address, node, in self.dg.nodes.items():
            if self.dg.get_by_address(address)['rel'] == 'appos' and self.dg.get_by_address(address)['head'] > address:
                head_address = self.dg.get_by_address(address)['head']
                if self.dg.get_by_address(head_address)['ctag'] in {'VERB', 'AUX'}:
                    self.dg.get_by_address(address).update({'rel': 'obl'})
                elif self.dg.get_by_address(head_address)['ctag'] in {'NOUN', 'PROPN', 'PRON', 'ADJ'}:
                    self.dg.get_by_address(address).update({'rel': 'nmod'})

    def _fix_cop_head(self):
        """
        A copula cannot be head. If so, the dependents' head addresses are changed to the head's head address
        """

        for address, node in self.dg.nodes.items():
            if node['head'] != '_':
                headaddress = node['head']
                if self.dg.get_by_address(headaddress)['rel'] == 'cop':
                    head_headaddress = self.dg.get_by_address(headaddress)['head']
                    self.dg.get_by_address(address).update({'head': head_headaddress})

    def _fix_zero_dep(self):

        for address, node in self.dg.nodes.items():
            if node['rel'] != 'root' and node['head'] == 0:
                if node['rel'] == 'cc' and self.dg.get_by_address(address+1)['head'] == 0 and self.dg.get_by_address(address+3)['head'] == 0:
                    if self.dg.get_by_address(address+1)['rel'] == 'advmod' and self.dg.get_by_address(address+3)['rel'] == 'obl':
                        self.dg.get_by_address(address).update({'head': address+1})
                        self.dg.get_by_address(address+1).update({'head': address-1})
                        self.dg.get_by_address(address+3).update({'head': address+1})

    def _fix_many_subj(self):
        """
        If subjects of a verb are more than one, the ones following the first subject get the deprel 'obl'
        """

        #for address, node in self.dg.nodes.items():
        #    if self.dg.get_by_address(address)['rel'] == 'nsubj':
        #        head_verbs_head = self.dg.get_by_address(address)['head']
        #        break

        #print(self.dg.num_subj())
        nsubj = self.dg.num_subj()

        if nsubj:
            count = 0
            for address, node in self.dg.nodes.items():
                if node['word'] in nsubj:
                    if count == 0:
                        count += 1
                    elif count > 0:
                        self.dg.get_by_address(address).update({'rel': 'obl'})

#        count = 0
#        for address, node in self.dg.nodes.items():
#            if self.dg.get_by_address(address)['rel'] == 'nsubj' and count == 0:
#                count += 1
#                head_verbs_head = self.dg.get_by_address(address)['head']
#            if self.dg.get_by_address(address)['rel'] == 'nsubj' and count >= 1 \
#                and self.dg.get_by_address(address-1)['ctag'] in {'PUNCT', 'CCONJ'} and self.dg.get_by_address(address)['head'] == head_verbs_head:
#                self.dg.get_by_address(address).update({'rel': 'obl'})
#                count += 1

    #def _fix_det_mark(self):

    #    for address, node in self.dg.nodes.items():
    #        if node['ctag'] == 'DET' and node['rel'] == 'mark':
    #            self.dg.get_by_address(address).update({'ctag':''})


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
            t = tree.remove_nodes(tags=['CODE'], trace=True)
        else:
            t = IndexedCorpusTree.fromstring(tree, trim_id_tag=True, preprocess=True).remove_nodes(tags=['CODE'], trace=True)
        if self.auto_tags:
            TAG_DICT = self._get_tag_dict(t)

        self.dg = UniversalDependencyGraph()

        if t.corpus_id == None:
            self.dg.original_ID = 'ID_MISSING'
        else:
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
                if t[i][0] in {'0', '*', '{','<'}:   #if t[1].pos()[0][0] in {'0', '*'}:
                    continue

                
                if '---' in t[i]:
                    FORM = LEMMA = '-'
                    # tag = tag_list[nr]
                
                elif '-' in t[i]:
                    # if leaf is for whatever reason a single symbol with no 
                    # hyphen treat seperately
                    if len(t[i]) == 1:
                        FORM = LEMMA = tag = tag_list[nr]
                    # If terminal node with no label (token-lemma)
                    # e.g. tók-taka
                    else:
                        FORM = decode_escaped(t[i].split('-', 1)[0])
                        LEMMA = decode_escaped(t[i].split('-', 1)[1])
                        # tag = tag_list[nr]
                elif t[i][0] in {'<dash/>', '<dash>', '</dash>',}:
                    FORM = LEMMA = '-'
                    # tag = tag_list[nr]
                else: # If no lemma present
                    FORM = t[i]
                    LEMMA = None
                tag = tag_list[nr]
                if '+' in tag:
                    tag = re.sub('\w+\+', '', tag)
                if '21' in tag:
                    tag = re.sub('21', '', tag)
                elif '22' in tag:
                    tag = re.sub('22', '', tag)
                elif '31' in tag:
                    tag = re.sub('31', '', tag)
                elif '32' in tag:
                    tag = re.sub('32', '', tag)
                elif '33' in tag:
                    tag = re.sub('33', '', tag)
                elif tag.endswith('TTT'):
                    tag = re.sub('-TTT', '', tag)
                # token_lemma = str(FORM+'-'+LEMMA)
                XPOS = tag
                MISC = defaultdict(lambda: None)
                # Feature Classes called here
                if self.faroese:
                    #print('HALLO')
                    UPOS = Features.get_UD_tag(tag, True)
                else:
                    UPOS = Features.get_UD_tag(tag, False)
                if self.auto_tags:
                    # ifd tag found from POS tagger output
                    ifd_tag = TAG_DICT.get(FORM, 'x')[0]
                    if ifd_tag == None:
                        if UPOS == 'PRON':
                            ifd_tag = 'fp2en'
                        else:
                            for w, tl in TAG_DICT.items():
                                if tl[1] == LEMMA:
                                    ifd_tag = tl[0]
                                else:
                                    ifd_tag = 'x'
                    if LEMMA == None:
                        # print(TAG_DICT.get(re.sub(r'\$', '', FORM), '_'))
                        # print(FORM)
                        try:
                            LEMMA = TAG_DICT.get(re.sub(r'\$', '', FORM), '_')[1]
                        except IndexError:
                            LEMMA = '_'
                    FEATS = Features(ifd_tag).features
                    MISC = defaultdict(lambda: None, {'IFD_tag': ifd_tag})
                elif self.faroese:
                    FEATS = FO_Features(tag).get_features()
                    #print(FEATS)
                    #print(type(FEATS))
                    MISC = defaultdict(lambda: None)
                else:
                    FEATS = ICE_Features(tag).get_features()
                    MISC = defaultdict(lambda: None)
                if FORM not in {'None', None}:
                    self.dg.add_node({'address': nr,
                                      'word': FORM,
                                      'lemma': LEMMA,
                                      'ctag': UPOS, # upostag
                                      'tag': XPOS,   # xpostag
                                      'feats': FEATS,
                                      'deps': defaultdict(list),
                                      'rel': '_',
                                      'misc': MISC})
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
                            #self.dg.get_by_address(mod_nr).update({'head': head_nr, 'rel': 'dep'})
                            self.dg.get_by_address(mod_nr).update({'head': head_nr, 'rel': self._relation(mod_tag, head_tag)})
                            self.dg.root = self.dg.get_by_address(mod_nr)

                            # print(self.dg.get_by_address(mod_nr))

                        # elif head_tag.endswith('=1'):
                            # # DEBUG:
                            # print(head_tag)
                            # print(self.dg.root)
                            # input()

                    elif child[0] == '0' or '*' in child[0] or '{' in child[0] or child[0][0] == '<' or mod_tag == 'CODE':
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

        # # self.add_space_after()
        # self._features()

        # NOTE: Here call method to fix dependency graph if needed?
        if self.dg.num_roots() != 1:

            # # DEBUG:
            # print(self.dg.to_conllU())
            # input()

            self._fix_root_relation()

        # for address, node in self.dg.nodes.items():
        #     if node['rel'] in {'aux', 'aux:pass'} and node['tag'] != 'AUX':
        #         node.update({'ctag': 'AUX'})

        rel_counts = self.dg.rels()
        ctag_counts = self.dg.ctags()

        if rel_counts['ccomp/xcomp'] > 0:
            self._fix_ccomp()
        if rel_counts['nsubj'] > 1:
            self._fix_many_subj()
        
        #self._fix_left_right_alignments()
        
        # if rel_counts['aux'] > 0:
        #     self._fix_aux_tag()
        if rel_counts['acl/advcl'] > 0:
            self._fix_acl_advcl()
        if rel_counts['punct'] > 0:
            self._fix_punct_heads()
            self._fix_punct_tag()
        if rel_counts['aux'] > 0:
            self._fix_aux_tag()
        if rel_counts['advmod'] > 0:
            self._fix_advmod_tag()
        if rel_counts['nummod'] > 0:
            self._fix_nummod_tag()
        if ctag_counts['PROPN'] > 0:
            self._fix_flatname_dep()
        if rel_counts['mark'] > 0:
            self._fix_mark_dep()
        if rel_counts['rel'] > 0:
            self._fix_dep()
        if ctag_counts['AUX'] > 0:
            self._fix_root_tag()
        self._fix_head_id_same()
        if ctag_counts['X'] > 0:
            self._fix_flat_foreign()
        if ctag_counts['CCONJ'] > 0:
            self._fix_cconj_rel()
        if rel_counts['cop'] > 0:
            self._fix_cop_head()
        if rel_counts['appos'] > 0:
            self._fix_appos_lr()
        if rel_counts['cc'] > 0:
            self._fix_cc_tag()
            #self._fix_cc_rel()
            self._fix_zero_dep()
        if rel_counts['conj'] > 0:
            self._fix_conj_rel()
        if ctag_counts['PUNCT'] > 0:
            self._fix_punct_rel()


        # if self.dg.get_by_address(len(self.dg.nodes)-1)['word'] == None:
        #     self._fix_empty_node()

        # if rel_counts['cop'] > 0:
        #     self._fix_cop()

        return self.dg
    
            
    @staticmethod
    def check_left_to_right(dgraph):
        """
        Certain UD relations must always go left-to-right.
        """
        for address in dgraph.addresses():
            cols = dgraph.get_by_address(address)
            if re.match(r'^[1-9][0-9]*-[1-9][0-9]*$', str(cols['address'])):
                continue
            # if DEPREL >= len(cols):
            #     return # this has been already reported in trees()
            # According to the v2 guidelines, apposition should also be left-headed, although the definition of apposition may need to be improved.
            if re.match(r"^(conj|fixed|flat|goeswith|appos)", cols['rel']):
                ichild = int(cols['address'])
                iparent = int(cols['head'])
                if ichild < iparent:
                    # We must recognize the relation type in the test id so we can manage exceptions for legacy treebanks.
                    # For conj, flat, and fixed the requirement was introduced already before UD 2.2, and all treebanks in UD 2.3 passed it.
                    # For appos and goeswith the requirement was introduced before UD 2.4 and legacy treebanks are allowed to fail it.
                    # testid = "right-to-left-%s" % lspec2ud(cols['rel'])
                    testmessage = 'Line %s: Relation %s must go left-to-right.\nWord form: %s' % (address, cols['rel'], cols['word'])
                    print(testmessage)

    @staticmethod
    def check_left_to_right(dgraph):
        """
        Certain UD relations must always go left-to-right.
        """
        for address in dgraph.addresses():
            cols = dgraph.get_by_address(address)
            if re.match(r'^[1-9][0-9]*-[1-9][0-9]*$', str(cols['address'])):
                continue
            # if DEPREL >= len(cols):
            #     return # this has been already reported in trees()
            # According to the v2 guidelines, apposition should also be left-headed, although the definition of apposition may need to be improved.
            if re.match(r"^(conj|fixed|flat|goeswith|appos)", cols['rel']):
                ichild = int(cols['address'])
                iparent = int(cols['head'])
                if ichild < iparent:
                    # We must recognize the relation type in the test id so we can manage exceptions for legacy treebanks.
                    # For conj, flat, and fixed the requirement was introduced already before UD 2.2, and all treebanks in UD 2.3 passed it.
                    # For appos and goeswith the requirement was introduced before UD 2.4 and legacy treebanks are allowed to fail it.
                    # testid = "right-to-left-%s" % lspec2ud(cols['rel'])
                    testmessage = 'Line %s: Relation %s must go left-to-right.\nWord form: %s' % (address, cols['rel'], cols['word'])
                    print(testmessage)


    @staticmethod
    def add_space_after(dgraph):
        """10.03.20
        Fills in Space_after feature in misc column.

        """

        for address in dgraph.addresses():
            # print(dgraph.get_by_address(address)['word'])
            id_to_fix = int(address) - 1
            if dgraph.get_by_address(address)['ctag'] == 'PUNCT':
                # id_to_fix = int(address) - 1
                if id_to_fix < 0:
                    continue
                elif dgraph.get_by_address(address)['ctag'] == '„':
                    dgraph.get_by_address(address)['misc']['SpaceAfter'] = 'No'
                elif dgraph.get_by_address(id_to_fix)['lemma'] in {'„', ':', '|'} or address == '1':
                    continue
                else:
                    dgraph.get_by_address(id_to_fix)['misc']['SpaceAfter'] = 'No'
            # adding space after word ending in $. Needs better fix
            elif dgraph.get_by_address(address)['word'].endswith('$') and dgraph.get_by_address(address)['ctag'] not in {'VERB', 'AUX', 'SCONJ'}:
                dgraph.get_by_address(address)['misc']['SpaceAfter'] = 'No'

        return dgraph


    @staticmethod
    def join_graphs(to_join):
        """
        Takes in a list of UniversalDependencyGraph objects and joins them into
        a single UniversalDependencyGraph object, taking into account correct
        relations and deps.


        Arguments:
            to_join (list): List of dependencyGraphs that are to be joined.
        Returns:
            new_dg (UniversalDependencyGraph): New dependency graph of they
                the joined sentences.

        """

        # for dg in to_join:
        #     print(dg.to_conllU())
        new_dg = to_join[0]
        # print('==NEW==')
        # print(new_dg.to_conllU())
        new_dg.original_ID = [str(dg.original_ID) for dg  in to_join]
        for node in new_dg.nodes.values():
            if node['head'] == 0:
                new_root = node['address']
        new_id = len(new_dg.nodes)
        for old_dg in to_join[1:]:
            # print('==OLD==')
            # print(old_dg.to_conllU())
            old_new_addresses = {}
            for node in old_dg.nodes.values():
                old_new_addresses[node['address']] = new_id
                if node['address'] == None or node['word'] in {'None', None}:
                    continue
                else:
                    node.update({'address': new_id})
                new_id +=1
            for node in old_dg.nodes.values():
                if node['address'] == 0 or node['tag'] == 'TOP' or node['word'] in {'None', None}:
                    # print(node)
                    continue
                if node['head'] == 0:
                    node.update({'head': new_root, 'rel':'conj', 'misc':{'OriginalHead':'0'}})
                    if node['ctag'] == 'PUNCT':
                        node.update({'rel' : 'punct'})
                    # TODO: fix misc, erases previous
                else:
                    # print(node)
                    try:
                        node.update({'head' : old_new_addresses[node['head']]})
                    except KeyError:
                        print(node)
                        for x in to_join:
                            print(x.plain_text())
                        #print(list(to_join))
                        print(node['head'])
                        raise

                new_dg.add_node(node)

        # TODO: fix deps:
        # for node in new_dg.nodes.values():
        #     node.update({'deps' : None})
        # for i in range(len(new_dg.nodes)+1):
        #     new_dg.add_arc(new_dg.get_by_address(i)['head'], i)
        # print(new_dg)

        return new_dg



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
