import os
import glob
import re

origdir = 'CoNLLU/additions2019/althingi'
corrdir = 'Manual_correction/additions2019/althingi'


def collect_filenames(directory, abspath=True):
    os.chdir(directory)
    conlluFiles = glob.glob("**/*.conllu", recursive=True)
    conlluFiles = [f for f in conlluFiles if f != None]
    if abspath == True:
        conlluFiles = [os.path.abspath(f) for f in conlluFiles]
    os.chdir('../../../')
    return conlluFiles 

orig_set = set(collect_filenames(origdir, False))
corr_set = set(collect_filenames(corrdir, False))

file_names = orig_set.intersection(corr_set)

def run_diff(orig_files, corr_files):
    for file in corr_files:
        name = file.split('Manual_correction/')[1]
        for orig_file in orig_files:
            orig_name = orig_file.split('CoNLLU/')[1]
            if orig_name == name:
                output = 'diff/' + name.split('/')[-1]
                os.system('diff '+orig_file+' '+file+' > '+output)

def get_results(diff_file):
    f = open(diff_file, 'r')
    lines = f.read()
    #print(lines)
    spl = re.split('\d+[,\w\d]+\n', lines)
    pairs = []
    #print(spl)
    for s in spl:
        if s != None or s != ' ':
            try:
                pairs.append((s.split('---')[0], s.split('---')[1]))
            except IndexError:
                print(s)
                pass
                #raise

orig_filenames = collect_filenames(origdir)
corr_filenames = collect_filenames(corrdir)
full_filenames = collect_filenames('CoNLLU/additions2019')

import pyconll
import collections

sents = {}

for file in corr_filenames:
    corpus = pyconll.load_from_file(file)
    for sentence in corpus:
        nl = []
        for token in sentence:
            nl.append((token.id, token.form, token.head, token.deprel))
        sents[sentence.id] = nl
        

#print(sents)

sents_orig = {}

for file in orig_filenames:
    name = file.split('althingi/')[1]
    if name in file_names:
        corpus = pyconll.load_from_file(file)
        for sentence in corpus:
            nl = []
            for token in sentence:
                nl.append((token.id, token.form, token.head, token.deprel))
            sents_orig[sentence.id] = nl

sents_orig_althingi = {}

for file in orig_filenames:
    corpus = pyconll.load_from_file(file)
    for sentence in corpus:
        nl = []
        for token in sentence:
            nl.append((token.id, token.form, token.head, token.deprel))
        sents_orig_althingi[sentence.id] = nl

sents_orig_full = {}

for file in full_filenames:
    try:
        corpus = pyconll.load_from_file(file)
    except:
        pass
    for sentence in corpus:
        nl = []
        for token in sentence:
            nl.append((token.id, token.form, token.head, token.deprel))
        sents_orig_full[sentence.id] = nl

print('\n')
print('Total no. of sentences in additions2019: ', len(sents_orig_full))

no_toks = 0

for sent, toks in sents_orig_full.items():
    no_toks += len(toks)

print('Total no. of tokens in additions2019: ', no_toks)

print('\n')
print('Total no. of sentences in althingi: ', len(sents_orig_althingi))

no_toks = 0

for sent, toks in sents_orig_althingi.items():
    no_toks += len(toks)

print('Total no. of tokens in althingi: ', no_toks)

#print(sents_orig)

comp = {}

for sent, toks in sents.items():
    for orig_sent, orig_toks in sents_orig.items():
        if sent == orig_sent:
            comp[sent] = zip(toks, orig_toks)

#for x, y in comp.items():
#    print(x, list(y))

head_deprel = 0
head = 0
head_info = collections.defaultdict(int)
deprel = 0
deprel_info = collections.defaultdict(int)

obl = 0
acl = 0
case = 0
amod = 0
advmod = 0
dep = 0
ccomp = 0
advcl = 0
compound = 0
conj = 0
punct = 0
cop = 0
cc = 0
nsubj = 0
mark = 0
aux = 0
obj = 0

corr_deprels = collections.defaultdict(int)

for sent, zipped in comp.items():
    for el in zipped:
        corr = el[0]
        orig = el[1]
        corr_head = corr[2]
        corr_deprel = corr[3]
        orig_head = orig[2]
        orig_deprel = orig[3]
        corr_deprels[orig_deprel] += 1
        if corr_head != orig_head and corr_deprel != orig_deprel:
            #print('Hvorki haus né deprel eru eins')
            #if corr_deprel != 'punct':
            head_deprel += 1
        if corr_head != orig_head and corr_deprel == orig_deprel:
            #print('Haus er ekki sá sami')
            #if corr_deprel != 'punct':
            head += 1
            head_info[orig_deprel] += 1
        if corr_deprel != orig_deprel and corr_head == orig_head:
            #print('Deprel er ekki það sama')
            #if corr_deprel != 'obl:arg':
            deprel += 1
            deprel_info[orig_deprel] += 1

for k, v in head_info.items():
    v_upd = (v / corr_deprels[k])*100
    head_info[k] = v_upd

for k, v in deprel_info.items():
    v_upd = (v / corr_deprels[k])*100
    deprel_info[k] = v_upd

print('No. of manually-corrected sentences: ', len(sents))

no_toks_corr = 0

for sent, toks in sents.items():
    no_toks_corr += len(toks)

print('Total no. of manually-corrected tokens: ', no_toks_corr)

print('\n')
print('Both head and deprel wrong: ', head_deprel)
print('Head wrong: ', head)
print('Deprel wrong: ', deprel)
print('\n')

print('Percentage of heads wrong: ', (head/no_toks_corr)*100, '%')
print('Percentage of deprels wrong: ', (deprel/no_toks_corr)*100, '%')
print('Percentage of both head and deprel wrong: ', (head_deprel/no_toks_corr)*100, '%')

print('\n')

print('Wrong deprel label used:')
for k, v in sorted(deprel_info.items(), key=lambda item: item[1], reverse=True):
    print(k, v)

print('\n')

print('Deprels connected to wrong heads:')
for k, v in sorted(head_info.items(), key=lambda item: item[1], reverse=True):
    print(k, v)

print('\n')
print('Frequency of all dependency relations:')
for k, v in sorted(corr_deprels.items(), key=lambda item: item[1], reverse=True):
    print(k, v)