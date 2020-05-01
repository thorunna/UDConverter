import re
import sys
import os

'''
Regex string to find (some) fixes in CoNLLU:
    \t\$[^tdðu].*\t.*\t_\tN[^E]

# TODO:
    - 1725.biskupasogur.nar-rel.conllu
        Skaga$ $fjarðar$ $sýslum
    - 2008.mamma.nar-fic.psd
        gjör$ $svo$ $vel
    - 1210.thorlakur.rel-sag.psd
        Páls$ $messu in
    - 1250.sturlunga.nar-sag.psd
        Staðar$ $Kolbeins
        Staðar$ $Böðvars
    - 1270.gragas.law-law.psd
        vígsakar$ $aðilinn
    - 1325.arni.nar-sag.psd
        tíunda$ $skipti
        Helga$ $son
    - 1540.ntacts.rel-bib.psd
        [Öö]ngvan$ $eg$ $inn (two examples, do not join article)
        lögmáls$ $lesturinn
    - 1593.eintal.rel-oth.conllu
        fórnfæringar$ $sauðum
    - 1611.okur.rel-oth.conllu
        leóns$ $haus
        kirkju$ $embættið
        guðssonar$ $blóði
    - 1630.gerhard.rel-oth.conllu
        öngvan$ $eg$ $inn (two examples, do not join article)
    - 1659.pislarsaga.bio-aut.conllu
        Kirkjubóls$ $ferð$ $inni
    - 1661.indiafari.bio-tra.conllu
        hvers$ $kyns
        hnífs$ $lag
        fram$ $parti
        af$ $reisu
    - 1675.armann.nar-fic.conllu
        alls$ $konar
    - 1675.magnus.bio-oth.conllu
        kirkju$ $göngu$ $na
    - 1675.modars.nar-fic.psd
        Móðals$ $felli
    - 1680.skalholt.nar-rel.psd
        einu$ $sinni
        nokkurs$ $staðar
        Árna$ $nesi
    - 1720.vidalin.rel-ser.psd
        húss$ $móðir$ $in (do not join article)
    - 1725.biskupasogur.nar-rel.psd
        Hallgríms$ $son
        hagleiks$ $gáfu
        mátt$ $leysi
        hagleiks$ $maður
        utan$ $lands
        þess$ $háttar (two examles)
        Skaga$ $fjarðar$ $sýslum
    - 1791.jonsteingrims.bio-aut.psd
        gáleysis$ $orð
        klausturs$ $stapp
        frost$ $veður
    - 1830.hellismenn.nar-sag.psd
        Eiríks$ $sonar
    - 1882.torfhildur.nar-fic.psd
        bónda$ $garði
        þrætu$ $efni
    - 1902.fossar.nar-fic.psd
        utan$ $bæjar
        riddara$ $sögum
        Íslendinga$ $sögum
    - 1908.ofurefli.nar-fic.psd
        ofbeldis$ $gaur
    - 1920.arin.rel-ser.psd
    - 1985.margsaga.nar-fic.psd
        trúar$ $lífinu
    - 1985.sagan.nar-fic.psd
        [Ee]inu$ $sinni (10 examples)
        Postulíns$ $hundar
        glæpa$ $beltinu
    - 2008.mamma.nar-fic.psd
    - 2008.ofsi.nar-sag.psd

# ISSUES: Possibly remove '$'?
    - 1350.marta.rel-sag.conllu
        til$ $herbergis
        næst$ $líkam
    - 1480.jarlmann.nar-sag.conllu
        öllu$ $megin
    - 1661.indiafari.bio-tra.conllu
        í$ $bland
    - 1888.grimur.nar-fic.psd
        öðru$ $megin
    - 1985.margsaga.nar-fic.psd
        báðu$ $megin
    - 1985.sagan.nar-fic.psd
        fullan$ $munn

Hinrik Hafsteinsson 2019
Part of UniTree project for IcePaHC

Text preperation script for IcePaHC corpus file (.psd). Not to be run by itself,
part of preprocessing pipeline.
 - Joins various nodes small split by '$' in IcePaHC notation
 - input: .psd file on command line (edits files in situ by renaming/removing)

grep queries:
    grep -n -E 'einhvers\$|annars\$|nokkurs\$|einhvers\$|einhvörs\$|hvers\$' testing/corpora/icecorpus/psd_prt_testing/*
    grep -n -E '\(N-\w \$.*-.*\)' testing/corpora/icecorpus/psd_prt_testing/*
'''

