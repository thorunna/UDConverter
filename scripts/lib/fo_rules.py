

cconj = {'og', 'men', 'tí', 'ella', 'bæði', 'annaðhvørt', 'hvørki'}

UD_map = {
    'ADJ' : 'ADJ',  # Adjectives tagged as ADJ
    'ADV' : 'ADV',  # Adverbs tagged as ADV
    'ALS' : 'ADV',  #ALSO
    'BAG' : 'VERB', #verandi
    'BE' : 'VERB',  #vera, verður cop í relations?
    'BEI' : 'VERB', # boðháttur
    'BEN' : 'VERB',
    'BED' : 'VERB',
    'BEP' : 'VERB',
    'C' : 'SCONJ',  # complimentizer tagged as SCONJ (subordinate conjunction)
    'D' : 'DET',    # generalized determiners tagged as DET (determiner)
    'DAN' : 'VERB', #gjörd
    'DO' : 'VERB',  #'gera', do, tagged as verb
    'DOD' : 'VERB',
    'DOI' : 'VERB',
    'DON' : 'VERB',
    'DOP' : 'VERB',
    'ES' : 'PRON',  #expletive tagged as PRON
    'FOR' : 'P', #P?
    'FP' : 'PART',  #focus particles marked as PART
    'FW' : 'X',
    'HV' : 'AUX',   # getur líka verið aðalsögn #'have' tagged as auxiliary verb
    'HVI' : 'VERB',
    'HVN' : 'VERB',
    'HVD' : 'VERB',
    'HVP' : 'VERB',
    'INT' : 'INTJ',    #interjection
    'MD' : 'AUX',   #modal verbs tagged as auxiliary
    'MDD' : 'AUX',
    'MDP' : 'AUX',
    'N' : 'NOUN',   # generalized nouns tagged as NOUN
    'NS' : 'NOUN',
    'NEG' : 'ADV',
    'NPR' : 'PROPN',    # proper nouns tagged as PROPN
    'NUM' : 'NUM',
    'ONE' : 'DET',
    'OTH' : 'PRON',
    'P' : 'ADP',    # generalized prepositions tagged as ADP
    'PRO' : 'PRON',
    'Q' : 'DET',    # quantifiers tagged as DET - upphaflega varpað yfir í ADJ
    'QR' : 'DET',
    'RAG' : 'VERB', # verðandi 
    'RD' : 'VERB',  #'verða', become, tagged as verb
    'RDP' : 'VERB',
    'RDI' : 'VERB',
    'RDN' : 'VERB',
    'RDD' : 'VERB',
    'RP' : 'ADP',   # specifiers of P/complements of P - Ath. flokka sem eitthvað annað?
    'RPX' : 'PART', # agnir markaðar sem PART
    'SUC' : 'PRON', #SUCH
    'TO' : 'PART',  # Infinitive marker tagged as PART (particle)
    'VAG' : 'VERB',
    'VAN' : 'VERB',
    'VB' : 'VERB',
    'VBD' : 'VERB',
    'VBN' : 'VERB',
    'VBI' : 'VERB',
    'VBP' : 'VERB',
    'WAD' : 'ADV', #TODO: ath. betur - bara spor? - WADV
    'WD' : 'DET',   # WH-determiner tagged as DET (determiner)
    'WPR' : 'PRON',    #wh-pronouns - WPRO
    'WQ' : 'SCONJ'
}


