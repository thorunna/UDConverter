import re
import sys
import os

'''
Hinrik Hafsteinsson 2019
Part of UniTree project for IcePaHC

Text preperation script for IcePaHC conllU-format output
 - joins compound particles to corresponding verbs by looking for '$' markers
   in raw text data in treebank .conllu files
 - input: .conllu file on command line (edits files in situ by renaming/removing)

'''

with open('out.vilhjalmur_test.conllu', 'r') as file:
    outfile = open('out2.vilhjalmur_test.conllu', 'w')
    lines = file.readlines()
    indexes = reversed(range(len(lines)))
    for i in indexes:
        curr_line, prev_line = lines[i].split('\t'), lines[i-1].split('\t')
        if len(curr_line) == 1: continue
        # elif re.search('\$[a-zþæðöáéýúíó]', curr_line[1]):
        elif re.search(r'\$[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]', curr_line[1]) and not re.search(r'[0-9]-[0-9]', curr_line[0]):
            # print(prev_line)
            # print(curr_line)
            prev_line[1] = re.sub(r'\$', '', prev_line[1])
            curr_line[1] = re.sub(r'\$', '', curr_line[1])
            joined_token = prev_line[1] + curr_line[1]
            joined_number = prev_line[0] + '-' + curr_line[0]
            new_line = '\t'.join([joined_number, joined_token, '_', '_', '_', '_', '_', '_', '_', '_\n'])
            lines[i], lines[i-1] = '\t'.join(curr_line), '\t'.join(prev_line)
            lines.insert(i-1, new_line)
        elif re.search(r'\$[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]', curr_line[1]):
            print(prev_line)
            print(curr_line)
            prev_line[1] = re.sub(r'\$', '', prev_line[1])
            curr_line[1] = re.sub(r'\$', '', curr_line[1])
            joined_token = prev_line[1] + curr_line[1]
            joined_number = prev_line[0] + '-' + curr_line[0].split('-')[1]
            new_line = '\t'.join([joined_number, joined_token, '_', '_', '_', '_', '_', '_', '_', '_\n'])
            lines[i], lines[i-1] = '\t'.join(curr_line), '\t'.join(prev_line)
            lines.insert(i-1, new_line)
            lines.remove(lines[i+1])
            print(new_line)
    for line in lines:
        outfile.write(line)
    outfile.close()
