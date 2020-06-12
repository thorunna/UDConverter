# -*- coding: utf-8 -*-

"""06.03.20

Hinrik Hafsteinsson (hih43@hi.is)
Þórunn Arnardóttir (tha86@hi.is)

Debugging script that counts roots in CoNLL-U format sentences.
In UD each sentence should have exactly 1 root.
Part of UniTree project for IcePaHC

"""

import pyconll
import pyconll.util
import sys
import os
import re
import argparse
from collections import Counter, defaultdict


def get_root_errors(in_file, no_roots_file, many_roots_file, print_ids=False):
    """10.03.20
    Short summary.

    Args:
        in_file (string): Description of parameter `in_file`.
        no_roots_file (string): Description of parameter `no_roots_file`.
        many_roots_file (string): Description of parameter `many_roots_file`.

    Returns:
        None

    """
    count_roots = 0
    no_roots = 0
    many_roots = 0
    parse_errors = 0

    id_list_no = []
    id_list_many = []

    for sentence in in_file:
        count_roots = 0
        for token in sentence:
            if token.deprel == 'root' or token.head == '0':
                # print(token.deprel)
                count_roots = count_roots + 1
                # print(count_roots)
        if count_roots == 0:
            no_roots += 1
            no_roots_file.write(sentence.conll())
            no_roots_file.write('\n')
            no_roots_file.write('\n')
            # print('Sentences with != 1 root: ',sentence.conll())
            id_list_no.append(sentence.id)
        if count_roots > 1:
            many_roots += 1
            many_roots_file.write(sentence.conll())
            many_roots_file.write('\n')
            many_roots_file.write('\n')
            id_list_many.append(sentence.id)
            print(sentence.id)

    if print_ids == True:
        return (id_list_no, id_list_many)
    else:
        return (no_roots, many_roots)


    # print('Sents. with None (parse error):', parse_errors)

def get_ccomp_xcomp_errors(in_file, ccomp_xcomp_file):
    """26.03.20
    Short summary.

    Args:
        in_file (string): Description of parameter `in_file`.
        ccomp_xcomp_file (string): Description of parameter `no_roots_file`.

    Returns:
        None

    """
    ccomp_count = 0
    xcomp_count = 0
    error_count = 0
    error_sents = 0
    parse_errors = 0

    for sentence in in_file:
        for token in sentence:
            if token.deprel == 'ccomp/xcomp':
                error_count += 1
            elif token.deprel == 'ccomp':
                ccomp_count += 1
            elif token.deprel == 'xcomp':
                xcomp_count += 1
    return (ccomp_count, xcomp_count, error_count)


def get_acl_advcl_errors(in_file, acl_advcl_file):
    """26.03.20
    Short summary.

    Args:
        in_file (string): Description of parameter `in_file`.
        ccomp_xcomp_file (string): Description of parameter `no_roots_file`.

    Returns:
        None

    """
    acl_count = 0
    advcl_count = 0
    error_count = 0
    error_sents = 0
    parse_errors = 0

    for sentence in in_file:
        for token in sentence:
            if token.deprel == 'acl/advcl':
                error_count += 1
            elif token.deprel == 'acl':
                acl_count += 1
            elif token.deprel == 'advcl':
                advcl_count += 1
    return (acl_count, advcl_count, error_count)

def get_dependency_errors(in_file, dep_err_file):
    """26.03.20
    Short summary.

    Args:
        in_file (string): Description of parameter `in_file`.
        ccomp_xcomp_file (string): Description of parameter `no_roots_file`.

    Returns:
        None

    """
    dep_count = 0
    same_count = 0
    rel_count = 0
    question_count = 0
    # error_sents = 0
    # parse_errors = 0

    for sentence in in_file:
        for token in sentence:
            if token.head == token.id:
                same_count += 1
            if token.deprel == 'dep':
                dep_count += 1
            elif re.match('(rel|rel-.*)', str(token.deprel)):
                rel_count += 1
            elif token.deprel == '?':
                question_count += 1
    return (dep_count, same_count, rel_count, question_count)

def check_sentence_final(in_file):
    ends = defaultdict(int)
    for sentence in in_file:
        if sentence[-1].xpos == '.':
            ends[sentence[-1].form[0]] += 1
    return ends

def check_left_to_right_errors(in_file, **kwargs):
    if appos:
        pass
    else:
        cnt = Counter()
        rels = ['conj', 'fixed', 'flat:name', 'flat:foreign', 'goeswith', 'appos']
        for rel in rels:
            cnt[rel] = 0
        for sentence in in_file:
            for token in sentence:
                if re.match(r'^[1-9][0-9]*-[1-9][0-9]*$', token.id): continue
                if re.match(r'^(conj|fixed|flat|goeswith|appos)', token.deprel)\
                and int(token.id) < int(token.head):
                    cnt[token.deprel] += 1
                        

    return cnt