feats = {
    'Case' : {
        'N' : 'Nom',
        'A' : 'Acc',
        'D' : 'Dat',
        'G' : 'Gen'
    },
    
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
            'NPR' : 'Sing',    # noun singular number
            'NPRS' : 'Plur'
        },
        'Definite' : { # TODO: remove def from dict
            '$' : 'Def',
            '' : 'Ind'
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
            'I' : 'Ind',    #indicative (IcePaHC POS-tag)
            'S' : 'Sub',    #subjunctive (IcePaHC POS-tag)
        },
        'Tense' : {
            'P' : 'Pres',
            'D' : 'Past'
        },
        'VerbForm' : {
            '' : 'Fin',     #finite verb
            'inf' : 'Inf',     #infinitive verb
            'N' : 'Part',     #participle
            'G' : 'Part'
        }
    }
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
            'IP-INF-SBJ'    : {'dir':'r', 'rules':['VB', 'IP-INF', '.AN']},
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
            'IP-SUB'        : {'dir':'r', 'rules':['VP', 'VB', 'VB.*', 'DO.*', 'RD.*', 'DAN', 'VAN', 'RAN', 'HAN', 'BAN', 'VAG', 'RAG', 'HAG', 'BAG', 'RDN', 'BEN', 'HVN', 'HV.*', 'MD.*', 'IP-INF.*', 'ADJP', 'NP-PRD', 'NP.*', 'RD.*', 'ADVP', 'IP-SUB']},
            'IP-SUB-INF'    : {'dir':'r', 'rules':['VB']},
            'IP-SUB-LFD'    : {'dir':'r', 'rules':['VP', 'VB', 'VB.*', 'DO.*', 'DAN', 'VAN', 'RAN', 'HAN', 'BAN', 'RDN', 'BEN', 'HV.*', 'IP-INF.*', 'ADJP', 'NP-PRD', 'RD.*', 'NP', 'ADVP', 'IP-SUB', 'HVN']},
            'IP-SUB-PRN'    : {'dir':'r', 'rules':['VB.*', 'VAN']},
            'IP-SUB-PRN-ELAB': {'dir':'r', 'rules':['VB.*', 'VAN']},
            'IP-SUB-PRN=XXX': {'dir':'r', 'rules':['VB.*', 'VAN']},
            'IP-SUB-REP'    : {'dir':'r', 'rules':['VP', 'VB', 'VB.*', 'DO.*', 'RD.*', 'DAN', 'VAN', 'RAN', 'HAN', 'BAN', 'RDN', 'BEN', 'HVN', 'HV.*', 'MD.*', 'IP-INF.*', 'NP.*', 'ADJP', 'NP-PRD', 'RD.*', 'ADVP', 'IP-SUB']},
            'IP-SUB-SPE'    : {'dir':'r', 'rules':['VB.*', 'HV.*', '.*AG', 'IP-SUB-SPE', 'DO.*',]},
            'IP-SUB-SPE-PRN': {'dir':'r', 'rules':['VB.*', 'HV.*']},
            'IP-SUB-SPE-PRN-ELAB': {'dir':'r', 'rules':['VB.*', 'HV.*']},
            'IP-IMP'        : {'dir':'r', 'rules':['VB.', 'HV.']},    #imperative
            'IP-IMP-PRN'    : {'dir':'r', 'rules':['VB.']},
            'IP-IMP-SPE'    : {'dir':'r', 'rules':['VB.']},
            'IP-IMP-SPE-PRN': {'dir':'r', 'rules':['VB.']},
            'IP-IMP-SPE-SBJ': {'dir':'r', 'rules':['VB.']},
            'IP-SMC'        : {'dir':'r', 'rules':['IP-INF-SBJ', 'IP-SMC', 'NP-PRD', 'VAG-.', 'ADJP', 'NP.*']},    #small clause
            'IP-SMC-SBJ'    : {'dir':'r', 'rules':['IP-INF-SBJ', 'IP-SMC', 'NP-PRD', 'VAG-.', 'ADJP', 'NP.*']},
            'IP-SMC-SPE'    : {'dir':'r', 'rules':['IP-INF-SBJ', 'IP-SMC', 'NP-PRD', 'VAG-.', 'ADJP', 'NP.*']},
            'IP-PPL'        : {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG', 'IP-PPL', 'VAN', 'RAN', 'MAN', 'HAN', 'DAN', 'BAN', 'VBN', 'DON', 'MDN', 'HVN', 'RDN', 'BEN']},  #lýsingarháttarsetning
            'IP-PPL-ABS'    : {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG', 'IP-PPL', 'VAN', 'RAN', 'MAN', 'HAN', 'DAN', 'BAN', 'VBN', 'DON', 'MDN', 'HVN', 'RDN', 'BEN']},
            'IP-PPL-ABS-SPE': {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG', 'IP-PPL', 'VAN', 'RAN', 'MAN', 'HAN', 'DAN', 'BAN', 'VBN', 'DON', 'MDN', 'HVN', 'RDN', 'BEN']},
            'IP-PPL-OB1'    : {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG', 'IP-PPL', 'VAN', 'RAN', 'MAN', 'HAN', 'DAN', 'BAN', 'VBN', 'DON', 'MDN', 'HVN', 'RDN', 'BEN']},
            'IP-PPL-OB1-SPE': {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG', 'IP-PPL', 'VAN', 'RAN', 'MAN', 'HAN', 'DAN', 'BAN', 'VBN', 'DON', 'MDN', 'HVN', 'RDN', 'BEN']},
            'IP-PPL-OB2'    : {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG', 'IP-PPL', 'VAN', 'RAN', 'MAN', 'HAN', 'DAN', 'BAN', 'VBN', 'DON', 'MDN', 'HVN', 'RDN', 'BEN']},
            'IP-PPL-PRD'    : {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG', 'IP-PPL', 'VAN', 'RAN', 'MAN', 'HAN', 'DAN', 'BAN', 'VBN', 'DON', 'MDN', 'HVN', 'RDN', 'BEN']},
            'IP-PPL-PRN'    : {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG', 'IP-PPL', 'VAN', 'RAN', 'MAN', 'HAN', 'DAN', 'BAN', 'VBN', 'DON', 'MDN', 'HVN', 'RDN', 'BEN']},
            'IP-PPL-SBJ'    : {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG', 'IP-PPL', 'VAN', 'RAN', 'MAN', 'HAN', 'DAN', 'BAN', 'VBN', 'DON', 'MDN', 'HVN', 'RDN', 'BEN']},
            'IP-PPL-SPE'    : {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG', 'IP-PPL', 'VAN', 'RAN', 'MAN', 'HAN', 'DAN', 'BAN', 'VBN', 'DON', 'MDN', 'HVN', 'RDN', 'BEN']},
            'IP-PPL-SPE-OB1': {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG', 'IP-PPL', 'VAN', 'RAN', 'MAN', 'HAN', 'DAN', 'BAN', 'VBN', 'DON', 'MDN', 'HVN', 'RDN', 'BEN']},
            'IP-PPL-SPE-PRD': {'dir':'r', 'rules':['VAG', 'RAG', 'MAG', 'HAG', 'DAG', 'BAG', 'IP-PPL', 'VAN', 'RAN', 'MAN', 'HAN', 'DAN', 'BAN', 'VBN', 'DON', 'MDN', 'HVN', 'RDN', 'BEN']},
            'IP-ABS'        : {'dir':'r', 'rules':['VP', 'VB', 'VB.*', 'DO.*', 'RD.*', 'DAN', 'VAN', 'RAN', 'HAN', 'BAN', 'RDN', 'BEN', 'HVN', 'HV.*', 'MD.*', 'IP-INF.*', 'NP.*', 'ADJP', 'NP-PRD', 'RD.*', 'ADVP', 'IP-SUB', 'IP-ABS']},
            'IP-ABS-PRN'    : {'dir':'r', 'rules':['VP', 'VB', 'VB.*', 'DO.*', 'RD.*', 'DAN', 'VAN', 'RAN', 'HAN', 'BAN', 'RDN', 'BEN', 'HVN', 'HV.*', 'MD.*', 'IP-INF.*', 'NP.*', 'ADJP', 'NP-PRD', 'RD.*', 'ADVP', 'IP-SUB', 'IP-ABS']},
            'IP-ABS-SBJ'    : {'dir':'r', 'rules':['VP', 'VB', 'VB.*', 'DO.*', 'RD.*', 'DAN', 'VAN', 'RAN', 'HAN', 'BAN', 'RDN', 'BEN', 'HVN', 'HV.*', 'MD.*', 'IP-INF.*', 'NP.*', 'ADJP', 'NP-PRD', 'RD.*', 'ADVP', 'IP-SUB', 'IP-ABS']},
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
            'CP-QUE'        : {'dir':'r', 'rules':['IP-SUB.*', 'WNP', 'WADVP', 'CP-QUE', ]},    #question
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
            'NP'            : {'dir':'r', 'rules':['CP-FRL', 'N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'RRC', 'PRO-.', 'MAN-.', 'NP.*', 'Q.*', 'OTHER-.']},
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
            'NP-SBJ'        : {'dir':'r', 'rules':['N-N', 'N-.', 'NS-N', 'NPR-N', 'NPRS-N', 'MAN.*', 'PRO-.', 'NP.*', 'ADJ-N', 'OTHER-.', 'Q', 'IP-MAT-PRN']},
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
            'ADJP-PRN'      : {'dir':'r', 'rules':['ADJ-.', 'ADJR-.', 'ADJS-.', 'ADVR', 'ADJP', 'ONE', 'ONES', 'CP-TMP', 'Q.*']}, # ADJP bætt við útaf 1902.FOSSAR.NAR-FIC,.542, villa í ADJP-PRN hausavali
            'ADJP-PRN-ELAB' : {'dir':'r', 'rules':['ADJ-.', 'ADJR-.', 'ADJS-.', 'ADVR', 'ONE', 'ONES', 'CP-TMP', 'Q.*']},
            'ADJP-RSP'      : {'dir':'r', 'rules':['ADJ-.', 'ADJR-.', 'ADJS-.', 'ADVR', 'ONE', 'ONES', 'CP-TMP', 'Q.*']},
            'ADJP-TMP'      : {'dir':'r', 'rules':['ADJ-.', 'ADJR-.', 'ADJS-.', 'ADVR', 'ONE', 'ONES', 'CP-TMP', 'Q.*']},
            'ADJX'          : {'dir':'r', 'rules':['ADJ.*']},
            'WADJP'         : {'dir':'r', 'rules':['ADJ.*', 'ADV.*']},
            'WADJX'         : {'dir':'r', 'rules':['ADJ.*', 'ADV.*']},
            'PP'            : {'dir':'r', 'rules':['CP-FRL', 'N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'NP', 'NP-.+', 'FS', 'CP-ADV', 'IP-SMC', 'ADVP', 'ADJP', 'CP-.*', 'IP-INF.*', 'IP-PPL', 'P']},
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
            'CONJP'         : {'dir':'r', 'rules':['IP-MAT-SPE=1', 'N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'NP.*', 'NX', 'NUMP.*', 'NUM-.', 'QTP', 'QP', 'QX', 'IP-SUB', 'IP-MAT.*', 'IP-INF', 'IP-INF.*', 'IP-.+', 'CP-QUE', 'ADJP', 'ADJX', 'ADVP.*', 'PP', 'RRC', 'CONJ']},
            'CONJP-PP'      : {'dir':'r', 'rules':['NP.*', 'NX', 'N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'NUM-.', 'QP', 'QX', 'IP-SUB', 'IP-MAT', 'IP-INF', 'IP-.+', 'CP-QUE', 'ADJP', 'ADJX', 'PP', 'RRC', 'CONJ']},
            'CONJP-PRN'     : {'dir':'r', 'rules':['NP.*', 'NX', 'N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'NUM-.', 'QP', 'QX', 'IP-SUB', 'IP-MAT', 'IP-INF', 'IP-.+', 'CP-QUE', 'ADJP', 'ADJX', 'PP', 'RRC', 'CONJ']},
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
            'QTP'           : {'dir':'r', 'rules':['IP.*', 'NP.*', 'N.*', 'QTP']},      #quote phrase
            'QTP-SBJ'       : {'dir':'r', 'rules':['IP.*', 'NP.*']},
            'REP'           : {'dir':'r', 'rules':['NP', 'PP', 'ADJP', 'IP.*', 'VB.*']},      #repetition
            'RRC'           : {'dir':'r', 'rules':['V.+', 'ADJP', 'RRC.*', 'PP', '.AG']},      #reduced relative clause
            'RRC-PRN'       : {'dir':'r', 'rules':['V.+', 'ADJP', 'RRC.*', 'PP', '.AG']},
            'RRC-SPE'       : {'dir':'r', 'rules':['V.+', 'ADJP', 'RRC.*', 'PP', '.AG']},
            'NUMP'          : {'dir':'r', 'rules':['N-.', 'NS-.', 'NPR-.', 'NPRS-.', 'NUM-.']},
            'INTJP'         : {'dir':'r', 'rules':['INTJ', 'N-.', 'NS-.', 'NPR-.', 'NPRS-.']},
            'VP'            : {'dir':'r', 'rules':['V.+', 'BE.']},
            'XP'            : {'dir':'r', 'rules':['XXX']},
            'FS'            : {'dir':'r', 'rules':['CP-ADV']},
            'META'          : {'dir':'r', 'rules':['NP', 'N.*', 'CODE', 'LATIN']},
            'CODE'          : {'dir':'r', 'rules':['NP']},
            'TRANSLATION'   : {'dir':'r', 'rules':['NP']},
            'LATIN'         : {'dir':'r', 'rules':['CODE']}
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
      # None: '?',
      None: 'dep',
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
      'PPL-ABS': 'acl/advcl',  #?
      'PPL-ABS-SPE': 'acl/advcl',  #?
      'PPL-OB1': 'acl/advcl',  #?
      'PPL-OB1-SPE': 'acl/advcl',  #?
      'PPL-OB2': 'acl/advcl',  #?
      'PPL-PRD': 'acl/advcl',  #?
      'PPL-PRN': 'acl/advcl',  #?
      'PPL-SBJ': 'acl/advcl',  #?
      'PPL-SPE': 'acl/advcl',  #?
      'PPL-SPE-OB1': 'acl/advcl',  #?
      'PPL-SPE-PRD': 'acl/advcl',  #?
      'ABS': 'acl/advcl',        #absolutus
      'ABS-PRN': 'acl/advcl',
      'ABS-SBJ': 'acl/advcl'
}

relation_CP = {
      # None: '?',
      None: 'dep',
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


abbr_tokens = {'o.', 's.', 'frv.', 't.', 't.', 'd.', 'fl.', 't.$', '$d.', 'þ.$',
               '$e.', '$e.$', '$a.$', '$s.', 'a$', '$m$', '$k', 'm.$', '$a.',
               'm.$', '$a.$', '$s.', 't.$', '$d.'}
abbr_map = {
    #abbr : token, lemma, lemma(true)
    'o.' : (r'o\.', 'og', 'og', 'og'),
    's.' : (r's\.', 'svo', 'svo', ''),
    'frv.' : (r'frv\.', 'framvegis', 'framvegis', ''),
    't.' : (r't\.', 'til', 'til', ''),
    't.' : (r't\.', 'til', 't', ''),
    'd.' : (r'd\.', 'dæmis', 'dæmi', ''),
    'fl.' : (r'fl\.', 'fleira', 'margur', ''),
    't.$' : (r't\.\$', 'til', 't', 'til'),
    '$d.' : (r'\$d\.', 'dæmis', 'd', 'dæmi'),
    'þ.$' : (r'þ\.\$', 'það', 'þú', 'þú'),
    '$e.' : (r'\$e\.', 'er', 'vera', ''),
    '$e.$' : (r'\$e\.\$', 'er', 'vera', ''),
    '$a.$' : (r'\$a\.\$', 'að', 'a\.', 'að'),
    '$s.' : (r'\$s\.', 'segja', 's', 'segja'),
    'a$' : (r'a$', 'að', 'að', 'að'),
    '$m$' : (r'\$m$', 'minnsta', 'lítill', ''),
    '$k' : (r'\$k', 'kosti', 'kostur', ''),
    'm.$' : (r'm\.\$', 'meðal', 'm', 'meðal'),
    '$a.' : (r'\$a\.', 'annars', 'annar', ''),
    'm.$' : (r'm\.\$', 'meira', 'm', 'meira'),
    '$a.$' : (r'\$a\.\$', 'að', 'a\.', 'að'),
    '$s.' : (r'\$s\.', 'segja', 's', 'segja'),
    't.$' : (r't\.\$', 'til', 'til', ''),
    '$d.' : (r'\$d\.', 'dæmis', 'dæmis', '')}

mwes = []