# regex for joining "einhvernveginn"
einhvern_token = r'einhvern(?=\$)' # matches the token of 'einhvern' before a '$'
einhvern_node = r'\((ONE\+)?Q-\w einhv[eö]rn?\$-einhver\)' # matches a whole 'einhvern$' node
einhvern_trail_alt = r'(?<=einhvern)(?=\$)' # matches '$' at end of 'einhvern'\\
einhvern_trail = r'(?<=einhvern)\$'

einhvers_node = r'\((ONE\+)?Q-\w einhv[eö]r.\$-einhver\)'

vegur_node = r'\(N-\w \$veg\$-vegur\)'
vegur_token = r'(?<=\$)veg\$'

timi_node = r'\(N-. \$tíman{0,2}-tími\)'
timi_token = r'(?<=\$)tíman{0,2}'

# other regex
# second_node = r'\(N-\w \$.*-.*\)'
general_first_node = r'\((ONE\+)?(Q|OTHER|D|WD)-\w [a-zþæðöáéýúíó]+\$-[a-zþæðöáéýúíó]+\)'
general_first_token = r'[a-zþæðöáéýúíó]+\$'
general_first_trail = r'(?<=[a-zþæðöáéýúíó])(?=\$)'
general_first_split = r'(?<=[a-zþæðöáéýúíó])\$' # matches '$' at end of first token
general_first_lemma = r'(?<=\$-)[a-zþæðöáéýúíó]+(?=\))'

general_second_node = r'\(N-\w \$[^$\n]{2,}-[^$\n\)]*\)'
general_second_token = r'(?<=\$)[a-zþæðöáéýúíó]+'
general_second_lemma = r'(?<=-)[a-zþæðöáéýúíó]+(?=\)\))'


noun_trail = r'(?<=)\$(?=-)' # matches the trailing "$" of a noun
noun_node =  r' {0,1}\(((N|NS|NPR|NPRS)-|FW).*\$-' # matches a whole noun node
noun_token_incompl = r'(?<=N-. )[^($]*(?=-)' # noun token where "$" is missing

# in_path = str(sys.argv[1])
in_dir = 'testing/corpora/icecorpus/psd_prt_testing'
# in_path = 'testing/corpora/icecorpus/psd_orig/2008.ofsi.nar-sag.psd'
for filename in os.listdir(in_dir):
    print(filename)
    in_path = os.path.join(in_dir, filename)
    # out_path = in_path + '.tmp'

    in_file = open(in_path, 'r')
    # out_file = open(out_path, 'w')

    lines = in_file.readlines()
    indexes = range(len(lines))

    in_file.close()

    def join_adverbs(curr):
        '''
        # joins various words split by '$', mostly adverbs
            - einhvers$ $staðar e.g. 2008.ofsi.nar-sag.psd
            - annars$ $staðar e.g. 1250.sturlunga.nar-sag.psd
            - nokkurs$ $staðar e.g. 1680.skalholt.nar-rel.psd
            - annar$ $staðar e.g. 1888.grimur.nar-fic.psd
            - einhvers$ $konar e.g. 2008.ofsi.nar-sag.psd
            - hvers$ $konar e.g. 2008.ofsi.nar-sag.psd
        '''
        prev = curr-1
        if re.search(einhvern_node, lines[curr]) and re.search(vegur_node, lines[curr]):
            '''einhvern$ $veg($ $)inn'''
            # print(curr, lines[curr].strip())
            # print(re.findall(vegur_token, lines[curr]))
            lines[curr] = re.sub(einhvern_trail, re.findall(vegur_token, lines[curr])[0], lines[curr])
            lines[curr] = re.sub(vegur_node, '', lines[curr])
            # print('\t', curr, lines[curr].strip('\n'))
            # out_file.write(lines[curr])
        elif re.search(einhvern_node, lines[curr]) and re.search(timi_node, lines[curr]):
            '''einhvern$ $tímann'''
            # print(curr, lines[curr].strip())
            lines[curr] = re.sub(einhvern_trail, re.findall(timi_token, lines[curr])[0], lines[curr])
            lines[curr] = re.sub(timi_node, '', lines[curr])
            # print('\t', curr, lines[curr].strip('\n'))
            # out_file.write(lines[curr])
        elif re.search(general_first_node, lines[curr]) and re.search(general_second_node, lines[curr]) and not re.search(r'þann', lines[curr]):
            print(curr, lines[curr].strip())
            lines[curr] = re.sub(general_first_trail, re.findall(general_second_token, lines[curr])[0], lines[curr])
            lines[curr] = re.sub(general_first_lemma, re.findall(general_first_token, lines[curr])[0], lines[curr])
            lines[curr] = re.sub(general_first_split, '', lines[curr])
            lines[curr] = re.sub(general_second_node, '', lines[curr])
            print('\t', curr, lines[curr].strip())
        else:
            pass
            # print(lines[curr])
            # out_file.write(lines[curr])

    def join_mas(curr):
        if re.search(r'm\.\$', lines[curr]):
            pass

    for index in indexes:
        join_adverbs(index)

    in_file.close()