def main():

    parser = argparse.ArgumentParser(description='Count root errors in CoNLL-U file corpus')
    parser.add_argument('--input', '-i', type=str, required=True,
                        help='path to input CoNLL-U (.conllu) directory')
    # parser.add_argument('--output', '-o', type=str, required=False,
    #                     help='path to output directory')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='verbose flag')
    parser.add_argument('--sent_id', '-id', action='store_true',
                        help='flag for returning Treebank sentence IDs of matched sentences')
    parser.add_argument('--appos', action='store_true', help='flag for checking appos rel errors')

    error_types = parser.add_mutually_exclusive_group(required=True)
    error_types.add_argument('--roots', '-r',
                        help='check for number of roots in sentences', action='store_true')
    error_types.add_argument('--ccomp', '-c',
                        help='check for number of ccomp/xcomp in files', action='store_true')
    error_types.add_argument('--acl', '-a',
                        help='check for number of acl/advcl in files', action='store_true')
    error_types.add_argument('--dep', '-d',
                        help='check for number of dependency errors in files', action='store_true')
    error_types.add_argument('-punct', '-p',
                        help='check type of sentence final punctuation', action='store_true')
    error_types.add_argument('--left_right', '-lr', help='check for left-to-right errors', action='store_true')
    args = parser.parse_args()

    conllu_path = args.input

    if args.punct:
        ends = Counter()
        for conllu_file in os.listdir(conllu_path):
            print(conllu_file)
            train = pyconll.load_from_file(os.path.join(conllu_path, conllu_file))
            ends += Counter(check_sentence_final(train))
        for k,v in ends.items():
            print(f'{k}\t{v}')
    
    if args.left_right:
        if args.appos:
            total_counts = Counter()

    for conllu_file in os.listdir(conllu_path):
        train = pyconll.load_from_file(os.path.join(conllu_path, conllu_file))
        if args.roots:
            if args.sent_id:
                no_roots_ids, many_roots_ids = get_root_errors(train, None, None, print_ids=True)
                print('Sentences with no roots:')
                for id in no_roots_ids:
                    print(id)
                print('Sentences with many roots')
                for id in many_roots_ids:
                    print(id)
                return
            f = open('root_check/no_root_allt.conllu', 'a+')
            f2 = open('root_check/too_many_roots_allt.conllu', 'a+')
            if args.verbose:
                print('Current file:', conllu_file)
                no_roots, many_roots = get_root_errors(train, f, f2)
                print('Sents. with no roots:', no_roots)
                print('Sents. with many roots:', many_roots)
            else:
                no_roots, many_roots = get_root_errors(train, f, f2)
                print(f'{no_roots}\t{many_roots}\t{conllu_file}')
            f.close()
            f2.close()
        if args.ccomp:
            f = open('root_check/ccomp_xcomp_allt.conllu', 'w+')
            if args.verbose:
                print('Current file:', conllu_file)
                ccomp_xcomp_erros = get_ccomp_xcomp_errors(train, f)
                print('No. of ccomp/xcomp relations:', ccomp_xcomp_erros)
            else:
                ccomp, xcomp, ccomp_xcomp = get_ccomp_xcomp_errors(train, f)
                print(f'{ccomp}\t{xcomp}\t{ccomp_xcomp}\t{conllu_file}')
            f.close()
        if args.acl:
            f = open('root_check/acl_advcl_allt.conllu', 'w+')
            if args.verbose:
                print('Current file:', conllu_file)
                acl_advcl_errors = get_acl_advcl_errors(train, f)
                print('No. of ccomp/xcomp relations:', acl_advcl_errors)
            else:
                acl, advcl, acl_advcl = get_acl_advcl_errors(train, f)
                print(f'{acl}\t{advcl}\t{acl_advcl}\t{conllu_file}')
            f.close()
        if args.dep:
            f = open('root_check/dep_err_allt.conllu', 'w+')
            if args.verbose:
                print('Current file:', conllu_file)
                acl_advcl_errors = get_acl_advcl_errors(train, f)
                print('No. of dependency errors:', acl_advcl_errors)
            else:
                dep, same, rel, que = get_dependency_errors(train, f)
                print(f'{dep}\t{same}\t{rel}\t{que}\t{conllu_file}')
            f.close()
        if args.left_right:
            if args.appos:
                check_left_to_right(train, appos=True)
            else:
                counts = check_left_to_right_errors(train)
                # print('\t'.join([i[0] for i in sorted(counts.items())]))
                print('\t'.join([str(i[1]) for i in sorted(counts.items())])+f'\t{conllu_file}')
                


if __name__ == '__main__':
    main()
