from lib import DMII_data
import string
import re

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
    'P' : 'ADP',    # generalized prepositions tagged as ADP
    'RP' : 'ADP',   # specifiers of P/complements of P - Ath. flokka sem eitthvað annað?
    'Q' : 'ADJ',    # quantifiers tagged as ADJ - ATH ÞETTA ÞARF AÐ ENDURSKOÐA
    'C' : 'SCONJ',  # complimentizer tagged as SCONJ (subordinate conjunction)
    'V' : 'VERB',
    'W' : 'DET',    # WH-determiner tagged as DET (determiner)
    'R' : 'VERB',   # All forms of "verða" tagged as VERB
    'TO' : 'PART',  # Infinitive marker tagged as PART (particle)
    'NPR' : 'PROPN', # proper nouns tagged as PROPN
    'NPRS': 'PROPN',
    'PRO' : 'PRON',
    'WQ' : 'PRON',  #interrogative pronoun
    'NUM' : 'NUM',
    'ONE' : 'NUM',
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
            'N' : 'Sing'    # noun singular number
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
#    'SCONJ' : {},   #no features needed for subordinating conjunctions
#    'CCONJ' : {},   #no features needed for coordinating conjunctions
#    'ADP' : {},     #no features needed for adpositions
#    'PART' : {},    #no features possible for particles
#    'ADV' : {}      #no features possible for particles
}

def check_def(word):
    if word[-1] == '$':
        det = 'Definite=Def'
    else:
        det = 'Definite=Ind'
    return det

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
        elif tag[0:2] == 'DO' or tag[0:2] == 'DA':
            return 'VERB'       #ATH. merkt sem sögn í bili
        elif tag == 'CONJ' and word in cconj:
            return 'CCONJ'
        elif tag in string.punctuation:
            return 'PUNCT'
        else:
            try:
                return tags[tag[0]]
            except:
                return '_'
