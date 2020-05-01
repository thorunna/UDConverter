import re
import sys
import os

'''
# TODO: tripartite verbs (verb is third node) in files:
    1659.pislarsaga.bio-aut.conllu (3)
    1745.klim.nar-fic.conllu (2)
    1790.fimmbraedra.nar-sag.conllu (1)
    1791.jonsteingrims.bio-aut.conllu (1)
    1985.sagan.nar-fic.conllu (1)

Hinrik Hafsteinsson 2019
Part of UniTree project for IcePaHC

Text preperation script for IcePaHC corpus file (.psd). Not to be run by itself,
part of preprocessing pipeline.
 - Joins compound particles to corresponding verbs by checking for '$'
 - Also joins compound particles to adjectives
'''

# ONLY FOR DEBUG/TESTING The directory containing the .psd files
# IN_DIR = 'testing/corpora/icecorpus/psd_prt_testing'

# Path to input file as first argument
IN_FILE = sys.argv[1]

# Various regex strings defined
PARTICLE_NODE = r'\((RPX?|Q-.|ADVR?|PRO-.|ONE\+Q-.|OTHER-.|WD-.) [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+\$-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+\)'
PARTICLE_TOKEN = r'(?<= )[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(?=\$)' # matches

VERB_NODE = r'\((BE|DO|HV|MD|RD|V(A|B))(P|D|N|)(I|S|N|G|)(-(N|A|D|G))? \$[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+\)'
VERB_START = r'(?<=[A-Z] )\$(?=[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ])' # matches '$' in start of verb
VERB_TOKEN = r'(?<=\$)[A-ZA-ZÞÆÐÖÞÆÐÖÁÉÝÚÍÓÁÉÝÚÍÓ]+(?=-)'
VERB_TAG = r'(?<=\()(BE|DO|HV|MD|RD|V(A|B))(P|D|N|)(I|S|N|G|)(-(N|A|D|G))?'
LEMMA_START_GENERAL = r'((?<=[a-zþæðöáéýúíó]-)(?=[a-zþæðöáéýúíó]))' # MATCHES START OF LEMMA
LEMMA_TOKEN_GENERAL = r'(?<=-)[a-zþæðöáéýúíó]+(?=\)\))'
LEMMA_END_GENERAL = r'(?<=[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ])(?=\))' # matches end of lemma

MIDDLE_VERB_NODE = r'\((BE|DO|HV|MD|RD|V(A|B))(P|D|N|)(I|S|N|G|)+ \$[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+\$-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+\)'

ADJ_NODE = r'\(ADJ(-(N|A|D|G))? \$[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+\)'
ADJ_TAG = r'(?<=\()(ADJ(-(N|A|D|G))?)'


