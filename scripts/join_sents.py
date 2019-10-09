import os
import re
from pprint import pprint
import pyconll
from collections import defaultdict

from lib.joiners import SentJoiner, FileWriter



# class SentJoiner():
#     '''
#     '''
#     def __init__(self, file):
#         self.lines = file.readlines()
#         self.line_indexes = range(len(self.lines))
#         self.last_num = None
#         self.name = os.path.basename(file.name)
#         self.joined_sents = []
#         self.sent_num = 0
#         self.new_token_ID = 0
#         self.old_new_tokens = defaultdict(None)
#         self.token_key = None
#         self.first_root = None
#         self.lines = []
#
#
#     def _join_sents(self):
#         joined = ''
#         for i in self.line_indexes:
#             # self.lines[i] = self.lines[i].split('\t')
#             if self.lines[i][0] in {'#', '\n'}: continue
#             # elif self.lines[i+1]: # for catching eof
#             if re.search(r'^1\t[A-ZÞÆÐÖÁÉÝÚÍÓ]', self.lines[i]):
#                 # self.joined_sents.append(new_sent)
#                 # new_sent = ''
#                 joined += '\n'
#                 joined += self.lines[i]
#             else:
#                 joined += self.lines[i]
#         # self.joined_sents = [pyconll.load_from_string(sentence) for sentence in corpus.joined_sents]
#         self.joined_sents = joined
#
#     def _set_sent_ID(self):
#         ID = '%s_%s' % (corpus.name, self.sent_num)
#         return ID
#
#     def _get_keys(self):
#         self.token_key = token.form + '-' + token.id
#
#     def _set_token_IDs(self, sentence):
#         subsentence = 0
#         for token in sentence:
#             if token.id == '1':
#                 subsentence += 1
#             self.new_token_ID += 1
#             placeholder_ID = '.'.join([token.id, str(self.new_token_ID), str(subsentence)])
#             # print(token.id, token.form)
#             self.token_key = '-'.join([token.form, placeholder_ID, str(subsentence)])
#             # self.new_token_ID += 1
#             if int(token.id) != self.new_token_ID:
#                 self.old_new_tokens[token.id] = token.form, str(self.new_token_ID)
#                 token.id = placeholder_ID
#                 # print('Old:', token.id, token.form)
#                 # print('New:', token.id, token.form)
#                 # print('\t', token.id)
#         for token in sentence:
#             if not '.' in token.id:
#                 print(token.conll())
#                 if token.deprel == 'root':
#                     self.first_root = token.id
#             else:
#                 try:
#                     token.head = self.old_new_tokens[token.head][1]
#                     print(token.conll())
#                 except KeyError:
#                     token.head = self.first_root
#                     token.deprel = 'conj'
#                     print(token.conll())
#
#         return sentence
#
#     def _add_to_fixed(sent):
#         self.lines.append(sent)
#
#     def set_vars(self):
#         '''
#         Sets all object attributes for CoNLL-U file
#         '''
#         # sentences joined based on punctuation
#         self._join_sents()
#         # CoNLL-U object read from string as iterable
#         conll = pyconll.iter_from_string(corpus.joined_sents) # reads sentence
#         # iterated through sentences
#         for sentence in conll:
#             self.sent_num += 1
#             # function called to set sentence ID
#             sentence.id = self._set_sent_ID()
#             # function called to set token IDs and fix dependency heads
#             sentence = self._set_token_IDs(sentence)
#             # new token ID attribute zeroed out
#             self.new_token_ID = 0
#             # print(sentence.conll())
#             print(self.old_new_tokens)
#
#             input()
#             self.old_new_tokens = defaultdict(None)

# with open('fyrsta_fyrsta.conllu', 'r') as file:
with open('testing/CoNLLU_output/1150.homiliubok.rel-ser.conllu', 'r') as file:

    corpus = SentJoiner(file)
    corpus.set_vars()

    # conll = pyconll.iter_from_string(corpus.joined_sents)
    # for i in corpus.lines:
    #     print(i)
    #     input()
    f = FileWriter(corpus)
    f.write_to_file(sepdir=True, overwrite=False)
    # for sentence in conll:
    #     counter += 1
    #     sentence.id = '%s_%s' % (corpus.name, counter)
    #     print(sentence.id)
