import os
import re
import string
import os
from pprint import pprint
from collections import defaultdict

# in_path = str(sys.argv[1])
# in_path = 'taggers/test_conllu/2008.mamma.nar-fic.conllu'
in_path = 'testing/CoNLLU_output/2008.ofsi.nar-sag.conllu'
out_path = in_path + '.tmp'

filename = os.path.basename(in_path)

OTB_path = os.path.join('taggers','tagged', re.sub('conllu', 'txt.tagged', filename))
# OTB_path = 'taggers/tagged/2008.mamma.nar-fic.txt.tagged'

CoNLLU_file = open(in_path, 'r')
OTB_file = open(OTB_path, 'r')

CoNLLU_lines = [line.split('\t') for line in list(CoNLLU_file.readlines())]



def getTagDict(file):
    index = 0
    # empty tuple returned to trip token correction if end of dict found
    indexedWords = defaultdict(lambda: ('',''))
    for line in file.readlines():
        # print(line)
        if not '\t' in line: continue
        word,tag = line.strip('\n').split('\t')
        index += 1
        indexedWords[index] = word, tag
    return indexedWords

OTB_tagDict = getTagDict(OTB_file)

OTB_map = {
        'Gender' : {
            'k' : 'Masc',
            'v' : 'Fem',
            'h' : 'Neut',
            'x' : 'None'
        },
        'Number': {
            'f' : 'Plur',  # noun, plural number
            'e' : 'Sing'    # noun singular number
        },
        'PronType' : {
            'p' : 'Prs',    #personal
            'e' : 'Prs',    #posessive (tagged as personal)
            # 'a' : 'Rcp',   #reciprocal
            's' : 'Int',     #interrogative
            't' : 'Rel',     #relative
            'a' : 'Dem',     #demonstrative
            'b' : 'Dem',
            'o' : 'Ind'    #indefinite
        },
        'Tense' : {
            'n' : 'Pres',   #present tense
            'þ' : 'Past',    #past tense
            'NF' : None
        },
        'Person' : {
            '1' : '1',
            '2' : '2',
            '3' : '3'
        },
        'Case' : {
            'n' : 'Nom',   # nominative case
            'o' : 'Acc',   # accusative case
            'þ' : 'Dat',  # dative case
            'e' : 'Gen',   # dative case
            None : 'Nom'
        },
        'Mood' : {
            'n' : 'infinitive',
            'b' : 'Imp',  #imperative
            'f' : 'Ind',   #indicative
            'v' : 'Sub',   #subjunctive
            'I' : 'Ind',    #indicative (IcePaHC POS-tag)
            'S' : 'Sub',    #subjunctive (IcePaHC POS-tag)
            'OSKH' : None   # TEMP
        },
        'VerbForm' : {
            '' : 'Fin',     #finite verb
            'n' : 'Inf',     #infinitive verb
            'l' : 'Part',     #participle
            'þ' : 'Part',     #participle
            's' : 'Sup'
        },
        'Voice' : {
            'g' : 'Act',     #active voice
            'm' : 'Mid',     #middle voice
            'pass' : 'Pass'     #passive voice
        },
        'Definite' : {
            's' : 'Ind', # adjectives
            'v' : 'Def', # adjectives
            'g' : 'Def', # nouns
            'o' : 'ÓBEYGT',
            None : 'Ind'
        },
        'Degree' : {
            'f' : 'Pos', # adjectives
            'm' : 'Com', # adjectives
            'e' : 'Sup' # nouns
        },
        'NumType' : {
            'f' : 'Card',    #Cardinal number
            'a' : 'Card',
            'o' : 'Ord',     # FIX Ordinal number (not in OTB tag)
            'p' : 'Frac'     #Fraction
        }
    }

