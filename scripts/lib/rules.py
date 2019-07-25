

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
            'EF' : 'Gen',
            'D' : 'Dat'
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
#    'PART' : {},    #no features possible for particles
}

head_rules = {
            'IP-INF'        : {'dir':'r', 'rules':['VB', 'DO', 'VAN', 'IP-INF']},
#            'IP-INF-1'      : {'dir':'r', 'rules':['VB', 'DO', 'VAN']},
#            'IP-INF=1'      : {'dir':'r', 'rules':['VB', 'DO', 'VAN']},
#            'IP-INF=2'      : {'dir':'r', 'rules':['VB', 'DO', 'VAN']},
#            'IP-INF=3'      : {'dir':'r', 'rules':['VB', 'DO', 'VAN']},
#            'IP-INF=4'      : {'dir':'r', 'rules':['VB', 'DO', 'VAN']},
#            'IP-INF=5'      : {'dir':'r', 'rules':['VB', 'DO', 'VAN']},
#            'IP-INF=6'      : {'dir':'r', 'rules':['VB', 'DO', 'VAN']},
#            'IP-INF=7'      : {'dir':'r', 'rules':['VB', 'DO', 'VAN']},
#            'IP-INF=23'     : {'dir':'r', 'rules':['VB', 'DO', 'VAN']},
            'IP-INF-ABS'    : {'dir':'r', 'rules':['VB']},
            'IP-INF-ABS-PRN': {'dir':'r', 'rules':['VB']},
            'IP-INF-PRP'    : {'dir':'r', 'rules':['VB', 'IP-INF']},      #tilgangsnafnháttur
#            'IP-INF-PRP=1': {'dir':'r', 'rules':['VB']},
            'IP-INF-PRP-PRN-SPE': {'dir':'r', 'rules':['VB']},
            'IP-INF-PRP-PRN': {'dir':'r', 'rules':['VB']},
#            'IP-INF-PRP-PRN=2': {'dir':'r', 'rules':['VB']},
            'IP-INF-PRP-SPE': {'dir':'r', 'rules':['VB']},
#            'IP-INF-PRP-SPE=1': {'dir':'r', 'rules':['VB']},
            'IP-INF-PRP-SPE-PRN': {'dir':'r', 'rules':['VB']},
            'IP-INF-SPE'    : {'dir':'r', 'rules':['VB']},      #spe = direct speech
#            'IP-INF-SPE=1'  : {'dir':'r', 'rules':['VB']},
#            'IP-INF-SPE=2'  : {'dir':'r', 'rules':['VB']},
#            'IP-INF-SPE=3'  : {'dir':'r', 'rules':['VB']},
            'IP-INF-SPE-ADT': {'dir':'r', 'rules':['VB']},
            'IP-INF-SPE-DEG': {'dir':'r', 'rules':['VB']},
            'IP-INF-SPE-LFD': {'dir':'r', 'rules':['VB']},
            'IP-INF-SPE-PRN': {'dir':'r', 'rules':['VB']},
#            'IP-INF-SPE-PRN=1': {'dir':'r', 'rules':['VB']},
#            'IP-INF-SPE-PRN=3': {'dir':'r', 'rules':['VB']},
            'IP-INF-SPE-PRN-ELAB': {'dir':'r', 'rules':['VB']},
            'IP-INF-SPE-PRP': {'dir':'r', 'rules':['VB']},
            'IP-INF-SPE-PRP-PRN': {'dir':'r', 'rules':['VB']},
            'IP-INF-SPE-SBJ': {'dir':'r', 'rules':['VB']},
#            'IP-INF-TTT'    : {'dir':'r', 'rules':['VB']},
#            'IP-INF-ZZZ'    : {'dir':'r', 'rules':['VB']},
            'IP-INF-PRN'    : {'dir':'r', 'rules':['VB']},
#            'IP-INF-PRN=1'  : {'dir':'r', 'rules':['VB']},
#            'IP-INF-PRN=2'  : {'dir':'r', 'rules':['VB']},
#            'IP-INF-PRN=3'  : {'dir':'r', 'rules':['VB']},
#            'IP-INF-PRN=4'  : {'dir':'r', 'rules':['VB']},
#            'IP-INF-PRN=6'  : {'dir':'r', 'rules':['VB']},
#            'IP-INF-PRN=7'  : {'dir':'r', 'rules':['VB']},
            'IP-INF-PRN-ELAB': {'dir':'r', 'rules':['VB']},
#            'IP-INF-PRN-ELAB=2': {'dir':'r', 'rules':['VB']},
#            'IP-INF-PRN-ELAB=3': {'dir':'r', 'rules':['VB']},
            'IP-INF-PRN-PRP': {'dir':'r', 'rules':['VB']},
            'IP-INF-PRN-SPE': {'dir':'r', 'rules':['VB']},
            'IP-INF-RSP'    : {'dir':'r', 'rules':['VB']},
            'IP-INF-SBJ'    : {'dir':'r', 'rules':['VB']},
            'IP-INF-SBJ-SPE': {'dir':'r', 'rules':['VB']},
#            'IP-INF-SBJ=2'  : {'dir':'r', 'rules':['VB']},
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
            'IP-MAT'        : {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'VAN', 'HV.*', 'NP', 'ADJP', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT']},
#            'IP-MAT-1'      : {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'HV.*', 'NP-1', 'ADJP', 'VAN', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT-1']},
#            'IP-MAT=1'      : {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'HV.*', 'NP', 'ADJP', 'VAN', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT']}, 
#            'IP-MAT=16'     : {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'HV.*', 'NP', 'ADJP', 'VAN', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT']}, 
#            'IP-MAT=2'      : {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'HV.*', 'NP', 'ADJP', 'VAN', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT']}, 
#            'IP-MAT=3'      : {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'HV.*', 'NP', 'ADJP', 'VAN', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT']}, 
#            'IP-MAT=5'      : {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'HV.*', 'NP', 'ADJP', 'VAN', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT']}, 
#            'IP-MAT=9'      : {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'HV.*', 'NP', 'ADJP', 'VAN', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT']}, 
#            'IP-MAT-TTT'    : {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'NP', 'ADJP', 'VAN', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT.*']},
            'IP-MAT-DIR'    : {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'VAN', 'HV.*', 'NP', 'ADJP', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT']},
#            'IP-MAT-KOMINN' : {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'VAN', 'HV.*', 'NP', 'ADJP', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT']},
            'IP-MAT-LFD'    : {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'VAN', 'HV.*', 'NP', 'ADJP', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT']},
            'IP-MAT-OB1'    : {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'VAN', 'HV.*', 'NP', 'ADJP', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT']},
            'IP-MAT-PRN'    : {'dir':'r', 'rules':['VB.*']},
            'IP-MAT-PRN-ELAB': {'dir':'r', 'rules':['VB.*']},
#            'IP-MAT-PRN-ELAB=1': {'dir':'r', 'rules':['VB.*']},
            'IP-MAT-PRN-LFD': {'dir':'r', 'rules':['VB.*']},
            'IP-MAT-PRN-SPE': {'dir':'r', 'rules':['VB.*']},
#            'IP-MAT-PRN-SPE=1': {'dir':'r', 'rules':['VB.*']},
#            'IP-MAT-PRN=1'  : {'dir':'r', 'rules':['VB.*']},
#            'IP-MAT-PRN=2'  : {'dir':'r', 'rules':['VB.*']},
#            'IP-MAT-PRN=3'  : {'dir':'r', 'rules':['VB.*']},
            'IP-MAT-SBJ'    : {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'VAN', 'HV.*', 'NP', 'ADJP', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT']},
            'IP-MAT-SPE'    : {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'NP', 'ADJP', 'VAN', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT.*']},
            'IP-MAT-SPE-PRN': {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'NP', 'ADJP', 'VAN', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT.*']},
            'IP-MAT-SPE-PRN-ELAB': {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'NP', 'ADJP', 'VAN', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT.*']},
            'IP-MAT-SPE-PRN-LFD': {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'NP', 'ADJP', 'VAN', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT.*']},
#            'IP-MAT-SPE-PRN=1': {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'NP', 'ADJP', 'VAN', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT.*']},
            'IP-MAT-SPE-SBJ': {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'NP', 'ADJP', 'VAN', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT.*']},
#            'IP-MAT-SPE-TTT': {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'NP', 'ADJP', 'VAN', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT.*']},
#            'IP-MAT-SPE=1'  : {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'NP', 'ADJP', 'VAN', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT.*']},
#            'IP-MAT-SPE=2'  : {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'NP', 'ADJP', 'VAN', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT.*']},
#            'IP-MAT-SPE=3'  : {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'NP', 'ADJP', 'VAN', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT.*']},
#            'IP-MAT-SPE=4'  : {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'NP', 'ADJP', 'VAN', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT.*']},
#            'IP-MAT-SPE=5'  : {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'NP', 'ADJP', 'VAN', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT.*']},
            'IP-MAT-SUB-SPE': {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'NP', 'ADJP', 'VAN', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT.*']},
            'IP-MAT-SMC'    : {'dir':'r', 'rules':['VB', 'VB.*','RD.*', 'DO.*', 'DAN', 'VAN', 'HV.*', 'NP', 'ADJP', 'NP-PRD', 'N.*', 'IP-SMC', 'IP-MAT']},    
#            'IP-SUB'        : {'dir':'r', 'rules':['IP-INF.*', 'VB', 'VB.*', 'DO.*', 'DAN', 'NP-PRD', 'RD.*', 'ADVP', 'ADJP', 'IP-SUB', 'NP-PRD']},    #meira?
            'IP-SUB'        : {'dir':'r', 'rules':['VB', 'VB.*', 'DO.*', 'DAN', 'VAN', 'RAN', 'HAN', 'BAN', 'RDN', 'BEN', 'HV.*', 'IP-INF.*', 'ADJP', 'NP-PRD', 'RD.*', 'NP', 'ADVP', 'IP-SUB', 'HVN']},
#            'IP-SUB=1'      : {'dir':'r', 'rules':['VB', 'VB.*', 'DO.*', 'DAN', 'VAN', 'RAN', 'HAN', 'BAN', 'RDN', 'BEN', 'HV.*', 'IP-INF.*', 'ADJP', 'NP-PRD', 'RD.*', 'NP', 'ADVP', 'IP-SUB', 'HVN']},
#            'IP-SUB=10'     : {'dir':'r', 'rules':['VB', 'VB.*', 'DO.*', 'DAN', 'VAN', 'RAN', 'HAN', 'BAN', 'RDN', 'BEN', 'HV.*', 'IP-INF.*', 'ADJP', 'NP-PRD', 'RD.*', 'NP', 'ADVP', 'IP-SUB', 'HVN']},
#            'IP-SUB=11'     : {'dir':'r', 'rules':['VB', 'VB.*', 'DO.*', 'DAN', 'VAN', 'RAN', 'HAN', 'BAN', 'RDN', 'BEN', 'HV.*', 'IP-INF.*', 'ADJP', 'NP-PRD', 'RD.*', 'NP', 'ADVP', 'IP-SUB', 'HVN']},
#            'IP-SUB=12'     : {'dir':'r', 'rules':['VB', 'VB.*', 'DO.*', 'DAN', 'VAN', 'RAN', 'HAN', 'BAN', 'RDN', 'BEN', 'HV.*', 'IP-INF.*', 'ADJP', 'NP-PRD', 'RD.*', 'NP', 'ADVP', 'IP-SUB', 'HVN']},
#            'IP-SUB=13'     : {'dir':'r', 'rules':['VB', 'VB.*', 'DO.*', 'DAN', 'VAN', 'RAN', 'HAN', 'BAN', 'RDN', 'BEN', 'HV.*', 'IP-INF.*', 'ADJP', 'NP-PRD', 'RD.*', 'NP', 'ADVP', 'IP-SUB', 'HVN']},
#            'IP-SUB=19'     : {'dir':'r', 'rules':['VB', 'VB.*', 'DO.*', 'DAN', 'VAN', 'RAN', 'HAN', 'BAN', 'RDN', 'BEN', 'HV.*', 'IP-INF.*', 'ADJP', 'NP-PRD', 'RD.*', 'NP', 'ADVP', 'IP-SUB', 'HVN']},
#            'IP-SUB=2'      : {'dir':'r', 'rules':['VB', 'VB.*', 'DO.*', 'DAN', 'VAN', 'RAN', 'HAN', 'BAN', 'RDN', 'BEN', 'HV.*', 'IP-INF.*', 'ADJP', 'NP-PRD', 'RD.*', 'NP', 'ADVP', 'IP-SUB', 'HVN']},
#            'IP-SUB=3'      : {'dir':'r', 'rules':['VB', 'VB.*', 'DO.*', 'DAN', 'VAN', 'RAN', 'HAN', 'BAN', 'RDN', 'BEN', 'HV.*', 'IP-INF.*', 'ADJP', 'NP-PRD', 'RD.*', 'NP', 'ADVP', 'IP-SUB', 'HVN']},
#            'IP-SUB=4'      : {'dir':'r', 'rules':['VB', 'VB.*', 'DO.*', 'DAN', 'VAN', 'RAN', 'HAN', 'BAN', 'RDN', 'BEN', 'HV.*', 'IP-INF.*', 'ADJP', 'NP-PRD', 'RD.*', 'NP', 'ADVP', 'IP-SUB', 'HVN']},
#            'IP-SUB=5'      : {'dir':'r', 'rules':['VB', 'VB.*', 'DO.*', 'DAN', 'VAN', 'RAN', 'HAN', 'BAN', 'RDN', 'BEN', 'HV.*', 'IP-INF.*', 'ADJP', 'NP-PRD', 'RD.*', 'NP', 'ADVP', 'IP-SUB', 'HVN']},
#            'IP-SUB=6'      : {'dir':'r', 'rules':['VB', 'VB.*', 'DO.*', 'DAN', 'VAN', 'RAN', 'HAN', 'BAN', 'RDN', 'BEN', 'HV.*', 'IP-INF.*', 'ADJP', 'NP-PRD', 'RD.*', 'NP', 'ADVP', 'IP-SUB', 'HVN']},
#            'IP-SUB=7'      : {'dir':'r', 'rules':['VB', 'VB.*', 'DO.*', 'DAN', 'VAN', 'RAN', 'HAN', 'BAN', 'RDN', 'BEN', 'HV.*', 'IP-INF.*', 'ADJP', 'NP-PRD', 'RD.*', 'NP', 'ADVP', 'IP-SUB', 'HVN']},
#            'IP-SUB=8'      : {'dir':'r', 'rules':['VB', 'VB.*', 'DO.*', 'DAN', 'VAN', 'RAN', 'HAN', 'BAN', 'RDN', 'BEN', 'HV.*', 'IP-INF.*', 'ADJP', 'NP-PRD', 'RD.*', 'NP', 'ADVP', 'IP-SUB', 'HVN']},
#            'IP-SUB=9'      : {'dir':'r', 'rules':['VB', 'VB.*', 'DO.*', 'DAN', 'VAN', 'RAN', 'HAN', 'BAN', 'RDN', 'BEN', 'HV.*', 'IP-INF.*', 'ADJP', 'NP-PRD', 'RD.*', 'NP', 'ADVP', 'IP-SUB', 'HVN']},
#            'IP-SUB=X'      : {'dir':'r', 'rules':['VB', 'VB.*', 'DO.*', 'DAN', 'VAN', 'RAN', 'HAN', 'BAN', 'RDN', 'BEN', 'HV.*', 'IP-INF.*', 'ADJP', 'NP-PRD', 'RD.*', 'NP', 'ADVP', 'IP-SUB', 'HVN']},
#            'IP-SUB=XXX'    : {'dir':'r', 'rules':['VB', 'VB.*', 'DO.*', 'DAN', 'VAN', 'RAN', 'HAN', 'BAN', 'RDN', 'BEN', 'HV.*', 'IP-INF.*', 'ADJP', 'NP-PRD', 'RD.*', 'NP', 'ADVP', 'IP-SUB', 'HVN']},
#            'IP-SUB-1'      : {'dir':'r', 'rules':['VB', 'VB.*', 'DO.*', 'DAN', 'VAN', 'RAN', 'HAN', 'BAN', 'RDN', 'BEN', 'HV.*', 'IP-INF.*', 'ADJP', 'NP-PRD', 'RD.*', 'NP', 'NP-2', 'ADVP', 'IP-SUB', 'HVN']},
#            'IP-SUB-4'      : {'dir':'r', 'rules':['ADJP', 'IP-INF.*', 'VB', 'VB.*', 'DO.*', 'DAN', 'VAN', 'RAN', 'HAN', 'BAN', 'NP-PRD', 'RD.*', 'ADVP', 'IP-SUB', 'NP', 'NP-2', 'HVN']},
            'IP-SUB-INF'    : {'dir':'r', 'rules':[]},
            'IP-SUB-LFD'    : {'dir':'r', 'rules':['VB', 'VB.*', 'DO.*', 'DAN', 'VAN', 'RAN', 'HAN', 'BAN', 'RDN', 'BEN', 'HV.*', 'IP-INF.*', 'ADJP', 'NP-PRD', 'RD.*', 'NP', 'ADVP', 'IP-SUB', 'HVN']},
            'IP-SUB-PRN'    : {'dir':'r', 'rules':['VB.*', 'VAN']},
            'IP-SUB-PRN-ELAB': {'dir':'r', 'rules':['VB.*', 'VAN']},
#            'IP-SUB-PRN-ELAB=3': {'dir':'r', 'rules':['VB.*', 'VAN']},
#            'IP-SUB-PRN-ELAB=6': {'dir':'r', 'rules':['VB.*', 'VAN']},
#            'IP-SUB-PRN=1'  : {'dir':'r', 'rules':['VB.*', 'VAN']},
#            'IP-SUB-PRN=10' : {'dir':'r', 'rules':['VB.*', 'VAN']},
#            'IP-SUB-PRN=2'  : {'dir':'r', 'rules':['VB.*', 'VAN']},
#            'IP-SUB-PRN=3'  : {'dir':'r', 'rules':['VB.*', 'VAN']},
#            'IP-SUB-PRN=4'  : {'dir':'r', 'rules':['VB.*', 'VAN']},
#            'IP-SUB-PRN=5'  : {'dir':'r', 'rules':['VB.*', 'VAN']},
#            'IP-SUB-PRN=6'  : {'dir':'r', 'rules':['VB.*', 'VAN']},
#            'IP-SUB-PRN=7'  : {'dir':'r', 'rules':['VB.*', 'VAN']},
#            'IP-SUB-PRN=8'  : {'dir':'r', 'rules':['VB.*', 'VAN']},
            'IP-SUB-PRN=XXX': {'dir':'r', 'rules':['VB.*', 'VAN']},
            'IP-SUB-REP'    : {'dir':'r', 'rules':[]},
#            'IP-SUB-REP=4'  : {'dir':'r', 'rules':[]},
            'IP-SUB-SPE'    : {'dir':'r', 'rules':['VB.*', 'HV.*']},
            'IP-SUB-SPE-PRN': {'dir':'r', 'rules':['VB.*', 'HV.*']},
            'IP-SUB-SPE-PRN-ELAB': {'dir':'r', 'rules':['VB.*', 'HV.*']},
#            'IP-SUB-SPE-PRN=1': {'dir':'r', 'rules':['VB.*', 'HV.*']},
#            'IP-SUB-SPE-PRN=2': {'dir':'r', 'rules':['VB.*', 'HV.*']},
#            'IP-SUB-SPE-PRN=3': {'dir':'r', 'rules':['VB.*', 'HV.*']},
#            'IP-SUB-SPE-TTT': {'dir':'r', 'rules':['VB.*', 'HV.*']},
#            'IP-SUB-SPE=1'  : {'dir':'r', 'rules':['VB.*', 'HV.*']},
#            'IP-SUB-SPE=2'  : {'dir':'r', 'rules':['VB.*', 'HV.*']},
#            'IP-SUB-SPE=3'  : {'dir':'r', 'rules':['VB.*', 'HV.*']},
#            'IP-SUB-SPE=4'  : {'dir':'r', 'rules':['VB.*', 'HV.*']},
#            'IP-SUB-SPE=5'  : {'dir':'r', 'rules':['VB.*', 'HV.*']},
#            'IP-SUB-SPE=6'  : {'dir':'r', 'rules':['VB.*', 'HV.*']},
#            'IP-SUB-SPE=9'  : {'dir':'r', 'rules':['VB.*', 'HV.*']},
#            'IP-SUB-TTT'    : {'dir':'r', 'rules':[]},
            'IP-IMP'        : {'dir':'r', 'rules':['VB.']},    #imperative
#            'IP-IMP=1'      : {'dir':'r', 'rules':['VB.']},
            'IP-IMP-PRN'    : {'dir':'r', 'rules':['VB.']},
            'IP-IMP-SPE'    : {'dir':'r', 'rules':['VB.']},
#            'IP-IMP-SPE=1'  : {'dir':'r', 'rules':['VB.']},
#            'IP-IMP-SPE=6'  : {'dir':'r', 'rules':['VB.']},
            'IP-IMP-SPE-PRN': {'dir':'r', 'rules':['VB.']},
#            'IP-IMP-SPE-PRN=1': {'dir':'r', 'rules':['VB.']},
#            'IP-IMP-SPE-PRN=2': {'dir':'r', 'rules':['VB.']},
            'IP-IMP-SPE-SBJ': {'dir':'r', 'rules':['VB.']},
            'IP-SMC'        : {'dir':'r', 'rules':['IP-INF-SBJ', 'IP-SMC', 'NP-PRD', 'VAG-.', 'ADJP', 'NP.*']},    #small clause
            'IP-SMC-SBJ'    : {'dir':'r', 'rules':['IP-INF-SBJ', 'IP-SMC', 'NP-PRD', 'VAG-.', 'ADJP', 'NP.*']},
            'IP-SMC-SPE'    : {'dir':'r', 'rules':['IP-INF-SBJ', 'IP-SMC', 'NP-PRD', 'VAG-.', 'ADJP', 'NP.*']},
#            'IP-SMC-SPE=1'  : {'dir':'r', 'rules':['IP-INF-SBJ', 'IP-SMC', 'NP-PRD', 'VAG-.', 'ADJP', 'NP.*']},
#            'IP-SMC-SPE=2'  : {'dir':'r', 'rules':['IP-INF-SBJ', 'IP-SMC', 'NP-PRD', 'VAG-.', 'ADJP', 'NP.*']},
#            'IP-SMC-TTT'    : {'dir':'r', 'rules':['IP-INF-SBJ', 'IP-SMC', 'NP-PRD', 'VAG-.', 'ADJP', 'NP.*']},
#            'IP-SMC=1'      : {'dir':'r', 'rules':['IP-INF-SBJ', 'IP-SMC', 'NP-PRD', 'VAG-.', 'ADJP', 'NP.*']},
#            'IP-SMC=2'      : {'dir':'r', 'rules':['IP-INF-SBJ', 'IP-SMC', 'NP-PRD', 'VAG-.', 'ADJP', 'NP.*']},
            'IP-PPL'        : {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG']},  #lýsingarháttarsetning
            'IP-PPL-ABS'    : {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG']},
            'IP-PPL-ABS-SPE': {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG']},
#            'IP-PPL-ABS=5'  : {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG']},
            'IP-PPL-OB1'    : {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG']},
            'IP-PPL-OB1-SPE': {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG']},
            'IP-PPL-OB2'    : {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG']},
            'IP-PPL-PRD'    : {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG']},
            'IP-PPL-PRN'    : {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG']},
            'IP-PPL-SBJ'    : {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG']},
            'IP-PPL-SPE'    : {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG']},
            'IP-PPL-SPE-OB1': {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG']},
            'IP-PPL-SPE-PRD': {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG']},
  #          'IP-PPL=1'      : {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG']},
  #          'IP-PPL=3'      : {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG']},
            'IP-ABS'        : {'dir':'r', 'rules':[]},
            'IP-ABS-PRN'    : {'dir':'r', 'rules':[]},
            'IP-ABS-SBJ'    : {'dir':'r', 'rules':[]},
#            'IP-ABS=1'      : {'dir':'r', 'rules':[]},
#            'IP-ABS=2'      : {'dir':'r', 'rules':[]},
            'CP-THT'        : {'dir':'r', 'rules':['IP-SUB.*','.*']},   #að
#            'CP-THT=XXX'    : {'dir':'r', 'rules':['IP-SUB.*','.*']},
#            'CP-THT-1'      : {'dir':'r', 'rules':['IP-SUB.*','.*']},
            'CP-THT-SBJ'    : {'dir':'r', 'rules':['IP-SUB.*','.*']},   #extraposed subject
            'CP-THT-SBJ-SPE': {'dir':'r', 'rules':['IP-SUB.*','.*']},
            'CP-THT-SPE'    : {'dir':'r', 'rules':['IP-SUB.*','.*']},
#            'CP-THT-SPE=1'  : {'dir':'r', 'rules':['IP-SUB.*','.*']},
            'CP-THT-SPE-PRN': {'dir':'r', 'rules':['IP-SUB.*','.*']},
            'CP-THT-SPE-SBJ': {'dir':'r', 'rules':['IP-SUB.*','.*']},
            'CP-THT-PRN'    : {'dir':'r', 'rules':['IP-SUB.*','.*']},
            'CP-THT-PRN-NaN': {'dir':'r', 'rules':['IP-SUB.*','.*']},
            'CP-THT-PRN-SPE': {'dir':'r', 'rules':['IP-SUB.*','.*']},
#            'CP-THT-PRN-1'  : {'dir':'r', 'rules':['IP-SUB.*','.*']},
#            'CP-THT-PRN-2'  : {'dir':'r', 'rules':['IP-SUB.*','.*']},
#            'CP-THT-PRN-3'  : {'dir':'r', 'rules':['IP-SUB.*','.*']},
#            'CP-THT-PRN-4'  : {'dir':'r', 'rules':['IP-SUB.*','.*']},
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
#            'CP-DEG-1'      : {'dir':'r', 'rules':['IP-SUB.*']},
#            'CP-DEG-2'      : {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-FRL'        : {'dir':'r', 'rules':['IP-SUB.*', 'WNP.*']},  #free relative
            'CP-FRL-SPE'    : {'dir':'r', 'rules':['IP-SUB.*', 'WNP.*']},
            'CP-REL'        : {'dir':'r', 'rules':['IP-SUB.*']},    #relative
#            'CP-REL-1'      : {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-REL-SPE'    : {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-REL-SPE-PRN': {'dir':'r', 'rules':['IP-SUB.*']},
#            'CP-REL-TTT'    : {'dir':'r', 'rules':['IP-SUB.*']},
            'CP-QUE'        : {'dir':'r', 'rules':['IP-SUB.*']},    #question
#            'CP-QUE=1'      : {'dir':'r', 'rules':['IP-SUB.*']},
#            'CP-QUE=2'      : {'dir':'r', 'rules':['IP-SUB.*']},
#            'CP-QUE-1'      : {'dir':'r', 'rules':['IP-SUB.*']},
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
#            'CP-QUE-PRN=1'  : {'dir':'r', 'rules':['IP-SUB.*']},
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
#            'CP-EXL=1'      : {'dir':'r', 'rules':['IP-INF']},
#            'CP-EOP-1'      : {'dir':'r', 'rules':['IP-INF']},
#            'CP-EOP-2'      : {'dir':'r', 'rules':['IP-INF']},
            'CP-TMC'        : {'dir':'r', 'rules':['IP-INF.*']},  #tough-movement
            'CP-TMC-SPE'    : {'dir':'r', 'rules':['IP-INF.*']},
            'CP-TMP'        : {'dir':'r', 'rules':['IP-INF.*']},
#            'CP-TMC-3'      : {'dir':'r', 'rules':['IP-INF']},
            'NP'            : {'dir':'r', 'rules':['CP-FRL', 'N-.', 'NS-.', 'NPR-.', 'PRO-.', 'NP.*', 'Q.*', 'MAN-.', 'OTHER-.']},
#            'NP=1'            : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'PRO-.', 'NP.*', 'Q.*', 'MAN-.', 'OTHER-.', 'CP-FRL']},
#            'NP-1'          : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NP.*', 'PRO-.', 'Q.*', 'MAN-.', 'OTHER-.']},
#            'NP-2'          : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NP.*', 'PRO-.', 'Q.*', 'MAN-.', 'OTHER-.']},
#            'NP-4'          : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NP.*', 'PRO-.', 'Q.*', 'MAN-.', 'OTHER-.']},
            'NP-ADV'        : {'dir':'r', 'rules':['NP.*', 'N-.', 'PRO-.', 'ADJ.*', 'Q.*', 'CP.*']},
            'NP-ADV-LFD'    : {'dir':'r', 'rules':['NP.*', 'N-.', 'PRO-.', 'ADJ.*', 'Q.*', 'CP.*']},
            'NP-ADV-RSP'    : {'dir':'r', 'rules':['NP.*', 'N-.', 'PRO-.', 'ADJ.*', 'Q.*', 'CP.*']},
            'NP-CMP'        : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'MAN-.', 'OTHER-.']},
            'NP-PRN'        : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'PRO-.', 'MAN-.', 'OTHER-.']},   #viðurlag, appositive
#            'NP-PRN-1'      : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'PRO-.', 'MAN-.', 'OTHER-.']},
#            'NP-PRN-3'      : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'PRO-.', 'MAN-.', 'OTHER-.']},
            'NP-PRN-ELAB'   : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'PRO-.', 'MAN-.', 'OTHER-.']},
#            'NP-PRN-LLL'    : {'dir':'r', 'rules':['N-.', 'NS.*', 'NP.*', 'OTHER-.']},
            'NP-PRN-REP'    : {'dir':'r', 'rules':['N-.', 'NS.*', 'NP.*', 'OTHER-.']},
#            'NP-PRN-TTT'    : {'dir':'r', 'rules':['N-.', 'NS.*', 'NP.*', 'OTHER-.']},
#            'NP-PRN-ELAB-1' : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'PRO-.', 'MAN-.', 'OTHER-.']},
            'NP-RSP'        : {'dir':'r', 'rules':['N-.', 'NS.*', 'NP.*', 'OTHER-.']},
            'NP-SBJ'        : {'dir':'r', 'rules':['N-N', 'N-.', 'NS-N', 'NPR-N', 'NPRS-N', 'PRO-.', 'ADJ-N', 'MAN-N', 'OTHER-.']},
            'NP-SBJ-LFD'    : {'dir':'r', 'rules':['N-N', 'N-.', 'NS-N', 'NPR-N', 'NPRS-N', 'PRO-.', 'ADJ-N', 'MAN-N', 'OTHER-.']},
            'NP-SBJ-RSP'    : {'dir':'r', 'rules':['N-N', 'NS-N', 'NPR-N', 'NPRS-N', 'PRO-.', 'ADJ-N', 'MAN-N', 'OTHER-.']},
#            'NP-SBJ-TTT'    : {'dir':'r', 'rules':['N-N', 'N-.', 'NS-N', 'NPR-N', 'NPRS-N', 'PRO-.', 'ADJ-N', 'MAN-N', 'OTHER-.']},
#            'NP-SBJ-ZZZ-2SBJ': {'dir':'r', 'rules':['N-N', 'N-.', 'NS-N', 'NPR-N', 'NPRS-N', 'PRO-.', 'ADJ-N', 'MAN-N', 'OTHER-.']},
            'NP-SMC'        : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'PRO-.', 'NP.*', 'Q.*', 'MAN-.', 'OTHER-.', 'CP-FRL']},
            'NP-SPE'            : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'PRO-.', 'NP.*', 'Q.*', 'MAN-.', 'OTHER-.', 'CP-FRL']},
#            'NP-SBJ-1'      : {'dir':'r', 'rules':['N-N', 'NS-N', 'NPR-N', 'PRO-.', 'ADJ-N', 'MAN-N', 'OTHER-.']},
#            'NP-SBJ-2'      : {'dir':'r', 'rules':['N-N', 'NS-N', 'NPR-N', 'PRO-.', 'ADJ-N', 'MAN-N', 'OTHER-.']},
#            'NP-SBJ-4'      : {'dir':'r', 'rules':['N-N', 'NS-N', 'NPR-N', 'PRO-.', 'ADJ-N', 'MAN-N', 'OTHER-.']},
            'NP-OB1'        : {'dir':'r', 'rules':['N-.', 'NPR-A', 'NS-.', 'NP', 'NP-.+' 'ONE+Q-A', 'MAN-A', 'OTHER-.', 'PRO-.']},
#            'NP-OB1=1'      : {'dir':'r', 'rules':['N-.', 'NPR-A', 'NS-.', 'NP', 'ONE+Q-A', 'MAN-A', 'OTHER-.', 'PRO-.']},
#            'NP-OB1=2'      : {'dir':'r', 'rules':['N-.', 'NPR-A', 'NS-.', 'NP', 'ONE+Q-A', 'MAN-A', 'OTHER-.', 'PRO-.']},
#            'NP-OB1=3'      : {'dir':'r', 'rules':['N-.', 'NPR-A', 'NS-.', 'NP', 'ONE+Q-A', 'MAN-A', 'OTHER-.', 'PRO-.']},
#            'NP-OB1=5'      : {'dir':'r', 'rules':['N-.', 'NPR-A', 'NS-.', 'NP', 'ONE+Q-A', 'MAN-A', 'OTHER-.', 'PRO-.']},
            'NP-OB1-LFD'    : {'dir':'r', 'rules':['N-.', 'NPR-A', 'NS-.', 'NP', 'ONE+Q-A', 'MAN-A', 'OTHER-.', 'PRO-.']},
            'NP-OB1-RSP'    : {'dir':'r', 'rules':['N-.', 'NPR-A', 'NS-.', 'NP', 'ONE+Q-A', 'MAN-A', 'OTHER-.', 'PRO-.']},
#            'NP-OB1-TTT'    : {'dir':'r', 'rules':['N-.', 'NPR-A', 'NS-.', 'NP', 'ONE+Q-A', 'MAN-A', 'OTHER-.', 'PRO-.']},
            'NP-OB2'        : {'dir':'r', 'rules':['NP.*', 'PRO-.', 'N-D', 'NS-D', 'NPR-.', 'CP-FRL', 'MAN-.', 'OTHER-.']},    #MEIRA?
            'NP-OB2-RSP'    : {'dir':'r', 'rules':['NP.*', 'PRO-.', 'N-D', 'NS-D', 'NPR-.', 'CP-FRL', 'MAN-.', 'OTHER-.']},
#            'NP-OB2-TTT'    : {'dir':'r', 'rules':['NP.*', 'PRO-.', 'N-D', 'NS-D', 'NPR-.', 'CP-FRL', 'MAN-.', 'OTHER-.']},
            'NP-OB3'        : {'dir':'r', 'rules':['PRO-D', 'N-D', 'NS-D', 'NPR-D', 'MAN-.', 'OTHER-.']},
            'NP-PRD'        : {'dir':'r', 'rules':['N-.', 'NS.*', 'NP.*', 'OTHER-.']},     #sagnfylling copulu
#            'NP-PRD-TTT'    : {'dir':'r', 'rules':['N-.', 'NS.*', 'NP.*', 'OTHER-.']},
            'NP-SPR'        : {'dir':'r', 'rules':['N-.', 'NS-.']},   #secondary predicate
            'NP-POS'        : {'dir':'r', 'rules':['N-.', 'NPR-.', 'PRO-.', 'NP-.+', 'MAN-.', 'OTHER-.']},
            'NP-POS-RSP'    : {'dir':'r', 'rules':['N-.', 'NPR-.', 'PRO-.', 'NP-.+', 'MAN-.', 'OTHER-.']},
#            'NP-POS-TTT'    : {'dir':'r', 'rules':['N-.', 'NPR-.', 'PRO-.', 'NP-.+', 'MAN-.', 'OTHER-.']},
            'NP-COM'        : {'dir':'r', 'rules':['N.*', 'NP.*', 'OTHER-.']},  #fylliliður N sem er ekki í ef.
            'NP-ADT'        : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'MAN-.', 'OTHER-.']},    #clause-level dative adjuncts, e.g. instrumental datives
            'NP-TMP'        : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'ADJ-.', 'NUM-.', 'OTHER-.']},    #temporal NP
            'NP-TMP-LFD'    : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'ADJ-.', 'NUM-.', 'OTHER-.']},
            'NP-TMP-RSP'    : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'ADJ-.', 'NUM-.', 'OTHER-.']},
#            'NP-TTT'        : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'PRO-.', 'NP.*', 'Q.*', 'MAN-.', 'OTHER-.', 'CP-FRL']},
            'NP-MSR'        : {'dir':'r', 'rules':['NS-.', 'N-.', 'Q-.', 'QS-.', 'QR-.', 'OTHER-.', 'ADV']},
            'NP-MSR-LFD'    : {'dir':'r', 'rules':['NS-.', 'N-.', 'Q-.', 'QS-.', 'QR-.', 'OTHER-.', 'ADV']},
            'NP-MSR-RSP'    : {'dir':'r', 'rules':['NS-.', 'N-.', 'Q-.', 'QS-.', 'QR-.', 'OTHER-.', 'ADV']},
#            'NP-MSR-TTT'    : {'dir':'r', 'rules':['NS-.', 'N-.', 'Q-.', 'QS-.', 'QR-.', 'OTHER-.', 'ADV']},
            'NP-NUM'        : {'dir':'r', 'rules':[]},
            'NP-VOC'        : {'dir':'r', 'rules':['N-N', 'NS-N', 'MAN-N', 'OTHER-.']},
            'NP-VOC-LFD'    : {'dir':'r', 'rules':['N-N', 'NS-N', 'MAN-N', 'OTHER-.']},
            'NP-DIR'        : {'dir':'r', 'rules':['N-.', 'NP.*']},
            'NP-DIR-LFD'    : {'dir':'r', 'rules':['N-.', 'NP.*']},
            'NP-DIR-PRN'    : {'dir':'r', 'rules':['N-.', 'NP.*']},
            'ADJP'          : {'dir':'r', 'rules':['ADJ-.', 'ADJR-.', 'ADJS-.', 'ADVR', 'ONE', 'ONES', 'CP-TMP']},
#            'ADJP-1'        : {'dir':'r', 'rules':['ADJ.*', 'ADJR.*', 'ADJS.*', 'ADVR', 'ONE', 'ONES']},
            'ADJP-SPR'      : {'dir':'r', 'rules':['ADJ-.', 'ADJS-N']},     #SPR = secondary predicate
            'ADJP-SPR-LFD'  : {'dir':'r', 'rules':[]},
#            'ADJP-SPR-TTT'  : {'dir':'r', 'rules':[]},
            'ADJP-DIR'      : {'dir':'r', 'rules':[]},
            'ADJP-LFD'      : {'dir':'r', 'rules':[]},
            'ADJP-LOC'      : {'dir':'r', 'rules':[]},  #eitt dæmi um ADJP-OC
            'ADJP-PRN'      : {'dir':'r', 'rules':[]},
            'ADJP-PRN-ELAB' : {'dir':'r', 'rules':[]},
            'ADJP-RSP'      : {'dir':'r', 'rules':[]},
            'ADJP-TMP'      : {'dir':'r', 'rules':[]},
#            'ADJP-TTT'      : {'dir':'r', 'rules':[]},
            'ADJX'          : {'dir':'r', 'rules':[]},
            'WADJP'         : {'dir':'r', 'rules':[]},
            'WADJX'         : {'dir':'r', 'rules':[]},
            'PP'            : {'dir':'r', 'rules':['CP-FRL', 'NP', 'NP-.+', 'CP-ADV', 'IP-SMC', 'ADVP', 'ADJP', 'CP-.*', 'IP-INF.*', 'P']},
#            'PP-1'          : {'dir':'r', 'rules':['NP', 'NP-.+', 'CP-ADV', 'IP-SMC', 'ADVP', 'ADJP', 'CP-.*', 'IP-INF.*', 'P']},
#            'PP-2'          : {'dir':'r', 'rules':['NP', 'NP-.+', 'CP-ADV', 'IP-SMC', 'ADVP', 'ADJP', 'CP-.*', 'IP-INF.*', 'P']},
            'PP-BY'         : {'dir':'r', 'rules':['NP', 'NP-.+', 'CP-ADV', 'IP-SMC', 'ADVP', 'ADJP', 'CP-.*', 'IP-INF.*', 'P']},
            'PP-BY-RSP'     : {'dir':'r', 'rules':['NP', 'NP-.+', 'CP-ADV', 'IP-SMC', 'ADVP', 'ADJP', 'CP-.*', 'IP-INF.*', 'P']},
            'PP-PRN'        : {'dir':'r', 'rules':['CP-ADV', 'NP', 'P']},
            'PP-PRN-ELAB'   : {'dir':'r', 'rules':['CP-ADV', 'NP', 'P']},
            'PP-RSP'        : {'dir':'r', 'rules':['NP', 'NP-.+', 'CP-ADV', 'IP-SMC', 'ADVP', 'ADJP', 'CP-.*', 'IP-INF.*', 'P']},
            'PP-SBJ'        : {'dir':'r', 'rules':['NP', 'NP-.+', 'CP-ADV', 'IP-SMC', 'ADVP', 'ADJP', 'CP-.*', 'IP-INF.*', 'P']},
#            'PP-TTT'        : {'dir':'r', 'rules':['NP', 'NP-.+', 'CP-ADV', 'IP-SMC', 'ADVP', 'ADJP', 'CP-.*', 'IP-INF.*', 'P']},
#            'PP-PRN-1'      : {'dir':'r', 'rules':['CP-ADV', 'NP', 'P']},
#            'PP-PRN-2'      : {'dir':'r', 'rules':['CP-ADV', 'NP', 'P']},
            'PP-LFD'        : {'dir':'r', 'rules':['CP-ADV.*', 'CP-THT', 'NP', 'PP']},    #left dislocation
            'ADVP'          : {'dir':'r', 'rules':['ADV', 'ADVR', 'ADVS', 'WADV']},
            'ADVP-DIR'      : {'dir':'r', 'rules':['ADV', 'WADV']},
            'ADVP-DIR-LFD'  : {'dir':'r', 'rules':['ADV', 'WADV']},
            'ADVP-DIR-RSP'  : {'dir':'r', 'rules':['ADV', 'WADV']},
            'ADVP-LOC'      : {'dir':'r', 'rules':['ADV', 'WADV']},
            'ADVP-LOC-LFD'  : {'dir':'r', 'rules':['ADV', 'WADV']},
            'ADVP-LOC-RSP'  : {'dir':'r', 'rules':['ADV', 'WADV']},
#            'ADVP-LOC-TTT'  : {'dir':'r', 'rules':['ADV', 'WADV']},
            'ADVP-TMP'      : {'dir':'r', 'rules':['ADV', 'WADV']},
            'ADVP-TMP-LFD'  : {'dir':'r', 'rules':['ADV', 'WADV']},
            'ADVP-TMP-PRN'  : {'dir':'r', 'rules':['ADV', 'WADV']},
            'ADVP-TMP-RSP'  : {'dir':'r', 'rules':['ADV', 'WADV']},
#            'ADVP-TMP-TTT'  : {'dir':'r', 'rules':['ADV', 'WADV']},
            'ADVP-RSP'      : {'dir':'r', 'rules':['ADV', 'WADV']},
            'ADVP-RSP-RSP'  : {'dir':'r', 'rules':['ADV', 'WADV']},
            'ADVP-TMP-RSP'  : {'dir':'r', 'rules':['ADV', 'WADV']},
            'ADVP-ELAB'     : {'dir':'r', 'rules':['ADV', 'WADV']},
            'ADVP-LFD'      : {'dir':'r', 'rules':['ADV', 'WADV']},
            'ADVP-MSR'      : {'dir':'r', 'rules':['ADV', 'WADV']},
            'ADVP-PRN'      : {'dir':'r', 'rules':['ADV', 'WADV']},
            'ADVP-PRN-ELAB' : {'dir':'r', 'rules':['ADV', 'WADV']},
            'ADVP-PRN-REP'  : {'dir':'r', 'rules':['ADV', 'WADV']},
            'ADVP-RMP'      : {'dir':'r', 'rules':['ADV', 'WADV']},
#            'ADVP-TTT'      : {'dir':'r', 'rules':['ADV', 'WADV']},
            'ADVX'          : {'dir':'r', 'rules':['ADV', 'WADV']},
            'WADVP'         : {'dir':'r', 'rules':['WADV']},
            'WADVP-LOC'     : {'dir':'r', 'rules':['WADV']},
            'WADVP-NaN'     : {'dir':'r', 'rules':['WADV']},
#            'WADVP-1'       : {'dir':'r', 'rules':['WADV']},
#            'WADVP-2'       : {'dir':'r', 'rules':['WADV']},
#            'WADVP-3'       : {'dir':'r', 'rules':['WADV']},
            'CONJP'         : {'dir':'r', 'rules':['NP.*', 'NX', 'NUM-.', 'IP-SUB', 'IP-MAT=1', 'IP-INF', 'IP-.+', 'CP-QUE', 'PP', 'CONJ']},
            'CONJP-PP'      : {'dir':'r', 'rules':[]},
            'CONJP-PRN'     : {'dir':'r', 'rules':[]},
#            'CONJP-1'       : {'dir':'r', 'rules':['NP.*', 'NX', 'NUM-.', 'IP-SUB', 'IP-MAT=1', 'IP-INF', 'IP-.+', 'CP-QUE', 'PP', 'CONJ']},
#            'CONJP-4'       : {'dir':'r', 'rules':['NP.*', 'NX', 'NUM-.', 'IP-SUB', 'IP-MAT=1', 'IP-INF', 'IP-.+', 'CP-QUE', 'PP', 'CONJ']},
            'WNP'           : {'dir':'r', 'rules':['WPRO-.', 'PRO-.', 'N-.', 'Q-.', 'WQ-.', 'WD-.']}, #MEIRA?
            'WNP-COM'       : {'dir':'r', 'rules':['WPRO-.', 'PRO-.', 'N-.', 'Q-.', 'WQ-.', 'WD-.']},
            'WNP-MSR'       : {'dir':'r', 'rules':['WPRO-.', 'PRO-.', 'N-.', 'Q-.', 'WQ-.', 'WD-.']},
#            'WNP-NaN'       : {'dir':'r', 'rules':['WPRO-.', 'PRO-.', 'N-.', 'Q-.']},    #kemur einu sinni fyrir, bara spor
            'WNP-POS'       : {'dir':'r', 'rules':['WPRO-.', 'PRO-.', 'N-.', 'Q-.', 'WQ-.', 'WD-.']},
            'WNP-PRN-ELAB'  : {'dir':'r', 'rules':['WPRO-.', 'PRO-.', 'N-.', 'Q-.', 'WQ-.', 'WD-.']},
#            'WNP-1'         : {'dir':'r', 'rules':['WPRO-.', 'PRO-.', 'N-.']},
#            'WNP-2'         : {'dir':'r', 'rules':['WPRO-.', 'PRO-.', 'N-.']},
#            'WNP-3'         : {'dir':'r', 'rules':['WPRO-.', 'PRO-.', 'N-.']},
#            'WNP-4'         : {'dir':'r', 'rules':['WPRO-.', 'PRO-.', 'N-.']},
            'WPP'           : {'dir':'r', 'rules':['WNP.*', 'WADVP.*', 'NP.*']},
#            'WPP-1'         : {'dir':'r', 'rules':['WNP', 'NP']},
            'NX'            : {'dir':'r', 'rules':['N.*']},
            'FRAG-LFD'      : {'dir':'r', 'rules':['CP.*', 'IP.*', 'NP.*', 'PP']},
            'FRAG'          : {'dir':'r', 'rules':['CP.*', 'IP.*', 'NP.*', 'PP']},
#            'FRAG-TTT'      : {'dir':'r', 'rules':['IP-SMC', 'NP']},
            'QP'            : {'dir':'r', 'rules':['Q-.', 'QS-.', 'QR-.']},
            'WQP'           : {'dir':'r', 'rules':['Q-.', 'QS-.', 'QR-.']},
            'QTP'           : {'dir':'r', 'rules':['IP.*', 'NP.*']},      #quote phrase
            'QTP-SBJ'       : {'dir':'r', 'rules':['IP.*', 'NP.*']},
            'REP'           : {'dir':'r', 'rules':['NP', 'PP', 'ADJP', 'IP.*', 'VB.*']},      #repetition
#            'REP-TTT'       : {'dir':'r', 'rules':[]},
            'RRC'           : {'dir':'r', 'rules':['V.+', 'ADJP', 'RRC.*', 'PP']},      #reduced relative clause   
#            'RRC=2'         : {'dir':'r', 'rules':[]}, 
#            'RRC=4'         : {'dir':'r', 'rules':[]},
            'RRC-PRN'       : {'dir':'r', 'rules':['V.+', 'ADJP', 'RRC.*', 'PP']}, 
#            'RRC-PRN=2'     : {'dir':'r', 'rules':[]}, 
            'RRC-SPE'       : {'dir':'r', 'rules':['V.+', 'ADJP', 'RRC.*', 'PP']},
            'NUMP'          : {'dir':'r', 'rules':['NUM-.']},
            'INTJP'         : {'dir':'r', 'rules':['INTJ']},
            'VP'            : {'dir':'r', 'rules':['V.+', 'BE.']}, 
            'XP'            : {'dir':'r', 'rules':['XXX']}
            }

relation_NP = {
      'ADV': 'obl?',
      'ADV-LFD': 'obl?',
      'ADV-RSP': 'obl?',
      'CMP': 'obl?',
      'PRN': 'appos',     #viðurlag, appositive
      'PRN-ELAB': 'appos',
      'PRN-REP': 'appos',
      'RSP': 'obl?',
      'SBJ': 'nsubj',
      'SBJ-LFD': 'nsubj',
      'SBJ-RSP': 'nsubj',     
      'SMC': 'nsubj?',
      'SPE': 'nsubj?',
      'OB1': 'obj',
      'OB1-LFD': 'obj',
      'OB1-RSP': 'obj',
      'OB2': 'iobj',
      'OB2-RSP': 'iobj',
      'OB3': 'iobj',
      'PRD': 'acl?',    #sagnfylling, predicate
      'SPR': 'xcomp?',
      'POS': 'nmod:poss',      #Örvar: 'POS': 'case'
      'POS-RSP': 'nmod:poss',
      'COM': 'nmod:poss',
      'ADT': 'obl',    #ATH. rétt?
      'TMP': 'advmod',  #ATH. rétt?
      'TMP-LFD': 'advmod',
      'TMP-RSP': 'advmod',
      'NUM': 'nummod',
      'MSR': 'amod',   #measure phrase
      'VOC': 'vocative',
      'VOC-LFD': 'vocative',
      'DIR': 'obl',
      'DIR-LFD': 'obl',
      'DIR-PRN': 'obl'
}

relation_IP = {
      'INF': 'ccomp', #?, xcomp ef ekkert frumlag
#     'INF=3': '',
      'INF-ABS': 'ccomp', #TODO: xcomp ef ekkert frumlag
      'INF-ABS-PRN': 'ccomp', #TODO: xcomp ef ekkert frumlag
      'INF-PRP': 'advcl',
      'INF-PRP-PRN': 'advcl',
      'INF-PRP-PRN-SPE': 'advcl',
      'INF-PRP-SPE': 'advcl',
      'INF-PRP-SPE-PRN': 'advcl',
      'INF-SPE': 'xcomp',  #ATH. réttur merkimiði?
      'INF-SPE-ADT': '?',      # ADT = clause-level dative adjunct
      'INF-SPE-DEG': '?',
      'INF-SPE-LFD': 'xcomp?',
      'INF-SPE-PRN': '?',
      'INF-SPE-PRN-ELAB': '?',    #sama merki og INF-SPE-PRN
      'INF-SPE-PRP': 'advcl',
      'INF-SPE-PRP-PRN': '?',
      'INF-SPE-SBJ': 'ccomp?',
      'INF-PRN': 'xcomp', #ADVCL?
      'INF-PRN-ELAB': 'xcomp',
      'INF-PRN-PRP': 'advcl',     #notað í til þess að
      'INF-PRN-SPE': 'xcomp',
      'INF-RSP': 'ccomp',      # RSP = resumptive
      'INF-SBJ': '?',
      'INF-SBJ-SPE': '?',
      'INF-DEG': '?',
      'INF-DEG-PRN': '?',
      'INF-DEG-SPE': '?',
      'INF-LFD': 'ccomp',     #TODO: xcomp ef ekkert frumlag
      'INF-PRD': 'advcl?',
      'INF-ADT': 'advcl?',
      'INF-ADT-SPE': 'advcl?',
      'INF-ADT-SPE-LFD': 'advcl?',
      'INF-ADT-LFD': 'advcl?',
      'INF-ADT-PRN': 'advcl?',
      'MAT': '',        #þarf ekki að hafa merkimiða því sögnin er alltaf rót?
#      'MAT=1': '',
      'MAT-DIR': '',    #sama og MAT    
      'MAT-LFD': '',    #sama og MAT
      'MAT-OB1': 'advcl',     #kemur einu sinni fyrir, haus á eftir nær(þegar), jonsteingrims
      'MAT-PRN': 'ccomp?',
      'MAT-PRN-ELAB': 'ccomp?',
      'MAT-PRN-LFD': 'ccomp?',
      'MAT-PRN-SPE': 'ccomp?',
      'MAT-SBJ': '',
      'MAT-SPE': '',
      'MAT-SPE-PRN': 'ccomp?',
      'MAT-SPE-PRN-ELAB': 'ccomp?',
      'MAT-SPE-PRN-LFD': 'ccomp?',
      'MAT-SPE-SBJ': '',
      'MAT-SUB-SPE': '',
      'MAT-SMC': '',    #sama og MAT, kemur einu sinni fyrir og hausinn er rót
      'SUB': 'ATH',
      'SUB-INF': 'xcomp',
      'SUB-LFD': '',
      'SUB-PRN': 'ccomp/xcomp?',
      'SUB-PRN-ELAB': 'ccomp/xcomp?',
      'SUB-REP': '?',    # REP = repetition
#      'SUB-PRN=4': 'aux:pass',     #sérstakt dæmi
      'SUB-SPE': '',
      'SUB-SPE-PRN': 'ccomp/xcomp?',
      'SUB-SPE-PRN-ELAB': 'ccomp/xcomp?',       # ELAB = elaborations
      'IMP': 'ccomp',
      'IMP-PRN': 'ccomp',
      'IMP-SPE': 'ccomp',
      'IMP-SPE-PRN': 'ccomp',
      'IMP-SPE-SBJ': 'ccomp',
      'SMC': 'acl?',
      'SMC-SBJ': 'acl?',
      'SMC-SPE': 'acl?',
      'PPL': 'advcl/acl?',  #?
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
      'THT': 'ccomp',
      'THT-SBJ': 'ccomp',
      'THT-SBJ-SPE': 'ccomp',
      'THT-SPE': 'ccomp',
      'THT-SPE-PRN': 'ccomp',
      'THT-SPE-SBJ': 'ccomp',
      'THT-PRN': 'ccomp',
      'THT-PRN-NaN': 'ccomp',
      'THT-PRN-SPE': 'ccomp',
      'THT-LFD': 'ccomp',
      'THT-RSP': 'ccomp',     #resumptive element
      'CAR': 'acl:relcl',
      'CAR-SPE': 'acl:relcl',
      'CLF': 'acl:relcl',
      'CLF-SPE': 'acl:relcl',
      'CMP': 'advcl?',      #ATH. rétt?
      'CMP-LFD': 'advcl?',
      'CMP-SPE': 'advcl?',
      'DEG': 'ccomp',      #ATH. rétt?  
      'DEG-SPE': 'ccomp',
      'FRL': 'acl:relcl?',    #ccomp?, free relative 
      'FRL-SPE': 'acl:relcl?',
      'REL': 'acl:relcl',
      'REL-SPE': 'acl:relcl',
      'REL-SPE-PRN': 'acl:relcl',  
      'QUE': 'ccomp',
      'QUE-SPE': 'ccomp',
      'QUE-SPE-LFD': 'ccomp',
      'QUE-SPE-LFD-PRN': 'ccomp',
      'QUE-SPE-LFD-SBJ': 'ccomp',
      'QUE-ADV': 'advcl?',
      'QUE-ADV-LFD': 'advcl?',
      'QUE-ADV-SPE': 'advcl?',
      'QUE-ADV-SPE-LFD': 'advcl?',
      'QUE-LFD': 'ccomp',
      'QUE-PRN': 'ccomp?',
      'QUE-PRN-ELAB': 'ccomp?',
      'QUE-PRN-SPE': 'ccomp?',
      'QUE-SBJ': 'ccomp',
      'ADV': 'advcl',
      'ADV-LFD': 'advcl',
      'ADV-LFD-SPE': 'advcl',
      'ADV-PRN': 'advcl',
      'ADV-RSP': 'advcl',
      'ADV-SPE': 'advcl',
      'ADV-SPE-LFD': 'advcl',
      'ADV-SPE-PRN': 'advcl',
      'EOP': 'xcomp',
      'EOP-SPE': 'xcomp',
      'EOP-SPE-PRN': 'xcomp',
      'EXL': 'ccomp',        #exclamative, same parse as QUE
      'EXL-SPE': 'ccomp',
      'TMC': 'xcomp?',        #tough movement
      'TMC-SPE': 'xcomp?',
      'TMP': '?'        #ekki frl. í setningu, xcomp, acl eða advcl?
}
