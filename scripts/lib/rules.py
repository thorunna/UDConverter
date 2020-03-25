

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

OTB_map = {
        'Gender' : {
            'k' : 'Masc',
            'v' : 'Fem',
            'h' : 'Neut',
            'x' : None
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
            'o' : None, # 'ÓBEYGT', TODO: check if output 100% correct
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

DMII_map = {
        'Gender' : { # TODO: add gender to feature matrix
            'kk' : 'Masc',
            'kvk' : 'Fem',
            'hk' : 'Neut',
            'KK' : 'Masc',
            'KVK' : 'Fem',
            'HK' : 'Neut',
        },
        'Number': {
            'FT' : 'Plur',  # noun, plural number
            'ET' : 'Sing'    # noun singular number
        },
        'PronType' : {
            'pfn' : 'Prs',    #personal
            'abfn' : 'Rcp',   #reciprocal
            'sp' : 'Int',     #interrogative
            'tv' : 'Rel',     #relative
            'ab' : 'Dem',     #demonstrative
            'oakv' : 'Ind'    #indefinite
        },
        'Tense' : {
            'NT' : 'Pres',   #present tense
            'ÞT' : 'Past',    #past tense
            'NF' : None
        },
        'Person' : {
            '1P' : '1',
            '2P' : '2',
            '3P' : '3'
        },
        'Case' : {
            'NF' : 'Nom',   # nominative case (DMII)
            'ÞF' : 'Acc',   # accusative case (DMII)
            'ÞGF' : 'Dat',  # dative case (DMII)
            'ÞG' : 'Dat',   # dative case (DMII, alternative)
            'EF' : 'Gen',   # genitive case (DMII)
            'N' : 'Nom',    # nominative case (IcePaHC)
            'A' : 'Acc',    # accusative case (IcePaHC)
            'D' : 'Dat',    # dative case (IcePaHC)
            'G' : 'Gen',    # genitive case (IcePaHC)
            None : 'Nom'
        },
        'Mood' : {
            'IMP' : 'Imp',  #imperative
            'FH' : 'Ind',   #indicative
            'VH' : 'Sub',   #subjunctive
            'I' : 'Ind',    #indicative (IcePaHC POS-tag)
            'S' : 'Sub',    #subjunctive (IcePaHC POS-tag)
            'OSKH' : None   # TEMP
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
        'Definite' : {
            'SB' : 'Ind', # strong inflection (adjectives)
            'VB' : 'Def', # weak inflection (adjectives)
            'gr' : 'Def', # DMII definite article marker
            'ET' : 'Ind', # if def marker not present in DMII
            'FT' : 'Ind', # if def marker not present in DMII
            None : None
        },
    },

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
            'HK' : 'Neut',
            'hann' : 'Masc',    # for capturing personal pronoun gender
            'hún' : 'Fem',      # for capturing personal pronoun gender
            'það' : 'Neut',     # for capturing personal pronoun gender
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
            'P' : 'Pos',    #first degree
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
    'ADV' : {
        'Degree' : {
            'P' : 'Pos',     #first degree
            'R' : 'Cmp',    #second Degree
            'S' : 'Sup'     #third degree
        },
        'Case' : {
            'N' : 'Nom',
            'A' : 'Acc',
            'D' : 'Dat',
            'G' : 'Gen'
        }
    },
    'VERB' : {
        'Mood' : {
            'IMP' : 'Imp',  #imperative
            'FH' : 'Ind',   #indicative
            'VH' : 'Sub',   #subjunctive
            'I' : 'Ind',    #indicative (IcePaHC POS-tag)
            'S' : 'Sub',    #subjunctive (IcePaHC POS-tag)
        },
        'Tense' : {
            'NT' : 'Pres',   #present tense
            'ÞT' : 'Past',    #past tense
            'P' : 'Pres',
            'D' : 'Past'
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
            'NF' : 'Nom',   # nominative case (DMII)
            'ÞF' : 'Acc',   # accusative case (DMII)
            'ÞGF' : 'Dat',  # dative case (DMII)
            'ÞG' : 'Dat',   # dative case (DMII, alternative)
            'EF' : 'Gen',   # genitive case (DMII)
            'N' : 'Nom',    # nominative case (IcePaHC)
            'A' : 'Acc',    # accusative case (IcePaHC)
            'D' : 'Dat',    # dative case (IcePaHC)
            'G' : 'Gen',    # genitive case (IcePaHC)
            None : 'Nom'
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
            'FH' : 'Ind',   #indicative
            'VH' : 'Sub',   #subjunctive
            'I' : 'Ind',    #indicative (IcePaHC POS-tag)
            'S' : 'Sub',    #subjunctive (IcePaHC POS-tag)
        },
        'Tense' : {
            'NT' : 'Pres',   #present tense
            'ÞT' : 'Past',    #past tense
            'P' : 'Pres',
            'D' : 'Past'
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
            '' : 'Frac'      #Fraction
        }
    },
    'ADP' : {
        'AdpType' : {
            'P' : 'Prep'
        }
    },
#    'SCONJ' : {},   #no features needed for subordinating conjunctions
#    'CCONJ' : {},   #no features needed for coordinating conjunctions
#    'PART' : {},    #no features possible for particles
}

head_rules = {
            'IP-INF'        : {'dir':'r', 'rules':['VB', 'DO', 'VAN', 'IP-INF']},
            'IP-INF-ABS'    : {'dir':'r', 'rules':['VB']},
            'IP-INF-ABS-PRN': {'dir':'r', 'rules':['VB']},
            'IP-INF-PRP'    : {'dir':'r', 'rules':['VB', 'IP-INF']},      #tilgangsnafnháttur
            'IP-INF-PRP-PRN-SPE': {'dir':'r', 'rules':['VB']},
            'IP-INF-PRP-PRN': {'dir':'r', 'rules':['VB']},
            'IP-INF-PRP-SPE': {'dir':'r', 'rules':['VB']},
            'IP-INF-PRP-SPE-PRN': {'dir':'r', 'rules':['VB']},
            'IP-INF-SPE'    : {'dir':'r', 'rules':['VB']},      #spe = direct speech
            'IP-INF-SPE-ADT': {'dir':'r', 'rules':['VB']},
            'IP-INF-SPE-DEG': {'dir':'r', 'rules':['VB']},
            'IP-INF-SPE-LFD': {'dir':'r', 'rules':['VB']},
            'IP-INF-SPE-PRN': {'dir':'r', 'rules':['VB']},
            'IP-INF-SPE-PRN-ELAB': {'dir':'r', 'rules':['VB']},
            'IP-INF-SPE-PRP': {'dir':'r', 'rules':['VB']},
            'IP-INF-SPE-PRP-PRN': {'dir':'r', 'rules':['VB']},
            'IP-INF-SPE-SBJ': {'dir':'r', 'rules':['VB']},
            'IP-INF-PRN'    : {'dir':'r', 'rules':['VB']},
            'IP-INF-PRN-ELAB': {'dir':'r', 'rules':['VB']},
            'IP-INF-PRN-PRP': {'dir':'r', 'rules':['VB']},
            'IP-INF-PRN-SPE': {'dir':'r', 'rules':['VB']},
            'IP-INF-RSP'    : {'dir':'r', 'rules':['VB']},
            'IP-INF-SBJ'    : {'dir':'r', 'rules':['VB']},
            'IP-INF-SBJ-SPE': {'dir':'r', 'rules':['VB']},
            'IP-INF-DEG'    : {'dir':'r', 'rules':['VB']},  #degree infinitive
            'IP-INF-DEG-PRN': {'dir':'r', 'rules':['VB']},
            'IP-INF-DEG-SPE': {'dir':'r', 'rules':['VB']},
            'IP-INF-LFD'    : {'dir':'r', 'rules':['VB']},
            'IP-INF-PRD'    : {'dir':'r', 'rules':['VB']},
            'IP-INF-ADT'    : {'dir':'r', 'rules':['VB']},
            'IP-INF-ADT-LFD': {'dir':'r', 'rules':['VB']},
            'IP-INF-ADT-PRN': {'dir':'r', 'rules':['VB']},
            'IP-INF-ADT-SPE': {'dir':'r', 'rules':['VB']},
            'IP-INF-ADT-SPE-LFD': {'dir':'r', 'rules':['VB']},
            'IP-MAT'        : {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'VAN', 'HV.*', 'VAG', 'DAG', 'HAG', 'VP', 'IP-MAT-\d', 'PP', 'ADJP', 'RP', 'NP-PRD', 'NP-SBJ', 'NP', 'N.*', 'IP-SMC', 'IP-MAT', 'IP-MAT-*']},
            'IP-MAT=\d'     : {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'VAN', 'HV.*', 'VAG', 'DAG', 'HAG', 'VP', 'IP-MAT-\d', 'PP', 'ADJP', 'RP', 'NP-PRD', 'NP', 'N.*', 'IP-SMC', 'IP-MAT', 'IP-MAT-*']},
            #'IP-MAT-1'       : {'dir':'r', 'rules':['NP-MSR']},
            #'IP-MAT=1'      : {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'VAN', 'HV.*', 'VAG', 'DAG', 'HAG', 'VP', 'PP', 'ADJP', 'NP-PRD', 'NP', 'N.*', 'IP-SMC', 'IP-MAT']},
            #'IP-MAT=1'      : {'dir':'r', 'rules':['NP-SBJ']},
            'IP-MAT-DIR'    : {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'VAN', 'HV.*', 'VAG', 'DAG', 'HAG', 'VP', 'ADJP', 'NP', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT']},
            'IP-MAT-LFD'    : {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'VAN', 'HV.*', 'VAG', 'DAG', 'HAG', 'VP', 'ADJP', 'NP', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT']},
            'IP-MAT-OB1'    : {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'VAN', 'HV.*', 'VAG', 'DAG', 'HAG', 'VP', 'ADJP', 'NP', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT']},
            'IP-MAT-PRN'    : {'dir':'r', 'rules':['VB.*', 'VP']},
            'IP-MAT-PRN-ELAB': {'dir':'r', 'rules':['VB.*', 'VP']},
            'IP-MAT-PRN-LFD': {'dir':'r', 'rules':['VB.*', 'VP']},
            'IP-MAT-PRN-SPE': {'dir':'r', 'rules':['VB.*', 'VP']},
            'IP-MAT-SBJ'    : {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'VAN', 'HV.*', 'VAG', 'DAG', 'HAG', 'VP', 'NP', 'ADJP', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT']},
            'IP-MAT-SPE'    : {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'VP', 'ADJP', 'NP', 'VAN', 'VAG', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT.*']},
            'IP-MAT-SPE=1'  : {'dir':'r', 'rules':['ADJP']},
            'IP-MAT-SPE-PRN': {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'NP', 'ADJP', 'VAN', 'VAG', 'VP', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT.*']},
            'IP-MAT-SPE-PRN-ELAB': {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'NP', 'ADJP', 'VAN', 'VAG', 'VP', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT.*']},
            'IP-MAT-SPE-PRN-LFD': {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'NP', 'ADJP', 'VAN', 'VAG', 'VP', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT.*']},
            'IP-MAT-SPE-SBJ': {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'NP', 'ADJP', 'VAN', 'VAG', 'VP', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT.*']},
            'IP-MAT-SUB-SPE': {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'NP', 'ADJP', 'VAN', 'VP', 'VAG', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT.*']},
            'IP-MAT-SMC'    : {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'VAN', 'HV.*', 'NP', 'VAG', 'VP', 'ADJP', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT']},
            #MD.* á eftir VB: ef VB er spor ruglast venslin en þá getur MD sem hjálparsögn líka verið haus. Ef MD er seinna er það seinna í lagi
            'IP-SUB'        : {'dir':'r', 'rules':['VP', 'VB', 'VB.*', 'DO.*', 'RD.*', 'DAN', 'VAN', 'RAN', 'HAN', 'BAN', 'RDN', 'BEN', 'HVN', 'HV.*', 'MD.*', 'IP-INF.*', 'ADJP', 'NP.*', 'NP-PRD', 'RD.*', 'ADVP', 'IP-SUB']},
            'IP-SUB-INF'    : {'dir':'r', 'rules':['VB']},
            'IP-SUB-LFD'    : {'dir':'r', 'rules':['VP', 'VB', 'VB.*', 'DO.*', 'DAN', 'VAN', 'RAN', 'HAN', 'BAN', 'RDN', 'BEN', 'HV.*', 'IP-INF.*', 'ADJP', 'NP-PRD', 'RD.*', 'NP', 'ADVP', 'IP-SUB', 'HVN']},
            'IP-SUB-PRN'    : {'dir':'r', 'rules':['VB.*', 'VAN']},
            'IP-SUB-PRN-ELAB': {'dir':'r', 'rules':['VB.*', 'VAN']},
            'IP-SUB-PRN=XXX': {'dir':'r', 'rules':['VB.*', 'VAN']},
            'IP-SUB-REP'    : {'dir':'r', 'rules':['VP', 'VB', 'VB.*', 'DO.*', 'RD.*', 'DAN', 'VAN', 'RAN', 'HAN', 'BAN', 'RDN', 'BEN', 'HVN', 'HV.*', 'MD.*', 'IP-INF.*', 'NP.*', 'ADJP', 'NP-PRD', 'RD.*', 'ADVP', 'IP-SUB']},
            'IP-SUB-SPE'    : {'dir':'r', 'rules':['VB.*', 'HV.*']},
            'IP-SUB-SPE-PRN': {'dir':'r', 'rules':['VB.*', 'HV.*']},
            'IP-SUB-SPE-PRN-ELAB': {'dir':'r', 'rules':['VB.*', 'HV.*']},
            'IP-IMP'        : {'dir':'r', 'rules':['VB.']},    #imperative
            'IP-IMP-PRN'    : {'dir':'r', 'rules':['VB.']},
            'IP-IMP-SPE'    : {'dir':'r', 'rules':['VB.']},
            'IP-IMP-SPE-PRN': {'dir':'r', 'rules':['VB.']},
            'IP-IMP-SPE-SBJ': {'dir':'r', 'rules':['VB.']},
            'IP-SMC'        : {'dir':'r', 'rules':['IP-INF-SBJ', 'IP-SMC', 'NP-PRD', 'VAG-.', 'ADJP', 'NP.*']},    #small clause
            'IP-SMC-SBJ'    : {'dir':'r', 'rules':['IP-INF-SBJ', 'IP-SMC', 'NP-PRD', 'VAG-.', 'ADJP', 'NP.*']},
            'IP-SMC-SPE'    : {'dir':'r', 'rules':['IP-INF-SBJ', 'IP-SMC', 'NP-PRD', 'VAG-.', 'ADJP', 'NP.*']},
            'IP-PPL'        : {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG']},  #lýsingarháttarsetning
            'IP-PPL-ABS'    : {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG']},
            'IP-PPL-ABS-SPE': {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG']},
            'IP-PPL-OB1'    : {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG']},
            'IP-PPL-OB1-SPE': {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG']},
            'IP-PPL-OB2'    : {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG']},
            'IP-PPL-PRD'    : {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG']},
            'IP-PPL-PRN'    : {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG']},
            'IP-PPL-SBJ'    : {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG']},
            'IP-PPL-SPE'    : {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG']},
            'IP-PPL-SPE-OB1': {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG']},
            'IP-PPL-SPE-PRD': {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG']},
            'IP-ABS'        : {'dir':'r', 'rules':['VP', 'VB', 'VB.*', 'DO.*', 'RD.*', 'DAN', 'VAN', 'RAN', 'HAN', 'BAN', 'RDN', 'BEN', 'HVN', 'HV.*', 'MD.*', 'IP-INF.*', 'NP.*', 'ADJP', 'NP-PRD', 'RD.*', 'ADVP', 'IP-SUB']},
            'IP-ABS-PRN'    : {'dir':'r', 'rules':['VP', 'VB', 'VB.*', 'DO.*', 'RD.*', 'DAN', 'VAN', 'RAN', 'HAN', 'BAN', 'RDN', 'BEN', 'HVN', 'HV.*', 'MD.*', 'IP-INF.*', 'NP.*', 'ADJP', 'NP-PRD', 'RD.*', 'ADVP', 'IP-SUB']},
            'IP-ABS-SBJ'    : {'dir':'r', 'rules':['VP', 'VB', 'VB.*', 'DO.*', 'RD.*', 'DAN', 'VAN', 'RAN', 'HAN', 'BAN', 'RDN', 'BEN', 'HVN', 'HV.*', 'MD.*', 'IP-INF.*', 'NP.*', 'ADJP', 'NP-PRD', 'RD.*', 'ADVP', 'IP-SUB']},
            'CP-THT'        : {'dir':'r', 'rules':['IP-SUB.*','.*']},   #að
            'CP-THT-SBJ'    : {'dir':'r', 'rules':['IP-SUB.*','.*']},   #extraposed subject
            'CP-THT-SBJ-SPE': {'dir':'r', 'rules':['IP-SUB.*','.*']},
            'CP-THT-SPE'    : {'dir':'r', 'rules':['IP-SUB.*','.*']},
            'CP-THT-SPE-PRN': {'dir':'r', 'rules':['IP-SUB.*', 'IP-MAT.*', '.*']},
            'CP-THT-SPE-SBJ': {'dir':'r', 'rules':['IP-SUB.*','.*']},
            'CP-THT-PRN'    : {'dir':'r', 'rules':['IP-SUB.*','.*']},
            'CP-THT-PRN-NaN': {'dir':'r', 'rules':['IP-SUB.*','.*']},
            'CP-THT-PRN-SPE': {'dir':'r', 'rules':['IP-SUB.*','.*']},
            'CP-THT-LFD'    : {'dir':'r', 'rules':['IP-SUB.*','.*']},
            'CP-THT-RSP'    : {'dir':'r', 'rules':['IP-SUB.*','.*']},
            'CP-CAR'        : {'dir':'r', 'rules':['IP-SUB.*']},    #clause-adjoined relatives
            'CP-CAR-SPE'    : {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-CLF'        : {'dir':'r', 'rules':['IP-SUB.*']},    #it-cleft
            'CP-CLF-SPE'    : {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-CMP'        : {'dir':'r', 'rules':['IP-SUB.*']},    #comparative clause
            'CP-CMP-LFD'    : {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-CMP-SPE'    : {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-DEG'        : {'dir':'r', 'rules':['IP-SUB.*']},  #degree complements
            'CP-DEG-SPE'    : {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-FRL'        : {'dir':'r', 'rules':['IP-SUB.*', 'WNP.*']},  #free relative
            'CP-FRL-SPE'    : {'dir':'r', 'rules':['IP-SUB.*', 'WNP.*']},
            'CP-REL'        : {'dir':'r', 'rules':['IP-SUB.*']},    #relative
            'CP-REL-SPE'    : {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-REL-SPE-PRN': {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-QUE'        : {'dir':'r', 'rules':['WNP', 'WADVP', 'CP-QUE', 'IP-SUB.*']},    #question
            'CP-QUE-SPE'    : {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-QUE-SPE-LFD': {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-QUE-SPE-PRN': {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-QUE-SPE-SBJ': {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-QUE-ADV'    : {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-QUE-ADV-LFD': {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-QUE-ADV-SPE': {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-QUE-ADV-SPE-LFD': {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-QUE-LFD'    : {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-QUE-PRN'    : {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-QUE-PRN-ELAB': {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-QUE-PRN-SPE': {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-QUE-SBJ'    : {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-ADV'        : {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-ADV-LFD'    : {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-ADV-LFD-SPE': {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-ADV-PRN'    : {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-ADV-RSP'    : {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-ADV-SPE'    : {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-ADV-SPE-LFD': {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-ADV-SPE-PRN': {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-EOP'        : {'dir':'r', 'rules':['IP-INF.*']},  #empty operator
            'CP-EOP-SPE'    : {'dir':'r', 'rules':['IP-INF.*']},
            'CP-EOP-SPE-PRN': {'dir':'r', 'rules':['IP-INF.*']},
            'CP-EXL'        : {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-EXL-SPE'    : {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-TMC'        : {'dir':'r', 'rules':['IP-INF.*']},  #tough-movement
            'CP-TMC-SPE'    : {'dir':'r', 'rules':['IP-INF.*']},
            'CP-TMP'        : {'dir':'r', 'rules':['IP-INF.*']},
            'NP'            : {'dir':'r', 'rules':['CP-FRL', 'N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'PRO-.', 'MAN-.', 'NP.*', 'Q.*', 'OTHER-.']},
            'NP-ADV'        : {'dir':'r', 'rules':['CP-FRL', 'N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'PRO-.', 'NP.*', 'ADJ.*', 'Q.*', 'SUCH', 'MAN-.', 'OTHER-.', 'CP.*']},
            'NP-LFD'        : {'dir':'r', 'rules':['CP-FRL', 'N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'PRO-.', 'NP.*', 'Q.*', 'MAN-.', 'OTHER-.']},
            'NP-ADV-LFD'    : {'dir':'r', 'rules':['NP.*', 'N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'PRO-.', 'ADJ.*', 'Q.*', 'CP.*']},
            'NP-ADV-RSP'    : {'dir':'r', 'rules':['NP.*', 'N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'PRO-.', 'ADJ.*', 'Q.*', 'CP.*']},
            'NP-CMP'        : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'MAN-.', 'OTHER-.']},
            'NP-PRN'        : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NP', 'NPRS-.', 'PRO-.', 'MAN-.', 'OTHER-.']},   #viðurlag, appositive
            'NP-PRN-ELAB'   : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'PRO-.', 'MAN-.', 'OTHER-.']},
            'NP-PRN-REP'    : {'dir':'r', 'rules':['N-.', 'NS.*', 'NP.*', 'OTHER-.']},
            'NP-RSP'        : {'dir':'r', 'rules':['N-.', 'NS.*', 'NP.*', 'OTHER-.']},
            #NP-SBJ: 'NP.*' var á undan 'PRO', búið að víxla til að NP-PRN verði appos og PRO nsubj
            'NP-SBJ'        : {'dir':'r', 'rules':['N-N', 'N-.', 'NS-N', 'NPR-N', 'NPRS-N', 'MAN.*', 'PRO-.', 'NP.*', 'ADJ-N', 'OTHER-.', 'Q']},
            'NP-SBJ-LFD'    : {'dir':'r', 'rules':['N-N', 'N-.', 'NS-N', 'NPR-N', 'NPRS-N', 'MAN.*', 'NP.*', 'PRO-.', 'ADJ-N', 'OTHER-.']},
            'NP-SBJ-RSP'    : {'dir':'r', 'rules':['N-N', 'N-.', 'NS-N', 'NPR-N', 'NPRS-N', 'MAN.*', 'NP.*', 'PRO-.', 'ADJ-N', 'OTHER-.']},
            'NP-SMC'        : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'PRO-.', 'NP.*', 'Q.*', 'MAN-.', 'OTHER-.', 'CP-FRL']},
            'NP-SPE'            : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'PRO-.', 'NP.*', 'Q.*', 'MAN-.', 'OTHER-.', 'CP-FRL']},
            'NP-OB1'        : {'dir':'r', 'rules':['N-.', 'NPR-.', 'NPRS-.', 'NS-.', 'NP', 'NP-.+', 'PRO-.', 'ONE+Q-A', 'MAN-A', 'OTHER-.']},
            'NP-OB1-LFD'    : {'dir':'r', 'rules':['N-.', 'NPR-.', 'NPRS-.', 'NS-.', 'NP', 'ONE+Q-A', 'MAN-A', 'OTHER-.', 'PRO-.']},
            'NP-OB1-RSP'    : {'dir':'r', 'rules':['N-.', 'NPR-.', 'NPRS-.', 'NS-.', 'NP', 'ONE+Q-A', 'MAN-A', 'OTHER-.', 'PRO-.']},
            'NP-OB2'        : {'dir':'r', 'rules':['NP.*', 'PRO-.', 'N-D', 'NS-D', 'NPR-.', 'NPRS-.', 'CP-FRL', 'MAN-.', 'OTHER-.']},    #MEIRA?
            'NP-OB2-RSP'    : {'dir':'r', 'rules':['NP.*', 'PRO-.', 'N-D', 'NS-D', 'NPR-.', 'NPRS-.', 'CP-FRL', 'MAN-.', 'OTHER-.']},
            'NP-OB3'        : {'dir':'r', 'rules':['PRO-D', 'N-D', 'NS-D', 'NPR-D', 'NPRS-D', 'MAN-.', 'OTHER-.']},
            'NP-PRD'        : {'dir':'r', 'rules':['N-.', 'NS.*', 'NP.*', 'PRO.*' 'OTHER-.', 'NUMP']},     #sagnfylling copulu
            'NP-SPR'        : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.' 'NPRS-.',]},   #secondary predicate
            'NP-POS'        : {'dir':'r', 'rules':['NPR-.', 'N-.', 'NS-.', 'NPRS-.', 'PRO-.', 'NP', 'NP-.+', 'MAN-.', 'OTHER-.']},
            'NP-POS-RSP'    : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'PRO-.', 'NP-.+', 'MAN-.', 'OTHER-.']},
            'NP-COM'        : {'dir':'r', 'rules':['N.*', 'NP.*', 'OTHER-.']},  #fylliliður N sem er ekki í ef.
            'NP-ADT'        : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'MAN-.', 'OTHER-.']},    #clause-level dative adjuncts, e.g. instrumental datives
            'NP-TMP'        : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'ADJ-.', 'NUM-.', 'OTHER-.']},    #temporal NP
            'NP-TMP-LFD'    : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'ADJ-.', 'NUM-.', 'OTHER-.']},
            'NP-TMP-RSP'    : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'ADJ-.', 'NUM-.', 'OTHER-.']},
            'NP-MSR'        : {'dir':'r', 'rules':['NS-.', 'N-.', 'NPR-.', 'NPRS-.', 'Q-.', 'QS-.', 'QR-.', 'OTHER-.', 'ADJ-.', 'ADJR-.', 'ADJS-.', 'ADV', 'ADV.*']},
            'NP-MSR-LFD'    : {'dir':'r', 'rules':['NS-.', 'N-.', 'NPR-.', 'NPRS-.', 'Q-.', 'QS-.', 'QR-.', 'OTHER-.', 'ADJ-.', 'ADJR-.', 'ADJS-.', 'ADV', 'ADV.*']},
            'NP-MSR-RSP'    : {'dir':'r', 'rules':['NS-.', 'N-.', 'NPR-.', 'NPRS-.', 'Q-.', 'QS-.', 'QR-.', 'OTHER-.', 'ADJ-.', 'ADJR-.', 'ADJS-.', 'ADV', 'ADV.*']},
            'NP-NUM'        : {'dir':'r', 'rules':[]},
            'NP-VOC'        : {'dir':'r', 'rules':['N-N', 'NS-N', 'MAN-N', 'OTHER-.']},
            'NP-VOC-LFD'    : {'dir':'r', 'rules':['N-N', 'NS-N', 'MAN-N', 'OTHER-.']},
            'NP-DIR'        : {'dir':'r', 'rules':['N-.', 'NS-.', 'NP.*']},
            'NP-DIR-LFD'    : {'dir':'r', 'rules':['N-.', 'NS-.', 'NP.*']},
            'NP-DIR-PRN'    : {'dir':'r', 'rules':['N-.', 'NS-.', 'NP.*']},
            'ADJP'          : {'dir':'r', 'rules':['VAN', 'ADJ-.', 'ADJR-.', 'ADJS-.', 'ADVP', 'ADVR', 'ONE', 'ONES', 'CP-TMP', 'N.+', 'Q.*', 'ADJP']},
            #'ADJP-SPR'      : {'dir':'r', 'rules':['ADJ-.', 'ADJS-N']},     #SPR = secondary predicate
            'ADJP-SPR-LFD'  : {'dir':'r', 'rules':['ADJ-.', 'ADJS-N']},
            'ADJP-DIR'      : {'dir':'r', 'rules':['ADJ-.', 'ADJR-.', 'ADJS-.', 'ADVR', 'ONE', 'ONES', 'CP-TMP', 'Q.*']},
            'ADJP-LFD'      : {'dir':'r', 'rules':['ADJ-.', 'ADJR-.', 'ADJS-.', 'ADVR', 'ONE', 'ONES', 'CP-TMP', 'Q.*']},
            'ADJP-LOC'      : {'dir':'r', 'rules':['ADJ-.', 'ADJR-.', 'ADJS-.', 'ADVR', 'ONE', 'ONES', 'CP-TMP', 'Q.*']},  #eitt dæmi um ADJP-OC
            'ADJP-PRN'      : {'dir':'r', 'rules':['ADJ-.', 'ADJR-.', 'ADJS-.', 'ADVR', 'ONE', 'ONES', 'CP-TMP', 'Q.*']},
            'ADJP-PRN-ELAB' : {'dir':'r', 'rules':['ADJ-.', 'ADJR-.', 'ADJS-.', 'ADVR', 'ONE', 'ONES', 'CP-TMP', 'Q.*']},
            'ADJP-RSP'      : {'dir':'r', 'rules':['ADJ-.', 'ADJR-.', 'ADJS-.', 'ADVR', 'ONE', 'ONES', 'CP-TMP', 'Q.*']},
            'ADJP-TMP'      : {'dir':'r', 'rules':['ADJ-.', 'ADJR-.', 'ADJS-.', 'ADVR', 'ONE', 'ONES', 'CP-TMP', 'Q.*']},
            'ADJX'          : {'dir':'r', 'rules':['ADJ.*']},
            'WADJP'         : {'dir':'r', 'rules':['ADJ.*', 'ADV.*']},
            'WADJX'         : {'dir':'r', 'rules':['ADJ.*', 'ADV.*']},
            'PP'            : {'dir':'r', 'rules':['CP-FRL', 'N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'NP', 'NP-.+', 'FS', 'CP-ADV', 'IP-SMC', 'ADVP', 'ADJP', 'CP-.*', 'IP-INF.*', 'P']},
            'PX'            : {'dir':'r', 'rules':['CP-FRL', 'NP', 'NP-.+', 'FS', 'CP-ADV', 'IP-SMC', 'ADVP', 'ADJP', 'CP-.*', 'IP-INF.*', 'P']},
            'PP-BY'         : {'dir':'r', 'rules':['NP', 'NP-.+', 'CP-ADV', 'IP-SMC', 'ADVP', 'ADJP', 'CP-.*', 'IP-INF.*', 'P']},
            'PP-BY-RSP'     : {'dir':'r', 'rules':['NP', 'NP-.+', 'CP-ADV', 'IP-SMC', 'ADVP', 'ADJP', 'CP-.*', 'IP-INF.*', 'P']},
            'PP-PRN'        : {'dir':'r', 'rules':['CP-ADV', 'NP', 'P']},
            'PP-PRN-ELAB'   : {'dir':'r', 'rules':['CP-ADV', 'NP', 'P']},
            'PP-RSP'        : {'dir':'r', 'rules':['NP', 'NP-.+', 'CP-ADV', 'IP-SMC', 'ADVP', 'ADJP', 'CP-.*', 'IP-INF.*', 'P']},
            'PP-SBJ'        : {'dir':'r', 'rules':['NP', 'NP-.+', 'CP-ADV', 'IP-SMC', 'ADVP', 'ADJP', 'CP-.*', 'IP-INF.*', 'P']},
            'PP-LFD'        : {'dir':'r', 'rules':['CP-ADV.*', 'CP-THT', 'NP', 'PP']},    #left dislocation
            'ADVP'          : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'ADV', 'ADVR', 'ADVS', 'WADV']},
            'ADVP-DIR'      : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'ADV', 'WADV']},
            'ADVP-DIR-LFD'  : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'ADV', 'WADV']},
            'ADVP-DIR-RSP'  : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'ADV', 'WADV']},
            'ADVP-LOC'      : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'ADV', 'WADV']},
            'ADVP-LOC-LFD'  : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'ADV', 'WADV']},
            'ADVP-LOC-RSP'  : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'ADV', 'WADV']},
            'ADVP-TMP'      : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'ADV', 'WADV']},
            'ADVP-TMP-LFD'  : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'ADV', 'WADV']},
            'ADVP-TMP-PRN'  : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'ADV', 'WADV']},
            'ADVP-TMP-RSP'  : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'ADV', 'WADV']},
            'ADVP-RSP'      : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'ADV', 'WADV']},
            'ADVP-RSP-RSP'  : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'ADV', 'WADV']},
            'ADVP-TMP-RSP'  : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'ADV', 'WADV']},
            'ADVP-ELAB'     : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'ADV', 'WADV']},
            'ADVP-LFD'      : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'ADV', 'WADV']},
            'ADVP-MSR'      : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'ADV', 'WADV']},
            'ADVP-PRN'      : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'ADV', 'WADV']},
            'ADVP-PRN-ELAB' : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'ADV', 'WADV']},
            'ADVP-PRN-REP'  : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'ADV', 'WADV']},
            'ADVP-RMP'      : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'ADV', 'WADV']},
            'ADVX'          : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'ADV', 'WADV']},
            'WADVP'         : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'WADV']},
            'WADVP-LOC'     : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'WADV']},
            'WADVP-NaN'     : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'WADV']},
            'CONJP'         : {'dir':'r', 'rules':['IP-MAT-SPE=1', 'N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'NP.*', 'NX', 'NUMP.*', 'NUM-.', 'QTP', 'QP', 'QX', 'IP-SUB', 'IP-MAT.*', 'IP-INF', 'IP-.+', 'CP-QUE', 'ADJP', 'ADJX', 'ADVP.*', 'PP', 'CONJ']},
            'CONJP-PP'      : {'dir':'r', 'rules':['NP.*', 'NX', 'N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'NUM-.', 'QP', 'QX', 'IP-SUB', 'IP-MAT', 'IP-INF', 'IP-.+', 'CP-QUE', 'ADJP', 'ADJX', 'PP', 'CONJ']},
            'CONJP-PRN'     : {'dir':'r', 'rules':['NP.*', 'NX', 'N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'NUM-.', 'QP', 'QX', 'IP-SUB', 'IP-MAT', 'IP-INF', 'IP-.+', 'CP-QUE', 'ADJP', 'ADJX', 'PP', 'CONJ']},
            'WNP'           : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'Q-.', 'WQ-.', 'WPRO-.', 'PRO-.', 'WD-.', 'NP.*', 'WNP.*']}, #MEIRA?
            'WNP-COM'       : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'Q-.', 'WQ-.', 'WPRO-.', 'PRO-.', 'WD-.', 'NP.*', 'WNP.*']},
            'WNP-MSR'       : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'Q-.', 'WQ-.', 'WPRO-.', 'PRO-.', 'WD-.', 'NP.*', 'WNP.*']},
            'WNP-POS'       : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'Q-.', 'WQ-.', 'WPRO-.', 'PRO-.', 'NP.*', 'WNP.*']},
            'WNP-PRN-ELAB'  : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'Q-.', 'WQ-.', 'WPRO-.', 'PRO-.', 'WD-.', 'NP.*', 'WNP.*']},
            'WPP'           : {'dir':'r', 'rules':['WNP.*', 'WADVP.*', 'NP.*']},
            'NX'            : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'NP.*']},
            'WNX'           : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'NP.*']},
            'FRAG-LFD'      : {'dir':'r', 'rules':['CP.*', 'IP.*', 'NP.*', 'PP']},
            'FRAG'          : {'dir':'r', 'rules':['CP.*', 'IP.*', 'N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'NP.*', 'PP', 'ADJP']},
            'QP'            : {'dir':'r', 'rules':['N-.', 'NS-.', 'Q-.', 'QS-.', 'QR-.']},
            'WQP'           : {'dir':'r', 'rules':['Q-.', 'QS-.', 'QR-.']},
            'QTP'           : {'dir':'r', 'rules':['IP.*', 'NP.*', 'N.*']},      #quote phrase
            'QTP-SBJ'       : {'dir':'r', 'rules':['IP.*', 'NP.*']},
            'REP'           : {'dir':'r', 'rules':['NP', 'PP', 'ADJP', 'IP.*', 'VB.*']},      #repetition
            'RRC'           : {'dir':'r', 'rules':['V.+', 'ADJP', 'RRC.*', 'PP']},      #reduced relative clause
            'RRC-PRN'       : {'dir':'r', 'rules':['V.+', 'ADJP', 'RRC.*', 'PP']},
            'RRC-SPE'       : {'dir':'r', 'rules':['V.+', 'ADJP', 'RRC.*', 'PP']},
            'NUMP'          : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'NUM-.']},
            'INTJP'         : {'dir':'r', 'rules':['INTJ', 'N-.', 'NS-.', 'NPR-.', 'NPRS-.']},
            'VP'            : {'dir':'r', 'rules':['V.+', 'BE.']},
            'XP'            : {'dir':'r', 'rules':['XXX']},
            'FS'            : {'dir':'r', 'rules':['CP-ADV']},
            'META'          : {'dir':'r', 'rules':['NP', 'N.*']},
            'CODE'          : {'dir':'r', 'rules':['NP']},
            'TRANSLATION'   : {'dir':'r', 'rules':['NP']}
            }

