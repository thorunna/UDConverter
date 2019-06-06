import string


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
    'NPR' : 'POPN', # proper nouns tagged as POPN
    'NPRS': 'POPN',
    'PRO' : 'PRON',
    'NUM' : 'NUM',
    'ONE' : 'NUM',
    'ADJ' : 'ADJ',  # Adjectives tagged as ADV
    'ADJR' : 'ADJ', # Comparative adjectives tagged as ADV
    'ADJS' : 'ADJ', # Superlative adjectives tagged as ADV
    'ADV' : 'ADV',  # Adverbs tagged as ADV
    'NEG' : 'ADV',
    'ADVR' : 'ADV', # Comparative adverbs tagged as ADV
    'ADVS' : 'ADV', # Superlative adverbs tagged as ADV
    'ALSO' : 'ADV',
    'OTHER' : 'PRON',
    'OTHERS' : 'PRON'
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
            '' : 'Masc',
            '' : 'Fem',
            '' : 'Neut'
        }
    },
    'POPN' : { # Case, Number, Definite
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
            'NPRS' : 'Plur',  # noun, plural number
            'NP' : 'Sing'    # noun singular number
        },
        'Case' : {
            'N' : 'Nom',    # nominative case
            'A' : 'Acc',    # accusative case
            'D' : 'Dat',    # dative case
            'G' : 'Gen'     # genitive case
        }
    },
    'DET' : {},
    'ADP' : {},
    'ADJ' : {},
    'SCONJ' : {},
    'VERB' : {},
    'DET' : {},
    'PART' : {},
    'NUM' : {},
    'ADJ' : {},
    'ADV' : {}
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
        # elif tag.startswith('PRO'):
        #     return tags['PRO']
        # elif tag.startswith('NUM') or tag.startswith('ONE'):
        #     return 'NUM'
        elif tag == 'CONJ' and word in cconj:
            return 'CCONJ'
        elif tag in string.punctuation:
            return 'PUNCT'
        else:
            try:
                return tags[tag[0]]
            except:
                return '_'

def get_feats(leaf):
    if leaf[0][0] not in {'*', '0'}: # ATH Used while traces etc. are still in data
        lemma = leaf[0].split('-')[1]
        token = leaf[0].split('-')[0]
        tag = leaf[1]
        UD_tag = get_UD_tag(tag, lemma)
        if UD_tag in {'NOUN', 'POPN'}:
            tag_name = tag.split('-')[0]
            tag_info = tag.split('-')[1]
            case = 'Case='+feats[UD_tag]['Case'][tag_info]
            num = 'Number='+feats[UD_tag]['Number'][tag_name]
            det = check_def(token)
            return case+'|'+num+'|'+det
        # if UD_tag == 'PRON':
        #     tag_name = tag.split('-')[0]
        #     tag_info = tag.split('-')[1]
        #     case = 'Case='+feats[UD_tag]['Case'][tag_info]
        #     num = 'Number='+feats[UD_tag]['Number'][tag_name]
        #     return leaf
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
