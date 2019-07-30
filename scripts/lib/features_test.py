
'''
features_test.py
Hinrik Hafsteinsson (hih43@hi.is)
Þórunn Arnardóttir (tha86@hi.is)
2019
Part of UniTree project for IcePaHC
'''

from lib import DMII_data
from lib.rules import tags, feats, cconj
import string
import re
from nltk.tree import Tree
from collections import OrderedDict
import inspect

DMII_no = DMII_data.DMII_data('no')
DMII_lo = DMII_data.DMII_data('lo')
DMII_fn = DMII_data.DMII_data('fn')
DMII_to = DMII_data.DMII_data('to')
DMII_ao = DMII_data.DMII_data('ao')
DMII_so = DMII_data.DMII_data('so')

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
    by class methods in Word class (see below), per each word
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
        feature variables names are keys and with their respective attr values
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
    Dependency (UD) format. Uses DMII data extensively

    Uses Tree.pos objects from NLTK Tree module (here called leaf objects)
    to get Universal Dependency format POS tage

    Saves further grammatical features in a IcelandicUDFeatures class instance

    # TODO: Add all word classes from original features.py script
    '''

    def __init__(self, leaf):
        self.leaf = leaf
        self.lemma = leaf[0].split('-')[1]
        self.token = leaf[0].split('-')[0].lower()
        self.tag = leaf[1]
        self.tag_name = None
        self.tag_info = None
        self.tag_extra = None
        self.UD_tag = None
        self.features = IcelandicUDFeatures() # Feature class instance created
        self.tags = tags
        self.feats = feats 
        self.cconj = cconj

    def getUD_tag(self):
        '''
        Checks IcePaHC POS-tag of leaf and saves Universal Dependency format
        POS-tag as instance variable (self.UD_tag) by comparing with 'tags' dict
        '''
        tag = self.tag.split('-')[0]
            # This condition can be minimized further
        try:
            self.UD_tag = self.tags[tag]
            return self
        except:
            # raise
            if re.search(r'(DO|DA|RD|RA)', tag[0:2]):
                self.UD_tag = 'VERB'       #ATH. merkt sem sögn í bili
                return self
            elif re.search(r'(BE|BA|HV|HA|MD|MA)', tag[0:2]):
                self.UD_tag = 'AUX'
                return self
            elif tag == 'CONJ' and self.lemma in self.cconj:
                self.UD_tag = 'CCONJ'
                return self
            elif tag in string.punctuation:
                self.UD_tag = 'PUNCT'
                return self
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
        else: # NOTE: Why is this here again? :/
            self.tag_name = self.tag
            # self.tag_name = self.tag
            # self.tag_info = '0'
            # self.UD_tag = 'ADV'
            return self

    def tag_cleanup(self):
        '''
        Removes various unimportant information from IcePaHC tag
        '''
        if self.tag == 'ADV-Q-N':
            self.tag = re.sub('ADV-', '', self.tag)
        if self.tag == 'ADVR-Q-D':
            self.tag = re.sub('ADVR-', '', self.tag)
        if self.tag_name == 'NPR+NS':
            self.tag_name = re.sub('\+NS', '', self.tag_name)
            self.UD_tag = 'PROPN'
        if self.tag == 'RP-2':
            self.tag = re.sub('-2', '', self.tag)
        if self.tag_info == 'TTT':
            self.tag_info = self.tag.split('-')[1]

        # TODO: find permanent fix for this, where -N is not default
        # e.g. join words in .psd file that have these numbers in tag
        if re.search(r'\w{1,5}(21|22|31|32|33)', self.tag):
            self.tag = re.sub(r'(21|22|31|32|33)', '-N', self.tag)
            return self.split_tag()

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
        if '-' in tag:
            tag = tag.split('-')[0]
        else:
            tag = tag
        try:
            for k, v in DMII_so.items():
                if token == k[0] and self.lemma == k[1] and v[0].startswith('LHÞT') or v[0].startswith('OP-LHÞT'):
                    if v[0].startswith('OP-'):
                        ID = re.sub('OP-', '', v[0])
                    ID = v[0]
                    self.features.Case = self.feats[UD_tag]['Case'][tag_info]
                    self.features.Number = self.feats[UD_tag]['Number'][(ID.split('-')[3])[-2:]]
                    self.features.Gender = self.feats[UD_tag]['Gender'][ID.split('-')[2]]
                    self.features.Tense = self.feats[UD_tag]['Tense']['ÞT']
                    self.features.VerbForm = self.feats[UD_tag]['VerbForm']['part']
                    if tag[1] == 'B':
                        return self
                    elif tag[1] == 'A':
                        self.features.Voice = self.feats[UD_tag]['Voice']['pass']
                        return self
                elif token == k[0] and self.lemma == k[1] and v[0].endswith('SAGNB'):
                    ID = v[0]
                    self.features.VerbForm = self.feats[UD_tag]['VerbForm'][ID.split('-')[1]]
                    self.features.Voice = self.feats[UD_tag]['Voice'][ID.split('-')[0]]
                    return self
                else:
                    return 'Orðasamstæða finnst ekki í BÍN-dictinu'
        except KeyError:
            return 'lykill finnst ekki'
        except TypeError:
            return 'orð finnst ekki í BÍN'

    def feats_verb_else(self):
        '''
        Finds features for all 'other' verbs
        '''
        tag = self.tag
        token = self.token
        UD_tag = self.UD_tag
        try:
            ID = DMII_data.check_DMII(DMII_so, token, self.lemma)[0]
            if ID.startswith('OP'):     #upplýsingar um ópersónulega beygingu teknar út
                ID = re.sub('OP-', '', ID)
            self.features.Tense = self.feats[UD_tag]['Tense'][ID.split('-')[2]]
            self.features.Mood = self.feats[UD_tag]['Mood'][ID.split('-')[1]]
            self.features.Voice = self.feats[UD_tag]['Voice'][ID.split('-')[0]]
            self.features.Person = self.feats[UD_tag]['Person'][ID.split('-')[3]]
            self.features.Number = self.feats[UD_tag]['Number'][ID.split('-')[4]]
            return self
        except (TypeError, KeyError, IndexError):   #ef orð finnst ekki í BÍN eru upplýsingar frá Icepahc notaðar
            if tag[2] == 'D':
                self.features.Tense = self.feats[UD_tag]['Tense']['ÞT']
            elif tag[2] == 'P':
                self.features.Tense = self.feats[UD_tag]['Tense']['NT']
            if tag[3] == 'I':
                self.features.Mood = self.feats[UD_tag]['Mood']['FH']
            elif tag[3] == 'S':
                self.features.Mood = self.feats[UD_tag]['Mood']['VH']
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
        if tag_info:
            self.features.Case = self.feats[UD_tag]['Case'][tag_info]
        else:
            self.features.Case = None
        self.features.Number = self.feats[UD_tag]['Number'][tag_name]
        try:
            ID = DMII_data.check_DMII(DMII_no, token, self.lemma)
            self.features.Gender = self.feats[UD_tag]['Gender'][ID[1]]
            if ID[0].endswith('gr'):
                self.features.Definite = 'Def'
            else:
                self.features.Definite = 'Ind'
            return self
        except (TypeError, IndexError, KeyError) as err:
        # except Exception as err:
            self.features.ERROR = error_info(err)
            return self

    def get_feats_pron(self):
        for k, v in DMII_fn.items():
            if v[1] == 'pfn':
                nummark = v[0]
                self.features.Number = self.feats[self.UD_tag]['Number'][nummark[-2:]]
                self.features.PronType = self.feats[self.UD_tag]['PronType'][v[1]]
                if self.token.startswith('$'):
                    self.features.Clitic = 'Yes'
                    return self
                else:
                    return self
            if v[1] == 'abfn':
                self.features.Number = self.feats[self.UD_tag]['Number']['ET']
                self.features.PronType = self.feats[self.UD_tag]['PronType'][v[1]]
                return self
            if v[1] == 'fn':
                mark = v[0]
                try:
                    self.features.Number = self.feats[self.UD_tag]['Number'][mark[-2:]]
                except KeyError as err:
                    self.features.Number = error_info(err)
                if '_' in mark:
                    self.features.Gender = self.feats[self.UD_tag]['Gender'][mark.split('_')[1]]
                    if self.token.startswith('$'):
                        self.features.Clitic = 'Yes'
                        return self
                    else:
                        return self
                elif '-' in mark:
                    self.features.Gender = self.feats[self.UD_tag]['Gender'][mark.split('-')[0]]
                    if self.token.startswith('$'):
                        self.features.Clitic = 'Yes'
                        return self
                    else:
                        return self

    def get_feats_num(self):
        '''
        Finds features for numerals
        '''
        tag = self.tag
        token = self.token
        UD_tag = self.UD_tag
        try:
            ID = DMII_data.check_DMII(DMII_to, token, self.lemma)[0]
            mark = ID.split('_')[1]
            self.features.Gender = self.feats[UD_tag]['Gender'][ID.split('_')[0]]
            self.features.Number = self.feats[UD_tag]['Number'][mark[-2:]]
            if self.tag_name[-1] == 'P':
                self.features.NumType = self.feats[UD_tag]['NumType']['P']
                return self
            else:
                self.features.NumType = self.feats[UD_tag]['NumType']['O']
                return self
        except (TypeError, KeyError):   #ef orðið finnst ekki
            if self.tag_name[-1] == 'P':
                self.features.NumType = self.feats[UD_tag]['NumType']['P']
                return self
            else:
                self.features.NumType = self.feats[UD_tag]['NumType']['O']
                return self

    def get_feats_adj(self):
        '''
        Finds features for all adjectives
        '''
        tag = self.tag
        token = self.token
        UD_tag = self.UD_tag
        try:
            if self.tag_name[-1] == 'R':
                self.features.Degree = self.feats[UD_tag]['Degree']['R']
            elif self.tag_name[-1] == 'S':
                self.features.Degree = self.feats[UD_tag]['Degree']['S']
            else:
                self.features.Degree = self.feats[UD_tag]['Degree']['P']
            ID = DMII_data.check_DMII(DMII_lo, self.token, self.lemma)[0]
            self.features.Gender = self.feats[UD_tag]['Gender'][ID.split('-')[1]]
            self.features.Number = self.feats[UD_tag]['Number'][ID.split('-')[2][-2:]]
            return self
        except KeyError as err:
            self.features.ERROR = error_info(err)
            return self
        except TypeError as err:   #handles mismatch between word class analysis in Icepahc and BÍN, quantifiers tagged as ADJ in UD, WIP for pronouns tagged as ADJ in UD?
            try:
                ID = DMII_data.check_DMII(DMII_fn, self.token, self.lemma)[0]
                if '-' in ID:
                    self.features.Gender = self.feats[UD_tag]['Gender'][ID.split('-')[0]]
                    self.features.Number = self.feats[UD_tag]['Number'][(ID.split('-')[1])[-2:]]
                    return self
                elif '_' in ID:
                    self.features.Gender = self.feats[UD_tag]['Gender'][ID.split('_')[1]]
                    self.features.Number = self.feats[UD_tag]['Number'][(ID.split('_')[2])[-2:]]
                    return self
                else:
                    self.features.Number = self.feats[UD_tag]['Number'][ID[-2:]]
                    self.features.ERROR = error_info(err)
                    return self
            except (TypeError, KeyError) as err:
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
        if self.tag_info is not None and self.tag_info.isdigit() and self.UD_tag not in {'CCONJ', 'PART', 'SCONJ', 'ADP', 'VERB', 'AUX'}:
            self.features.Case = self.feats[self.UD_tag]['Case']['N']
            return self
        if self.UD_tag in {'VERB', 'AUX'}:    #TODO: include all verbs
            self.get_feats_verb()
        elif self.UD_tag in {'NOUN', 'PROPN'}:
            self.get_feats_noun()
        elif self.UD_tag == 'PRON':
            self.get_feats_pron()
        elif self.UD_tag == 'ADJ':
            self.get_feats_adj()
        elif self.UD_tag == 'ADV':
            self.get_feats_adv()
        elif self.UD_tag == 'ADP':
            self.get_adp_feats()
        elif self.UD_tag == 'NUM':
            self.get_feats_num()
        elif self.UD_tag == 'DET':
            if self.tag_info:
                self.features.Case = self.feats[self.UD_tag]['Case'][self.tag_info]
            else:
                self.features.Case = None
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
