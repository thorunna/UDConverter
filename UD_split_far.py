import pyconll
import os
import re
import sys
import glob

path = 'CoNLLU/farpahc/1928.ntacts.rel-bib.conllu'
"""
for file in os.listdir(path):
    sent_count = 0
    conll = pyconll.iter_from_file(os.path.join(path, file))
    for sentence in conll:
        sent_count += 1
    #print(file, sent_count)
"""
PREFIXES = ['dev', 'test']

output_file = f'fo_farpahc-ud-dev.conllu'
print(f'Writing to file: {output_file}')
with open(output_file, 'w+') as f:
    conll = pyconll.iter_from_file(os.path.join(path))
    sent_count = 0
    for sentence in conll:
        sent_count += 1
        f.write(sentence.conll())
        f.write('\n\n')
        if sent_count == 300:
            break

output_file = f'fo_farpahc-ud-test.conllu'
print(f'Writing to file: {output_file}')
with open(output_file, 'w+') as f:
    conll = pyconll.iter_from_file(os.path.join(path))
    sent_count = 0
    for sentence in conll:
        sent_count += 1
        if sent_count >= 301:
            f.write(sentence.conll())
            f.write('\n\n')


path_tr = 'CoNLLU/farpahc/1936.ntjohn.rel-bib.conllu'

output_file = f'fo_farpahc-ud-train.conllu'
print(f'Writing to file: {output_file}')
with open(output_file, 'w+') as f:
    conll = pyconll.iter_from_file(os.path.join(path_tr))
    for sentence in conll:
        f.write(sentence.conll())
        f.write('\n\n')