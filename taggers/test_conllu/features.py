
'''
features rewrite
Hinrik Hafsteinsson (hih43@hi.is)
Þórunn Arnardóttir (tha86@hi.is)
2019
Part of UniTree project for IcePaHC
'''

import string
import re
from collections import OrderedDict
import inspect

OTB_map = {
        'Gender' : { # TODO: add gender to feature matrix
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
            'b' : 'Dem'
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
            'e' : 'Dat',   # dative case
            None : 'Nom'
        },
        'Mood' : {
            'n' : 'infinitive'
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
            'l' : 'Part'     #participle
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
            None : None
        },
    },


def error_info(err):
    '''
    Debug method
    Returns the current line number in our program and type of exception.
    '''
    err = str(type(err).__name__)
    return err+' Loc: '+str(inspect.currentframe().f_back.f_lineno)

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

class Word:
    '''
    Class for finding Icelandic grammatical features of words in Universal
    Dependency (UD) format. Uses OTB tags

    TEST
    TEST
    TEST
    '''

    def __init__(self, leaf):
        self.leaf = leaf
        self.features = IcelandicUDFeatures() # Feature class instance created

    def getUD_tag(self):
        '''
        Checks IcePaHC POS-tag of leaf and saves Universal Dependency format
        POS-tag as instance variable (self.UD_tag) by comparing with 'tags' dict
        '''
        tag = self.tag.split('-')[0]
        try:
            self.UD_tag = self.tags[tag]
            return self
        except:
            # raise
            # if re.search(r'(DO|DA|RD|RA)', tag[0:2]):
            #     self.UD_tag = 'VERB'       #ATH. merkt sem sögn í bili
            #     return self
            # elif re.search(r'(BE|BA|HV|HA|MD|MA)', tag[0:2]):
            #     self.UD_tag = 'AUX'
            #     return self
            # elif tag == 'CONJ' and self.lemma in self.cconj:
            #     self.UD_tag = 'CCONJ'
            #     return self
            # elif tag in string.punctuation:
            #     self.UD_tag = 'PUNCT'
            #     return self
            else:
                self.UD_tag = self.tags.get(tag[0], '_')
                return self

    def split_tag(self):
        '''
        Splits IcePaHC tag into sub-parts if '-' in tag
        '''
        if '-' in self.tag:
            self.tag_name, self.tag_info = self.tag.split('-', 1)
            if '-' in self.tag_info:
                self.tag_info, self.tag_extra = self.tag_info.split('-')
            return self
        # elif self.UD_tag in {'VERB', 'AUX', 'ADP'}: # NOTE: QUICK FIX
        #     return self
        else:
            self.tag_name = self.tag
            return self

    def get_feats_verb(self):
        '''
        Finds features for verbs
        Updates features for infinitives, imperatives and present participles
        Calls methods for all other verbs
        '''
        tag = self.tag
        UD_tag = self.UD_tag
        if len(tag) == 2 or tag.endswith('TTT') or re.search(r'VB-[123]', tag):       #infinitive
            self.features.VerbForm = self.feats[UD_tag]['VerbForm']['inf']
            return self
        elif re.search(r'([DV][AB]N)', tag[:3]):     #VAN (lh.þt. í þolmynd) og VBN (lh.þt.)
            part_feats = self.feats_verb_part()
            return part_feats
        elif tag[1:3] == 'AG':      #lh.nt., VAG, DAG og RAG
            self.features.VerbForm = self.feats[UD_tag]['VerbForm']['part']
            self.features.Tense = self.feats[UD_tag]['Tense']['NT']
            return self
        elif len(tag) == 3 and tag[2] == 'I':     #imperative
            self.features.Mood = self.feats[UD_tag]['Mood']['IMP']
            return self
        elif len(tag) == 3:
            rdn_feats = self.feats_verb_part()
            return rdn_feats
        else:
            # return None
            else_feats = self.feats_verb_else()
            return else_feats

    def feats_verb_part(self):     #VAN, VBN, DAN, DON, RDN
        '''
        Finds features for verbs that are participles
        Relevant IcePaHC tags:
        VAN, VBN, DAN, DON, RDN
        '''
        tag = self.tag
        token = self.token
        UD_tag = self.UD_tag
        tag_name, tag_info = self.tag_name, self.tag_info
        # print(tag_name, tag_info)
        if '-' in tag:
            tag = tag.split('-')[0]
        else:
            tag = tag
        self.features.Case = self.feats[UD_tag]['Case'].get(tag_info)
        self.features.Tense = self.feats[UD_tag]['Tense']['ÞT']
        self.features.VerbForm = self.feats[UD_tag]['VerbForm']['part']
        DMII_entries = DMII_so.get(self.lemma)
        if not DMII_entries:
            self.features.ERROR = 'NOT_FOUND'
            return self
        try:
            for entry in DMII_entries:
                # print(entry.token, entry.features)
                if token == entry.token and entry.subclass == 'LHÞT':
                    self.features.Number = entry.features['Number']
                    self.features.Gender = entry.features['Gender']
                    if tag[1] == 'B':
                        return self
                    elif tag[1] == 'A':
                        self.features.Voice = self.feats[UD_tag]['Voice']['pass']
                        return self
                # elif # NOTE: Leftover from supine, maybe can be deleted?
                #     self.features.VerbForm = entry.features['VerbForm']
                #     self.features.Voice = entry.features['Voice']
                #     return self
                else:
                    continue
        except KeyError:
            # raise
            self.features.ERROR = error_info(err)
            return self
        except TypeError:
            # raise
            self.features.ERROR = error_info(err)
            return self

    def feats_verb_else(self):
        '''
        Finds features for all 'other' verbs
        '''
        tag = self.tag
        token = self.token
        UD_tag = self.UD_tag
        self.features.Tense = self.feats[UD_tag]['Tense'][tag[2]]
        self.features.Mood = self.feats[UD_tag]['Mood'][tag[3]]
        DMII_entries = DMII_so.get(self.lemma)
        if not DMII_entries:
            self.features.ERROR = 'NOT_FOUND'
            return self
        for entry in DMII_entries:
            # print(entry.token, entry.features)
            # print((token, self.features.Mood, self.features.Tense), (entry.features['Mood'], entry.features['Tense'], entry.token))
            try:
                if (token, self.features.Mood, self.features.Tense) == (entry.token, entry.features.get('Mood'), entry.features.get('Tense')):
                    # print(entry.token, entry.features)
                    self.features.Voice = entry.features['Voice']
                    self.features.Person = entry.features['Person']
                    self.features.Number = entry.features['Number']
                    return self
                else:
                    continue
            except (TypeError, KeyError, IndexError) as err:   #ef orð finnst ekki í BÍN eru upplýsingar frá Icepahc notaðar
                # continue
                # print(entry.token, entry.features)
                # raise
                self.features.ERROR = error_info(err)
                return self

    def get_feats_noun(self):
        '''
        Finds features for all nouns and proper names
        # TODO: add full proper name support (not found in DMII)
        '''
        tag = self.tag
        token = self.token
        UD_tag = self.UD_tag
        tag_name, tag_info = self.tag_name, self.tag_info
        self.features.Case = self.feats[UD_tag]['Case'].get(tag_info)
        self.features.Number = self.feats[UD_tag]['Number'][tag_name]
        DMII_entries = DMII_no.get(self.lemma)
        if not DMII_entries:
            self.features.ERROR = 'NOT_FOUND'
            return self
        for entry in DMII_entries:
            try:
                if (self.token, self.features.Case, self.features.Number) == (entry.token, entry.features['Case'], entry.features['Number']):
                    self.features.Gender = entry.features.get('Gender')
                    self.features.Definite = entry.features.get('Definite')
                    return self
                else:
                    continue
            except Exception as err:
                # raise
                self.features.ERROR = error_info(err)
                return self

    def get_feats_pron(self):
        '''
        # NOTE: 'hann', 'hún' and 'það' do not have native gender marker in
                DMII data. This should be fixed with if condition
        # ERROR: 'vér' is never found as it has lemma 'ég' in IcePaHC, which
                doesn't match DMII
        '''
        self.features.Case = self.feats[self.UD_tag]['Case'].get(self.tag_info)
        DMII_entries = DMII_fn.get(self.lemma)
        if self.token.startswith('$'):
            self.features.Clitic = 'Yes'
        if not DMII_entries:
            self.features.ERROR = 'NOT_FOUND'
            return self
        for entry in DMII_entries:
            if entry.token == self.token:
                if not self.features.Case:
                    self.features.Case = entry.features.get('Case')
                self.features.Number = entry.features.get('Number')
                self.features.PronType = entry.features.get('PronType')
                self.features.Gender = entry.features.get('Gender')
            if self.lemma in {'hann', 'hún', 'það'}:
                self.features.Gender = self.feats[self.UD_tag]['Gender'][self.lemma]
            else:
                continue
            return self

    def get_feats_num(self):
        '''
        Finds features for numerals
        '''
        DMII_entries = DMII_to.get(self.lemma)
        # print(self.token, self.tag)
        self.features.NumType = 'Card'# self.feats[UD_tag]['NumType']['C'] (Specific data not present in IcePaHC)
        try:
            self.features.Case = self.feats[self.UD_tag]['Case'].get(self.tag.split('-')[1])
            if not DMII_entries:
                self.features.ERROR = 'NOT_FOUND'
                return self
            for entry in DMII_entries:
                if self.token == entry.token and self.features.Case == entry.features['Case']:
                    self.features.Gender = entry.features.get('Gender')
                    self.features.Number = entry.features.get('Number')
                    return self
                else:
                    continue
        except Exception as err:   #ef orðið finnst ekki
            # raise
            self.features.ERROR =  error_info(err)
            return self

    def get_feats_adj(self):
        '''
        Finds features for all adjectives
        '''
        tag = self.tag
        token = self.token
        UD_tag = self.UD_tag
        tag_name, tag_info = self.tag_name, self.tag_info
        # print(token, tag, tag_name, tag_info)
        self.features.Case = self.feats[UD_tag]['Case'].get(tag_info)
        if self.tag_name[-1] == 'R':
            self.features.Degree = self.feats[UD_tag]['Degree']['R']
        elif self.tag_name[-1] == 'S':
            self.features.Degree = self.feats[UD_tag]['Degree']['S']
        else:
            self.features.Degree = self.feats[UD_tag]['Degree']['P']
        DMII_entries = DMII_lo.get(self.lemma)
        if not DMII_entries:
            self.features.ERROR = 'NOT_FOUND'
            return self
        try:
            for entry in DMII_entries:
                if (entry.token, entry.features['Case']) == (self.token, self.features.Case):
                    self.features.Gender = entry.features.get('Gender')
                    self.features.Number = entry.features.get('Number')
                    self.features.Definite = entry.features.get('Definite')
                    return self
        except Exception as err: #handles mismatch between word class analysis in Icepahc and BÍN, quantifiers tagged as ADJ in UD, WIP for pronouns tagged as ADJ in UD?
            try:
                self.get_feats_pron()
            except (TypeError, KeyError) as err:
                # raise
                self.features.ERROR =  error_info(err)
                return self

    def get_feats_adv(self):
        '''
        Finds features for adverbs (?)
        '''
        UD_tag = self.UD_tag
        tag_name = self.tag
        if tag_name[-1] == 'R':
            self.features.Degree = self.feats[UD_tag]['Degree']['R']
    #        return degree
        elif tag_name[-1] == 'S':
            self.features.Degree = self.feats[UD_tag]['Degree']['S']
    #        return degree
        else:
            self.features.Degree = self.feats[UD_tag]['Degree']['P']
        return self

    def get_adp_feats(self):
        '''
        # NOTE: Think this does something with adpositions (???)
        '''
        self.features.AdpType = self.feats[self.UD_tag]['AdpType']['P']
        return self

    def getinfo(self):
        '''
        Populates instance variables with relevant information
        Must be called specifically outside of class for class to function
        '''
        self.split_tag() # IcePaHC tag split (if applicable)
        self.tag_cleanup() # IcePaHC tag info cleaned
        self.getUD_tag() # UD_tag variable populated
        if self.tag_info is not None and self.tag_info.isdigit() and self.UD_tag not in {'CCONJ', 'SCONJ', 'VERB', 'AUX', 'ADP', 'PART'}:
            # print(self.leaf, self.UD_tag)
            self.features.Case = self.feats[self.UD_tag]['Case']['N']
            return self
        if self.UD_tag in {'VERB', 'AUX'}:    #TODO: include all verbs
            # self.features.all_features = '_'
            self.get_feats_verb()
        elif self.UD_tag in {'NOUN', 'PROPN'}:
            # self.features.all_features = '_'
            self.get_feats_noun()
        elif self.UD_tag == 'PRON':
            # self.features.all_features = '_'
            self.get_feats_pron()
        elif self.UD_tag == 'ADJ':
            # self.features.all_features = '_'
            self.get_feats_adj()
        elif self.UD_tag == 'ADV':
            # self.features.all_features = '_'
            self.get_feats_adv()
        elif self.UD_tag == 'ADP':
            # self.features.all_features = '_'
            self.get_adp_feats()
        elif self.UD_tag == 'NUM':
            # self.features.all_features = '_'
            self.get_feats_num()
        elif self.UD_tag == 'DET':
            self.features.all_features = '_'
            # if self.tag_info:
            #     self.features.Case = self.feats[self.UD_tag]['Case'][self.tag_info]
            # else:
            #     self.features.Case = None
        else:
            self.features.all_features = '_'
        self.features.setAll_features()
        return self