UD_map = {
    # ipsd_tag : UD_tag
    'N' : 'NOUN',   # generalized nouns tagged as NOUN
    'D' : 'DET',    # generalized determiners tagged as DET (determiner)
    'ONE' : 'DET',  #ath. áður taggað sem NUM
    'ONES' : 'DET',
    'P' : 'ADP',    # generalized prepositions tagged as ADP
    'RP' : 'ADP',   # specifiers of P/complements of P - Ath. flokka sem eitthvað annað?
    'RPX' : 'ADP',
    'Q' : 'ADJ',    # quantifiers tagged as ADJ - ATH ÞETTA ÞARF AÐ ENDURSKOÐA
    'C' : 'SCONJ',  # complimentizer tagged as SCONJ (subordinate conjunction)
    'V' : 'VERB',
    'DO' : 'VERB',  #'gera', do, tagged as verb
    'HV' : 'AUX',   #'have' tagged as auxiliary verb
    'MD' : 'AUX',   #modal verbs tagged as auxiliary
    'RD' : 'VERB',    #'verða', become, tagged as verb
    'W' : 'DET',    # WH-determiner tagged as DET (determiner)
    'R' : 'VERB',   # All forms of "verða" tagged as VERB
    'TO' : 'PART',  # Infinitive marker tagged as PART (particle)
    'FP' : 'PART',  #focus particles marked as PART
    'NPR' : 'PROPN', # proper nouns tagged as PROPN
    'NPRS': 'PROPN',
    'PRO' : 'PRON',
    'WQ' : 'PRON',  #interrogative pronoun
    'WPRO' : 'PRON',  #wh-pronouns
    'SUCH' : 'PRON',
    'ES' : 'PRON',  #expletive tagged as PRON
    'MAN' : 'PRON',
    'NUM' : 'NUM',
    'ADJ' : 'ADJ',  # Adjectives tagged as ADV
    'ADJR' : 'ADJ', # Comparative adjectives tagged as ADV
    'ADJS' : 'ADJ', # Superlative adjectives tagged as ADV
    'ADV' : 'ADV',  # Adverbs tagged as ADV
    'WADV' : 'ADV', #TODO: ath. betur - bara spor?
    'NEG' : 'ADV',
    'ADVR' : 'ADV', # Comparative adverbs tagged as ADV
    'ADVS' : 'ADV', # Superlative adverbs tagged as ADV
    'ALSO' : 'ADV',
    'OTHER' : 'PRON',
    'OTHERS' : 'PRON',
    'INTJ' : 'INTJ',    #interjection
    'FW' : 'X',
    'X' : 'X'
}



class IcelandicUDFeatures:
    """
    Class for handling features of a Word class object
    Each feature is an instance variable with default value None and is updated
    by class methods in Word class (see below), per word
    """

    def __init__(self):
        # Feature list
        self.Case = None
        self.Number = None
        self.Definite = None
        self.Gender = None
        self.PronType = None
        self.Degree = None
        self.Mood = None
        self.Tense = None
        self.VerbForm = None
        self.Voice = None
        self.Person = None
        self.NumType = None
        self.AdpType = None
        self.Clitic = None
        self.Foreign = None
        # Compiled features
        self.all_features = None
        # Debug
        self.ERROR = None

    def setAll_features(self):
        '''
        Joins features present into a dict object (self.all_features) where
        feature variable names are keys and with their respective attr values
        as dict values
        '''
        if not isinstance(self.all_features, str):
            feats = {}
            for k,v in self.__dict__.items():
                if v is not None:
                    feats[k] = v
                else:
                    continue
            self.all_features = feats

    def featString(self):
        '''
        returns feature dict in string format that matches ConllU output
        returns '_' if feature dict empty

        ex: Number=Plur|Mood=Sub|Tense=Pres|Voice=Act|Person=1
        ex: _

        # TODO: FIX ORDER
        '''
        # TODO: Order output (random as is)
        NoneType = type(None)
        if not isinstance(self.all_features, (str, NoneType)):
            return '|'.join(['='.join([k,v]) for k,v in self.all_features.items()])
        else:
            return self.all_features