"""
def get_feats(leaf):
    if leaf[0][0] not in {'*', '0'}: # ATH Used while traces etc. are still in data
        lemma = leaf[0].split('-')[1]
        token = leaf[0].split('-')[0]
        tag = leaf[1]
        UD_tag = get_UD_tag(tag, lemma)
        if UD_tag == 'NOUN':
            tag_name = tag.split('-')[0]
            tag_info = tag.split('-')[1]
            case = 'Case='+feats[UD_tag]['Case'][tag_info]
            num = 'Number='+feats[UD_tag]['Number'][tag_name]
            det = check_def(token)
            return case+'|'+num+'|'+det
        if UD_tag == 'PROPN':
            tag_name = tag.split('-')[0]
            tag_info = tag.split('-')[1]
            case = 'Case='+feats[UD_tag]['Case'][tag_info]
            num = 'Number='+feats[UD_tag]['Number'][tag_name]
            return case+'|'+num
        if UD_tag == 'PRON':
            print(tag)
            try:
                tag_name = tag.split('-')[0]
                tag_info = tag.split('-')[1]
                case = 'Case='+feats[UD_tag]['Case'][tag_info]
#                num = 'Number='+feats[UD_tag]['Number'][tag_name]      #Engar upplýsingar um num. eins og er
                return case
            except:
                return 'Tag cannot be split'    #TODO: díla við þetta
        if UD_tag == 'DET':
            tag_name = tag.split('-')[0]
            tag_info = tag.split('-')[1]
            case = 'Case='+feats[UD_tag]['Case'][tag_info]
            return case
        if UD_tag == 'ADJ':
            try:
                tag_name = tag.split('-')[0]
                tag_info = tag.split('-')[1]
                if tag_name[-1] == 'R':
                    degree = 'Degree=Cmp'
                elif tag_name[-1] == 'S':
                    degree = 'Degree=Sup'
                else:
                    degree = 'Degree=Pos'
                case = 'Case='+feats[UD_tag]['Case'][tag_info]  #TODO: ath. fleiri feats
                return case+'|'+degree
            except:
                if tag[-1] == 'R':
                    degree = 'Degree=Cmp'
                elif tag[-1] == 'S':
                    degree = 'Degree=Sup'
                else:
                    degree = 'Degree=Pos'
                return 'Tag cannot be split'+'|'+'case'    #TODO: díla við þetta
        if UD_tag == 'NUM':
            tag_name = tag.split('-')[0]
            tag_info = tag.split('-')[1]
            case = 'Case='+feats[UD_tag]['Case'][tag_info]  #TODO: ath. fleiri feats
            return case
        else:
            return '_'
"""
"""
def get_feats(leaf):
    if leaf[0][0] not in {'*', '0'}: # ATH Used while traces etc. are still in data
        lemma = leaf[0].split('-')[1]
        token = leaf[0].split('-')[0]
        tag = leaf[1]
        UD_tag = get_UD_tag(tag, lemma)
        if UD_tag in feats:
            try:        #TODO: ath. fleiri feats
                tag_name = tag.split('-')[0]
                tag_info = tag.split('-')[1]
                case = 'Case='+feats[UD_tag]['Case'][tag_info]
                if UD_tag in {'NOUN', 'PROPN'}:
                    num = 'Number='+feats[UD_tag]['Number'][tag_name]
                    det = check_def(token)
                    token = token.replace('$', '')
                    # print(token, lemma)
                    try:
                        gender = 'Gender='+feats[UD_tag]['Gender'][DMII_data.check_DMII(DMII_no, token, lemma)[1]]
                    except:
                        gender = None
                    # print(token, gender)
                    if gender:
                        return case+'|'+det+'|'+gender+'|'+num
                    else:
                        return case+'|'+det+'|'+'*'+'|'+num
                    # return case+'|'+num+'|'+det
                if UD_tag in {'PRON'}:
#                    number, case, PronType, gender
                    return case
#                    try:
#                        ID = DMII_data.check_DMII(DMII_lo, token, lemma)[0]
#                        number = [ID.split('-')[1]][-2:]
#                        gender = ID.split('-')[0]
#                        return number
#                    except:
#                        return 'Fn. finnst ekki'
#                    gender = 
#                    , 'DET', 'NUM'}:
#                    return case
                if UD_tag in {'DET'}:
                    print(UD_tag)
#                    case
                    pass
                if UD_tag == 'ADJ':
#                    case, degree, gender
                    if tag_name[-1] == 'R':
                        degree = 'Degree='+feats[UD_tag]['Degree']['R']
                    elif tag_name[-1] == 'S':
                        degree = 'Degree='+feats[UD_tag]['Degree']['S']
                    else:
                        degree = 'Degree='+feats[UD_tag]['Degree']['P']
                    # print(token, lemma)
                    ID = DMII_data.check_DMII(DMII_lo, token, lemma)[0]
                    # print(token, ID)
                    gender = 'Gender='+feats[UD_tag]['Gender'][ID.split('-')[1]]
                    # print(ID.split('-'))
                    # print(ID.split('-')[1])
                    if gender:
                        return case+'|'+degree+'|'+gender
                    else:
                        return case+'|'+degree+'*'
                if UD_tag == 'VERB':
                    pass
                if UD_tag == 'NUM':
#                    case, gender, number, NumType
                    return case
                if UD_tag == 'ADV':
#                    degree
                    pass
            except IndexError:
                return 'Tag cannot be split'      #ATH. some tags cannot be split (OTHER, WQ, ...)
        else:
            return '_'
"""
def get_feats(leaf):
    if leaf[0][0] not in {'*', '0'}: # ATH Used while traces etc. are still in data
        lemma = leaf[0].split('-')[1]
        token = leaf[0].split('-')[0]
        tag = leaf[1]
        print(token, tag) # TEMP
        UD_tag = get_UD_tag(tag, lemma)
        if UD_tag in feats:
            try:
                if UD_tag == 'VERB':    #works for VB and RD (verða)