relation_NP = {
      None: 'obl',
      'LFD': 'obl',
      'ADV': 'obl',
      'ADV-LFD': 'obl',
      'ADV-RSP': 'obl',
      'CMP': 'obl',
      'PRN': 'appos',     #viðurlag, appositive
      'PRNL': 'appos',
      'PRN-ELAB': 'appos',
      'PRN-REP': 'appos',
      'RSP': 'obl',
      'SBJ': 'nsubj',
      'SBJ-LFD': 'nsubj',
      'SBJ-RSP': 'nsubj',
      'SMC': 'obl',
      'SPE': 'nsubj',
      'OB1': 'obj',
      'OB1-LFD': 'obj',
      'OB1-RSP': 'obj',
      'OB2': 'iobj',
      'OB2-RSP': 'iobj',
      'OB3': 'iobj',
      'PRD': 'xcomp',    #sagnfylling, predicate
      'SPR': 'xcomp',
      'POS': 'nmod:poss',      #Örvar: 'POS': 'case'
      'POS-RSP': 'nmod:poss',
      'COM': 'nmod:poss',
      'ADT': 'obl',    #ATH. rétt?
      'TMP': 'obl',
      'TMP-LFD': 'obl',
      'TMP-RSP': 'obl',
      'NUM': 'nummod',
      'MSR': 'obl',   #measure phrase, frekar obl?
      'MSR-LFD': 'obl',
      'MSR-RSP': 'obl',
      'VOC': 'vocative',
      'VOC-LFD': 'vocative',
      'DIR': 'obl',
      'DIR-LFD': 'obl',
      'DIR-PRN': 'obl'
}