class features():
    '''
    '''
    def __init__(self, index, word_index):
        self.index = index
        self.word_index = word_index
        self.curr_line = self._get_line(CoNLLU_lines)
        # self.next_line = CoNLLU_lines[index+1]
        # self.prev_line = CoNLLU_lines[index-1]
        # self.prevprev_line = CoNLLU_lines[index-2]
        self.token = None
        self.IcePaHC_tag = None
        self.UD_tag = None
        self.OTB_token = None
        self.OTB_tag = None
        self.return_count = None
        self.features = IcelandicUDFeatures()
        self.methods = {
            'n' : self._noun_features,
            'l' : self._adjective_features,
            'f' : self._pronoun_features,
            'g' : self._determiner_features,
            't' : self._numeral_features,
            's' : self._verb_features,
            'a' : self._adverb_features,
            'e' : self._other_features,
            'x' : self._other_features
        }

    def _get_line(self, lst):
        if len(lst[self.index]) == 10:
            curr_line = lst[self.index]
            return curr_line

    def correct_token(self):
        self.word_index -= 1
        # if self.token == OTB_tagDict[self.word_index]:
        return self.get_OTB_tag()
        # else:
        #     print(self.token, OTB_tagDict[self.word_index][0], OTB_tagDict[self.word_index][1])
        #     self.OTB_token, self.OTB_tag == None, None
        #     return self

    def _noun_features(self, tag):
        if '-' in tag:
            tag, tag_extra = tag.split('-')
        self.features.Gender = OTB_map['Gender'][tag[1]]
        self.features.Number = OTB_map['Number'][tag[2]]
        self.features.Case = OTB_map['Case'][tag[3]]
        if len(tag) > 4:
            self.features.Definite = OTB_map['Definite'][tag[4]]
        else:
            self.features.Definite = OTB_map['Definite'][None]
        return self

    def _adjective_features(self, tag):
        self.features.Gender = OTB_map['Gender'][tag[1]]
        self.features.Number = OTB_map['Number'][tag[2]]
        self.features.Case = OTB_map['Case'][tag[3]]
        self.features.Definite = OTB_map['Definite'][tag[4]]
        self.features.Degree = OTB_map['Degree'][tag[5]]
        return self

    def _pronoun_features(self, tag):
        self.features.PronType = OTB_map['PronType'][tag[1]]
        if tag[2] in {'1', '2'}:
            self.features.Person = OTB_map['Person'][tag[2]]
        else:
            self.features.Gender = OTB_map['Gender'][tag[2]]
        self.features.Number = OTB_map['Number'][tag[3]]
        self.features.Case = OTB_map['Case'][tag[4]]
        return self

    def _determiner_features(self, tag):
        self.features.Gender = OTB_map['Gender'][tag[1]]
        self.features.Number = OTB_map['Number'][tag[2]]
        self.features.Case = OTB_map['Case'][tag[3]]
        return self

    def _numeral_features(self, tag):
        self.features.NumType = OTB_map['NumType'][tag[1]]
        if len(tag) > 2:
            self.features.Gender = OTB_map['Gender'][tag[2]]
            self.features.Number = OTB_map['Number'][tag[3]]
            self.features.Case = OTB_map['Case'][tag[4]]
        return self

    def _verb_features(self, tag):
        if tag[1] not in {'s', 'þ', 'l', 'n'}:
            self.features.Mood = OTB_map['Mood'][tag[1]]
            self.features.Voice = OTB_map['Voice'][tag[2]]
            self.features.Person = OTB_map['Person'][tag[3]]
            self.features.Number = OTB_map['Number'][tag[4]]
            self.features.Tense = OTB_map['Tense'][tag[5]]
            self.features.VerbForm = OTB_map['VerbForm']['']
        elif tag[1] in {'þ', 'l'}:
            self.features.VerbForm = OTB_map['VerbForm'][tag[1]]
            self.features.Voice = OTB_map['Voice'][tag[2]]
            if tag[1] == 'þ':
                self.features.Gender = OTB_map['Gender'][tag[3]]
                self.features.Number = OTB_map['Number'][tag[4]]
                self.features.Case = OTB_map['Case'][tag[5]]
        else:
            self.features.VerbForm = OTB_map['VerbForm'][tag[1]]
            self.features.Voice = OTB_map['Voice'][tag[2]]
        return self

    def _adverb_features(self, tag):
        if tag[-1] in {'m', 'e'}:
            if len(tag) == 2:
                return self
            else:
                self.features.Degree = OTB_map['Degree'][tag[-1]]
        else:
            self.features.Degree = OTB_map['Degree']['f']
        return self

    def _other_features(self, tag):
        if tag[0] == 'e':
            self.features.Foreign = 'Yes'

    def _get_features(self, tag):
        self.methods.get(tag[0], lambda x: 'x')(tag)
        self.features.setAll_features()
        return self

    # Here follow methods for finding a word's UD-tag from its IcePaHC tag

    def _get_IcePaHC_tag(self):
        '''
        Isolates IcePaHC tag from line and saves as instance variable
        '''
        if isinstance(self.curr_line, list):# and self.curr_line[4] == 'None':
            self.IcePaHC_tag = self.curr_line[4]
            self._tag_cleanup()
            return self

    def _split_tag(self):
        '''
        Splits IcePaHC tag into sub-parts if '-' in tag (returns only first part)
        '''
        if '-' in self.IcePaHC_tag:
            self.IcePaHC_tag = self.IcePaHC_tag.split('-', 1)[0]
            return self
        else:
            self.IcePaHC_tag = self.IcePaHC_tag
            return self

    def _tag_cleanup(self):
        '''
        Removes various unimportant information from IcePaHC tag
        '''
        if self.IcePaHC_tag == 'ADV-Q-N':
            self.IcePaHC_tag = re.sub('ADV-', '', self.IcePaHC_tag)
        if self.IcePaHC_tag == 'ADVR-Q-D':
            self.IcePaHC_tag = re.sub('ADVR-', '', self.IcePaHC_tag)
        if self.IcePaHC_tag == 'RP-2':
            self.IcePaHC_tag = re.sub('-2', '', self.IcePaHC_tag)
        self.IcePaHC_tag = re.sub(r'-(1|2|3)', '', self.IcePaHC_tag) # removes all '-(1/2/3)' from tags
        # TODO: find permanent fix for this, where -N is not default
        # e.g. join words in .psd file that have these numbers in tag
        if re.search(r'\w{1,5}(21|22|31|32|33)', self.IcePaHC_tag):
            self.IcePaHC_tag = re.sub(r'(21|22|31|32|33)', '-N', self.IcePaHC_tag)
        return self._split_tag()

    def get_UD_tag(self):
        '''
        Checks IcePaHC POS-tag of word and saves Universal Dependency format
        POS-tag as instance variable (self.UD_tag) by comparing with 'tags' dict
        '''
        self._get_IcePaHC_tag()
        if self.IcePaHC_tag:
            try:
                self.UD_tag = UD_map[self.IcePaHC_tag]
                return self
            except:
                # raise
                if re.search(r'(DO|DA|RD|RA)', self.IcePaHC_tag[0:2]):
                    self.UD_tag = 'VERB'       #ATH. merkt sem sögn í bili
                    return self
                elif re.search(r'(BE|BA|HV|HA|MD|MA)', self.IcePaHC_tag[0:2]):
                    self.UD_tag = 'AUX'
                    return self
                elif self.IcePaHC_tag == 'CONJ':
                    self.UD_tag = 'CCONJ'
                    return self
                elif self.IcePaHC_tag in string.punctuation:
                    self.UD_tag = 'PUNCT'
                    return self
                else:
                    self.UD_tag = UD_map.get(self.IcePaHC_tag[0], '_')
                    return self


    def get_OTB_tag(self):
        self.return_count = 0
        if self.curr_line:
            self.token = re.sub(r'<dash/?>', '-', self.curr_line[1])
            if self.token[-1] == '.' and len(self.token) > 1:
                self.token = self.token[:-1]
            if not len(self.curr_line) == 10:
                return self
            if self.token == '<' and OTB_tagDict[self.word_index][0] == '-':
                self.token = '-'
                self.OTB_token = OTB_tagDict[self.word_index][0]
                self.OTB_tag = OTB_tagDict[self.word_index][1]
                return self
            if self.token == '<' and not self.curr_line[1] == OTB_tagDict[self.word_index][0]:
                return self
            if self.token[-1] == '$':
                self.OTB_token = OTB_tagDict[self.word_index][0] + '($ split)'
                self.OTB_tag = OTB_tagDict[self.word_index][1]
                return self
            if self.token[0] == '$':
                return self
            if self.curr_line[1] == self.curr_line[2] == self.curr_line[3] == 'None':
                return self
            # if self.token[-1] == '.':
            #     self.token = self.token[:-1]
            #     self.correct_token()
            #     self.return_count += 1
            #     # print(self.word_index, self.return_count)
            #     return self
            # if '_' in self.curr_line[3]:
            #     self.OTB_token = 'Placeholder'
            #     self.OTB_tag = 'Placeholder'
            #     return self
            # if len(self.prev_line) == 10 and '_' in self.prev_line[3]:
            #     self.OTB_token = OTB_tagDict[self.word_index][0]
            #     self.OTB_tag = OTB_tagDict[self.word_index][1]
            #     return self
            # if len(self.prevprev_line) == 10 and '_' in self.prevprev_line[3]:
            #     self.OTB_token = 'Placeholder'
            #     self.OTB_tag = 'Placeholder'
            #     return self
            elif not self.token in OTB_tagDict[self.word_index][0]:
                # self.OTB_token = OTB_tagDict[self.word_index][0]
                # self.OTB_tag = OTB_tagDict[self.word_index][1]
                # print(self.word_index, self.token, self.OTB_token, self.OTB_tag)
                self.correct_token()
                self.return_count += 1
                # print(self.word_index, self.return_count)
                return self
            else:
                self.OTB_token = OTB_tagDict[self.word_index][0]
                self.OTB_tag = OTB_tagDict[self.word_index][1]
                # self._get_features(self.OTB_tag)
                return self
        else:
            return self

CoNLLU_file.close()
OTB_file.close()

if __name__ == '__main__':
    line_indexes = [i for i in range(len(CoNLLU_lines))]
    word_index = 1
    # pprint(OTB_tagDict)
    '''
    for i in OTB_tagDict.items():
        print(i)
    '''
    for i in line_indexes:
        if i <= 4452:
            f = features(i, word_index)
            f.get_UD_tag()
            f.get_OTB_tag()
            # print(f.index, f.IcePaHC_tag, f.UD_tag)
            if f.OTB_token == 'Placeholder':
                print(f.word_index, f.token, f.OTB_token, f.OTB_tag, f.UD_tag)
            elif f.OTB_tag:
                word_index += 1
                print(f.word_index, f.token, f.OTB_token, f.OTB_tag, f.UD_tag)
