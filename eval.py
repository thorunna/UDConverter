import os
import glob
import re

origdir = "CoNLLU/additions2019/althingi"
corrdir = "Manual_correction_updated/additions2019/althingi"


def collect_filenames(directory, abspath=True):
    os.chdir(directory)
    conlluFiles = glob.glob("**/*.conllu", recursive=True)
    conlluFiles = [f for f in conlluFiles if f != None]
    if abspath == True:
        conlluFiles = [os.path.abspath(f) for f in conlluFiles]
    os.chdir("../../../")
    return conlluFiles


orig_set = set(collect_filenames(origdir, False))
corr_set = set(collect_filenames(corrdir, False))

file_names = orig_set.intersection(corr_set)


def run_diff(orig_files, corr_files):
    for file in corr_files:
        name = file.split("Manual_correction/")[1]
        for orig_file in orig_files:
            orig_name = orig_file.split("CoNLLU/")[1]
            if orig_name == name:
                output = "diff/" + name.split("/")[-1]
                os.system("diff " + orig_file + " " + file + " > " + output)


def get_results(diff_file):
    f = open(diff_file, "r")
    lines = f.read()
    # print(lines)
    spl = re.split("\d+[,\w\d]+\n", lines)
    pairs = []
    # print(spl)
    for s in spl:
        if s != None or s != " ":
            try:
                pairs.append((s.split("---")[0], s.split("---")[1]))
            except IndexError:
                print(s)
                pass
                # raise


orig_filenames = collect_filenames(origdir)
corr_filenames = collect_filenames(corrdir)
full_filenames = collect_filenames("CoNLLU/additions2019")

import pyconll
import collections

sents = {}

sent_count_corr = 0
for file in corr_filenames:
    corpus = pyconll.load_from_file(file)
    for sentence in corpus:
        sent_count_corr += 1
        nl = []
        for token in sentence:
            nl.append((token.id, token.form, token.head, token.deprel))
        sents[sentence.id] = nl

print("Sent count corr: ", sent_count_corr)

sents_orig = {}

sent_count_orig = 0
for file in orig_filenames:
    name = file.split("althingi/")[1]
    if name in file_names:
        corpus = pyconll.load_from_file(file)
        for sentence in corpus:
            sent_count_orig += 1
            nl = []
            for token in sentence:
                nl.append((token.id, token.form, token.head, token.deprel))
            sents_orig[sentence.id] = nl

print("Sent count orig: ", sent_count_orig)

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

print("\n")
print("Total no. of sentences in additions2019: ", len(sents_orig_full))

no_toks = 0

for sent, toks in sents_orig_full.items():
    no_toks += len(toks)

print("Total no. of tokens in additions2019: ", no_toks)

print("\n")
print("Total no. of sentences in althingi: ", len(sents_orig_althingi))

no_toks = 0

for sent, toks in sents_orig_althingi.items():
    no_toks += len(toks)

print("Total no. of tokens in althingi: ", no_toks)

comp = {}

for sent, toks in sents.items():
    for orig_sent, orig_toks in sents_orig.items():
        if sent == orig_sent:
            comp[sent] = list(zip(toks, orig_toks))

head_deprel = 0
head = 0
head_info = collections.defaultdict(int)
deprel = 0
deprel_info = collections.defaultdict(int)
total_count = 0
las_count = 0
uas_count = 0

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
err_per_sent = collections.defaultdict(tuple)

wrong_cops = []
wrong_cc = []

for sent, zipped in comp.items():
    sent_len = len(zipped)
    sent_errors = 0
    for el in zipped:
        corr = el[0]
        orig = el[1]
        corr_head = corr[2]
        corr_deprel = corr[3]
        orig_head = orig[2]
        orig_deprel = orig[3]
        corr_deprels[orig_deprel] += 1
        if corr_head != orig_head and corr_deprel != orig_deprel:
            head_deprel += 1
            total_count += 1
            las_count += 1
            uas_count += 1
            sent_errors += 1
            deprel += 1
            head += 1
        if corr_head != orig_head and corr_deprel == orig_deprel:
            head += 1
            head_info[orig_deprel] += 1
            total_count += 1
            las_count += 1
            uas_count += 1
            sent_errors += 1
        if corr_deprel != orig_deprel and corr_head == orig_head:
            deprel += 1
            deprel_info[orig_deprel] += 1
            total_count += 1
            las_count += 1
            sent_errors += 1

    err_per_sent[sent] = (sent_len, sent_errors)

head_info_perc = {}

for k, v in head_info.items():
    v_upd = (v / corr_deprels[k]) * 100
    head_info_perc[k] = v_upd

deprel_info_perc = {}

for k, v in deprel_info.items():
    v_upd = (v / corr_deprels[k]) * 100
    deprel_info_perc[k] = v_upd

no_toks_corr = 0

for sent, toks in sents.items():
    no_toks_corr += len(toks)


def print_wrong_deprel(deprel_info):
    print("\nWrong deprel label used:")
    for k, v in sorted(deprel_info.items(), key=lambda item: item[1], reverse=True):
        print(k, v)
    print("\nWrong deprel label used(%):")
    for k, v in sorted(
        deprel_info_perc.items(), key=lambda item: item[1], reverse=True
    ):
        print(k, v)


def print_wrong_heads(head_info):
    print("\nDeprels connected to wrong heads:")
    for k, v in sorted(head_info.items(), key=lambda item: item[1], reverse=True):
        print(k, v)
    print("\nDeprels connected to wrong heads(%):")
    for k, v in sorted(head_info_perc.items(), key=lambda item: item[1], reverse=True):
        print(k, v)


def print_deprels(corr_deprels):
    print("\nFrequency of all dependency relations:")
    for k, v in sorted(corr_deprels.items(), key=lambda item: item[1], reverse=True):
        print(k, v)


print("No. of manually-corrected sentences: ", len(sents))

print("Total no. of manually-corrected tokens: ", no_toks_corr)
print("Total no. of corrections: ", total_count)

print("\n")
print("Both head and deprel wrong: ", head_deprel)
print("Head wrong: ", head)
print("Deprel wrong: ", deprel)
print("\n")

print("LAS: ", 100 - ((las_count / no_toks_corr) * 100), "%")
print("UAS: ", 100 - ((uas_count / no_toks_corr) * 100), "%")

print("Percentage of heads wrong: ", (head / no_toks_corr) * 100, "%")
print("Percentage of heads correct: ", 100 - ((head / no_toks_corr) * 100), "%")
print("Percentage of deprels wrong: ", (deprel / no_toks_corr) * 100, "%")
print("Percentage of deprels correct: ", 100 - ((deprel / no_toks_corr) * 100), "%")
print(
    "Percentage of both head and deprel wrong: ",
    (head_deprel / no_toks_corr) * 100,
    "%",
)
