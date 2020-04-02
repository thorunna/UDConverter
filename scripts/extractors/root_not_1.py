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
import argparse


def get_root_errors(in_file, no_roots_file, many_roots_file):
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
        if count_roots > 1:
            many_roots += 1
            many_roots_file.write(sentence.conll())
            many_roots_file.write('\n')
            many_roots_file.write('\n')

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


    # print('Sents. with None (parse error):', parse_errors)


def main():

    parser = argparse.ArgumentParser(description='Count root errors in CoNLL-U file corpus')
    parser.add_argument('--input', '-i', type=str, required=True,
                        help='path to input CoNLL-U (.conllu) directory')
    # parser.add_argument('--output', '-o', type=str, required=False,
    #                     help='path to output directory')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='verbose flag')

    error_types = parser.add_mutually_exclusive_group(required=True)
    error_types.add_argument('--roots', '-r',
                        help='check for number of roots in sentences', action='store_true')
    error_types.add_argument('--ccomp', '-c',
                        help='check for number of ccomp/xcomp in files', action='store_true')

    args = parser.parse_args()


    conllu_path = args.input
    for conllu_file in os.listdir(conllu_path):
        train = pyconll.load_from_file(os.path.join(conllu_path, conllu_file))
        if args.roots:
            f = open('root_check/no_root_allt.conllu', 'w+')
            f2 = open('root_check/too_many_roots_allt.conllu', 'w+')
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


if __name__ == '__main__':
    main()