class NodeJoiner():
    '''
    Class for joining compound particles to corresponding verbs and adjectives
    and writes the "corrected" output to a file.

    IcePaHC notation splits particle-verb and particle-adjectives compounds
    with '$' symbol as shown below:

        (PP (P með-með)
            (NP (Q-D öllu-allur) (RP til$-til) (VAG-D $heyrandi-heyrandi)))
        (PP (P handa-handa)

    This can be in same line or in 2-3 lines. Words can also be split into three
    parts and this is taken into account in this class.
    '''
    def __init__(self, file):
        self.file = file
        self.lines = file.readlines()
        self.indexes = range(len(self.lines))
        self.path = file.name
        self.name = os.path.basename(file.name)
        self.out_dir = os.path.dirname(self.path) + '_out'

    def _join_tag(self, tag):
        new_tag = ''
        for c in tag:
            if c in new_tag and 'DO' not in new_tag:
                continue
            else:
                new_tag = new_tag + c
        # print(tag)
        # print(new_tag)
        return new_tag

    def join_same_line(self, index):
        '''
        Joins particles to verbs based on '$', if particle and verb on same line
        In:
            29827 (VBPI játir-játa)
        	29828 (IP-SUB-SPE=2 (CONJ og-og) (RP fyr$-fyr) (VBPI $lætur-láta))
        	29829 (NP-OB1 (PRO-A þær-hún)))))
        Out:
            29827 (VBPI játir-játa)
    		29828 (IP-SUB-SPE=2 (CONJ og-og) (VBPI fyrlætur-fyrláta))
    		29829 (NP-OB1 (PRO-A þær-hún)))))
        '''
        prev = index-1
        next = index+1
        if re.search(PARTICLE_NODE, self.lines[index]) and re.search(VERB_NODE, self.lines[index]):
            # print('\t', prev, self.lines[prev].strip())
            # print('\t', index, self.lines[index].strip())
            # print('\t', next, self.lines[next].strip())
            # print()
            # updated verb token
            self.lines[index] = re.sub(VERB_START, re.findall(PARTICLE_TOKEN, self.lines[index])[0], self.lines[index])
            # update verb lemma:
            # verb tag found
            verb_tag = re.findall(VERB_TAG, self.lines[index])[0]
            verb_tag = self._join_tag(verb_tag)
                # print(verb_tag)
            # tag used to find new verb token found
            new_verb_token_regex = r'(?<=' + verb_tag + r' )[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(?=-)'
            new_verb_token = re.findall(new_verb_token_regex, self.lines[index])[-1]
                # print(new_verb_token_regex)
                # print(new_verb_token)
            # token used to find verb lemma
            lemma_token_regex = r'(?<=' + new_verb_token + r'-)[a-zþæðöáéýúíó]+'
            lemma_token = re.findall(lemma_token_regex, self.lines[index])[0]
                # print(lemma_token_regex)
                # print(lemma_token)
            # lemma replaced with new lemma
            new_lemma = '-' + re.findall(PARTICLE_TOKEN, self.lines[index])[-1] + lemma_token
            self.lines[index] = re.sub('-' + lemma_token, new_lemma.lower(), self.lines[index], 1)
            # particle node deleted
            self.lines[index] = re.sub(PARTICLE_NODE + ' ', '', self.lines[index])

            # print('\t\t', prev, self.lines[prev].strip())
            # print('\t\t', index, self.lines[index].strip())
            # print('\t\t', next, self.lines[next].strip())
            # print()
        return self

    def join_two_lines(self, index):
        '''
        Joins particles to verbs based on '$', if on seperate line
        In:
        	35966 (RP fyrir$-fyrir)
        	35967 (VBN $heitið-heita)
        	35968 (, ,-,)
        Out:
        	35966
    		35967 (VBN fyrirheitið-fyrirheita)
    		35968 (, ,-,)
        '''
        prev = index-1
        next = index+1
        if re.search(PARTICLE_NODE, self.lines[prev]) and re.search(VERB_NODE, self.lines[index]):
            # print('\t', prev, self.lines[prev].strip())
            # print('\t', index, self.lines[index].strip())
            # print('\t', next, self.lines[next].strip())
            # print()

            # updated verb token
            self.lines[index] = re.sub(VERB_START, re.findall(PARTICLE_TOKEN, self.lines[prev])[0], self.lines[index])
            # update verb lemma:
            # verb tag found
            verb_tag = re.findall(VERB_TAG, self.lines[index])[0]
            verb_tag = self._join_tag(verb_tag)
            # print(verb_tag)
            # tag used to find new verb token found
            new_verb_token_regex = r'(?<=' + verb_tag + r' )[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(?=-)'
            new_verb_token = re.findall(new_verb_token_regex, self.lines[index])[-1]
                # print(new_verb_token_regex)
                # print(new_verb_token)
            # token used to find verb lemma
            lemma_token_regex = r'(?<=' + new_verb_token + r'-)[a-zþæðöáéýúíó]+'
            lemma_token = re.findall(lemma_token_regex, self.lines[index])[0]
                # print(lemma_token_regex)
                # print(lemma_token)
            # lemma replaced with new lemma
            new_lemma = '-' + re.findall(PARTICLE_TOKEN, self.lines[prev])[-1] + lemma_token
            self.lines[index] = re.sub('-' + lemma_token, new_lemma.lower(), self.lines[index], 1)
            # particle node deleted
            self.lines[prev] = re.sub(PARTICLE_NODE, '', self.lines[prev])

            # print('\t\t', prev, self.lines[prev].strip())
            # print('\t\t', index, self.lines[index].strip())
            # print('\t\t', next, self.lines[next].strip())
            # print()
        return self

    def join_three_lines(self, index):
        '''
        Joins particles to verbs based on '$', where there is a clitic
        or other "third" partition on third line. Doesn't join clitic to verb.
        In:
        	2249 (QTP (RP fyrir$-fyrir)
        	2250 (VBI $gef$-gefa)
        	2251 (NP (PRO-N $ðu-þú))))
        Out:
            2249 (QTP
    		2250 (VBI fyrirgef$-fyrirgefa)
    		2251 (NP (PRO-N $ðu-þú))))
        '''
        prev = index-1
        next = index+1
        if re.search(PARTICLE_NODE, self.lines[prev]) and re.search(MIDDLE_VERB_NODE, self.lines[index]):
            # print('\t', prev, self.lines[prev].strip())
            # print('\t', index, self.lines[index].strip())
            # print('\t', next, self.lines[next].strip())
            # print()

            # updated verb token
            self.lines[index] = re.sub(VERB_START, re.findall(PARTICLE_TOKEN, self.lines[prev])[0], self.lines[index])
            # update verb lemma:
            # verb tag found
            verb_tag = re.findall(VERB_TAG, self.lines[index])[0]
            verb_tag = self._join_tag(verb_tag)
                # print(verb_tag)
            # tag used to find new verb token found
            new_verb_token_regex = r'(?<=' + verb_tag + r' )[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(?=\$-)'
            new_verb_token = re.findall(new_verb_token_regex, self.lines[index])[-1]
                # print(new_verb_token_regex)
                # print(new_verb_token)
            # token used to find verb lemma
            lemma_token_regex = r'(?<=' + new_verb_token + r'\$-)[a-zþæðöáéýúíó]+'
            lemma_token = re.findall(lemma_token_regex, self.lines[index])[0]
                # print(lemma_token_regex)
                # print(lemma_token)
            # lemma replaced with new lemma
            new_lemma = '-' + re.findall(PARTICLE_TOKEN, self.lines[prev])[-1] + lemma_token
            self.lines[index] = re.sub('-' + lemma_token, new_lemma.lower(), self.lines[index], 1)
            # particle node deleted
            self.lines[prev] = re.sub(PARTICLE_NODE, '', self.lines[prev])

            # print('\t\t', prev, self.lines[prev].strip())
            # print('\t\t', index, self.lines[index].strip())
            # print('\t\t', next, self.lines[next].strip())
            # print()
        return self

    def join_adjectives(self, index):
        '''
        Joins particles with adjectives in same manner as verbs.
        '''
        prev = index-1
        next = index+1
        if re.search(PARTICLE_NODE, self.lines[index]) and re.search(ADJ_NODE, self.lines[index]):
            # print('\t', prev, self.lines[prev].strip())
            # print('\t', index, self.lines[index].strip())
            # print('\t', next, self.lines[next].strip())
            # print()

            self.lines[index] = re.sub(VERB_START, re.findall(PARTICLE_TOKEN, self.lines[index])[0], self.lines[index])
            # update adjective lemma:
            # adjective tag found
            adj_tag = re.findall(ADJ_TAG, self.lines[index])[0]
                # print(adj_tag)
            adj_tag = self._join_tag(adj_tag)
                # print(adj_tag)
            # tag used to find new verb token found
            new_adj_token_regex = r'(?<=' + adj_tag + r' )[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(?=-)'
            new_adj_token = re.findall(new_adj_token_regex, self.lines[index])[-1]
                # print(new_adj_token_regex)
                # print(new_adj_token)
            # token used to find adj lemma
            lemma_token_regex = r'(?<=' + new_adj_token + r'-)[a-zþæðöáéýúíó]+'
            lemma_token = re.findall(lemma_token_regex, self.lines[index])[0]
                # print(lemma_token_regex)
                # print(lemma_token)
            # lemma replaced with new lemma
            new_lemma = '-' + re.findall(PARTICLE_TOKEN, self.lines[index])[-1] + lemma_token
            self.lines[index] = re.sub('-' + lemma_token, new_lemma.lower(), self.lines[index], 1)
            # particle node deleted
            self.lines[prev] = re.sub(PARTICLE_NODE + ' ', '', self.lines[prev])

            # print('\t\t', prev, self.lines[prev].strip())
            # print('\t\t', index, self.lines[index].strip())
            # print('\t\t', next, self.lines[next].strip())
            # print()

        elif re.search(PARTICLE_NODE, self.lines[prev]) and re.search(ADJ_NODE, self.lines[index]):
            # print('\t', prev, self.lines[prev].strip())
            # print('\t', index, self.lines[index].strip())
            # print('\t', next, self.lines[next].strip())
            # print()

            self.lines[index] = re.sub(VERB_START, re.findall(PARTICLE_TOKEN, self.lines[prev])[0], self.lines[index])
            # update adjective lemma:
            # adjective tag found
            adj_tag = re.findall(ADJ_TAG, self.lines[index])[0]
                # print(adj_tag)
            adj_tag = self._join_tag(adj_tag)
                # print(adj_tag)
            # tag used to find new verb token found
            new_adj_token_regex = r'(?<=' + adj_tag + r' )[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(?=-)'
            new_adj_token = re.findall(new_adj_token_regex, self.lines[index])[-1]
                # print(new_adj_token_regex)
                # print(new_adj_token)
            # token used to find adj lemma
            lemma_token_regex = r'(?<=' + new_adj_token + r'-)[a-zþæðöáéýúíó]+'
            lemma_token = re.findall(lemma_token_regex, self.lines[index])[0]
                # print(lemma_token_regex)
                # print(lemma_token)
            # lemma replaced with new lemma
            new_lemma = '-' + re.findall(PARTICLE_TOKEN, self.lines[prev])[-1] + lemma_token
            self.lines[index] = re.sub('-' + lemma_token, new_lemma.lower(), self.lines[index], 1)
            # particle node deleted
            # print(re.findall(PARTICLE_NODE, self.lines[prev]))
            self.lines[prev] = re.sub(PARTICLE_NODE, '', self.lines[prev])
            self.lines[prev] = re.sub('\(NP \)', '', self.lines[prev])

            # print('\t\t', prev, self.lines[prev].strip())
            # print('\t\t', index, self.lines[index].strip())
            # print('\t\t', next, self.lines[next].strip())
            # print()

        return self

    def iterate_nodes(self):
        '''
        Runs input file through each method
        '''
        # print(self.name)
        for current_line_num in self.indexes:
            pass
            # verbs processed
            self.join_same_line(current_line_num)
            self.join_two_lines(current_line_num)
            self.join_three_lines(current_line_num)
            # adjectives processed
            self.join_adjectives(current_line_num)
        return self

    def _create_out_dir(self):
        if not os.path.isdir(self.out_dir):
            os.mkdir(self.out_dir)

    def write_to_file(self, **kwargs):
        '''
        Writes "corrected" lines of input to output file
        Required args: sepdir
            If sepdir=True: Output file goes to seperate directory
            If sepdir=False: Output file goes to input directory
        Optional args: overwrite
            If overwrite=True: Output file overwrites input file
        '''
        sepdir = kwargs.get('sepdir', None)
        overwrite = kwargs.get('overwrite', None)
        if sepdir == True and overwrite == True:
            print('Overwrite not possible if seperate output directory')
            return
        if sepdir == True:
            self._create_out_dir()
            outname = os.path.join(self.out_dir, self.name + '.tmp')
        else:
            outname = self.path + '.tmp'
        if os.path.exists(outname):
            print('File already exists. Run script again.')
            os.remove(outname)
            return
        with open(outname, 'w') as file:
            # print('Writing to file:', self.name)
            for line in self.lines:
                file.write(line)
        if overwrite == True:
            os.remove(self.path)
            os.rename(outname, self.path)

if __name__ == '__main__':
    file = open(IN_FILE, 'r')
    j = NodeJoiner(file)
    j.iterate_nodes()
    j.write_to_file(sepdir=False, overwrite=True)
    # for name in os.listdir(IN_DIR):
    #     file = open(os.path.join(IN_DIR, name), 'r')
    #     j = NodeJoiner(file)
    #     j.iterate_nodes()
    #     j.write_to_file(sepdir=False, overwrite=True)
    # print('Done.')
