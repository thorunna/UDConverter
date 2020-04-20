from lib.rules import relation_NP, relation_IP, relation_CP

import string

def determine_relations(mod_tag, mod_func, head_tag, head_func):

    # # DEBUG:
    # print('\n'+mod_tag, mod_func, head_tag, head_func, '\n')

    if mod_tag in ['NP', 'NX', 'WNX']:   #TODO: hvað ef mod_tag er bara NP?
        # -ADV, -CMP, -PRN, -SBJ, -OB1, -OB2, -OB3, -PRD, -POS, -COM, -ADT, -TMP, -MSR
        return relation_NP.get(mod_func, 'rel')
#       return relation_NP.get(mod_func, 'rel-'+mod_tag)
    elif mod_tag == 'WNP':
        return 'obj'
    elif mod_tag in ['NS', 'N', 'NPRS'] and head_tag in ['NP', 'NX', 'QTP', 'ADJP', 'CONJP', 'NPR']:    #seinna no. í nafnlið fær 'conj' og er háð fyrra no.
        return 'conj'
    elif mod_tag == 'NPR' and head_tag == 'CONJP':
        return 'conj'
    elif mod_tag == 'NPR' and head_tag in ['NP', 'NX', 'QTP']:
        return 'flat:name'
    elif mod_tag == 'ES':
        return 'expl'   #expletive
    elif mod_tag in ['PRO', 'WPRO']:
        return 'nmod'
#        elif mod_tag == 'PRO' and head_tag == 'NP' and head_func == 'PRN':  #TODO: skoða betur, hliðstæð NPR sem eru bæði dobj?
#            return 'obj'
    elif mod_tag in ['D', 'WD', 'ONE', 'ONES', 'OTHER', 'OTHERS', 'SUCH']:
        return 'det'
    elif mod_tag[:3] == 'ADJ' or mod_tag[:4] == 'WADJ' or mod_tag in ['Q', 'QR', 'QS', 'WQP']:
            # -SPR (secondary predicate)
        return 'amod'
    #elif mod_tag == 'PP' and head_tag == 'IP':  #CP-ADV
    #    return 'advcl'
    elif mod_tag in ['PP', 'WPP', 'PX']:
            # -BY, -PRN
        return 'obl'        #NP sem er haus PP fær obl nominal  #TODO: haus CP-ADV (sem er PP) á að vera merktur advcl
    elif mod_tag == 'P':
        return 'case'
    elif mod_tag[:3] == 'ADV' or mod_tag in ['NEG', 'FP', 'QP', 'ALSO', 'WADV', 'WADVP']:    #FP = focus particles  #QP = quantifier phrase - ATH.
        if head_func == 'QUE' or head_tag == 'WNP':
            # Ætti að grípa spurnarorð í spurnarsetningum, sem eru mark skv. greiningu HJ
            return 'mark'
        else:
            # -DIR, -LOC, -TP
            return 'advmod'
    elif mod_tag == 'NS' and head_tag == 'ADVP' and head_func == 'TMP':     #ath. virkar fyrir eitt dæmi, of greedy?
        return 'conj'
    elif mod_tag in ['RP', 'RPX']:
        return 'compound:prt'
    elif mod_tag == 'IP' and mod_func == 'SUB' and head_tag == 'CP' and head_func == 'FRL':
        return 'acl:relcl'
    elif mod_tag in ['IP', 'VP']:
        return relation_IP.get(mod_func, 'rel')
#            return relation_IP.get(mod_func, 'rel-'+mod_tag)
    elif mod_tag[:2] == 'VB' and head_tag == 'CP':
        return 'ccomp'
    elif mod_tag in ['VAN', 'DAN', 'HAN', 'BAN']:
        return 'aux:pass'
    elif mod_tag in ['VBN', 'DON', 'HVN', 'RDN']:   #ath. VBN getur verið rót
        if head_func and '=' in head_func:
            return 'conj'
        else:
            # return '?'
            return 'dep'
    elif mod_tag[:2] in ['VB', 'DO', 'HV', 'RD', 'MD']: #todo
        return 'aux'
    elif mod_tag[:2] == 'BE' or mod_tag == 'BAN':  #copular, TODO: ekki alltaf copular
        return 'cop'
    elif mod_tag == 'VAG':
        # return 'amod?'
        return 'amod'
    elif mod_tag == 'RRC':
        return 'acl:relcl'
        # return 'acl:relcl?'

    elif mod_tag == 'CONJ':
        return 'cc'
    elif mod_tag in ['CONJP', 'N'] and head_tag in ['NP', 'N', 'PP']:      #N: tvö N í einum NP tengd með CONJ
        return 'conj'
    elif mod_tag == 'CONJP' and head_tag == 'IP':
        return relation_IP.get(head_func, 'rel')
#            return relation_IP.get(head_func, 'rel-'+mod_tag+head_tag+head_func)
    elif mod_tag == 'CONJP':
        return 'conj'
    elif mod_tag == 'CP' and mod_func == 'REL' and head_tag == 'ADVP':
        return 'advcl'
    elif mod_tag == 'CP':
        return relation_CP.get(mod_func, 'rel')
#            return relation_CP.get(mod_func, 'rel-'+mod_tag)
    elif mod_tag in ['C', 'CP', 'TO', 'WQ']:  #infinitival marker with marker relation
        return 'mark'
    elif mod_tag in ['NUM', 'NUMP']:
        return 'nummod'
    elif mod_tag == 'FRAG':
        return 'xcomp'
    elif mod_tag in string.punctuation or mod_tag == 'LB':
        return 'punct'
    elif mod_tag in ['INTJ', 'INTJP'] or head_tag == 'INTJP':
        return 'discourse'
    elif mod_tag in ['FOREIGN', 'FW', 'ENGLISH', 'LATIN'] or head_tag in ['FOREIGN', 'FW', 'ENGLISH', 'LATIN']:
        return 'flat:foreign'
    elif mod_tag in ['XXX', 'XP', 'X', 'QTP', 'REP', 'FS', 'LS', 'META', 'REF']:      #XXX = annotator unsure of parse, LS = list marker
        return 'dep'    #unspecified dependency
    elif head_tag in ['META', 'CODE', 'REF', 'FRAG']:
        return 'dep'
    elif mod_tag in ['N', 'NS', 'NPR', 'NPRS']:
        # return 'rel'
        return 'dep'

    # return 'rel-'+mod_tag
    return 'dep'
