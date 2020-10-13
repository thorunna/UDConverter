import re
import sys
import os
from datetime import datetime
from collections import defaultdict
import pyconll

'''

# TODO:
    FINISH IMPLEMENTING join_various_nodes() method

2019
Hinrik Hafsteinsson
Þórunn Arnardóttir
Part of UniTree project for IcePaHC

Module for joining various nodes in IcePaHC files split by '$'
'''

# ONLY FOR DEBUG/TESTING The directory containing the .psd files
# IN_DIR = 'testing/corpora/icecorpus/psd_prt_testing'

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

    Fixed issues (former TODO):
    # tripartite verbs (verb is third node) in files:
        1659.pislarsaga.bio-aut.conllu (3)
        1745.klim.nar-fic.conllu (2)
        1790.fimmbraedra.nar-sag.conllu (1)
        1791.jonsteingrims.bio-aut.conllu (1)
        1985.sagan.nar-fic.conllu (1)

    '''
    def __init__(self, file):
        self.file = file
        self.lines = file #file.readlines()
        self.indexes = range(len(self.lines))
        # self.path = file.name
        # self.name = os.path.basename(file.name)
        # self.file_type = os.path.splitext(file.name)[1]

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

    def join_verbs_same_line(self, index):
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

        Also joins where particle is already split in two on same line
        In:
            1002 (VAN stiftuð-stifta)
            1003 (IP-MAT-SPE-PRN=1 (CONJ og-og) (RP upp$-upp) (RP $á$-á) (VAN $lögð-leggja))
            1004 (PP-BY (P af-af)
        Out:
            1002 (VAN stiftuð-stifta)
            1003 (IP-MAT-SPE-PRN=1 (CONJ og-og) (VAN uppálögð-uppáleggja))
            1004 (PP-BY (P af-af)
        '''

        PARTICLE_NODE = r'\((P|RPX?|Q-.|ADVR?|PRO-.|ONE\+Q-.|OTHER-.|WD-.) [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+\$-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+\)'
        PARTICLE_TOKEN = r'(?<= )[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(?=\$)' # matches
        PARTICLE_MIDDLE_NODE = r'\((P|RPX?|Q-.|ADVR?|PRO-.|ONE\+Q-.|OTHER-.|WD-.) \$[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+\$-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+\)'
        PARTICLE_MIDDLE_TOKEN = r'(?<= )\$[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(?=\$)'
        PARTICLE_START = r'(?<= )\$(?=[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ])'

        VERB_NODE = r'\((BE|DO|HV|MD|RD|V(A|B))(P|D|N|)(I|S|N|G|)(-(N|A|D|G))? \$[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+\)'
        VERB_START = r'(?<=[A-Z] )\$(?=[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ])' # matches '$' in start of verb
        VERB_TOKEN = r'(?<=\$)[A-ZA-ZÞÆÐÖÞÆÐÖÁÉÝÚÍÓÁÉÝÚÍÓ]+(?=-)'
        VERB_TAG = r'(?<=\()(BE|DO|HV|MD|RD|V(A|B))(P|D|N|)(I|S|N|G|)(-(N|A|D|G))?'
        LEMMA_START_GENERAL = r'((?<=[a-zþæðöáéýúíó]-)(?=[a-zþæðöáéýúíó]))' # MATCHES START OF LEMMA
        LEMMA_TOKEN_GENERAL = r'(?<=-)[a-zþæðöáéýúíó]+(?=\)\))'
        LEMMA_END_GENERAL = r'(?<=[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ])(?=\))' # matches end of lemma


        prev = index-1
        next = index+1
        if re.search(PARTICLE_NODE, self.lines[index]) and re.search(VERB_NODE, self.lines[index]) and re.search(PARTICLE_MIDDLE_NODE, self.lines[index]):
            # print('\t', prev, self.lines[prev].strip())
            # print('\t', index, self.lines[index].strip())
            # print('\t', next, self.lines[next].strip())
            # print()

            # particles joined
            self.lines[index] = re.sub(PARTICLE_START, re.findall(PARTICLE_TOKEN, self.lines[index])[0], self.lines[index], 1)
                # print('\t', index, self.lines[index].strip())
            # firstparticle node deleted
            self.lines[index] = re.sub(PARTICLE_NODE + ' ', '', self.lines[index], 1)
                # print('\t', index, self.lines[index].strip())
            # update verb token
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
        elif re.search(PARTICLE_NODE, self.lines[index]) and re.search(VERB_NODE, self.lines[index]):
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

    def join_verbs_two_lines(self, index):
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

        PARTICLE_NODE = r'\((P|RPX?|Q-.|ADVR?|PRO-.|ONE\+Q-.|OTHER-.|WD-.) [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+\$-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+\)'
        PARTICLE_TOKEN = r'(?<= )[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(?=\$)' # matches

        VERB_NODE = r'\((BE|DO|HV|MD|RD|V(A|B))(P|D|N|)(I|S|N|G|)(-(N|A|D|G))? \$[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+\)'
        VERB_START = r'(?<=[A-Z] )\$(?=[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ])' # matches '$' in start of verb
        VERB_TOKEN = r'(?<=\$)[A-ZA-ZÞÆÐÖÞÆÐÖÁÉÝÚÍÓÁÉÝÚÍÓ]+(?=-)'
        VERB_TAG = r'(?<=\()(BE|DO|HV|MD|RD|V(A|B))(P|D|N|)(I|S|N|G|)(-(N|A|D|G))?'
        LEMMA_START_GENERAL = r'((?<=[a-zþæðöáéýúíó]-)(?=[a-zþæðöáéýúíó]))' # MATCHES START OF LEMMA
        LEMMA_TOKEN_GENERAL = r'(?<=-)[a-zþæðöáéýúíó]+(?=\)\))'
        LEMMA_END_GENERAL = r'(?<=[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ])(?=\))' # matches end of lemma

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

    def join_verbs_three_lines(self, index):
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

        Also joins particles that are already split in two, to verb.
        In:
            15581 (RP upp$-upp)
            15582 (RP $á$-á)
            15583 (VAN $lagt-leggja))))))))))
        Out:
            15581
            15582
            15583 (VAN uppálagt-uppáleggja))))))))))
        '''

        PARTICLE_NODE = r'\((P|RPX?|Q-.|ADVR?|PRO-.|ONE\+Q-.|OTHER-.|WD-.) [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+\$-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+\)'
        PARTICLE_TOKEN = r'(?<= )[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(?=\$)' # matches
        PARTICLE_MIDDLE_NODE = r'\((P|RPX?|Q-.|ADVR?|PRO-.|ONE\+Q-.|OTHER-.|WD-.) \$[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+\$-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+\)'
        PARTICLE_MIDDLE_TOKEN = r'(?<= )\$[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(?=\$)'
        PARTICLE_START = r'(?<= )\$(?=[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ])'

        VERB_NODE = r'\((P|BE|DO|HV|MD|RD|V(A|B))(P|D|N|)(I|S|N|G|)(-(N|A|D|G))? \$[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+\$?-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+\)'
        VERB_START = r'(?<=[A-Z] )\$(?=[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ])' # matches '$' in start of verb
        VERB_TOKEN = r'(?<=\$)[A-ZA-ZÞÆÐÖÞÆÐÖÁÉÝÚÍÓÁÉÝÚÍÓ]+(?=-)'
        VERB_TAG = r'(?<=\()(BE|DO|HV|MD|RD|V(A|B))(P|D|N|)(I|S|N|G|)(-(N|A|D|G))?'
        LEMMA_START_GENERAL = r'((?<=[a-zþæðöáéýúíó]-)(?=[a-zþæðöáéýúíó]))' # MATCHES START OF LEMMA
        LEMMA_TOKEN_GENERAL = r'(?<=-)[a-zþæðöáéýúíó]+(?=\)\))'
        LEMMA_END_GENERAL = r'(?<=[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ])(?=\))' # matches end of lemma

        MIDDLE_VERB_NODE = r'\((BE|DO|HV|MD|RD|V(A|B))(P|D|N|)(I|S|N|G|)+ \$[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+\$-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+\)'

        prevprev = index-2
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
        elif re.search(PARTICLE_MIDDLE_NODE, self.lines[prev]) and re.search(VERB_NODE, self.lines[index]):
            # print('\t', prev, self.lines[prevprev].strip())
            # print('\t', index, self.lines[prev].strip())
            # print('\t', next, self.lines[index].strip())
            # print()

            # particles joined
            self.lines[prev] = re.sub(PARTICLE_START, re.findall(PARTICLE_TOKEN, self.lines[prevprev])[0], self.lines[prev])
            # updated verb token
            self.lines[index] = re.sub(VERB_START, re.findall(PARTICLE_TOKEN, self.lines[prev])[0], self.lines[index])
            # update verb lemma:
            # verb tag found
            verb_tag = re.findall(VERB_TAG, self.lines[index])[0]
            verb_tag = self._join_tag(verb_tag)
            # print(verb_tag)
            # tag used to find new verb token found
            new_verb_token_regex = r'(?<=' + verb_tag + r' )[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(?=-)'
            # print(new_verb_token_regex)
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
            self.lines[prevprev] = re.sub(PARTICLE_NODE, '', self.lines[prevprev])

            # print('\t\t', prev, self.lines[prevprev].strip())
            # print('\t\t', index, self.lines[prev].strip())
            # print('\t\t', next, self.lines[index].strip())
            # print()
        return self

    def join_adjectives(self, index):
        '''
        Joins particles with adjectives in same manner as verbs.
        '''

        ADJ_NODE = r'\(ADJ(-(N|A|D|G))? \$[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+\)'
        ADJ_TAG = r'(?<=\()(ADJ(-(N|A|D|G))?)'

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

    def join_NPs(self, index):
        '''
        Joins nouns and determiners in raw text data in treebank .psd files
        '''
        prev = index-1
        next = index+1
        
        det_token = r'(?<=D-. \$)[a-zþæðöáéýúíó]*(?=[-\)])' # matches the token of a determiner, excluding "$"
        det_token_alt = r'(?<=D-.-TTT \$)[a-zþæðöáéýúíó]*(?=[-\)])' # matches det token in case of -TTT in tag
        det_token_caps = r'(?<=D-. \$)[A-ZÞÆÐÖÁÉÝÚÍÓ]*(?=[-\)])' # match det token if in caps (few examples)
        det_node = r' ?\(D-[A-Z] \$[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ*$-]*\)' # matches a whole determiner node
        # det_node_alt = r'-TTT'
        noun_trail = r'(?<=)\$(?=[-\)])' # matches the trailing "$" of a noun
        noun_node =  r' {0,1}\(((N|NS|NPR|NPRS)-|FW).*\$-' # matches a whole noun node
        noun_token_incompl = r'(?<=N-. )(</?dash/?>)?[^($]*(?=[-\)])' # noun token where "$" is missing

        prev = index-1
        next = index+1
        
        if re.search(det_token, self.lines[index]) and re.search(noun_trail, self.lines[index]):
            
            # print('\t', prev, self.lines[prev].strip())
            # print('\t', index, self.lines[index].strip())
            # print('\t', next, self.lines[next].strip())
            # print()
            
            self.lines[index] = re.sub(noun_trail, re.findall(det_token, self.lines[index])[0], self.lines[index])
            self.lines[index] = re.sub(det_node, '', self.lines[index])

            # print('\t\t\t', prev, self.lines[prev].strip())
            # print('\t\t\t', index, self.lines[index].strip())
            # print('\t\t\t', next, self.lines[next].strip())
            # print()

        elif re.search(det_token, self.lines[index]) and not re.search(noun_trail, self.lines[index]) and re.search(noun_trail, self.lines[prev]):

            # print('\t', prev, self.lines[prev].strip())
            # print('\t', index, self.lines[index].strip())
            # print('\t', next, self.lines[next].strip())
            # print()

            self.lines[prev] = re.sub(noun_trail, re.findall(det_token, self.lines[index])[0], self.lines[prev])
            self.lines[index] = re.sub(det_node, '', self.lines[index])

            # print('\t\t', prev, self.lines[prev].strip())
            # print('\t\t', index, self.lines[index].strip())
            # print('\t\t', next, self.lines[next].strip())
            # print()

        elif re.search(det_token, self.lines[index]) and re.search(noun_token_incompl, self.lines[index]):

            # print('\t', prev, self.lines[prev].strip())
            # print('\t', index, self.lines[index].strip())
            # print('\t', next, self.lines[next].strip())
            # print()

            noun_token = re.findall(noun_token_incompl, self.lines[index])[0] + '$'
            self.lines[index] = re.sub(noun_token_incompl, noun_token, self.lines[index])
            self.lines[index] = re.sub(noun_trail, re.findall(det_token, self.lines[index])[0], self.lines[index])
            self.lines[index] = re.sub(det_node, '', self.lines[index])

            # print('\t\t', prev, self.lines[prev].strip())
            # print('\t\t', index, self.lines[index].strip())
            # print('\t\t', next, self.lines[next].strip())
            # print()

        if re.search(det_token_caps, self.lines[index]):
            '''
            Fixes determiners in all caps.
            Only occurs in:
                1150.firstgrammar.sci-lin.psd
                1150.homiliubok.rel-ser.psd
                1985.sagan.nar-fic.psd
            In:
                2149 (IP-MAT (CONJ En-en)
                2150 (NP-SBJ (N-N GEISLI$-GEISLI) (D-N $NN-HINN))
                2151 (VBPI skín-skína)
            Out:
                2149 (IP-MAT (CONJ En-en)
                2150 (NP-SBJ (N-N GEISLINN-GEISLI))
                2151 (VBPI skín-skína)
            '''

            # print('\t', prev, self.lines[prev].strip())
            # print('\t', index, self.lines[index].strip())
            # print('\t', next, self.lines[next].strip())
            # print()

            self.lines[index] = re.sub(noun_trail, re.findall(det_token_caps, self.lines[index])[0], self.lines[index])
            self.lines[index] = re.sub(det_node, '', self.lines[index])

            # print('\t\t', prev, self.lines[prev].strip())
            # print('\t\t', index, self.lines[index].strip())
            # print('\t\t', next, self.lines[next].strip())
            # print()
        return self

    def join_split_nodes(self, index):
        tags_22 = r'\((ADJ|ADJR|ADV|FP|N|NPR|NS|NUM|ONE|Q|VAG|VAN|VBN|VBPI|WPRO)(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?22(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+\)'
        tags_33 = r'\((ADJ|ADJR|ADV|FP|N|NPR|NS|NUM|ONE|Q|VAG|VAN|VBN|VBPI|WPRO)(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?33(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+\)'

        if re.search(tags_22, self.lines[index]):
            match = self.lines[index]

            token_21 = re.sub('[\sA-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ\-0-9\(\)=]*\s+\([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?(-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)? \([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?21(-[NADG])? ', '', match)
            token_21 = re.sub('-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+\) \((ADJ|ADJR|ADV|FP|N|NPR|NS|NUM|ONE|Q|VAG|VAN|VBN|VBPI|WPRO)(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?22(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+\)+\n', '', token_21)

            token_22 = re.sub('[\sA-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ\-0-9\(\)=]*\s+\([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?(-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)? \([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?21(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+\) \((ADJ|ADJR|ADV|FP|N|NPR|NS|NUM|ONE|Q|VAG|VAN|VBN|VBPI|WPRO)(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?22(-[NADG])? ', '', match)
            token_22 = re.sub('-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+\)+\n', '', token_22)

            lemma_22 = re.sub('[\sA-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ\-0-9\(\)=]*\s+\([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?(-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)? \([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?21(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+\) \((ADJ|ADJR|ADV|FP|N|NPR|NS|NUM|ONE|Q|VAG|VAN|VBN|VBPI|WPRO)(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?22(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+-', '', match)
            lemma_22 = re.sub('\)+\n', '', lemma_22)

            new_token = token_21+token_22
            new_lemma = token_21+lemma_22
            new_token_lemma = new_token+'-'+new_lemma

            substitute_line = re.sub('\([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?21(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+\) \((ADJ|ADJR|ADV|FP|N|NPR|NS|NUM|ONE|Q|VAG|VAN|VBN|VBPI|WPRO)(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?22(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+\)', new_token_lemma, match)
            self.lines[index] = self.lines[index].replace(match, substitute_line)
            if re.search(r'<\/?dash\/?>',self.lines[index]):
                self.lines[index] = re.sub(r'<\/?dash\/?>', '', self.lines[index])
            return self

        elif re.search(tags_33, self.lines[index]):

            match = self.lines[index]

            token_31 = re.sub('[\sA-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ\-0-9\(\)=]*\s+\([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?(-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)? \([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?31(-[NADG])? ', '', match)
            token_31 = re.sub('-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+\) \([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?32(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+\) \([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?33(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+\)+\n', '', token_31)

            token_32 = re.sub('[\sA-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ\-0-9\(\)=]*\s+\([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?(-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)? \([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?31(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+\) \([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?32(-[NADG])? ', '', match)
            token_32 = re.sub('-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+\) \([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?33(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+\)+\n', '', token_32)

            token_33 = re.sub('[\sA-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ\-0-9\(\)=]*\s+\([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?(-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)? \([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?31(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+\) \([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?32(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+\) \([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?33(-[NADG])? ', '', match)
            token_33 = re.sub('-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+\)+\n', '', token_33)

            lemma_33 = re.sub('[\sA-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ\-0-9\(\)=]*\s+\([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?(-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)? \([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?31(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+\) \([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?32(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+\) \([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?33(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+-', '', match)
            lemma_33 = re.sub('\)+\n', '', lemma_33)

            new_token = token_31+token_32+token_33
            new_lemma = token_31+token_32+lemma_33
            new_token_lemma = new_token+'-'+new_lemma

            substitute_line = re.sub('\([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?31(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+\) \([A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?32(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+\) \((ADJ|ADJR|ADV|FP|N|NPR|NS|NUM|ONE|Q|VAG|VAN|VBN|VBPI|WPRO)(\+[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+)?33(-[NADG])? [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ<>]+\)', new_token_lemma, match)
            self.lines[index] = self.lines[index].replace(match, substitute_line)
            if re.search(r'<\/?dash\/?>',self.lines[index]):
                self.lines[index] = re.sub(r'<\/?dash\/?>', '', self.lines[index])
            return self

    def join_adverbs(self, index):
        '''
        # joins various words split by '$', mostly adverbs
            - einhvers$ $staðar e.g. 2008.ofsi.nar-sag.psd
            - annars$ $staðar e.g. 1250.sturlunga.nar-sag.psd
            - nokkurs$ $staðar e.g. 1680.skalholt.nar-rel.psd
            - annar$ $staðar e.g. 1888.grimur.nar-fic.psd
            - einhvers$ $konar e.g. 2008.ofsi.nar-sag.psd
            - hvers$ $konar e.g. 2008.ofsi.nar-sag.psd
        '''

        # regex for joining "einhvernveginn"
        einhvern_token = r'einhvern(?=\$)' # matches the token of 'einhvern' before a '$'
        einhvern_node = r'\((ONE\+)?Q-\w einhv[eö]rn?\$-einhver\)' # matches a whole 'einhvern$' node
        einhvern_trail_alt = r'(?<=einhvern)(?=\$)' # matches '$' at end of 'einhvern'\\
        einhvern_trail = r'(?<=einhvern)\$'

        einhvers_node = r'\((ONE\+)?Q-\w einhv[eö]r.\$-einhver\)'

        vegur_node = r'\(N-\w \$veg\$-vegur\)'
        vegur_token = r'(?<=\$)veg\$'

        timi_node = r'\(N-. \$tíman{0,2}-tími\)'
        timi_token = r'(?<=\$)tíman{0,2}'

        # other regex
        # second_node = r'\(N-\w \$.*-.*\)'
        general_first_node = r'\((ONE\+)?(Q|OTHER|D|WD)-\w [a-zþæðöáéýúíó]+\$-[a-zþæðöáéýúíó]+\)'
        general_first_token = r'[a-zþæðöáéýúíó]+\$'
        general_first_trail = r'(?<=[a-zþæðöáéýúíó])(?=\$)'
        general_first_split = r'(?<=[a-zþæðöáéýúíó])\$' # matches '$' at end of first token
        general_first_lemma = r'(?<=\$-)[a-zþæðöáéýúíó]+(?=\))'

        general_second_node = r'\(N-\w \$[^$\n]{2,}-[^$\n\)]*\)'
        general_second_token = r'(?<=\$)[a-zþæðöáéýúíó]+'
        general_second_lemma = r'(?<=-)[a-zþæðöáéýúíó]+(?=\)\))'


        noun_trail = r'(?<=)\$(?=-)' # matches the trailing "$" of a noun
        noun_node =  r' {0,1}\(((N|NS|NPR|NPRS)-|FW).*\$-' # matches a whole noun node
        noun_token_incompl = r'(?<=N-. )[^($]*(?=-)' # noun token where "$" is missing


        prev = index-1
        if re.search(einhvern_node, self.lines[index]) and re.search(vegur_node, self.lines[index]):
            '''einhvern$ $veg($ $)inn'''
            # print(curr, self.lines[index].strip())
            # print(re.findall(vegur_token, self.lines[index]))
            self.lines[index] = re.sub(einhvern_trail, re.findall(vegur_token, self.lines[index])[0], self.lines[index])
            self.lines[index] = re.sub(vegur_node, '', self.lines[index])
            # print('\t', curr, self.lines[index].strip('\n'))
            # out_file.write(self.lines[index])
        elif re.search(einhvern_node, self.lines[index]) and re.search(timi_node, self.lines[index]):
            '''einhvern$ $tímann'''
            # print(curr, self.lines[index].strip())
            self.lines[index] = re.sub(einhvern_trail, re.findall(timi_token, self.lines[index])[0], self.lines[index])
            self.lines[index] = re.sub(timi_node, '', self.lines[index])
            # print('\t', curr, self.lines[index].strip('\n'))
            # out_file.write(self.lines[index])
        elif re.search(general_first_node, self.lines[index]) and re.search(general_second_node, self.lines[index]) and not re.search(r'þann', self.lines[index]):
            # print(curr, self.lines[index].strip())
            self.lines[index] = re.sub(general_first_trail, re.findall(general_second_token, self.lines[index])[0], self.lines[index])
            self.lines[index] = re.sub(general_first_lemma, re.findall(general_first_token, self.lines[index])[0], self.lines[index])
            self.lines[index] = re.sub(general_first_split, '', self.lines[index])
            self.lines[index] = re.sub(general_second_node, '', self.lines[index])
            # print('\t', curr, lines[curr].strip())

    def join_various_nodes(self, index):
        '''
        # TODO:
            FINISH IMPLEMENTING SCRIPT

        Joins various nouns not covered by other parts of module.
        Mostly not systematic
        '''
        di_nodes = [
            ('Páls\$', '\$messu'),
            ('Staðar\$', '\$Kolbeins'),
            ('Staðar\$', '\$Böðvars'),
            ('Staðar<dash/>\$', '\$Böðvars'),
            ('vígsakar\$', '\$aðilinn'),
            ('tíunda\$', '\$skipti'),
            ('Helga\$', '\$son'),
            ('lögmáls\$', '\$lesturinn'),
            ('fórnfæringar\$', '\$sauðum'),
            ('leóns\$', '\$haus'),
            ('kirkju\$', '\$embættið'),
            ('guðssonar\$', '\$blóði'),
            ('öngvan\$', '\$eg\$'),
            ('Kirkjubóls\$', '\$ferð\$'),
            ('hvers\$', '\$kyns'),
            ('hnífs\$', '\$lag'),
            ('fram\$', '\$parti'),
            ('af\$', '\$reisu'),
            ('alls\$', '\$konar'),
            ('kirkju\$', '\$göngu\$'),
            ('Móðals\$', '\$felli'),
            ('einu\$', '\$sinni'),
            ('nokkurs\$', '\$staðar'),
            ('Árna\$', '\$nesi'),
            ('húss\$', '\$móðir\$'),
            ('Hallgríms\$', '\$son'),
            ('hagleiks\$', '\$gáfu'),
            ('mátt\$', '\$leysi'),
            ('hagleiks\$', '\$maður'),
            ('utan\$', '\$lands'),
            ('þess\$', '\$háttar'),
            ('gáleysis\$', '\$orð'),
            ('klausturs\$', '\$stapp'),
            ('frost\$', '\$veður'),
            ('Eiríks\$', '\$sonar'),
            ('bónda\$', '\$garði'),
            ('þrætu\$', '\$efni'),
            ('utan\$', '\$bæjar'),
            ('riddara\$', '\$sögum'),
            ('Íslendinga\$', '\$sögum'),
            ('ofbeldis\$', '\$gaur'),
            ('trúar\$', '\$lífinu'),
            ('Postulíns\$', '\$hundar'),
            ('glæpa\$', '\$beltinu'),
            ('gjör\$', '\$svo\$')
        ]

        tripart = ('Skaga\$', '\$fjarðar\$', '\$sýslum')

        first_token = r'(?<=-[A-Z] )[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ*$-<>]+(?=\$)' # matches first token, excluding "$"
        first_trail = r'(?<=)\$(?=-)' # matches the trailing "$" of a noun
        first_lemma = r'(?<=[a-zþæðöáéýúíó<>]-)[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(?=\))'
        second_node = r' ?\(N[A-Z]{0,3}-[A-Z] \$[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ*$-]*\)' # matches a whole determiner node
        second_token =  r'(?<=-. \$)[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]*(?=-)' # matches the token of the second node, excluding "$"
        second_lemma = r'(?<=[a-zþæðöáéýúíó]-)[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+(?=\))'

        pos_nodes = r'\(NP-POS \(N[A-Z]{0,2}-. [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ*$-<>]+\) \(CONJ og-og\) \(N[A-Z]{0,2}-. [A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ*<>]+\$-[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ*<>]+\)\)'

        prev = index-1
        next = index+1
        for pair in di_nodes:
            first_word = pair[0]
            second_word = pair[1]
            if re.search(second_word, self.lines[index]) and re.search(first_word, self.lines[index]):
                # print('\t', prev, self.lines[prev].strip())
                # print('\t', index, self.lines[index].strip())
                # print('\t', next, self.lines[next].strip())
                # print()

                new_lemma = re.findall(first_token, self.lines[index])[0] + re.findall(second_lemma, self.lines[index])[0]
                self.lines[index] = re.sub(first_trail, re.findall(second_token, self.lines[index])[0], self.lines[index])
                self.lines[index] = re.sub(second_node, '', self.lines[index])
                self.lines[index] = re.sub(first_lemma, new_lemma, self.lines[index])

                # print('\t\t', prev, self.lines[prev].strip())
                # print('\t\t', index, self.lines[index].strip())
                # print('\t\t', next, self.lines[next].strip())
                # print()

            elif re.search(second_word, self.lines[index]) and re.search(first_word, self.lines[prev]):
                # print('\t', prev, self.lines[prev].strip())
                # print('\t', index, self.lines[index].strip())
                # print('\t', next, self.lines[next].strip())
                # print()

                # print('\t\t', prev, self.lines[prev].strip())
                # print('\t\t', index, self.lines[index].strip())
                # print('\t\t', next, self.lines[next].strip())
                # print()

                pass
            elif re.search(second_word, self.lines[index]) and re.search(first_word, self.lines[prev-1]):
                # print('\t', prev, self.lines[prev-1].strip())
                # print('\t', prev, self.lines[prev].strip())
                # print('\t', index, self.lines[index].strip())
                # print('\t', next, self.lines[next].strip())
                # print()

                # print('\t\t', prev, self.lines[prev-1].strip())
                # print('\t\t', prev, self.lines[prev].strip())
                # print('\t\t', index, self.lines[index].strip())
                # print('\t\t', next, self.lines[next].strip())
                # print()

                pass
            # else:
            #     # print('\t', prev, self.lines[prev].strip())
            #     # print('\t', index, self.lines[index].strip())
            #     # print('\t', next, self.lines[next].strip())
            #     # print()
            #     pass
            elif re.search(pos_nodes, self.lines[index]):
                '''
                Possibly not fixable here...
                1022 (NP-SBJ (D-N þessi-þessi)
                1023 (NP-POS (N-G óþolinmæðis-óþolinmæði) (CONJ og-og) (N-G gáleysis$-gáleysi))
                1024 (NS-N $orð-orð))
                '''

                # print('\t', prev, self.lines[prev].strip())
                # print('\t', index, self.lines[index].strip())
                # print('\t', next, self.lines[next].strip())
                # print()



    def join_clitics(self, index):
        curr_line, prev_line = self.lines[index].split('\t'), self.lines[index-1].split('\t')
        if len(curr_line) == 1 or len(prev_line) == 1: return self
        if prev_line[4] == '_': return self
        # elif re.search('\$[a-zþæðöáéýúíó]', curr_line[1]):
        elif re.search('\$[ðtd]?[uú]', curr_line[1]) or re.search(r'\$ði', curr_line[1]):
            ''' All instance of "þú"-type clitics fixed here '''
            if prev_line[4] == 'C' or re.search(r'(BE|DO|HV|MD|RD|V(A|B))(P|D|N|)(I|S|N|G|)(-(N|A|D|G))?', prev_line[4]) == False:
                ''' Fixes 'at$ $tú' and 'því$ $at$ $tú' '''
                # print(prev_line)
                # print(curr_line)
                if prev_line[1][0] == '$':
                    ''' því$ $at$ $tú '''
                    prevprev_line = self.lines[index-2].split('\t')
                    joined_token = prevprev_line[1] + prev_line[1] + curr_line[1]
                    joined_token = re.sub(r'\$\$', '', joined_token)
                    joined_number = prevprev_line[0] + '-' + curr_line[0]
                    new_line = '\t'.join([joined_number, joined_token, '_', '_', '_', '_', '_', '_', '_', '_\n'])
                    curr_line[1] = re.sub(r'\$[tðd]?[uú]', 'þú', curr_line[1])
                    prev_line[1] = re.sub(r'\$', '', prev_line[1])
                    prevprev_line[1] = re.sub(r'\$', '', prevprev_line[1])
                    curr_line[9] = re.sub(r'\|SpaceAfter=No', '', curr_line[9])
                    curr_line[9] = re.sub(r'SpaceAfter=No', '_', curr_line[9])
                    prev_line[9] = re.sub(r'\|SpaceAfter=No', '', prev_line[9])
                    prev_line[9] = re.sub(r'SpaceAfter=No', '_', prev_line[9])
                    self.lines[index], self.lines[index-1], self.lines[index-2] = '\t'.join(curr_line), '\t'.join(prev_line), '\t'.join(prevprev_line)
                    self.lines.insert(index-2, new_line)
                    # print(new_line.strip('\n'))
                    # print(prevprev_line)
                    # print(prev_line)
                    # print(curr_line)
                else:
                    ''' at$ $tú '''
                    joined_token = prev_line[1] + curr_line[1]
                    joined_token = re.sub(r'\$\$', '', joined_token)
                    # print(joined_token)
                    joined_number = prev_line[0] + '-' + curr_line[0]
                    if re.search(r'SpaceAfter=No', curr_line[9]):
                        new_line = '\t'.join([joined_number, joined_token, '_', '_', '_', '_', '_', '_', '_', 'SpaceAfter=No\n'])
                    else:
                        new_line = '\t'.join([joined_number, joined_token, '_', '_', '_', '_', '_', '_', '_', '_\n'])
                    curr_line[1] = re.sub(r'\$[tðd]?[uú]', 'þú', curr_line[1])
                    prev_line[1] = re.sub(r'\$', '', prev_line[1])
                    # print(prev_line)
                    # print(curr_line)
                    # print(new_line.strip('\n'))
                    curr_line[9] = re.sub(r'\|SpaceAfter=No', '', curr_line[9])
                    curr_line[9] = re.sub(r'SpaceAfter=No', '_', curr_line[9])
                    prev_line[9] = re.sub(r'\|SpaceAfter=No', '', prev_line[9])
                    prev_line[9] = re.sub(r'SpaceAfter=No', '_', prev_line[9])
                    self.lines[index], self.lines[index-1] = '\t'.join(curr_line), '\t'.join(prev_line)
                    self.lines.insert(index-1, new_line)
                return
            # print(prev_line)
            # print(curr_line)
            joined_token = prev_line[1] + curr_line[1]
            if len(prev_line[4]) == 3 and prev_line[4][-1] == 'I':
                # print('IMPERATIVE!!!')
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
            elif re.search(r'[^g][iu]\$', prev_line[1]):
                prev_line[1] = re.sub(r'\$', 'ð', prev_line[1])
            else:
                prev_line[1] = re.sub(r'\$', '', prev_line[1])
            curr_line[1] = re.sub(r'\$[tðd]?[uú]', 'þú', curr_line[1])
            curr_line[1] = re.sub(r'\$ði', 'þið', curr_line[1])
            joined_token = re.sub(r'\$\$', '', joined_token)
            joined_number = prev_line[0] + '-' + curr_line[0]
            if re.search(r'SpaceAfter=No', curr_line[9]):
                new_line = '\t'.join([joined_number, joined_token, '_', '_', '_', '_', '_', '_', '_', 'SpaceAfter=No\n'])
            else:
                new_line = '\t'.join([joined_number, joined_token, '_', '_', '_', '_', '_', '_', '_', '_\n'])
            curr_line[9] = re.sub(r'\|SpaceAfter=No', '', curr_line[9])
            curr_line[9] = re.sub(r'SpaceAfter=No', '_', curr_line[9])
            prev_line[9] = re.sub(r'\|SpaceAfter=No', '', prev_line[9])
            prev_line[9] = re.sub(r'SpaceAfter=No', '_', prev_line[9])
            self.lines[index], self.lines[index-1] = '\t'.join(curr_line), '\t'.join(prev_line)
            # print(new_line.strip('\n'))
            # print(prev_line)
            # print(curr_line)
            self.lines.insert(index-1, new_line)
        # elif re.search('\$[A-Za-zþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ]+', curr_line[1]):
        #     print(index-1, prev_line)
        #     print(index, curr_line)
        elif re.search(r'\$ð?i$', curr_line[1]):
            '''Clitics on plural interrogative verb forms, "borðið$ $i"   '''
            joined_token = prev_line[1] + curr_line[1]
            joined_token = re.sub(r'\$\$', '', joined_token)
            joined_number = prev_line[0] + '-' + curr_line[0]
            if re.search(r'SpaceAfter=No', curr_line[9]):
                new_line = '\t'.join([joined_number, joined_token, '_', '_', '_', '_', '_', '_', '_', 'SpaceAfter=No\n'])
            else:
                new_line = '\t'.join([joined_number, joined_token, '_', '_', '_', '_', '_', '_', '_', '_\n'])
            prev_line[1] = re.sub(r'\$', '', prev_line[1])
            curr_line[1] = re.sub(r'\$i', 'þið', curr_line[1])
            # print(new_line.strip('\n'))
            # print(index-1, prev_line)
            # print(index, curr_line)
            curr_line[9] = re.sub(r'\|SpaceAfter=No', '', curr_line[9])
            curr_line[9] = re.sub(r'SpaceAfter=No', '_', curr_line[9])
            prev_line[9] = re.sub(r'\|SpaceAfter=No', '', prev_line[9])
            prev_line[9] = re.sub(r'SpaceAfter=No', '_', prev_line[9])
            self.lines[index], self.lines[index-1] = '\t'.join(curr_line), '\t'.join(prev_line)
            self.lines.insert(index-1, new_line)
        elif re.search(r'\$(S|s|a|[kg][ia]?|veg)$', curr_line[1]):
            '''Old Norse clitics, -a, -k, -s, -gi, -ki'''
            # print(index-1, prev_line)
            # print(index, curr_line)
            joined_token = prev_line[1] + curr_line[1]
            joined_token = re.sub(r'\$\$', '', joined_token)
            joined_number = prev_line[0] + '-' + curr_line[0]
            if re.search(r'SpaceAfter=No', curr_line[9]):
                new_line = '\t'.join([joined_number, joined_token, '_', '_', '_', '_', '_', '_', '_', 'SpaceAfter=No\n'])
            else:
                new_line = '\t'.join([joined_number, joined_token, '_', '_', '_', '_', '_', '_', '_', '_\n'])
            prev_line[1] = re.sub(r'\$', '', prev_line[1])
            if curr_line[2] == 'kostur':
                return self
            elif curr_line[2] == 'ég':
                curr_line[1] = re.sub(r'\$k', 'ek', curr_line[1])
                # print(new_line.strip('\n'))
                # print(index-1, prev_line)
                # print(index, curr_line)
            elif curr_line[2] == 'es':
                curr_line[1] = re.sub(r'\$s', 'es', curr_line[1])
                # print(new_line.strip('\n'))
                # print(index-1, prev_line)
                # print(index, curr_line
            elif curr_line[2] == 'er':
                curr_line[1] = re.sub(r'\$s', 'es', curr_line[1])
            elif curr_line[2] == 'a':
                curr_line[1] = re.sub(r'\$k', '', curr_line[1])
                # print(new_line.strip('\n'))
                # print(index-1, prev_line)
                # print(index, curr_line)
            elif curr_line[2] == 'sem':
                curr_line[1] = re.sub(r'\$s', 'sem', curr_line[1])
            elif curr_line[2] in {'ekki', 's', 'at', 'gi', 'k', 'vegur'}:
                curr_line[1] = re.sub(r'\$', '', curr_line[1])
                # print(new_line.strip('\n'))
                # print(index-1, prev_line)
                # print(index, curr_line)
            curr_line[9] = re.sub(r'\|SpaceAfter=No', '', curr_line[9])
            curr_line[9] = re.sub(r'SpaceAfter=No', '_', curr_line[9])
            prev_line[9] = re.sub(r'\|SpaceAfter=No', '', prev_line[9])
            prev_line[9] = re.sub(r'SpaceAfter=No', '_', prev_line[9])
            self.lines[index], self.lines[index-1] = '\t'.join(curr_line), '\t'.join(prev_line)
            self.lines.insert(index-1, new_line)
            # print(new_line.strip('\n'))
            # print(index-1, prev_line)
            # print(index, curr_line)
        elif re.search(r'[þÞ]\$', prev_line[1]):
            '''Old Norse clitic þ-, e.g. þ$ $eygi = þó eygi'''
            joined_token = prev_line[1] + curr_line[1]
            joined_token = re.sub(r'\$\$', '', joined_token)
            joined_number = prev_line[0] + '-' + curr_line[0]
            if re.search(r'SpaceAfter=No', curr_line[9]):
                new_line = '\t'.join([joined_number, joined_token, '_', '_', '_', '_', '_', '_', '_', 'SpaceAfter=No\n'])
            else:
                new_line = '\t'.join([joined_number, joined_token, '_', '_', '_', '_', '_', '_', '_', '_\n'])
            prev_line[1] = re.sub(r'þ\$', 'þó', prev_line[1])
            prev_line[1] = re.sub(r'Þ\$', 'ÞÓ', prev_line[1])
            curr_line[1] = re.sub(r'\$', '', curr_line[1])
            curr_line[9] = re.sub(r'\|SpaceAfter=No', '', curr_line[9])
            curr_line[9] = re.sub(r'SpaceAfter=No', '_', curr_line[9])
            prev_line[9] = re.sub(r'\|SpaceAfter=No', '', prev_line[9])
            prev_line[9] = re.sub(r'SpaceAfter=No', '_', prev_line[9])
            self.lines[index], self.lines[index-1] = '\t'.join(curr_line), '\t'.join(prev_line)
            self.lines.insert(index-1, new_line)
            # print(new_line.strip('\n')
        return self

    def fix_joined_space_after(self, index):

        curr_line, token_end_line = self.lines[index].split('\t'), self.lines[index+2].split('\t')
        if len(curr_line) == 1 or len(token_end_line) == 1: return self
        # if token_end_line[4] == '_': return self
        elif re.search(r'\d+-\d+', curr_line[0]):
            print('ID match')
            if re.search(r'SpaceAfter=No', token_end_line[9]):
                print('SpaceAfter match')
                token_end_line[9] = re.sub(r'\|SpaceAfter=No', '', token_end_line[9])
                curr_line[9] = 'SpaceAfter=No\n'
                self.lines[index], self.lines[index+2] = '\t'.join(curr_line), '\t'.join(token_end_line)



    def iterate_nodes(self):
        '''
        Runs input file through each method, line by line
        Mostly used for debugging
        '''
        # print(self.name)
        # print(self.file_type)
        if self.file_type == '.psd':
            for current_line_num in self.indexes:
                # adverbs processed
                self.join_adverbs(current_line_num)
                # NPs processed
                self.join_NPs(current_line_num)
                self.join_split_nodes(current_line_num)
                # verbs processed
                self.join_verbs_same_line(current_line_num)
                self.join_verbs_two_lines(current_line_num)
                self.join_verbs_three_lines(current_line_num)
                # adjectives processed
                self.join_adjectives(current_line_num)
                # various remaining nodes processed
                self.join_various_nodes(current_line_num)
        elif self.file_type == '.conllu':
            for current_line_num in reversed(self.indexes):
                self.join_clitics(current_line_num)
                self.fix_joined_space_after(current_line_num)
        return self

    # def _create_out_dir(self):
    #     if not os.path.isdir(self.out_dir):
    #         os.mkdir(self.out_dir)
    #     # else:
        #     print('Output directory already exists. Remove and run again.')

class SentJoiner():
    '''
    '''
    def __init__(self, graph_list):
        # self.input_lines = file.readlines()
        # self.path = file.name
        # self.line_indexes = range(len(self.input_lines))
        # self.last_num = None
        # self.name = os.path.basename(file.name)
        # self.joined_sents = []
        self.sent_num = len(graph_list)
        self.new_token_ID = 0
        self.old_new_tokens = defaultdict(None)
        self.token_key = None
        self.first_root = None
        # self.lines = []


    def _join_sents(self):
        joined = ''
        for i in self.line_indexes:
            # self.input_lines[i] = self.input_lines[i].split('\t')
            if self.input_lines[i][0] in {'#', '\n'}: continue
            # elif self.input_lines[i+1]: # for catching eof
            if re.search(r'^1\t[A-ZÞÆÐÖÁÉÝÚÍÓ]', self.input_lines[i]):
                # self.joined_sents.append(new_sent)
                # new_sent = ''
                joined += '\n'
                joined += self.input_lines[i]
            else:
                joined += self.input_lines[i]
        # self.joined_sents = [pyconll.load_from_string(sentence) for sentence in corpus.joined_sents]
        self.joined_sents = joined

    def _set_sent_ID(self):
        ID = '%s_%s' % (self.name, self.sent_num)
        return ID

    def _get_keys(self):
        self.token_key = token.form + '-' + token.id

    def _set_token_IDs(self, sentence):
        subsentence = 0
        for token in sentence:
            if '-' in token.id:
                return sentence
            if token.id == '1':
                subsentence += 1
            self.new_token_ID += 1
            placeholder_ID = '.'.join([token.id, str(self.new_token_ID), str(subsentence)])
            # print(token.id, token.form)
            self.token_key = '-'.join([token.form, placeholder_ID, str(subsentence)])
            # self.new_token_ID += 1
            if int(token.id) != self.new_token_ID:
                self.old_new_tokens[token.id] = token.form, str(self.new_token_ID)
                token.id = placeholder_ID
                # print('Old:', token.id, token.form)
                # print('New:', token.id, token.form)
                # print('\t', token.id)
        for token in sentence:
            if not '.' in token.id:
                # print(token.conll())
                if token.deprel == 'root':
                    self.first_root = token.id
            else:
                try:
                    token.head = self.old_new_tokens[token.head][1]
                    # print(token.conll())
                except KeyError:
                    token.head = self.first_root
                    token.deprel = 'conj'
                    # print(token.conll())
                finally:
                    token.id = token.id.split('.')[1]

        return sentence

    def _add_to_fixed(self, sent):
        self.lines.append(sent)
        self.lines.append('\n\n')

    def set_vars(self):
        '''
        Sets all object attributes for CoNLL-U file
        '''
        # sentences joined based on punctuation
        self._join_sents()
        # CoNLL-U object read from string as iterable
        conll = pyconll.iter_from_string(self.joined_sents) # reads sentence
        # iterated through sentences
        for sentence in conll:
            self.sent_num += 1
            # function called to set sentence ID
            sentence.id = self._set_sent_ID()
            # function called to set token IDs and fix dependency heads
            sentence = self._set_token_IDs(sentence)
            # new token ID attribute zeroed out
            self.new_token_ID = 0
            # print(sentence.conll())
            # print(self.old_new_tokens)

            # input()
            self.old_new_tokens = defaultdict(None)
            self._add_to_fixed(str(sentence.conll()))

class FileWriter():
    '''
    Class to write .lines attribute of a Joiner object (NodeJoiner,
    SentJoiner) to an outut file.
    '''
    def __init__(self, Joiner):
        self.j = Joiner
        self.out_dir = os.path.dirname(self.j.path) + '_out' + datetime.today().strftime('_%d-%m-%Y')


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
            outname = os.path.join(self.out_dir, self.j.name + '.tmp')
        else:
            outname = self.j.path + '.tmp'
        if os.path.exists(outname):
            print('File already exists. Run script again.')
            os.remove(outname)
            return
        with open(outname, 'w') as file:
            # print('Writing to file:', self.name)
            for line in self.j.lines:
                file.write(line)
        if overwrite == True:
            os.remove(self.j.path)
            os.rename(outname, self.j.path)


if __name__ == '__main__':

    for file in os.listdir('testing/corpora/icecorpus/psd'):
    # for file in os.listdir('testing/CoNLLU_output'):
        # IN_FILE = os.path.join('testing/CoNLLU_output', file)
        IN_FILE = os.path.join('testing/corpora/icecorpus/psd', file)
        # IN_FILE = sys.argv[1]
        file = open(IN_FILE, 'r')
        j = NodeJoiner(file)
        print(j.name)
        j.iterate_nodes()
        # for current_line_num in j.indexes:
        #     # print(current_line_num)
        #     # if j.file_type == '.psd':
        #     j.join_various_nouns(current_line_num)
            # elif j.file_type == '.conllu':
            #     pass
        # j.write_to_file(sepdir=True, overwrite=False)
        # for name in os.listdir(IN_DIR):
        #     file = open(os.path.join(IN_DIR, name), 'r')
        #     j = NodeJoiner(file)
        #     j.iterate_nodes()
        #     j.write_to_file(sepdir=False, overwrite=True)
        # print('Done.')
