

"""25.03.20
Script for getting tree from IcePaHC by sentence ID.

Usage:
python3 get_tree.py 2008.OFSI.NAR-SAG,.13

Prints tree .13 from 2008.ofsi.nar.psd file.

"""

import os
import re
from sys import argv
from nltk.corpus.util import LazyCorpusLoader
from nltk.data import path

from lib.reader import IcePaHCFormatReader

path.extend(['../testing/'])

ICEPAHC = LazyCorpusLoader(
    'icecorpus/psd/', IcePaHCFormatReader,
    r'.*\.psd', cat_pattern=r'.*(nar|rel|sci|bio|law)\-.*'
    )

INPUT_ID = argv[1]
file_id = INPUT_ID.split(',')[0].lower()+'.psd'
tree_num = INPUT_ID.split(',')[1]

for tree in ICEPAHC.parsed_sents(file_id):
    if tree.corpus_id_num == tree_num:
        print(tree)
