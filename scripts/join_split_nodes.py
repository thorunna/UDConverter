import re
import sys
import os

'''
Þórunn Arnardóttir 2019
Part of UniTree project for IcePaHC

Text preparation script for IcePaHC corpus files.
 - joins words in treebank .psd files which should be written as one, tagged as e.g. 'N21' and 'N22'
 - input: .psd file on command line
'''

tags_22 = r'\((ADJ|ADJR|ADV|FP|N|NPR|NS|NUM|ONE|Q|VAG|VAN|VBN|VBPI|WPRO)(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?22(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+\)'
tags_33 = r'\((ADJ|ADJR|ADV|FP|N|NPR|NS|NUM|ONE|Q|VAG|VAN|VBN|VBPI|WPRO)(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?33(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+\)'

in_path = str(sys.argv[1])
out_path = in_path + '.tmp'

in_file = open(in_path, 'r')
out_file = open(out_path, 'w')

lines = in_file.readlines()
indexes = range(len(lines))

for curr in indexes:
	if re.search(tags_22, lines[curr]):
		match = lines[curr]

		token_21 = re.sub('[\sA-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ\-0-9\(\)]*\s+\([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?(-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)? \([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?21(-[NADG])? ', '', match)
		token_21 = re.sub('-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+\) \((ADJ|ADJR|ADV|FP|N|NPR|NS|NUM|ONE|Q|VAG|VAN|VBN|VBPI|WPRO)(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?22(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+\)+\n', '', token_21)

		token_22 = re.sub('[\sA-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ\-0-9\(\)]*\s+\([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?(-[NADG])? \([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?21(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+\) \((ADJ|ADJR|ADV|FP|N|NPR|NS|NUM|ONE|Q|VAG|VAN|VBN|VBPI|WPRO)(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?22(-[NADG])? ', '', match)
		token_22 = re.sub('-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+\)+\n', '', token_22)

		lemma_22 = re.sub('[\sA-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ\-0-9\(\)]*\s+\([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?(-[NADG])? \([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?21(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+\) \((ADJ|ADJR|ADV|FP|N|NPR|NS|NUM|ONE|Q|VAG|VAN|VBN|VBPI|WPRO)(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?22(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+-', '', match)
		lemma_22 = re.sub('\)+\n', '', lemma_22)

		new_token = token_21+token_22
		new_lemma = token_21+lemma_22
		new_token_lemma = new_token+'-'+new_lemma

		substitute_line = re.sub('\([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?21(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+\) \((ADJ|ADJR|ADV|FP|N|NPR|NS|NUM|ONE|Q|VAG|VAN|VBN|VBPI|WPRO)(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?22(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+\)', new_token_lemma, match)
		subbed_line = lines[curr].replace(match, substitute_line)
		if '<dash>' in subbed_line:
			subbed_line = re.sub('<dash>', '', subbed_line)
		out_file.write(subbed_line)
	elif re.search(tags_33, lines[curr]):
		match = lines[curr]

		token_31 = re.sub('[\sA-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ\-0-9\(\)]*\s+\([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?(-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)? \([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?31(-[NADG])? ', '', match)
		token_31 = re.sub('-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+\) \([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?32(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+\) \([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?33(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+\)+\n', '', token_31)

		token_32 = re.sub('[\sA-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ\-0-9\(\)]*\s+\([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?(-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)? \([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?31(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+\) \([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?32(-[NADG])? ', '', match)
		token_32 = re.sub('-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+\) \([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?33(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+\)+\n', '', token_32)

		token_33 = re.sub('[\sA-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ\-0-9\(\)]*\s+\([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?(-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)? \([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?31(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+\) \([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?32(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+\) \([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?33(-[NADG])? ', '', match)
		token_33 = re.sub('-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+\)+\n', '', token_33)

		lemma_33 = re.sub('[\sA-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ\-0-9\(\)]*\s+\([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?(-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)? \([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?31(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+\) \([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?32(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+\) \([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?33(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+-', '', match)
		lemma_33 = re.sub('\)+\n', '', lemma_33)

		new_token = token_31+token_32+token_33
		new_lemma = token_31+token_32+lemma_33
		new_token_lemma = new_token+'-'+new_lemma

		substitute_line = re.sub('\([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?31(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+\) \([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?32(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+\) \((ADJ|ADJR|ADV|FP|N|NPR|NS|NUM|ONE|Q|VAG|VAN|VBN|VBPI|WPRO)(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?33(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+\)', new_token_lemma, match)
		subbed_line = lines[curr].replace(match, substitute_line)
		if '<dash>' in subbed_line:
			subbed_line = re.sub('<dash>', '', subbed_line)
		out_file.write(subbed_line)
	else:
		out_file.write(lines[curr])

in_file.close()
out_file.close()

os.remove(in_path)
os.rename(out_path, in_path)
