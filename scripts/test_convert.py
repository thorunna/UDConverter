# -*- coding: utf-8 -*-

'''06.03.20

Hinrik Hafsteinsson (hih43@hi.is)
Þórunn Arnardóttir (tha86@hi.is)
Debugging script for use with depender.py module
Part of UniTree project for IcePaHC
'''

import os
import re
from sys import argv

from nltk.corpus.util import LazyCorpusLoader
from nltk.data import path

from lib import relations, depender
from lib.reader import IcePaHCFormatReader


path.extend(['../testing/'])

ICEPAHC = LazyCorpusLoader(
    'icecorpus/psd/', IcePaHCFormatReader,
    r'.*\.psd', cat_pattern=r'.*(nar|rel|sci|bio|law)\-.*'
    )

TREE = ''

INPUT_ID = argv[1]
file_id = INPUT_ID.split(',')[0].lower()+'.psd'
tree_num = INPUT_ID.split(',')[1]

for tree in ICEPAHC.parsed_sents(file_id):
    if tree.corpus_id_num == tree_num:
        TREE = tree


# def main(infile):
#     '''05.03.20
#     Test case for debugging head choice algorithm
#     Prints output to command line. Used in tandem with debug lines in depender.py
#
#     Args:
#         infile (string): Path to input file.
#
#     '''
#     c = depender.Converter()
#     psd = ''
#     with open(infile) as file:
#         for line in file:
#             psd += line
#             if len(line.strip()) == 0:
#                 dep = c.create_dependency_graph(psd)
#                 print(dep.plain_text())
#                 print(dep.to_conllU())
#                 input()
#                 psd = ''

def main(tree):
    '''05.03.20
    Test case for debugging head choice algorithm
    Prints output to command line. Used in tandem with debug lines in depender.py

    Args:
        infile (string): Path to input file.

    '''
    print(tree)
    c = depender.Converter()
    dep = c.create_dependency_graph(tree)
    print(dep.plain_text())
    print(dep.to_conllU())
    input()
    psd = ''


if __name__ == '__main__':
    main(TREE)
