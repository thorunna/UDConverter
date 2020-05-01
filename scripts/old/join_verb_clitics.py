import re
import sys
import os

'''
Hinrik Hafsteinsson 2019
Part of UniTree project for IcePaHC

Text preperation script for IcePaHC conllU-format output
 - joins clitics to corresponding verbs and converts subtokens to standard
   spelling  by looking for '$' markers in raw text data in treebank .conllu files
 - input: .conllu file on command line (edits files in situ by renaming/removing)
 - format example

    unmodified .conllu:
        1	Heyr$	heyra	VERB	VBDI	Mood=Imp|Tense=Past	0	root	_	_
        2	$ðu	þú	PRON	PRO-N	Case=Nom|Number=Plur|Gender=Neut	1	nsubj	_	_
    modified .conllu
        1-2	Heyrðu	_	_	_	_	_	_	_	_
        1	Heyr	heyra	VERB	VBDI	Mood=Imp|Tense=Past	0	root	_	_
        2	þú	þú	PRON	PRO-N	Case=Nom|Number=Plur|Gender=Neut	1	nsubj	_	_
'''

in_path = str(sys.argv[1])
out_path = in_path + '.tmp'

with open(in_path, 'r') as file:
    outfile = open(out_path, 'w')
    lines = file.readlines()
    indexes = reversed(range(len(lines)))
    for i in indexes:
        curr_line, prev_line = lines[i].split('\t'), lines[i-1].split('\t')
        if len(curr_line) == 1: continue
        # elif re.search('\$[a-zþæðöáéýúíó]', curr_line[1]):
        elif re.search('\$[ðtd]?[uú]', curr_line[1]):
            # print(curr_line)
            joined_token = prev_line[1] + curr_line[1]
            if re.search(r'Mood=Imp', prev_line[5]):
                if re.search(r'(s|[^Gg]er|[^áís]t)\$', prev_line[1]):
                    prev_line[1] = re.sub(r'\$', 't', prev_line[1])
                if re.search(r'ð\$', prev_line[1]):
                    prev_line[1] = re.sub(r'ð\$', '', prev_line[1])
                else:
                    prev_line[1] = re.sub(r'\$', '', prev_line[1])
                # print(curr_line)
            elif re.search(r'[^iEeaæu]r\$', prev_line[1]):
                prev_line[1] = re.sub(r'\$', 'ð', prev_line[1])
            elif re.search(r'([Ee]r|s|al|[^ílntrs]t|un|il|rf)\$', prev_line[1]):
                prev_line[1] = re.sub(r'\$', 't', prev_line[1])
            else:
                prev_line[1] = re.sub(r'\$', '', prev_line[1])
            curr_line[1] = re.sub(r'\$[tðd]?[uú]', 'þú', curr_line[1])
            lines[i], lines[i-1] = '\t'.join(curr_line), '\t'.join(prev_line)
            joined_token = re.sub(r'\$\$', '', joined_token)
            joined_number = prev_line[0] + '-' + curr_line[0]
            new_line = '\t'.join([joined_number, joined_token, '_', '_', '_', '_', '_', '_', '_', '_\n'])
            lines.insert(i-1, new_line)
    for line in lines:
        outfile.write(line)
    outfile.close()

# os.remove(in_path)
# os.rename(out_path, in_path)