if __name__ == '__main__':
    sent1 = '(IP-MAT (NP-OB2 (D-A Inn-hinn) (ADJS-A æðsta-æðri) (N-A föður-faðir)) (VBPI biðjum-biðja) (NP-SBJ (PRO-N vér-ég)) (NP-OB1 (D-G innar-hinn) (ADJS-G æðstu-æðri) (N-G bænar-bæn) (, :-:) (NP-PRN (FW Sanctificetur-sanctificetur) (FW nomen-nomen) (FW tuum-tuum))) (. .-.))'
    sent2 = '(IP-MAT (VBDI Ætluðu-ætla) (ADVP-TMP (ADV þá-þá)) (NP-SBJ (Q-N allir-allur)) (CP-THT (C að-að) (IP-SUB (NP-SBJ (NPR-N Gunnar-gunnar)) (MDDS mundi-munu) (VB falla-falla) (PP (P þegar-þegar) (CP-ADV (C er-er) (IP-SUB (NP-SBJ (PRO-N þeir-hann)) (VBDS tækju-taka) (PP (P til-til) (NP (N-G glímu-glíma)))))))))'
    sent3 = '(IP-MAT (CONJ en-en) (ADVP (ADV þó-þó)) (BEDI voru-vera) (NP-SBJ (Q-N báðir-báðir)) (ADJP (ADJ-N sterklegir-sterklegur)) (. .-.))'
    sent4 = '(IP-MAT (NP-SBJ (NP (NPR-N Þorgrímur-þorgrímur) (NP-PRN (N-N bóndi-bóndi))) (CONJP *ICH*-1)) (VBDI sat-sitja) (PP (P á-á) (NP (N-D palli-palli))) (CONJP-1 (CONJ og-og) (NP (NPR-N Helga-helga) (NP-PRN (N-N dóttir-dóttir) (NP-POS (PRO-G hans-hann))))))'
    sent5 = '(IP-MAT (CONJ og-og) (VBDI skartaði-skarta) (NP-SBJ (PRO-N hún-hún)) (NP-MSR (ADJ-N allmikið-allmikill)) (. .-.))'
    sent6 = '(IP-MAT (NP-SBJ (NPR-N Gunnar-gunnar)) (VBDI fór-fara) (PP (P úr-úr) (NP (N-D kuflinum-kufl))))'
    sent7 = '(IP-MAT (CONJ og-og) (NP-SBJ-1 *exp*) (VBDI fauk-fjúka) (PP (P úr-úr) (NP (PRO-D honum-hann))) (NP-1 (N-N aska-aska) (Q-N mikil-mikill)) (. .-.))'
    sents = [sent1, sent2, sent3, sent4, sent5, sent6, sent7]
    for sent in sents:
        print('\n\n')
        tree = Tree.fromstring(sent)
        for leaf in tree.pos():
            word = Word(leaf).getinfo()
            f = word.features
            print(word.token, word.UD_tag, f.featString())
            #