#                    mood, tense, verbform, voice
                    if len(tag) == 2:       #infinitive
                        verbform = 'VerbForm='+feats[UD_tag]['VerbForm']['inf']
                        return verbform
                    elif tag[:3] == 'VAN' or tag[:3] == 'VBN':     #VAN (lh.þt. í þolmynd) og VBN (lh.þt.)
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
                        except KeyError:
                            return 'lykill finnst ekki'
                        except TypeError:
                            return 'orð finnst ekki í BÍN'
                    elif tag[1:3] == 'AG':      #lh.nt., VAG, DAG og RAG 
                        verbform = 'VerbForm='+feats[UD_tag]['VerbForm']['part']
                        tense = 'Tense='+feats[UD_tag]['Tense']['NT']
                        return tense+'|'+verbform
                    elif len(tag) == 3 and tag[2] == 'I':     #imperative
                        mood = 'Mood='+feats[UD_tag]['Mood']['IMP']
                        return mood
                    else:
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
                        except TypeError:   #ef orð finnst ekki í BÍN eru upplýsingar frá Icepahc notaðar
                            if tag[2] == 'D':
                                tense = 'Tense='+feats[UD_tag]['Tense']['ÞT']
                            elif tag[2] == 'P':
                                tense = 'Tense='+feats[UD_tag]['Tense']['NT']
                            if tag[3] == 'I':
                                mood = 'Mood='+feats[UD_tag]['Mood']['FH']
                            elif tag[3] == 'S':
                                mood = 'Mood='+feats[UD_tag]['Mood']['VH']
                            return mood+'|'+tense
                tag_name = tag.split('-')[0]
                tag_info = tag.split('-')[1]
                case = 'Case='+feats[UD_tag]['Case'][tag_info]
                if UD_tag in {'NOUN', 'PROPN'}:
                    num = 'Number='+feats[UD_tag]['Number'][tag_name]
                    det = check_def(token)
                    token = token.replace('$', '')
                    # print(token, token, lemma) # TEMP
                    try:
                        gender = 'Gender='+feats[UD_tag]['Gender'][DMII_data.check_DMII(DMII_no, token, lemma)[1]]
                    except:
                        gender = None
                    # print(token, gender) # TEMP
                    if gender:
                        return case+'|'+num+'|'+gender+'|'+det
                    else:
                        return case+'|'+num+'|'+det+'*'
                    # return case+'|'+num+'|'+det
                if UD_tag == 'PRON':
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
                            num = 'Number='+feats[UD_tag]['Number'][mark[-2:]]
                            try:
                                gender = 'Gender='+feats[UD_tag]['Gender'][mark.split('_')[1]]
                            except:
                                gender = 'Gender='+feats[UD_tag]['Gender'][mark.split('-')[0]]
                            return case+'|'+num+'|'+gender
                if UD_tag == 'DET':
                    return case 
                if UD_tag == 'NUM':
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
                    except TypeError:   #ATH. ef orðið finnst ekki
                        if tag_name[-1] == 'P':
                            numtype = 'NumType='+feats[UD_tag]['NumType']['P']
                            return numtype
                        else:
                            numtype = 'NumType='+feats[UD_tag]['NumType']['O']
                            return case+'|'+numtype
                if UD_tag == 'ADJ':
                    if tag_name[-1] == 'R':
                        degree = 'Degree='+feats[UD_tag]['Degree']['R']
                    elif tag_name[-1] == 'S':
                        degree = 'Degree='+feats[UD_tag]['Degree']['S']
                    else:
                        degree = 'Degree='+feats[UD_tag]['Degree']['P']
                    try:
                        ID = DMII_data.check_DMII(DMII_lo, token, lemma)[0]
                        if ID:
                            gender = 'Gender='+feats[UD_tag]['Gender'][ID.split('-')[1]]
                            num = 'Number='+feats[UD_tag]['Number'][(ID.split('-')[2])[-2:]]
#                            if gender:
                            return case+'|'+num+'|'+degree+'|'+gender
#                            else: # TEMP: WIP for pronouns tagged as ADJ in UD
#                                ID = DMII_data.check_DMII(DMII_fn, token, lemma)[0]
#                                gender = 'Gender='+feats[UD_tag]['Gender'][ID.split('-')[0]]
#                                return case+'|'+num+'|'+degree+'|'+gender
                        else:       #handles mismatch between world class analysis in Icepahc and BÍN, quantifiers tagged as ADJ in UD, WIP for pronouns tagged as ADJ in UD?
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
                    except TypeError:
                        return case+'|'+degree+'*'
            except KeyError:
                return '(Eitthvað að)'
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
