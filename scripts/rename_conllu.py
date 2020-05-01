import re
import sys
import os

# from lib.features import Features, getTagDict

'''
# TODO: Eventually move feature insertion into depender module

Hinrik Hafsteinsson 2019
Þórunn Arnardóttir
Part of UniTree project for IcePaHC

Text preperation script for CoNLL-U output file (.conllu). Not to be run by itself,
part of postprocessing pipeline.
 - Renames various string nodes in CoNLL-U lines
 - input: .conllu file on command line (edits files in situ by renaming/removing)
'''

WORD_INDEX = 1

def remove_split(line):
    '''
    '''
    if len(line) < 10: return line # '\t'.join(line)
    line = '\t'.join(line)
    line = re.sub(r'\$', '', line)
    return line.split('\t')

def check_None(line):
    line = line.split('\t')
    if len(line) < 10: return '\t'.join(line)
    elif 'None' in line:
        return None
    else:
        return '\t'.join(line)


def main():
    # pass
    in_path = sys.argv[1]
    # in_path = 'testing/CoNLLU_output/1350.bandamennM.nar-sag.conllu'

    out_path = in_path + '.tmp'
    in_file = open(in_path, 'r')
    out_file = open(out_path, 'w')

    filename = os.path.basename(in_path)
    # OTB_tagDict = getTagDict(filename)

    lines = in_file.readlines()
    lines = [line.split('\t') for line in lines]
    in_file.close()
    line_indexes = [i for i in range(len(lines))]

    for index in line_indexes:
        # lines[index] = fix_dash(lines[index])
        # lines[index] = rename_abbrevations(lines[index])
        lines[index] = remove_split(lines[index])
        # lines[index] = insert_features(lines, OTB_tagDict, index)
        # if lines[index] == None:
        #     print(lines[index])

    for line in lines:
        try:
            line = '\t'.join(line)
            out_file.write(line)
        except TypeError:
            continue
        # except TypeError:
        # print(line)


    out_file.close()
    os.remove(in_path)
    os.rename(out_path, in_path)

if __name__ == '__main__':
    # debug_iterate_lines()
    main()