relation_IP = {
      None: '?',
      'INF': 'acl',
      'INF-ABS': 'acl',
      'INF-ABS-PRN': 'acl',
      'INF-PRP': 'advcl',   #merkingin 'til þess að'
      'INF-PRP-PRN': 'advcl',
      'INF-PRP-PRN-SPE': 'advcl',
      'INF-PRP-SPE': 'advcl',
      'INF-PRP-SPE-PRN': 'advcl',
      'INF-SPE': 'acl',
      'INF-SPE-ADT': 'advcl',      # ADT = clause-level dative adjunct
      'INF-SPE-DEG': 'acl',
      'INF-SPE-LFD': 'acl',
      'INF-SPE-PRN': 'acl',
      'INF-SPE-PRN-ELAB': 'acl',    #sama merki og INF-SPE-PRN
      'INF-SPE-PRP': 'advcl',   #merkingin 'til þess að'
      'INF-SPE-PRP-PRN': 'advcl',
      'INF-SPE-SBJ': 'acl',
      'INF-PRN': 'acl',
      'INF-PRN-ELAB': 'acl',
      'INF-PRN-PRP': 'advcl',     #notað í til þess að
      'INF-PRN-SPE': 'acl',
      'INF-RSP': 'acl',      # RSP = resumptive
      'INF-SBJ': 'xcomp',
      'INF-SBJ-SPE': 'xcomp',
      'INF-DEG': 'acl',
      'INF-DEG-PRN': 'acl',
      'INF-DEG-SPE': 'acl',
      'INF-LFD': 'acl',
      'INF-PRD': 'csubj',
      'INF-ADT': 'advcl',   #clause-level modifier af því clause-level dative adjunct
      'INF-ADT-SPE': 'advcl',
      'INF-ADT-SPE-LFD': 'advcl',
      'INF-ADT-LFD': 'advcl',
      'INF-ADT-PRN': 'advcl',
      'MAT': 'conj',        #þarf ekki að hafa merkimiða því sögnin er alltaf rót? - conj þegar búið er að gera punkt til punkts
      'MAT-DIR': 'conj',    #sama og MAT
      'MAT-LFD': 'conj',    #sama og MAT
      'MAT-OB1': 'advcl',     #kemur einu sinni fyrir, haus á eftir nær(þegar), jonsteingrims
      'MAT-PRN': 'conj',
      'MAT-PRN-ELAB': 'conj',
      'MAT-PRN-LFD': 'conj',
      'MAT-PRN-SPE': 'conj',
      'MAT-SBJ': 'conj',
      'MAT-SPE': 'ccomp/xcomp',
      'MAT-SPE-PRN': 'ccomp/xcomp',
      'MAT-SPE-PRN-ELAB': 'ccomp/xcomp',
      'MAT-SPE-PRN-LFD': 'ccomp/xcomp',
      'MAT-SPE-SBJ': 'ccomp/xcomp',
      'MAT-SUB-SPE': 'ccomp/xcomp',
      'MAT-SMC': 'conj',    #sama og MAT, kemur einu sinni fyrir og hausinn er rót
      'SUB': 'conj',
      'SUB-INF': 'xcomp',
      'SUB-LFD': 'conj',   #skiptir ekki máli, kemur einu sinni fyrir og CP-liðurinn trompar
      'SUB-PRN': 'conj',
      'SUB-PRN-ELAB': 'conj',
      'SUB-REP': 'conj',    # REP = repetition
      'SUB-SPE': 'conj',
      'SUB-SPE-PRN': 'conj',
      'SUB-SPE-PRN-ELAB': 'conj',       # ELAB = elaborations
      'IMP': 'ccomp',   #frl. en innifalið í sögninni, þá ccomp eða xcomp?
      'IMP-PRN': 'ccomp',
      'IMP-SPE': 'ccomp',
      'IMP-SPE-PRN': 'ccomp',
      'IMP-SPE-SBJ': 'ccomp',
      'SMC': 'ccomp/xcomp',
      'SMC-SBJ': 'ccomp/xcomp',
      'SMC-SPE': 'ccomp/xcomp',
      'PPL': 'acl/advcl',  #?
      'PPL-ABS': 'advcl/acl?',  #?
      'PPL-ABS-SPE': 'advcl/acl?',  #?
      'PPL-OB1': 'advcl/acl?',  #?
      'PPL-OB1-SPE': 'advcl/acl?',  #?
      'PPL-OB2': 'advcl/acl?',  #?
      'PPL-PRD': 'advcl/acl?',  #?
      'PPL-PRN': 'advcl/acl?',  #?
      'PPL-SBJ': 'advcl/acl?',  #?
      'PPL-SPE': 'advcl/acl?',  #?
      'PPL-SPE-OB1': 'advcl/acl?',  #?
      'PPL-SPE-PRD': 'advcl/acl?',  #?
      'ABS': 'advcl/acl?',        #absolutus
      'ABS-PRN': 'advcl/acl?',
      'ABS-SBJ': 'advcl/acl?'
}