# out_file.close()
#
# os.remove(in_path)
# os.rename(out_path, in_path)

'''
Grep search results for single line fixes

    tabbed = fixed
    # = skipped
    . = alternate error

    1250.sturlunga.nar-sag.psd:1824:	  (NP-ADV (OTHER-G annar$-annar) (N-G $staðar-staður))
    1480.jarlmann.nar-sag.psd:14444:	  (NP-ADV (Q-D öllu$-allur) (N-D $megin-meginn))
# 1525.erasmus.nar-sag.psd:122:			    (NP-ADV (D-A þann$-sá) (N-A $veg-vegur))
. 1661.indiafari.bio-tra.psd:2269:		    (NP-POS (Q-G hvers-hver) (N-G $kyns-kyn))
    1675.armann.nar-fic.psd:2322:			       (NP-OB1 (NP-POS (Q-G alls$-alls) (N-G $konar-konar))
    1675.armann.nar-fic.psd:6430:	      (NP-ADV (ONE+Q-G einhvör$-einhver) (N-G $staðar-staður))
    1680.skalholt.nar-rel.psd:38:		      (IP-SUB (NP-TMP (ONE-D einu$-einn) (N-D $sinni-sinni))
    1680.skalholt.nar-rel.psd:1105:		(NP-TMP (ONE-D einu$-einn) (N-D $sinni-sinni))))))
    1680.skalholt.nar-rel.psd:1439:	  (NP-ADV (Q-G nokkurs$-nokkur) (N-G $staðar-staður))
    1725.biskupasogur.nar-rel.psd:12807:		   (NP (NP-POS (D-G þess$-sá) (N-G $háttar-háttur))
    1725.biskupasogur.nar-rel.psd:12969:		       (NP (NP-POS (D-G þess$-sá) (N-G $háttar-háttur))
    1888.grimur.nar-fic.psd:248:			      (NP-ADV (ADV alstaðar-alstaðar) (OTHER-G annar$-annar) (N-G $staðar-staður)))))))
	1888.grimur.nar-fic.psd:2220:	  (NP-ADV (ONE+Q-A einhvern$-einhver) (N-A $veg$-vegur) (D-A $inn-hinn))
    1888.grimur.nar-fic.psd:2683:	  (NP-ADV (OTHER-D öðru$-annar) (N-D $megin-meginn))
	1888.grimur.nar-fic.psd:2737:	  (NP-ADV (ONE+Q-A einhvern$-einhver) (N-A $veg$-vegur) (D-A $inn-hinn))
	1888.grimur.nar-fic.psd:5353:	  (NP-ADV (ONE+Q-A einhvern$-einhver) (N-A $veg$-vegur) (D-A $inn-hinn))
    1985.margsaga.nar-fic.psd:2952:		    (NP-PRD (NP-POS (ONE+Q-G einhvers$-einhver) (N-G $konar-konar))
    1985.margsaga.nar-fic.psd:9532:		      (NP-ADV (Q-D báðu$-báðir) (N-D $megin-meginn)))
    1985.margsaga.nar-fic.psd:19981:	  (NP-SBJ (NP-POS (ONE+Q-G einhvers$-einhver) (N-G $konar-konar))
    1985.sagan.nar-fic.psd:7943:(IP-MAT-SPE (NP-TMP (ONE-D Einu$-einn) (N-D $sinni-sinni))
    1985.sagan.nar-fic.psd:7971:(IP-MAT-SPE (NP-TMP (ONE-D Einu$-einn) (N-D $sinni-sinni))
    1985.sagan.nar-fic.psd:8001:			   (NP-MSR (ADV einu$-einu) (N-D $sinni-sinni))
    1985.sagan.nar-fic.psd:8320:			    (NP-TMP (ONE-D einu$-einn) (N-D $sinni-sinni))
    1985.sagan.nar-fic.psd:8350:(IP-MAT-SPE (NP-TMP (ONE-D einu$-einn) (N-D $sinni-sinni))
    1985.sagan.nar-fic.psd:8865:			    (NP-TMP (ONE-D Einu$-einn) (N-D $sinni-sinni))
    1985.sagan.nar-fic.psd:8893:	      (NP-TMP (ONE-D einu$-einn) (N-D $sinni-sinni))
    1985.sagan.nar-fic.psd:13360:	      (NP-MSR (ONE-D einu$-einn) (N-D $sinni-sinni))
    1985.sagan.nar-fic.psd:14926:	      (NP-TMP (ONE-D einu$-einn) (N-D $sinni-sinni))
    1985.sagan.nar-fic.psd:15003:	      (NP-MSR (ONE-D einu$-einn) (N-D $sinni-sinni))
# 1985.sagan.nar-fic.psd:16407:			 (IP-SMC (NP-SBJ (NS-A svefnpoka$-svefnpoki) (N-A $na-na))
# 1985.sagan.nar-fic.psd:17891:			      (NP (ADJ-D fullan$-fullur) (N-D $munn-munnur))))
	2008.ofsi.nar-sag.psd:4345:		    (NP-ADV (ONE+Q-A einhvern$-einhver) (N-A $veg$-vegur) (D-A $inn-hinn))
    2008.ofsi.nar-sag.psd:4641:		  (NP-ADV (ONE+Q-G einhvers$-einhver) (N-G $staðar-staður))
    2008.ofsi.nar-sag.psd:4710:		      (NP-ADV (ONE+Q-G einhvers$-einhver) (N-G $staðar-staður))
	2008.ofsi.nar-sag.psd:5053:		    (NP-TMP (ONE+Q-A einhvern$-einhver) (N-A $tíma-tími))
	2008.ofsi.nar-sag.psd:5132:	  (NP-ADV (ONE+Q-A einhvern$-einhver) (N-A $veg$-vegur) (D-A $inn-hinn))
	2008.ofsi.nar-sag.psd:6571:	      (NP-ADV (ONE+Q-A einhvern$-einhver) (N-A $veg$-vegur) (D-A $inn-hinn))
	2008.ofsi.nar-sag.psd:8692:	  (NP-ADV (ONE+Q-A einhvern$-einhver) (N-A $veginn-vegur))
    2008.ofsi.nar-sag.psd:8701:			    (NP-TMP (Q-A nokkurn$-nokkur) (N-A $tíma-tími))
. 2008.ofsi.nar-sag.psd:8832:			  (NP-TMP (Q-A nokkurntíma-nokkurntími) (N-A $tíma-tími))
    2008.ofsi.nar-sag.psd:8951:			       (NP-OB1 (NP-POS (ONE+Q-G einhvers$-einhver) (N-G $konar-konar))
	2008.ofsi.nar-sag.psd:12600:	  (NP-ADV-LFD (ONE+Q-A einhvern$-einhver) (N-A $veg$-vegur) (D-A $inn-hinn))
    2008.ofsi.nar-sag.psd:14522:			       (NP (WNP-POS (WD-G hvers$-hver) (N-G $konar-konar))
    2008.ofsi.nar-sag.psd:20393:			    (NP-TMP (Q-A nokkurn$-nokkur) (N-A $tíma-tími))
	2008.ofsi.nar-sag.psd:20705:	  (CONJP (IP-MAT=1 (NP-ADV (ONE+Q-A einhvern$-einhver) (N-A $veg$-vegur) (D-A $inn-hinn))
    2008.ofsi.nar-sag.psd.tmp:4641:		  (NP-ADV (ONE+Q-G einhvers$-einhver) (N-G $staðar-staður))
    2008.ofsi.nar-sag.psd.tmp:4710:		      (NP-ADV (ONE+Q-G einhvers$-einhver) (N-G $staðar-staður))
    2008.ofsi.nar-sag.psd.tmp:8701:		    (NP-TMP (Q-A nokkurn$-nokkur) (N-A $tíma-tími))
. 2008.ofsi.nar-sag.psd.tmp:8832:		  (NP-TMP (Q-A nokkurntíma-nokkurntími) (N-A $tíma-tími))
    2008.ofsi.nar-sag.psd.tmp:8951:		       (NP-OB1 (NP-POS (ONE+Q-G einhvers$-einhver) (N-G $konar-konar))
    2008.ofsi.nar-sag.psd.tmp:14522:		       (NP (WNP-POS (WD-G hvers$-hver) (N-G $konar-konar))
    2008.ofsi.nar-sag.psd.tmp:20393:		    (NP-TMP (Q-A nokkurn$-nokkur) (N-A $tíma-tími))
'''
