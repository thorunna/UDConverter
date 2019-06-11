from lib import DMII_data
import string

DMII_no = DMII_data.DMII_data('no')
DMII_lo = DMII_data.DMII_data('lo')
DMII_fn = DMII_data.DMII_data('fn')
DMII_pfn = DMII_data.DMII_data('pfn')
DMII_abfn = DMII_data.DMII_data('afturbfn')
DMII_to = DMII_data.DMII_data('to')
DMII_ao = DMII_data.DMII_data('ao')

# DMII_data.check_DMII(DMII_lo, 'góðrigóður')

cconj = {'og', 'eða', 'en', 'heldur', 'enda', 'ellegar',
        'bæði','hvorki','annaðhvort','hvort', 'ýmist'}

tags = {
    # ipsd_tag : UD_tag
    'N' : 'NOUN',   # generalized nouns tagged as NOUN
    'D' : 'DET',    # generalized determiners tagged as DET (determiner)
    'P' : 'ADP',    # generalized prepositions tagged as ADP
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
            'NS' : 'Plur',  # noun, plural number
            'N' : 'Sing'    # noun singular number
        },
        'Case' : {
            'N' : 'Nom',    # nominative case
            'A' : 'Acc',    # accusative case
            'D' : 'Dat',    # dative case
            'G' : 'Gen'     # genitive case
        },
        'PronType' : {
            '' : 'Prs',     #personal
            '' : 'Rcp',     #reciprocal
            '' : 'Int',     #interrogative
            '' : 'Rel',     #relative
            '' : 'Dem',     #demonstrative
            '' : 'Ind'      #indefinite
        },
        'Gender' : {
            'kk' : 'Masc',
            'kvk' : 'Fem',
            'hk' : 'Neut'
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
    'VERB' : {},
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
            'O' : 'Card',    #Cardinal number
            'P' : 'Ord',     #Ordinal number
            '' : 'Frac'     #Fraction
        }
    },
    'ADV' : {
        'Degree' : {
            'P' : 'Pos',    #first degree
            'R' : 'Cmp',    #second Degree
            'S' : 'Sup'     #third degree
        }
    },
#    'SCONJ' : {},   #no features needed for subordinating conjunctions
#    'CCONJ' : {},   #no features needed for coordinating conjunctions
#    'ADP' : {},     #no features needed for adpositions
#    'PART' : {},    #no features possible for particles
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
                    # print(token, token+lemma)
                    try:
                        gender = 'Gender='+feats[UD_tag]['Gender'][DMII_data.check_DMII(DMII_no, token+lemma)[1]]
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
#                        ID = DMII_data.check_DMII(DMII_lo, token+lemma)[0]
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
                    ID = DMII_data.check_DMII(DMII_lo, token+lemma)[0]
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
            try:        #TODO: ath. fleiri feats
                tag_name = tag.split('-')[0]
                tag_info = tag.split('-')[1]
                case = 'Case='+feats[UD_tag]['Case'][tag_info]
                if UD_tag in {'NOUN', 'PROPN'}:
                    num = 'Number='+feats[UD_tag]['Number'][tag_name]
                    det = check_def(token)
                    token = token.replace('$', '')
                    # print(token, token+lemma) # TEMP
                    try:
                        gender = 'Gender='+feats[UD_tag]['Gender'][DMII_data.check_DMII(DMII_no, token+lemma)[1]]
                    except:
                        gender = None
                    # print(token, gender) # TEMP
                    if gender:
                        return case+'|'+num+'|'+gender+'|'+det
                    else:
                        return case+'|'+num+'|'+det+'*'
                    # return case+'|'+num+'|'+det
                if UD_tag == 'PRON':
#                    number, case, PronType, gender
#                    ID = DMII_data.check_DMII(DMII_fn, token+lemma)[0]
#                    return ID
                    return case
                if UD_tag == 'DET':
                    return case 
                if UD_tag == 'NUM':
                    ID = DMII_data.check_DMII(DMII_to, token+lemma)[0]
                    gender = 'Gender='+feats[UD_tag]['Gender'][ID.split('_')[0]]
                    mark = ID.split('_')[1]
                    num = 'Number='+feats[UD_tag]['Number'][mark[-2:]]
#                    return case+'|'+num+'|'+gender
                    if tag_name[-1] == 'P':
                        numtype = 'NumType='+feats[UD_tag]['NumType']['P']
                        return case+'|'+num+'|'+gender+'|'+numtype
                    else:
                        numtype = 'NumType='+feats[UD_tag]['NumType']['O']
                        return case+'|'+num+'|'+gender+'|'+numtype
                if UD_tag == 'ADJ':
                    if tag_name[-1] == 'R':
                        degree = 'Degree='+feats[UD_tag]['Degree']['R']
                    elif tag_name[-1] == 'S':
                        degree = 'Degree='+feats[UD_tag]['Degree']['S']
                    else:
                        degree = 'Degree='+feats[UD_tag]['Degree']['P']
                    # print(token, lemma)
                    try:
                        ID = DMII_data.check_DMII(DMII_lo, token+lemma)[0]
#                        return ID
                        # print(token, ID)
                        gender = 'Gender='+feats[UD_tag]['Gender'][ID.split('-')[1]]
                        # print(ID.split('-'))
                        # print(ID.split('-')[1])
                        # det = 'Degree='+feats[UD_tag]['Degree'][ID.split('-')[0][-2:]]
                        # print(det)
                        if gender:
                            return case+'|'+degree+'|'+gender
                        else: # TEMP: WIP for pronouns tagged as ADJ in UD
                            ID = DMII_data.check_DMII(DMII_fn, token+lemma)[0]
                            gender = 'Gender='+feats[UD_tag]['Gender'][ID.split('-')[0]]
                            print(ID, gender)
                            return case+'|'+degree+'|'+gender
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
