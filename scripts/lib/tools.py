
import string
import re
import requests
import json

from lib.rules import relation_NP, relation_IP, relation_CP, abbr_map
from lib.reader import IndexedCorpusTree



def determine_relations(mod_tag, mod_func, head_tag, head_func):

    #return mod_tag, mod_func, head_tag, head_func
    # # DEBUG:
    # print('\n'+mod_tag, mod_func, head_tag, head_func, '\n')
    #return head_tag, head_func
    if mod_tag in ['NP', 'NX', 'WNX']:   #TODO: hvað ef mod_tag er bara NP?
        # -ADV, -CMP, -PRN, -SBJ, -OB1, -OB2, -OB3, -PRD, -POS, -COM, -ADT, -TMP, -MSR
        return relation_NP.get(mod_func, 'dep')
        # return relation_NP.get(mod_func, 'rel')
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
        return relation_IP.get(mod_func, 'dep')
        # return relation_IP.get(mod_func, 'rel')
#            return relation_IP.get(mod_func, 'rel-'+mod_tag)
    elif mod_tag[:2] == 'VB' and head_tag == 'CP':
        return 'ccomp'
    elif head_tag == 'IP' and head_func == 'INF-PRP':
        return 'advcl'
#    elif head_tag == 'IP' and head_func == 'INF':
#        return 'xcomp'
    elif head_tag == 'NP' and mod_tag == 'VAN':
        return 'amod'
    elif mod_tag in ['VAN', 'DAN', 'HAN', 'BAN', 'RAN']: # RAN vantaði?
        # return 'aux:pass' # UD hætt með aux:pass?
        return 'aux'
        # return 'verb' # testing dropping aux
    elif mod_tag in ['VBN', 'DON', 'HVN', 'RDN']:   #ath. VBN getur verið rót
        if head_func and '=' in head_func:
            return 'conj'
        else:
            # return '?'
            return 'dep'
    # elif mod_tag[:2] in ['VB', 'DO', 'HV', 'RD', 'MD']: #todo
    elif mod_tag[:2] in ['DO', 'HV', 'RD', 'MD']: #todo
        return 'aux'
        # return 'verb' # testing dropping aux in output
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
        return relation_IP.get(head_func, 'dep')
        # return relation_IP.get(head_func, 'rel')
#            return relation_IP.get(head_func, 'rel-'+mod_tag+head_tag+head_func)
    elif mod_tag == 'CONJP':
        return 'conj'
    elif mod_tag == 'CP' and mod_func == 'REL' and head_tag == 'ADVP':
        return 'advcl'
    elif mod_tag == 'CP':
        return relation_CP.get(mod_func, 'dep')
        # return relation_CP.get(mod_func, 'rel')
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
    elif head_tag == 'IP' and head_func == 'SMC':
        return 'dep'

    # return 'rel-'+mod_tag
    return 'dep'

def decode_escaped(string, lemma=False):
    '''
    Fixes various punctuations (-, /, ') that are escaped in corpus data
    Also fixes most abbrevations in corpus data using abbrevations rules dictionar
    '''
    if re.search(r'[<>]', string):
        ''' Tokens processed '''
        # print('\t', line[1], line[2])
        if re.search(r'</?dash/?>', string):
            string= re.sub(r'</?dash/?>', '-',string)
        if re.search(r'</?slash/?>', string):
            string= re.sub(r'</?slash/?>', '/', string)
        if re.search(r'</?apostrophe/?>', string):
            string = re.sub(r'</?apostrophe/?>', "'", string)
        return string
    if string in abbr_map.keys():
        # print(string)
        string = re.sub(abbr_map[string][0], abbr_map[string][1], string)
            # if lemma == True:
            #     string = re.sub(pattern, output[1])
            # else:)

        # print(string)
        return string
    else:
        return string

def fix_IcePaHC_tree_errors(tree):
    '''
    Fixes specific punctuation errors in IcePaHC trees
    '''
    if not tree.corpus_id:
        return tree
    fileid = tree.corpus_id.split(',')[0]
    if fileid == '1150.HOMILIUBOK.REL-SER':
        if tree.corpus_id_num in {'.691', '.697', '.1040', '.1044', '.1572'}:
            tree.append(IndexedCorpusTree.fromstring('(. ?-?)'))
        elif tree.corpus_id_num == '.1486':
            tree.append(IndexedCorpusTree.fromstring('(. .-.)'))
    elif fileid == '1275.MORKIN.NAR-HIS':
        if tree.corpus_id_num == '.451':
            tree.append(IndexedCorpusTree.fromstring('(. .-.)'))
            tree.append(IndexedCorpusTree.fromstring('(" "-")'))
        elif tree.corpus_id_num == '.1680':
            tree.append(IndexedCorpusTree.fromstring('(. .-.)'))
    return tree

def tagged_corpus(corpus):
    '''
    Gets tagged data for corpus
    '''
    text = ''
    IDs = []
    counter = 0
    for tree in corpus:
        counter += 1
        text += re.sub(r' \.', '.',re.sub(r'(\$ \$|\*ICH\*|\*T\*)', '', ' '.join([tree[i].split('-')[0] for i in tree.treepositions() if isinstance(tree[i], str) and '-' in tree[i] ]))+'\n')

        if tree.corpus_id != None:
            IDs.append(tree.corpus_id)
        else:
            # IDs.append(IDs[0][:-1]+str(counter))
            IDs.append('ID_missing_'+str(counter))

    url = 'http://malvinnsla.arnastofnun.is'
    payload = {'text':text, 'lemma':'on'}
    headers = {}
    res = requests.post(url, data=payload, headers=headers)
    tagged = json.loads(res.text)
    tagged_sents = []
    for par in tagged['paragraphs']:
        tagged_sent = {}
        for sent in par['sentences']:
            for pair in sent:
                tagged_sent[pair['word']] = (pair['tag'], pair['lemma'])
        tagged_sents.append(tagged_sent)
    ID_sents = dict(zip(IDs, tagged_sents))

    # for i, j in ID_sents.items():
    #     print(i,j)
    #     input()
    # exit()

    return ID_sents
