import re
import sys
import os

'''
Hinrik Hafsteinsson 2019
Part of UniTree project for IcePaHC

Text preperation script for IcePaHC corpus files.
 - joins nouns and determiners in raw text data in treebank .psd files
 - input: .psd file on command line
'''


det_token = r'(?<=D-. \$).*(?=-)' # matches the token of a determiner, excluding "$"
det_node = r' {0,1}\(D-[ A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ*$-]*\)' # matches a whole determiner node
noun_trail = r'(?<=)\$(?=-)' # matches the trailing "$" of a noun
noun_node =  r' {0,1}\(((N|NS|NPR|NPRS)-|FW).*\$-' # matches a whole noun node
noun_token_incompl = r'(?<=N-. )[^($]*(?=-)' # noun token where "$" is missing

in_path = str(sys.argv[1])
out_path = in_path + '.tmp'

in_file = open(in_path, 'r')
out_file = open(out_path, 'w')

lines = in_file.readlines()
indexes = range(len(lines))

for curr in indexes:
    prev = curr-1
    if re.search(det_token, lines[curr]) and re.search(noun_trail, lines[curr]):
        # print(lines[curr].strip('\n'))
        lines[curr] = re.sub(noun_trail, re.findall(det_token, lines[curr])[0], lines[curr])
        lines[curr] = re.sub(det_node, '', lines[curr])
        # print(curr, lines[curr].strip('\n'), 'XXX')
        out_file.write(lines[curr])
    elif re.search(det_token, lines[curr]) and not re.search(noun_trail, lines[curr]) and re.search(noun_trail, lines[prev]):
        # print(prev, lines[prev].strip('\n'))
        # print(curr, lines[curr].strip('\n'))
        lines[prev] = re.sub(noun_trail, re.findall(det_token, lines[curr])[0], lines[prev])
        lines[curr] = re.sub(det_node, '', lines[curr])
        out_file.write(lines[prev])
        out_file.write(lines[curr])
        # print(prev, lines[prev].strip('\n'))
        # print(curr, lines[curr].strip('\n'), '===')
    elif re.search(det_token, lines[curr]) and re.search(noun_token_incompl, lines[curr]):
        noun_token = re.findall(noun_token_incompl, lines[curr])[0] + '$'
        lines[curr] = re.sub(noun_token_incompl, noun_token, lines[curr])
        lines[curr] = re.sub(noun_trail, re.findall(det_token, lines[curr])[0], lines[curr])
        lines[curr] = re.sub(det_node, '', lines[curr])
        out_file.write(lines[curr])
        # print(lines[curr].strip('\n'))
    elif not re.search(noun_node, lines[curr]):
        out_file.write(lines[curr])
    elif re.search(noun_node, lines[curr]) and not re.search(det_token, lines[curr+1]):
        #
        out_file.write(lines[curr])
        # print(curr, lines[curr].strip('\n'))

in_file.close()
out_file.close()

os.remove(in_path)
os.rename(out_path, in_path)