relation_CP = {
      None: '?',
      'THT': 'ccomp/xcomp',
      'THT-SBJ': 'ccomp/xcomp',
      'THT-SBJ-SPE': 'ccomp/xcomp',
      'THT-SPE': 'ccomp/xcomp',
      'THT-SPE-PRN': 'ccomp/xcomp',
      'THT-SPE-SBJ': 'ccomp/xcomp',
      'THT-PRN': 'ccomp/xcomp',
      'THT-PRN-NaN': 'ccomp/xcomp',
      'THT-PRN-SPE': 'ccomp/xcomp',
      'THT-LFD': 'ccomp/xcomp',
      'THT-RSP': 'ccomp/xcomp',     #resumptive element
      'CAR': 'acl:relcl',
      'CAR-SPE': 'acl:relcl',
      'CLF': 'acl:relcl',
      'CLF-SPE': 'acl:relcl',
      'CMP': 'advcl',      #ATH. acl í enska bankanum á eftir 'than', advcl í sænska og norska
      'CMP-LFD': 'advcl',
      'CMP-SPE': 'advcl',
      'DEG': 'advcl',
      'DEG-SPE': 'advcl',
      'FRL': 'ccomp/xcomp',    #ccomp?, free relative
      'FRL-SPE': 'ccomp/xcomp',
      'REL': 'acl:relcl',
      'REL-SPE': 'acl:relcl',
      'REL-SPE-PRN': 'acl:relcl',
      'QUE': 'ccomp/xcomp',
      'QUE-SPE': 'ccomp/xcomp',
      'QUE-SPE-LFD': 'ccomp/xcomp',
      'QUE-SPE-LFD-PRN': 'ccomp/xcomp',
      'QUE-SPE-LFD-SBJ': 'ccomp/xcomp',
      'QUE-SPE-PRN': 'ccomp/xcomp',
      'QUE-SPE-SBJ': 'ccomp/xcomp',
      'QUE-ADV': 'ccomp/xcomp',
      'QUE-ADV-LFD': 'ccomp/xcomp',
      'QUE-ADV-SPE': 'ccomp/xcomp',
      'QUE-ADV-SPE-LFD': 'ccomp/xcomp',
      'QUE-LFD': 'ccomp/xcomp',
      'QUE-PRN': 'ccomp/xcomp',
      'QUE-PRN-ELAB': 'ccomp/xcomp',
      'QUE-PRN-SPE': 'ccomp/xcomp',
      'QUE-SBJ': 'ccomp/xcomp',
      'ADV': 'advcl',
      'ADV-LFD': 'advcl',
      'ADV-LFD-SPE': 'advcl',
      'ADV-PRN': 'advcl',
      'ADV-RSP': 'advcl',
      'ADV-SPE': 'advcl',
      'ADV-SPE-LFD': 'advcl',
      'ADV-SPE-PRN': 'advcl',
      'EOP': 'xcomp',   #so. í nh. fylgir alltaf, ekkert frl.
      'EOP-SPE': 'xcomp',
      'EOP-SPE-PRN': 'xcomp',
      'EXL': 'ccomp/xcomp',        #exclamative, same parse as QUE
      'EXL-SPE': 'ccomp/xcomp',
      'TMC': 'xcomp',        #so. í nh. fylgir alltaf, ekkert frl.
      'TMC-SPE': 'xcomp',
      'TMP': 'xcomp'    #so. í nh fylgir alltaf, ekkert frl.
}
