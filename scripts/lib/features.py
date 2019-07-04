from lib import DMII_data
import string
import re

"""DMII_no = DMII_data.load_json('no')
DMII_lo = DMII_data.load_json('lo')
DMII_fn = DMII_data.load_json('fn')
DMII_to = DMII_data.load_json('to')
DMII_ao = DMII_data.load_json('ao')
DMII_so = DMII_data.load_json('so')"""

DMII_no = DMII_data.DMII_data('no')
DMII_lo = DMII_data.DMII_data('lo')
DMII_fn = DMII_data.DMII_data('fn')
DMII_to = DMII_data.DMII_data('to')
DMII_ao = DMII_data.DMII_data('ao')
DMII_so = DMII_data.DMII_data('so')

cconj = {'og', 'eða', 'en', 'heldur', 'enda', 'ellegar',
        'bæði','hvorki','annaðhvort','hvort', 'ýmist'}

tags = {
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
    'RD' : 'VB',    #'verða', become, tagged as verb
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

feats = {
    'NOUN' : {
        'Case' : {
            'N' : 'Nom',    # nominative case
            'A' : 'Acc',    # accusative case
            'D' : 'Dat',    # dative case
            'G' : 'Gen'     # genitive case
        },
        'Number': {
            'NS' : 'Plur',  # noun, plural number
            'N' : 'Sing',
            'NPR' : 'Sing'    # noun singular number
            # 'NPR' : ''
            # 'NPRS' : 'Plur' # proper noun plural
        },
        'Definite' : { # TODO: remove def from dict
            '$' : 'Def',
            '' : 'Ind'
        },
        'Gender' : { # TODO: add gender to feature matrix
            'kk' : 'Masc',
            'kvk' : 'Fem',
            'hk' : 'Neut'
        }
    },
    'PROPN' : { # Case, Number, Definite
        'Number': {
            'NPRS' : 'Plur',  # noun, plural number
            'NPR' : 'Sing'    # noun singular number
        },
        'Case' : {
            'N' : 'Nom',    # nominative case
            'A' : 'Acc',    # accusative case
            'D' : 'Dat',    # dative case
            'G' : 'Gen'     # genitive case
        }, 
        'Gender' : {
            'kk' : 'Masc',
            'kvk' : 'Fem',
            'hk' : 'Neut'
        }
    },
    'PRON' : { # Case, Gender, Number, PronType
        'Number': {
            'FT' : 'Plur',  # noun, plural number
            'ET' : 'Sing'    # noun singular number
        },
        'Case' : {
            'N' : 'Nom',    # nominative case
            'A' : 'Acc',    # accusative case
            'D' : 'Dat',    # dative case
            'G' : 'Gen'     # genitive case
        },
        'PronType' : {
            'pfn' : 'Prs',     #personal
            'abfn' : 'Rcp',     #reciprocal
            'sp' : 'Int',     #interrogative
            'tv' : 'Rel',     #relative
            'ab' : 'Dem',     #demonstrative
            'oakv' : 'Ind'      #indefinite
        },
        'Gender' : {
            'KK' : 'Masc',
            'KVK' : 'Fem',
            'HK' : 'Neut'
        }
    },
    'DET' : {
        'Case' : {
            'N' : 'Nom',
            'A' : 'Acc',
            'D' : 'Dat',
            'G' : 'Gen'
        }
    },
    'ADJ' : {
        'Case' : {
            'N' : 'Nom',
            'A' : 'Acc',
            'D' : 'Dat',
            'G' : 'Gen'
        },
        'Degree' : {
            'P' : 'Pos',     #first degree
            'R' : 'Cmp',    #second Degree
            'S' : 'Sup'     #third degree
        },
        'Gender' : {
            'KK' : 'Masc',
            'KVK' : 'Fem',
            'HK' : 'Neut'
        },
        'Number' : {
            'ET' : 'Sing',
            'FT' : 'Plur'
        }
    },
    'VERB' : {
        'Mood' : {
            'IMP' : 'Imp',  #imperative 
            'FH' : 'Ind',    #indicative
            'VH' : 'Sub'     #subjunctive
        },
        'Tense' : {
            'NT' : 'Pres',   #present tense
            'ÞT' : 'Past'    #past tense
        },
        'VerbForm' : {
            '' : 'Fin',     #finite verb
            'inf' : 'Inf',     #infinitive verb
            'part' : 'Part'     #participle
        },
        'Voice' : {
            'GM' : 'Act',     #active voice
            'MM' : 'Mid',     #middle voice
            'pass' : 'Pass'     #passive voice
        },
        'Person' : {
            '1P' : '1',
            '2P' : '2',
            '3P' : '3'
        },
        'Number' : {
            'ET' : 'Sing',
            'FT' : 'Plur'
        },
        'Case' : {
            'NF' : 'Nom',
            'ÞF' : 'Acc',
            'ÞGF' : 'Dat',
            'EF' : 'Gen'
        },
        'Gender' : {
            'KK' : 'Masc',
            'KVK' : 'Fem',
            'HK' : 'Neut'
        }
    },
    'AUX' : {
        'Mood' : {
            'IMP' : 'Imp',  #imperative 
            'FH' : 'Ind',    #indicative
            'VH' : 'Sub'     #subjunctive
        },
        'Tense' : {
            'NT' : 'Pres',   #present tense
            'ÞT' : 'Past'    #past tense
        },
        'VerbForm' : {
            '' : 'Fin',     #finite verb
            'inf' : 'Inf',     #infinitive verb
            'part' : 'Part'     #participle
        },
        'Voice' : {
            'GM' : 'Act',     #active voice
            'MM' : 'Mid',     #middle voice
            'pass' : 'Pass'     #passive voice
        },
        'Person' : {
            '1P' : '1',
            '2P' : '2',
            '3P' : '3'
        },
        'Number' : {
            'ET' : 'Sing',
            'FT' : 'Plur'
        },
        'Case' : {
            'NF' : 'Nom',
            'ÞF' : 'Acc',
            'ÞGF' : 'Dat',
            'EF' : 'Gen'
        },
        'Gender' : {
            'KK' : 'Masc',
            'KVK' : 'Fem',
            'HK' : 'Neut'
        }
    },
    'NUM' : {
        'Case' : {
            'N' : 'Nom',
            'A' : 'Acc',
            'D' : 'Dat',
            'G' : 'Gen'
        },
        'Gender' : {
            'KK' : 'Masc',
            'KVK' : 'Fem',
            'HK' : 'Neut'
        },
        'Number': {
            'FT' : 'Plur',  # plural
            'ET' : 'Sing'    # singular
        },
        'NumType' : {       #ATH. mögulegt að tilgreina þetta?
            'C' : 'Card',    #Cardinal number
            'O' : 'Ord',     #Ordinal number
            '' : 'Frac'     #Fraction
        }
    },
    'ADP' : {
        'AdpType' : {
            'P' : 'Prep'
        }
    },
#    'SCONJ' : {},   #no features needed for subordinating conjunctions
#    'CCONJ' : {},   #no features needed for coordinating conjunctions
#    'ADP' : {},     #no features needed for adpositions
#    'PART' : {},    #no features possible for particles
#    'ADV' : {}      #no features possible for particles
}

"""
def check_def(word):
    if word[-1] == '$':
        det = 'Definite=Def'
    else:
        det = 'Definite=Ind'
    return det
"""

def get_UD_tag(tag, word):
    # if ipsd_tag.beginswith('NPR'):
    #     return tags['NPR']
    tag = tag.split('-')[0]
    try:
        return tags[tag]
    except:
        if tag == 'NEG':
            return tags[tag]
        # elif tag.startswith('NUM') or tag.startswith('ONE'):
        #     return 'NUM'
        elif tag[0:2] == 'DO' or tag[0:2] == 'DA' or tag[0:2] == 'RD' or tag[0:2] == 'RA':
            return 'VERB'       #ATH. merkt sem sögn í bili
        elif tag[0:2] == 'BE' or tag[0:2] == 'BA' or tag[0:2] == 'HV' or tag[0:2] == 'HA' or tag[0:2] == 'MD' or tag[0:2] == 'MA':
            return 'AUX'
        elif tag == 'CONJ' and word in cconj:
            return 'CCONJ'
        elif tag in string.punctuation:
            return 'PUNCT'
        else:
            try:
                return tags[tag[0]]
            except:
                return '_'

def get_feats_verb(lemma, token, tag, UD_tag):
    if len(tag) == 2 or tag.endswith('TTT') or tag == 'VB-1' or tag == 'VB-3' or tag == 'VB-2':       #infinitive
        verbform = 'VerbForm='+feats[UD_tag]['VerbForm']['inf']
        return verbform
    elif tag[:3] == 'VAN' or tag[:3] == 'VBN' or tag[:3] == 'DAN' or tag[:3] == 'DON':     #VAN (lh.þt. í þolmynd) og VBN (lh.þt.)
        part_feats = feats_verb_part(lemma, token, tag, UD_tag)
        return part_feats
    elif tag[1:3] == 'AG':      #lh.nt., VAG, DAG og RAG 
        verbform = 'VerbForm='+feats[UD_tag]['VerbForm']['part']
        tense = 'Tense='+feats[UD_tag]['Tense']['NT']
        return tense+'|'+verbform
    elif len(tag) == 3 and tag[2] == 'I':     #imperative
        mood = 'Mood='+feats[UD_tag]['Mood']['IMP']
        return mood
    else:
        else_feats = feats_verb_else(lemma, token, tag, UD_tag)
        return else_feats                    

def feats_verb_part(lemma, token, tag, UD_tag):     #VAN, VBN, DAN, DON
    if '-' in tag:
        tag = tag.split('-')[0]
    try:
        for k, v in DMII_so.items():
            if token == k[0] and lemma == k[1] and v[0].startswith('LHÞT') or v[0].startswith('OP-LHÞT'):
                if v[0].startswith('OP-'):
                    ID = re.sub('OP-', '', v[0])
                ID = v[0]
                case = 'Case='+feats[UD_tag]['Case'][(ID.split('-')[3])[:-2]]
                num = 'Number='+feats[UD_tag]['Number'][(ID.split('-')[3])[-2:]]
                gender = 'Gender='+feats[UD_tag]['Gender'][ID.split('-')[2]]
                tense = 'Tense='+feats[UD_tag]['Tense']['ÞT']
                verbform = 'VerbForm='+feats[UD_tag]['VerbForm']['part']
                if tag[1] == 'B':
                    return case+'|'+num+'|'+gender+'|'+tense+'|'+verbform
                elif tag[1] == 'A':
                    voice = 'Voice='+feats[UD_tag]['Voice']['pass']
                    return case+'|'+voice+'|'+num+'|'+gender+'|'+tense+'|'+verbform
            elif token == k[0] and lemma == k[1] and v[0].endswith('SAGNB'):
                ID = v[0]
                verbform = 'VerbForm='+feats[UD_tag]['VerbForm'][ID.split('-')[1]]
                voice = 'Voice='+feats[UD_tag]['Voice'][ID.split('-')[0]]
                return voice+'|'+verbform
            else:
                return 'Orðasamstæða finnst ekki í BÍN-dictinu'
    except KeyError:
        return 'lykill finnst ekki'
    except TypeError:
        return 'orð finnst ekki í BÍN'

def feats_verb_else(lemma, token, tag, UD_tag):
    try:
        ID = DMII_data.check_DMII(DMII_so, token, lemma)[0]
        if ID.startswith('OP'):     #upplýsingar um ópersónulega beygingu teknar út
            ID = re.sub('OP-', '', ID)
        tense = 'Tense='+feats[UD_tag]['Tense'][ID.split('-')[2]]
        mood = 'Mood='+feats[UD_tag]['Mood'][ID.split('-')[1]]
        voice = 'Voice='+feats[UD_tag]['Voice'][ID.split('-')[0]]
        person = 'Person='+feats[UD_tag]['Person'][ID.split('-')[3]]
        num = 'Number='+feats[UD_tag]['Number'][ID.split('-')[4]]
        return person+'|'+num+'|'+mood+'|'+tense+'|'+voice        #TODO: finna orð í BÍN með hjálp tense og mood
    except (TypeError, KeyError):   #ef orð finnst ekki í BÍN eru upplýsingar frá Icepahc notaðar
        if tag[2] == 'D':
            tense = 'Tense='+feats[UD_tag]['Tense']['ÞT']
        elif tag[2] == 'P':
            tense = 'Tense='+feats[UD_tag]['Tense']['NT']
        if tag[3] == 'I':
            mood = 'Mood='+feats[UD_tag]['Mood']['FH']
            return mood+'|'+tense 
        elif tag[3] == 'S':
            mood = 'Mood='+feats[UD_tag]['Mood']['VH']
            return mood+'|'+tense 


def get_feats_noun(lemma, token, UD_tag, tag_name, case):
    if tag_name.endswith('21') or tag_name.endswith('22') or tag_name.endswith('31') or tag_name.endswith('32') or tag_name.endswith('33'):
        tag_name = re.sub('21', '', tag_name)
        tag_name = re.sub('22', '', tag_name)
        tag_name = re.sub('31', '', tag_name)
        tag_name = re.sub('32', '', tag_name)
        tag_name = re.sub('33', '', tag_name)
    num = 'Number='+feats[UD_tag]['Number'][tag_name]
#    det = check_def(token)
#    token = token.replace('$', '')
    try:
        ID = DMII_data.check_DMII(DMII_no, token, lemma)
        gender = 'Gender='+feats[UD_tag]['Gender'][ID[1]]
        if ID[0].endswith('gr'):
            det = 'Definite=Def'
        else:
            det = 'Definite=Ind' 
        return case+'|'+num+'|'+gender+'|'+det
    except (TypeError, IndexError):
        return case+'|'+num+'*'+'*'

def get_feats_pron(UD_tag, case):
    for k, v in DMII_fn.items():
        if v[1] == 'pfn':
            nummark = v[0]
            num = 'Number='+feats[UD_tag]['Number'][nummark[-2:]]
            prontype = 'PronType='+feats[UD_tag]['PronType'][v[1]]
            return case+'|'+num+'|'+prontype
        if v[1] == 'abfn':
            num = 'Number='+feats[UD_tag]['Number']['ET']
            prontype = 'PronType='+feats[UD_tag]['PronType'][v[1]]
            return case+'|'+num+'|'+prontype
        if v[1] == 'fn':
            mark = v[0]
            try:
                num = 'Number='+feats[UD_tag]['Number'][mark[-2:]]
            except KeyError:
                num = '*'
            try:
                gender = 'Gender='+feats[UD_tag]['Gender'][mark.split('_')[1]]
                return case+'|'+num+'|'+gender
            except:
                gender = 'Gender='+feats[UD_tag]['Gender'][mark.split('-')[0]]
                return case+'|'+num+'|'+gender

def get_feats_num(lemma, token, UD_tag, case, tag_name):
    try:
        ID = DMII_data.check_DMII(DMII_to, token, lemma)[0]
        gender = 'Gender='+feats[UD_tag]['Gender'][ID.split('_')[0]]
        mark = ID.split('_')[1]
        num = 'Number='+feats[UD_tag]['Number'][mark[-2:]]
        if tag_name[-1] == 'P':
            numtype = 'NumType='+feats[UD_tag]['NumType']['P']
            return case+'|'+num+'|'+gender+'|'+numtype
        else:
            numtype = 'NumType='+feats[UD_tag]['NumType']['O']
            return case+'|'+num+'|'+gender+'|'+numtype
    except (TypeError, KeyError):   #ef orðið finnst ekki
        if tag_name[-1] == 'P':
            numtype = 'NumType='+feats[UD_tag]['NumType']['P']
            return numtype
        else:
            numtype = 'NumType='+feats[UD_tag]['NumType']['O']
            return case+'|'+numtype

def get_feats_adj(lemma, token, UD_tag, case, tag_name):
    if tag_name[-1] == 'R':
        degree = 'Degree='+feats[UD_tag]['Degree']['R']
    elif tag_name[-1] == 'S':
        degree = 'Degree='+feats[UD_tag]['Degree']['S']
    else:
        degree = 'Degree='+feats[UD_tag]['Degree']['P']
    try:
        ID = DMII_data.check_DMII(DMII_lo, token, lemma)[0]
        gender = 'Gender='+feats[UD_tag]['Gender'][ID.split('-')[1]]
        num = 'Number='+feats[UD_tag]['Number'][ID.split('-')[2][-2:]]
        return case+'|'+num+'|'+degree+'|'+gender
    except KeyError:
        return case+'|'+degree+'*'
    except TypeError:   #handles mismatch between word class analysis in Icepahc and BÍN, quantifiers tagged as ADJ in UD, WIP for pronouns tagged as ADJ in UD?
        try:
            ID = DMII_data.check_DMII(DMII_fn, token, lemma)[0]
            if '-' in ID:
                gender = 'Gender='+feats[UD_tag]['Gender'][ID.split('-')[0]]
                num = 'Number='+feats[UD_tag]['Number'][(ID.split('-')[1])[-2:]]
                return case+'|'+num+'|'+degree+'|'+gender
            elif '_' in ID:
                gender = 'Gender='+feats[UD_tag]['Gender'][ID.split('_')[1]]
                num = 'Number='+feats[UD_tag]['Number'][(ID.split('_')[2])[-2:]]
                return case+'|'+num+'|'+degree+'|'+gender
            else:
                num = 'Number='+feats[UD_tag]['Number'][ID[-2:]]
                return case+'|'+num+'|'+degree+'*'
        except (TypeError, KeyError):
            return case+'|'+degree+'*'

def get_adp_feats(UD_tag):
    type = 'AdpType='+feats[UD_tag]['AdpType']['P']
    return type

def get_feats(leaf):
    if leaf[0][0] not in {'*', '0'}: # ATH Used while traces etc. are still in data
        lemma = leaf[0].split('-')[1]
        token = leaf[0].split('-')[0].lower()
        tag = leaf[1]
        UD_tag = get_UD_tag(tag, lemma)
        if UD_tag in feats:
            try:
                if UD_tag in {'VERB', 'AUX'}:    #TODO: include all verbs
                    verb_feats = get_feats_verb(lemma, token, tag, UD_tag)
                    return verb_feats   
                if UD_tag == 'ADP':
                    adp_feats = get_adp_feats(UD_tag)
                    return adp_feats
                if '-' in tag:
                    tag_name, tag_info = tag.split('-')
                else:
                    tag_name = tag
                    tag_info = '0'
                if tag_name == 'NUM+NUM':
                    tag_name = re.sub('NUM\+NUM', 'NUM', tag_name)
                    UD_tag = 'NUM'
                if tag_name == 'NUM+N':
                    tag_name = re.sub('NUM\+', '', tag_name)
                    UD_tag = 'NOUN'
                if tag_name == 'N+Q':
                    tag_name = re.sub('N\+', '', tag_name)
                    UD_tag = 'ADJ'
                if tag_name == 'NPR+NS':
                    tag_name = re.sub('\+NS', '', tag_name)
                    UD_tag = 'PROPN'
                if tag_name == 'ONE+Q':
                    tag_name = re.sub('ONE\+', '', tag_name)
                    UD_tag == 'ADJ'
                if tag == 'RP-2':
                    tag = re.sub('-2', '', tag)
                if tag_info == 'TTT':
                    tag_info = tag.split('-')[2]
                if tag_name == 'NP':
                    return '_'      #TODO: sækja BÍN-upplýsingar
                if tag_info.isdigit():
                    case = 'Case='+feats[UD_tag]['Case']['N']
                else:
                    case = 'Case='+feats[UD_tag]['Case'][tag_info]
                if UD_tag in {'NOUN', 'PROPN'}:
                    noun_feats = get_feats_noun(lemma, token, UD_tag, tag_name, case)
                    return noun_feats
                if UD_tag == 'PRON':
                    pron_feats = get_feats_pron(UD_tag, case)
                    return pron_feats
                if UD_tag == 'DET':
                    return case 
                if UD_tag == 'NUM':
                    num_feats = get_feats_num(lemma, token, UD_tag, case, tag_name)
                    return num_feats
                if UD_tag == 'ADJ':
                    adj_feats = get_feats_adj(lemma, token, UD_tag, case, tag_name)
                    return adj_feats
#            except KeyError:
#                return '(Eitthvað að)'
            except IndexError:
                return '(Tag cannot be split)'      #ATH. some tags cannot be split (OTHER, WQ, ...)
        else:
            return '_'

if __name__ == '__main__':
    # icepahc = LazyCorpusLoader(
    #     'icepahc-v0.9/psd_orig/', CategorizedBracketParseCorpusReader,
    #     r'.*\.psd', cat_pattern=r'.*(nar|rel|sci|bio|law)\-.*'
    # )
    # tree = tree = icepahc.parsed_sents()[2]
    # for leaf in tree.pos():
    #     feat = get_feats(leaf)
    #     if feat:
    #         print(leaf)
    pass
