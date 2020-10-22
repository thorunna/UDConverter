#!/bin/bash

echo '''
22.07.19
Hinrik Hafsteinsson
Þórunn Arnardóttir

fix_corpus_error.sh

Script for fixing various presumed errors in IcePaHC corpus files (.psd)
'''

# dir="./testing/corpora/icepahc-v0.9/psd"
# dir="../testing/corpora/icecorpus/psd "
corpus=$1
# dir="${corpus}_fixed"
dir=$2

if [ ! -d $dir ];
  then
    echo "Creating '$dir' directory..."
    mkdir $dir
  else
    echo "Directory '$dir' already exists. Using that."
fi

for file in $corpus/*; do
  echo "Copying file: ${file##*/}"
  cp $file $dir
done

echo "Fixing annotation errors..."

# 1150.firstgrammar.sci-lin.psd
sed -i "" 's/(DAN \&gört-gera)/(DAN $gört-gera)/g' $dir/1150.homiliubok.rel-ser.psd # .37

# 1150.homiliubok.rel-ser.psd
sed -i "" 's/( (LATIN (FW Assumptio-assumptio) (FW sancte-sancte) (FW Marie-marie))( (LATIN (FW Assumptio-assumptio) (FW sancte-sancte) (FW Marie-marie) (. .-.))/g' $dir/1150.homiliubok.rel-ser.psd # .11
sed -i "" 's/( (IP-MAT=1/( (IP-MAT-1/g' $dir/1150.homiliubok.rel-ser.psd # .37
sed -i "" 's/(WADJ hversu-hversu)/(WADV hversu-hversu)/g' $dir/1150.homiliubok.rel-ser.psd # .105
sed -i "" 's/(IP-SUB=3 (ADJP *T*-7)/(IP-SUB (ADJP *T*-7)/g' $dir/1150.homiliubok.rel-ser.psd # .112
sed -i "" 's/(CODE </heading>))/(CODE </heading>) (. .-.))/g' $dir/1150.homiliubok.rel-ser.psd # .137, .389
sed -i "" 's/(CODE </modern_translation_of_heading>))/(CODE </modern_translation_of_heading>) (. .-.))/g' $dir/1150.homiliubok.rel-ser.psd # .138
sed -i "" 's/(CODE </translation>))/(CODE </translation>) (. .-.))/g' $dir/1150.homiliubok.rel-ser.psd # .390
sed -i "" 's/(WQ (WADV hve-hve) (Q-N mikill-mikill))/(WQP (WADV hve-hve) (Q-N mikill-mikill))/g' $dir/1150.homiliubok.rel-ser.psd # .470
sed -i "" 's/(CODE </heading>))/(CODE </heading>) (. .-.))/g' $dir/1150.homiliubok.rel-ser.psd # .585, 676, 798
sed -i "" 's/(VBI \$gef-gefa)/(VBI \$gef\$-gefa)/g' $dir/1150.homiliubok.rel-ser.psd # .1648
sed -i "" 's/(NP-SBJ \$tu-þú)/(NP-SBJ (PRO-N \$tu-þú))/g' $dir/1150.homiliubok.rel-ser.psd # .246
sed -i "" 's/FOREIGN/FW/g' $dir/1150.homiliubok.rel-ser.psd # .338
sed -i "" 's/(NP-ADT járnum-járna)/(NP-ADT (NS-D járnum-járn))/g' $dir/1150.homiliubok.rel-ser.psd # .410
sed -i "" 's/( (\. \?-\?))//g' $dir/1150.homiliubok.rel-ser.psd # .691, .697, .1040, .1044, .1572
sed -i "" 's/( (\. \.-\.))//g' $dir/1150.homiliubok.rel-ser.psd # .1486
sed -i "" 's/(CP-REL (WADVP-3 (WADVP þar-þar))/(CP-REL (WADVP-3 (WADV þar-þar))/g' $dir/1150.homiliubok.rel-ser.psd # .42565
sed -i "" 's/(NP-SBJ \*con\*-N)/(NP-SBJ \*con\*)/g' $dir/1150.homiliubok.rel-ser.psd # .463
sed -i "" 's/(NP-SBJ \*con\*-D)/(NP-SBJ \*con\*)/g' $dir/1150.homiliubok.rel-ser.psd # .1325
sed -i "" 's/(NP-SBJ \*con\*-A)/(NP-SBJ \*con\*)/g' $dir/1150.homiliubok.rel-ser.psd # .1587

#1210.jartein.rel-sag.psd
sed -i "" 's/(D-A ið-hinn)/(D-A \$ð-hinn)/' $dir/1210.jartein.rel-sag.psd # .159
sed -i "" 's/(IP-MAT-KOMINN/(IP-MAT/' $dir/1210.jartein.rel-sag.psd # .321
sed -i "" 's/(N-A sylgju\$)/(N-A sylgju\$-sylgja)/' $dir/1210.jartein.rel-sag.psd # .552
sed -i "" 's/(CP-QUE-SPE (WADVP-2 (WADVP Hví-hví))/(CP-QUE-SPE (WADVP-2 (WADV Hví-hví))/' $dir/1210.jartein.rel-sag.psd # .4160

# 1250.sturlunga.nar-sag.psd
sed -i "" 's/(NS-A fjörðu-fjörður) (D-A \$na-hinn)/(NS-A fjörðu$-fjörður) (D-A \$na-hinn)/g' $dir/1250.sturlunga.nar-sag.psd # 398.338
# sed -i "" 's/NS-ADT/NP-ADT/g' $dir/1250.sturlunga.nar-sag.psd # 390.77, 393.187, 421.1076, 421.1096, 428.1318
sed -i "" 's/NP-A /NS-A /g' $dir/1250.sturlunga.nar-sag.psd # 135.1604
sed -i "" 's/(IP-SUB (ADVP-OC/(IP-SUB (ADVP-LOC/g' $dir/1250.sturlunga.nar-sag.psd # 448.2121
sed -i "" 's/(NP-SBJ \$tu-þú)/(NP-SBJ (PRO-N \$tu-þú))/g' $dir/1250.sturlunga.nar-sag.psd # 393.186, 419.994, 421.1061, 423.1171
sed -i "" 's/(WNP-N-1 hver-hver/(WNP-1 (WPRO-N hver-hver)/' $dir/1250.sturlunga.nar-sag.psd # 427.1265
sed -i "" 's/(CONJP-2 (CONJP og-og)/(CONJP-2 (CONJ og-og)/g' $dir/1250.sturlunga.nar-sag.psd # 417.903
sed -i "" 's/(VAN vist-vísa)/(N-N vist-vist)/' $dir/1250.sturlunga.nar-sag.psd # 405.609

# 1250.thetubrot.nar-sag.psd
sed -i "" 's/(NP-PRN-LL/(NP-PRN/' $dir/1250.thetubrot.nar-sag.psd # .151
sed -i "" 's/(CP-REL-SPE (WADVP-1 þar-þar)/(CP-REL-SPE (WADVP-1 (WADV þar-þar))/' $dir/1250.thetubrot.nar-sag.psd # .3111

# 1260.jomsvikingar.nar-sag.psd
sed -i "" 's/) (CONJ og-og) (NPR-N Gull<dash>Haraldur-gullharaldur))/) (CONJP (CONJ og-og) (NPR-N Gull<dash>Haraldur-gullharaldur)))/' $dir/1260.jomsvikingar.nar-sag.psd # .

# 1275.morkin.nar-his.psd
sed -i "" 's/( (. .-.))//' $dir/1275.morkin.nar-his.psd # .451, .1680
sed -i "" 's/( (" "-"))//' $dir/1275.morkin.nar-his.psd # .451
sed -i "" 's/(CP-REL (WADVP-1 (WADVP hvert-hvert))/(CP-REL (WADVP-1 (WADV hvert-hvert))/' $dir/1275.morkin.nar-his.psd # .11804
sed -i "" 's/(CP-QUE-SPE (WADVP-1 (WADVP Hví-hví))/(CP-QUE-SPE (WADVP-1 (WADV Hví-hví))/' $dir/1275.morkin.nar-his.psd # .16267
sed -i "" 's/(NP-TMP (NS-A ið-hinn)/(NP-TMP (D-A ið-hinn)/' $dir/1275.morkin.nar-his.psd # .1285

# 1300.alexander.nar-sag.psd
sed -i "" 's/(BEPI sér-sjá)/(BEPI sér-vera)/g' $dir/1300.alexander.nar-sag.psd # .55

# 1310.grettir.nar-sag.psd
sed -i "" 's/(NP-POS (N-S hryggjar-hryggur))))/(NP-POS (N-G hryggjar-hryggur))))/g' $dir/1310.grettir.nar-sag.psd # .95
sed -i "" 's/(IP-SUB (OTHER-WPRO-1 annaðhvort-annaðhvor)/(IP-SUB (OTHER+WPRO-1 annaðhvort-annaðhvor)/g' $dir/1310.grettir.nar-sag.psd # .1336

# 1325.arni.nar-sag.psd
sed -i "" 's/(IP-SUB-PRN=1 (CONJ og-og)/(IP-SUB-PRN (CONJ og-og)/g' $dir/1325.arni.nar-sag.psd # .236
sed -i "" 's/(IP-SUB-PRN=2 (CONJ og-og) (VB dæmast-dæma))/(IP-SUB-PRN (CONJ og-og) (VB dæmast-dæma))/g' $dir/1325.arni.nar-sag.psd # .284
sed -i "" 's/(IP-SUB=1 (PP (P með-með)/(IP-SUB (PP (P með-með)/g' $dir/1325.arni.nar-sag.psd # .564
sed -i "" 's/IP-SUB-=17/IP-SUB=17/g' $dir/1325.arni.nar-sag.psd # .927

# 1350.bandamennM.nar-sag.psd
sed -i "" 's/NP-AB1/NP-OB1/g' $dir/1350.bandamennM.nar-sag.psd # .558
sed -i "" 's/IP-SUB-SPE3/IP-SUB-SPE-3/g' $dir/1350.bandamennM.nar-sag.psd # .961
sed -i "" 's/D-N \$ðu/PRO-N \$ðu/g' $dir/1350.bandamennM.nar-sag.psd # .886
sed -i "" 's/D-N \$tu/PRO-N \$tu/g' $dir/1350.bandamennM.nar-sag.psd # .909
sed -i "" 's/NP-PRD Ófeigur-ófeigur/NP-PRD (NPR-N Ófeigur-ófeigur)/g' $dir/1350.bandamennM.nar-sag.psd # .9
sed -i "" 's/NP-PRN Ófeigur/NPR-N Ófeigur/g' $dir/1350.bandamennM.nar-sag.psd # .23

# 1350.finnbogi.nar-sag.psd
sed -i "" 's/(NP-SBJ \$tu-þú)/(NP-SBJ (PRO-N \$tu-þú))/g' $dir/1350.finnbogi.nar-sag.psd # .600
sed -i "" 's/(IP-MAT (NPR-N Bóndi-bóndi)/(IP-MAT (NP-SBJ (NPR-N Bóndi-bóndi))/' $dir/1350.finnbogi.nar-sag.psd # .604
sed -i "" 's/(IP-SUB=2 (NP-SBJ (OTHER-N annar-annar))/(IP-SUB (NP-SBJ (OTHER-N annar-annar))/g' $dir/1350.finnbogi.nar-sag.psd # .1456
sed -i "" 's/(NP-SBJ \$ú-þú)/(NP-SBJ (PRO-N \$tu-þú))/g' $dir/1350.finnbogi.nar-sag.psd # .890
sed -i "" 's/(IP-INF (BE \*)/(IP-INF (BE )/g' $dir/1350.finnbogi.nar-sag.psd # .1664
sed -i "" 's/(NP-PRN Rauður-rauður)/(NPR-N Rauður-rauður)/g' $dir/1350.finnbogi.nar-sag.psd # .1986
sed -i "" 's/(RBN orðinn-verða)/(RDN orðinn-verða)/' $dir/1350.finnbogi.nar-sag.psd # .2021
sed -i "" 's/(ADJP (ADJP limaður-limaður)/(ADJP (ADJ-N limaður-limaður)/' $dir/1350.finnbogi.nar-sag.psd # .2066
sed -i "" 's/(CP-COM/(NP-COM/' $dir/1350.finnbogi.nar-sag.psd # .2073
sed -i "" 's/(WADJP (WADVP Hversu-hversu) (ADJ-N gamall-gamall))/(WADJP (WADV Hversu-hversu) (ADJ-N gamall-gamall))/' $dir/1350.finnbogi.nar-sag.psd # 628.225

# 1350.marta.rel-sag.psd
sed -i "" 's/(NP-SBJ (NRP-N kóngur-kóngur) (FW Regulus-regulus))))/(NP-SBJ (NPR-N kóngur-kóngur) (FW Regulus-regulus))))/g' $dir/1350.marta.rel-sag.psd # .193
sed -i "" 's/(NP (NPR-D Lasarus-lasarus) (CONJ og-og) (NPR-D Mörtu-marta)))/(NP (NPR-D Lasarus-lasarus) (CONJ og-og) (NPR-D Mörtu-marta))) (. .-.))/g' $dir/1350.marta.rel-sag.psd # .281
sed -i "" 's/( (META (NP (FW Capitulum-capitulum))/( (META (NP (FW Capitulum-capitulum)) (. .-.))/g' $dir/1350.marta.rel-sag.psd # .467
sed -i "" 's/(FW Miraculum-miraculum)/(FW Miraculum-miraculum) (. .-.))/g' $dir/1350.marta.rel-sag.psd # .813, 883, 915, 924, 950, 958

# 1400.gunnar.nar-sag.psd
sed -i "" 's/Er\$\$-vera/Er\$-vera/g' $dir/1400.gunnar.nar-sag.psd # .82
sed -i "" 's/Leggðu-leggja/Legg\$-leggja/g' $dir/1400.gunnar.nar-sag.psd # .465

# 1400.viglundur.nar-sag.psd
sed -i "" 's/( (. .-.))//g' $dir/1400.viglundur.nar-sag.psd # .279
sed -i "" 's/( (" "-"))//g' $dir/1400.viglundur.nar-sag.psd # .280

# 1450.bandamenn.nar-sag.psd
sed -i "" 's;(NPR-G Skalla<dash/>Grímssonar-skalla<dash/>grímsson);(NP-POS (NPR-G Skalla<dash/>Grímssonar-skalla<dash/>grímsson);g' $dir/1450.bandamenn.nar-sag.psd # 29.205
sed -i "" 's/(NP-POS (NPR-G Kveldúlfssonar-kveldúlfsson)))))$/(NP-POS (NPR-G Kveldúlfssonar-kveldúlfsson))))))/g' $dir/1450.bandamenn.nar-sag.psd # 29.205
sed -i "" 's/(IP-INF-SPE (IP-INF-SPE (OTHER-WPRO annaðhvort-annaðhvort)/(IP-INF-SPE (IP-INF-SPE (OTHER+WPRO annaðhvort-annaðhvort)/g' $dir/1450.bandamenn.nar-sag.psd # 42.861

# 1450.ectorssaga.nar-sag.psd
sed -i "" 's/(HDDI/(HVDI/' $dir/1450.ectorssaga.nar-sag.psd # .1096
sed -i "" 's/(NP (Q+ŃUM-D hvorumtveggjum-hvorumtveggi))))/(NP (Q+NUM-D hvorumtveggjum-hvorumtveggi))))/' $dir/1450.ectorssaga.nar-sag.psd # .1117
sed -i "" 's/(ADJP-OC/(ADJP-LOC/g' $dir/1450.ectorssaga.nar-sag.psd # .1853

# 1450.judit.rel-bib.psd
sed -i "" 's/(CODE </heading>))/(CODE </heading>) (. .-.))/g' $dir/1450.judit.rel-bib.psd # .22, 48
sed -i "" 's/( (META (NP (ADJ-N 4-fjórir) (FW Kapitulum-kapitulum)))/( (META (NP (ADJ-N 4-fjórir) (FW Kapitulum-kapitulum)) (. .-.))/g' $dir/1450.judit.rel-bib.psd # .65

# 1450.vilhjalmur.nar-sag.psd
sed -i "" 's/(NP-SBJ \$tu-þú)/(NP-SBJ (PRO-N \$tu-þú))/g' $dir/1450.vilhjalmur.nar-sag.psd # .254
sed -i "" 's/(IP-SUB (N-N engi-engi)/(IP-SUB (NP-SBJ (Q-N engi-engi))/' $dir/1450.vilhjalmur.nar-sag.psd # .295
sed -i "" 's/(IP-SUB-SPE (NP-SBJ \$ú-þú)/(IP-SUB-SPE (NP-SBJ (PRO-N \$ú-þú))/g' $dir/1450.vilhjalmur.nar-sag.psd # .774
sed -i "" 's/(NP-OB2 ICH\*-1)/(NP-OB2 \*ICH\*-1)/g' $dir/1450.vilhjalmur.nar-sag.psd # .1008
sed -i "" 's/(IP-SMC (NP-SBJ \*)/(IP-SMC (NP-SBJ )/g' $dir/1450.vilhjalmur.nar-sag.psd # .1171
sed -i "" 's/(IP-INF (BE \*)/(IP-INF (BE )/g' $dir/1450.vilhjalmur.nar-sag.psd # .1210
sed -i "" 's/(NS-N rifin-rifinn)/(NS-N rif\$-rif)/g' $dir/1450.vilhjalmur.nar-sag.psd # 87.1768
sed -i "" 's/(. -))/(. .-.))/g' $dir/1450.vilhjalmur.nar-sag.psd # 28.474
sed -i "" 's/(, ,-,))/(, ,-,))/g' $dir/1450.vilhjalmur.nar-sag.psd # 28.475
sed -i "" 's/(IP-INF-SPE (NP-OB2 ICH*-1)/(IP-INF-SPE (NP-OB2 *ICH*-1)/g' $dir/1450.vilhjalmur.nar-sag.psd # 50.1008
sed -i "" 's/(P (RP upp-upp)/(PP (RP upp-upp)/g' $dir/1450.vilhjalmur.nar-sag.psd # 46.901
sed -i "" 's/(NX (VAN-A skyggðan-skyggðja) (N-A hjálm-hjálmur))))/(NX (VAN-A skyggðan-skyggja) (N-A hjálm-hjálmur))))/g' $dir/1450.vilhjalmur.nar-sag.psd # 78.1575

# 1450.bandamenn.nar-rel.psd
sed -i "" 's/(NP-PRD (NS-N engi-engi) (N-N svívirðing-svívirðing))/(NP-PRD (Q-N engi-enginn) (N-N svívirðing-svívirðing))/g' $dir/1475.aevintyri.nar-rel.psd # .346

# 1475.aevintyri.nar-rel.psd
sed -i "" 's/mát-mega/mát\$-mega/g' $dir/1475.aevintyri.nar-rel.psd # .805
# sed -i "" 's/skal-skulu/skal\$-skulu/g' $dir/1475.aevintyri.nar-rel.psd # .840
# greedy, causes errors. No automatic fix?

# 1525.erasmus.nar-sag.psd
sed -i "" 's/(IP-SUB-SPE-3 (/(IP-SUB-SPE-3 (/g' $dir/1525.erasmus.nar-sag.psd # .56
sed -i "" 's/(NP-SBJ \$u-þú)/(NP-SBJ (PRO-N \$u-þú))/g' $dir/1525.erasmus.nar-sag.psd # .88
sed -i "" 's/(CP-QUE-SPE (WADJP-1 (WADVP hversu-hversu)/(CP-QUE-SPE (WADJP-1 (WADV hversu-hversu)/g' $dir/1525.erasmus.nar-sag.psd # .366

# 1525.georgius.nar-rel.psd
sed -i "" 's/NPÖ-SBJ/NP-SBJ/g' $dir/1525.georgius.nar-rel.psd # .392
sed -i "" 's/(IP-MAT-KOMINN/(IP-MAT/' $dir/1525.georgius.nar-rel.psd # .743
sed -i "" 's/(IP-SUB-SPE=4 (NP-SBJ (NP-POS (NP-POS (PRO-G hans-hann))/(IP-SUB-SPE (NP-SBJ (NP-POS (NP-POS (PRO-G hans-hann))/' $dir/1525.georgius.nar-rel.psd # .1056

# 1540.ntacts.rel-bib.psd
sed -i "" 's/\$út-út/út\$-út/g' $dir/1540.ntacts.rel-bib.psd # 239.141
sed -i "" 's/\sann\$-sannur/sann-sannur/g' $dir/1540.ntacts.rel-bib.psd # 239.160
sed -i "" 's/(N-G borg-borg)/(N-G borgar\$-borg)/g' $dir/1540.ntacts.rel-bib.psd # 266.879
sed -i "" 's/(NS-D yfirboðuru-yfirboðari)/(NS-D yfirboðuru\$-yfirboðari)/g' $dir/1540.ntacts.rel-bib.psd # 273.1071

# 1540.ntjohn.rel-bib.psd
sed -i "" 's/(NP-SBJ ekki-ekkert)/(NP-SBJ (Q-N ekki-ekkert))/g' $dir/1540.ntjohn.rel-bib.psd # .414
sed -i "" 's/(NP-SBJ \$tu-þú)/(NP-SBJ (PRO-N \$tu-þú))/g' $dir/1540.ntjohn.rel-bib.psd # .1147, .1148, .1394
sed -i "" 's/(WNP-2 (WPRO-CASE hver-hver))/(WNP-2 (WPRO-N hver-hver))/g' $dir/1540.ntjohn.rel-bib.psd # .1069

# 1593.eintal.rel-oth.psd
sed -i "" 's/(CP-QUE (CP-QUE=2 (NEG Ei-ei)/(CP-QUE (CP-QUE (NEG Ei-ei)/g' $dir/1593.eintal.rel-oth.psd # .17
sed -i "" 's/(MDDI mun-mun)/(MDDI mun\$-mun)/g' $dir/1593.eintal.rel-oth.psd # .15
  # === missing command hera ===
sed -i "" 's/(VAN-D tekinni-taka)/(VAN-D \$tekinni-taka)/g' $dir/1593.eintal.rel-oth.psd # .431
sed -i "" 's/(IP-SUB-PRN=1 (ADVP (ADVR heldur-heldur))/(IP-SUB-PRN (ADVP (ADVR heldur-heldur))/g' $dir/1593.eintal.rel-oth.psd # .455
sed -i "" 's/(ADVP (ADVR eins-eins)))/(ADVP (ADVR \$eins-eins)))/g' $dir/1593.eintal.rel-oth.psd # .604

# 1611.okur.rel-oth.psd
sed -i "" 's/(BEPI s-s))))/(FW s-s))))/' $dir/1611.okur.rel-oth.psd # .11
sed -i "" 's/(IP-SUB-PRN=4 (CONJ og-og) (BEPS sé-vera))/(IP-SUB-PRN (CONJ og-og) (BEPS sé-vera))/' $dir/1611.okur.rel-oth.psd # .45
sed -i "" 's/(IP-SUB-PRN=2 (CONJ og-og)/(IP-SUB-PRN (CONJ og-og)/' $dir/1611.okur.rel-oth.psd # .112
sed -i "" 's/(CODE </heading>))/(CODE </heading>) (. .-.))/' $dir/1611.okur.rel-oth.psd # .124, 125
sed -i "" 's/(IP-SUB-PRN=8 (ADJ-N þrásamlega-þrásamlegur)/(IP-SUB-PRN (ADJ-N þrásamlega-þrásamlegur)/' $dir/1611.okur.rel-oth.psd # .414
sed -i "" 's/(WQ (WADV Hvað-hvað) (Q-N margar-margur))/(WQP (WADV Hvað-hvað) (Q-N margar-margur))/' $dir/1611.okur.rel-oth.psd # .524
sed -i "" 's/(FW et.-et.))/(FW et.-et.) (. .-.))/' $dir/1611.okur.rel-oth.psd # .580
sed -i "" 's/(CONJP (IP-SUB=5 (PP (P auk-auk)/(CONJP (IP-SUB (PP (P auk-auk)/' $dir/1611.okur.rel-oth.psd # .526
# sed -i "" 's/(NP-SBJ (NPR-N Jesús-jesús))/(NP-SBJ (NPR-N Jesús-jesús)/' $dir/1611.okur.rel-oth.psd # .581
# sed -i "" 's/tabtab      (NPR-N kristur-kristur)/tabtab      (NPR-N kristur-kristur))/' $dir/1611.okur.rel-oth.psd # .581
# commented out for now because of error

# 1628.olafuregils.bio-tra.psd
sed -i "" 's/(IP-INF-ZZZ/(IP-INF/' $dir/1628.olafuregils.bio-tra.psd # .205
sed -i "" 's/(N-N \$n-hinn)/(D-N \$n-hinn)/' $dir/1628.olafuregils.bio-tra.psd # 345
sed -i "" 's/(ADJP (N-A bezta-bestur) (CONJ og-og) (ADJS-A beinasta-beinastur))/(ADJP (ADJS-A bezta-bestur) (CONJ og-og) (ADJS-A beinasta-beinastur))/' $dir/1628.olafuregils.bio-tra.psd # 138
sed -i "" 's/(IP-SUB-PRN=2 (CONJ eður-eður)/(IP-SUB-PRN (CONJ eður-eður)/' $dir/1628.olafuregils.bio-tra.psd # 355
sed -i "" 's/(IP-INF (BE \*)/(IP-INF (BE )/' $dir/1628.olafuregils.bio-tra.psd # 755
sed -i "" 's/(CP-QUE-PRN=1 (CONJ og-og)/(CP-QUE-PRN (CONJ og-og)/' $dir/1628.olafuregils.bio-tra.psd # 867

# 1630.gerhard.rel-oth.psd
sed -i "" 's/(IP-IMP-SPE (VBI Sjá-sjá)/(IP-IMP-SPE (VBI Sjá\$-sjá)/g' $dir/1630.gerhard.rel-oth.psd # .901, .2991, .3003
sed -i "" 's/(VBI veit-vita)/(VBI veit\$-veita)/g' $dir/1630.gerhard.rel-oth.psd # .420
sed -i "" 's/(VBDI \$bjó-\$búa)/(VBDI \$bjó-búa)/g' $dir/1630.gerhard.rel-oth.psd # .553
sed -i "" 's/( (CP-QUE (WADVP-1 (WADVP Hvörninn-hvernig))/( (CP-QUE (WADVP-1 (WADV Hvörninn-hvernig))/g' $dir/1630.gerhard.rel-oth.psd # .673
sed -i "" 's/(OTHER-WPRO-N annaðhvört-annaðhvort)/(OTHER+WPRO-N annaðhvört-annaðhvort)/g' $dir/1630.gerhard.rel-oth.psd # .447
sed -i "" 's/(OTHER+WPRO annaðhvört-annaðhvort)/(OTHER+WPRO annaðhvört+annaðhvort)/g' $dir/1630.gerhard.rel-oth.psd # .448

# 1650.illugi-nar-sag.psd
sed -i "" 's/(IP-SMC (NP-SBJ \*)/(IP-SMC (NP-SBJ )/' $dir/1650.illugi-nar-sag.psd # .860
sed -i "" 's/(PP (P (P norðan-norðan) (CONJ og-og) (P austan-austan))/(PP (PP (P norðan-norðan) (CONJ og-og) (P austan-austan))/' $dir/1650.illugi-nar-sag.psd # .1165

# 1659.pislarsaga.bio-aut.psd
sed -i "" 's/(IP-SUB-PRN=2 (CONJ og-og)/(IP-SUB-PRN (CONJ og-og)/' $dir/1659.pislarsaga.bio-aut.psd # .109
sed -i "" 's/(NP-MSR (ADV-Q-N ofmargt-ofmargur))/(NP-MSR (ADV+Q-N ofmargt-ofmargur))/' $dir/1659.pislarsaga.bio-aut.psd # .261

# 1661.indiafari.bio-tra.psd
sed -i "" 's/(N-N stóð-stóð)/(VBDI stóð-standa)/' $dir/1661.indiafari.bio-tra.psd # .36
sed -i "" 's/(Q-G hvers-hver) (N-G \$kyns-kyn)/(Q-G hvers\$-hver) (N-G \$kyns-kyn)/' $dir/1661.indiafari.bio-tra.psd # 28.116
sed -i "" 's/(IP-SUB=1 (NP-SBJ (PRO-N hann-hann))/(IP-SUB (NP-SBJ (PRO-N hann-hann))/' $dir/1661.indiafari.bio-tra.psd # .125
sed -i "" 's/(IP-SUB=1 (VBN sýnt-sýna)/(IP-SUB (VBN sýnt-sýna)/' $dir/1661.indiafari.bio-tra.psd # .125
sed -i "" 's/(N-N bað-bað)/(VBDI bað-biðja)/' $dir/1661.indiafari.bio-tra.psd # .577
sed -i "" 's/(IP-MAT-SENT-BEFORE/(IP-MAT/' $dir/1661.indiafari.bio-tra.psd # .845
sed -i "" 's/(PP (P (P undir-undir) (CONJ og-og) (P af$-af))/(PP (PP (P undir-undir) (CONJ og-og) (P af$-af))/' $dir/1661.indiafari.bio-tra.psd # .950
sed -i "" 's/(NA þénara-þénari))/(N-A þénara-þénari))/' $dir/1661.indiafari.bio-tra.psd # .1000
sed -i "" 's/(CONJP-PRN (CONJP eður-eða)/(CONJP-PRN (CONJ eður-eða)/' $dir/1661.indiafari.bio-tra.psd # .1026
sed -i "" 's/(NÐR-G Helsingborgar-helsingborg)/(NPR-G Helsingborgar-helsingborg)/' $dir/1661.indiafari.bio-tra.psd # .1292

# 1675.armann.nar-fic.psd
sed -i "" 's/(VB \$sjá-\$sjá)/(VB \$sjá-sjá)/g' $dir/1675.armann.nar-fic.psd # 104.446, 108.578
sed -i "" 's/(IP-IMP-SPE (MDPI skal-skulu)/(IP-IMP-SPE (MDPI skal\$-skulu)/g' $dir/1675.armann.nar-fic.psd # 104.446, 108.578
sed -i "" 's/(NP-POS (Q\+N-G allskyns-allskyns) (NS-G handa-hönd))/(NP-POS (N\+Q-G allskyns-allskyns) (NS-G handa-hönd))/g' $dir/1675.armann.nar-fic.psd # 118.909

# 1675.magnus.bio-oth.psd
sed -i "" 's/(FW etc.-etc.))/(FW etc.-etc.) (. .-.))/g' $dir/1675.magnus.bio-oth.psd # .141

# 1680.skalholt.nar-rel.psd
sed -i "" 's/(NP (N-D erkibiskupi-erkibiskup)/(NP (N-D erkibiskupi-erkibiskup) (CONJP/' $dir/1680.skalholt.nar-rel.psd # .48
sed -i "" 's;(NPRS-D capitula<dash/>bræðrum-capitulabróðir);(NPRS-D capitula<dash/>bræðrum-capitulabróðir));' $dir/1680.skalholt.nar-rel.psd # .48
sed -i "" 's/(ITEM item-item)//' $dir/1680.skalholt.nar-rel.psd # .799
sed -i "" 's/( (NP-SBJ *exp*))//' $dir/1680.skalholt.nar-rel.psd # .605

# 1720.vidalin.rel-ser.psd
sed -i "" 's/(IP-SUB-PRN=1 (CONJ og-og)/(IP-SUB-PRN (CONJ og-og)/g' $dir/1720.vidalin.rel-ser.psd # .150
sed -i "" 's;(N-N umskurn-umskurn) (CONJ né-né) (N-N yfir<dash/>húð-yfir<dash/>húð))$;(N-N umskurn-umskurn) (CONJP (CONJ né-né) (N-N yfir<dash/>húð-yfir<dash/>húð)));' $dir/1720.vidalin.rel-ser.psd # .168
sed -i "" 's;(NS-G mennta-menntir) (CONJ og-og) (NS-G mann<dash/>kosta-mann<dash/>kostur)))$;(NS-G mennta-menntir) (CONJP (CONJ og-og) (NS-G mann<dash/>kosta-mann<dash/>kostur))));' $dir/1720.vidalin.rel-ser.psd # .329
sed -i "" 's;(N-N búningur-búningur) (CONJ og-og) (N-N klæða<dash/>snið-klæða<dash/>snið))$;(N-N búningur-búningur) (CONJP (CONJ og-og) (N-N klæða<dash/>snið-klæða<dash/>snið)));' $dir/1720.vidalin.rel-ser.psd # .384
sed -i "" 's;(NP-SBJ (N-N ágirni-ágirni)$;(NP-SBJ (N-N ágirni-ágirni) (CONJP;' $dir/1720.vidalin.rel-ser.psd # .928
sed -i "" 's;(N-N fé<dash/>dráttur-fé<dash/>dráttur)$;(N-N fé<dash/>dráttur-fé<dash/>dráttur));' $dir/1720.vidalin.rel-ser.psd # .928
sed -i "" 's;(N-D ráðleysu-ráðleysi) (CONJ og-og) (N-D hugar<dash/>víli-hugar<dash/>víli)))$;(N-D ráðleysu-ráðleysi) (CONJP (CONJ og-og) (N-D hugar<dash/>víli-hugar<dash/>víli))));' $dir/1720.vidalin.rel-ser.psd # .1064

# 1725.biskupasogur.nar-rel.psd
sed -i "" 's;(- ---);(- <dash/>-<dash/>);g' $dir/1725.biskupasogur.nar-rel.psd # .12, .24
sed -i "" 's/(IP-SUB-PRN=4 (CONJ og-og)/(IP-SUB-PRN (CONJ og-og)/g' $dir/1725.biskupasogur.nar-rel.psd # .168
sed -i "" 's/(NP-SBJ (NPRS-N herra-herra) (NPR-N Guðbrandur-guðbrandur))/(NP-SBJ (NPR-N herra-herra) (NPR-N Guðbrandur-guðbrandur))/g' $dir/1725.biskupasogur.nar-rel.psd # .135
sed -i "" 's/(FRAG-TTT (FW p.32.2-p.32.2) (CODE </paren>)))/(FRAG-TTT (FW p.32.2-p.32.2) (. .-.)))/g' $dir/1725.biskupasogur.nar-rel.psd # .193
sed -i "" 's/((IP-INF=1 (CONJ eður-eður)/(IP-INF (CONJ eður-eður)/g' $dir/1725.biskupasogur.nar-rel.psd # .376
sed -i "" 's/(IP-SUB-PRN=2 (CONJ eður-eður)/(IP-SUB-PRN (CONJ eður-eður)/g' $dir/1725.biskupasogur.nar-rel.psd # .412
sed -i "" 's/(FW offielalis-offielalis))/(FW offielalis-offielalis) (. .-.))/g' $dir/1725.biskupasogur.nar-rel.psd # .533
sed -i "" 's/(PP (P (CONJ *ICH*-4)/(PP (PP (CONJ *ICH*-4)/g' $dir/1725.biskupasogur.nar-rel.psd # .747

# 1745.klim.nar-fic.psd
sed -i "" 's/(IP-SUB-PRN=1 (CONJ og-og)/(IP-SUB-PRN (CONJ og-og)/g' $dir/1745.klim.nar-fic.psd # .106
sed -i "" 's/(CONJP (PRO-D mér-ég))/(NP-SBJ (PRO-D mér-ég))/g' $dir/1745.klim.nar-fic.psd # .289
sed -i "" 's/( (" "-"))//g' $dir/1745.klim.nar-fic.psd # .335

# 1790.fimmbraedra.nar-sag.psd
sed -i "" 's/(VAN \$lögð-\$leggja))/(RP upp\$-upp) (RP \$á\$-á) (VAN \$lögð-leggja))/g' $dir/1790.fimmbraedra.nar-sag.psd # .72
sed -i "" 's/(CONPJ (CONJ og-og)/(CONJP (CONJ og-og)/' $dir/1790.fimmbraedra.nar-sag.psd # .982
sed -i "" 's/(NP-SBJ-ZZZ-2SBJ/(NP-SBJ/' $dir/1790.fimmbraedra.nar-sag.psd # .1198
sed -i "" 's/(WNP-1 (WADVP Hvað-hvað) (ADV lengi-lengi))/(WNP-1 (WADV Hvað-hvað) (ADV lengi-lengi))/' $dir/1790.fimmbraedra.nar-sag.psd # .591

# 1791.jonsteingrims.bio-aut.psd
sed -i "" 's/(NS-N orðin-verða))/(RDN orðin-verða))/' $dir/1791.jonsteingrims.bio-aut.psd # .322
sed -i "" 's/(BE \*)/(BE )/' $dir/1791.jonsteingrims.bio-aut.psd # .398
sed -i "" 's/(NP-SBJ \$ðu-þú)/(NP-SBJ (PRO-N \$ðu-þú))/g' $dir/1791.jonsteingrims.bio-aut.psd # .971
sed -i "" 's/(PRO-C oss-ég)/(PRO-D oss-ég)/g' $dir/1791.jonsteingrims.bio-aut.psd # .461
sed -i "" 's/(IP-SUB-PRN=2 (CONJ og-og)/(IP-SUB-PRN (CONJ og-og)/g' $dir/1791.jonsteingrims.bio-aut.psd # .121
sed -i "" 's/(IP-SUB-PRN=2 (ADVP (ADV þó-þó))/(IP-SUB-PRN (ADVP (ADV þó-þó))/g' $dir/1791.jonsteingrims.bio-aut.psd # .1015
sed -i "" 's/(IP-SUB-PRN=3 (CONJ og-og) (BEPI er-vera))/(IP-SUB-PRN (CONJ og-og) (BEPI er-vera))/g' $dir/1791.jonsteingrims.bio-aut.psd # .114
sed -i "" 's/(IP-SUB-PRN=1 (NP-TMP (NS-D stundum-stundum))/(IP-SUB-PRN (NP-TMP (NS-D stundum-stundum))/g' $dir/1791.jonsteingrims.bio-aut.psd # .1318
sed -i "" 's/(CP-THT-SPE (FW nema-nema)/(CP-THT-SPE (FP nema-nema)/g' $dir/1791.jonsteingrims.bio-aut.psd # .1154

# 1830.hellismenn.nar-sag.psd
sed -i "" 's/(MDPI muntu-munu)/(MDPI mun\$-munu)/g' $dir/1830.hellismenn.nar-sag.psd # .256
sed -i "" 's/(BEDI kómu-koma)/(VBDI kómu-koma)/g' $dir/1830.hellismenn.nar-sag.psd # .1140
sed -i "" 's/(NP-SBJ \*)/(NP-SBJ )/g' $dir/1830.hellismenn.nar-sag.psd # .865

# 1835.jonasedli.sci-nat.psd
sed -i "" 's/(PP (P (P nær-nærri) (CONJ og-og) (P nær-nærri))/(PP (PP (P nær-nærri) (CONJ og-og) (P nær-nærri))/g' $dir/1835.jonasedli.sci-nat.psd # .17

# 1850.piltur.nar-fic.psd
sed -i "" 's/(ADVP-LOC hvervetna-hvervetna)/(ADVP-LOC (ADV hvervetna-hvervetna))/g' $dir/1850.piltur.nar-fic.psd # .12
sed -i "" 's/(NP-SBJ \$tu-þú)/(NP-SBJ (PRO-N \$tu-þú))/g' $dir/1850.piltur.nar-fic.psd # .187, .667
sed -i "" 's/(NP-SBJ \$ðu-þú)/(NP-SBJ (PRO-N \$ðu-þú))/g' $dir/1850.piltur.nar-fic.psd # .192
sed -i "" 's/(IP-SUB=1 (VBN litið-líta)/((IP-SUB (VBN litið-líta)/g' $dir/1850.piltur.nar-fic.psd # .223
sed -i "" 's/(CP-REL (WADVP-4 þegar-þegar)/(CP-REL (WADVP-4 (WADV þegar-þegar))/g' $dir/1850.piltur.nar-fic.psd # .10
sed -i "" 's/(D-MSN hinn-hinn)/(D-N hinn-hinn)/g' $dir/1850.piltur.nar-fic.psd # .17
sed -i "" 's/(NP-SBJ \*)/(NP-SBJ )/g' $dir/1850.piltur.nar-fic.psd # .672, 683
sed -i "" 's/(BE \*)/(BE )/g' $dir/1850.piltur.nar-fic.psd # .990
sed -i "" 's/( (IP-MAT (CONJP (CONJ og-og))/( (IP-MAT (CONJ og-og)/g' $dir/1850.piltur.nar-fic.psd # .1133

# 1882.torfhildur.nar-fic.psd
sed -i "" 's/(N-N Gott-gott)/(ADJ-N Gott-gott)/' $dir/1882.torfhildur.nar-fic.psd # .879

# 1883.voggur.nar-fic.psd
sed -i "" 's/(NPR-G hans-hann)/(PRO-G hans-hann)/g' $dir/1883.voggur.nar-fic.psd # .130

# 1859.hugvekjur.rel-ser.psd
sed -i "" 's/(IP-SUB-PRN=1 (CONJ og-og)/(IP-SUB-PRN (CONJ og-og)/' $dir/1859.hugvekjur.rel-ser.psd # .22
sed -i "" 's/(TO \*)/(TO )/' $dir/1859.hugvekjur.rel-ser.psd # .45, 499
sed -i "" 's/(PRO-N ðu-þú)/(PRO-N $ðu-þú)/' $dir/1859.hugvekjur.rel-ser.psd # .442
sed -i "" 's/(N-D komu-koma)/(VBDI komu-koma)/' $dir/1859.hugvekjur.rel-ser.psd # .707

# 1861.orrusta.nar-fic.psd
sed -i "" 's/(N-N brynjan-brynja)/(N-N brynja\$-brynja)/g' $dir/1861.orrusta.nar-fic.psd # .433
sed -i "" 's/( (IP-MAT (, -)/( (IP-MAT (, ,-,)/g' $dir/1861.orrusta.nar-fic.psd # .530
sed -i "" 's/(IP-SUB-PRN=1 (NP-SBJ (NS-N konur-kona))/(IP-SUB-PRN (NP-SBJ (NS-N konur-kona))/g' $dir/1861.orrusta.nar-fic.psd # .740
sed -i "" 's/(, -)/(, ,-,)/g' $dir/1861.orrusta.nar-fic.psd # .1742
 
# 1882.torfhildur.nar-fic.psd
sed -i "" 's/(PP (P (P í-í) (CONJ og-og) (P með-með))/(PP (PP (P í-í) (CONJ og-og) (P með-með))/g' $dir/1882.torfhildur.nar-fic.psd # .956
sed -i "" 's/IP-SUB-SUB/IP-SUB/g' $dir/1882.torfhildur.nar-fic.psd # .1983
sed -i "" 's/(NP-PRD (ADJA-N bezt-góður))/(NP-PRD (ADJS-N bezt-góður))/g' $dir/1882.torfhildur.nar-fic.psd # .1318
sed -i "" 's/(IP-PPL (NP-OB1 (ADVR-Q-D jafnmörgum-jafnmargur) (NS-D göllum-galli))/(IP-PPL (NP-OB1 (ADVR-D jafnmörgum-jafnmargur) (NS-D göllum-galli))/g' $dir/1882.torfhildur.nar-fic.psd # .1741
sed -i "" 's/(, -)/(, ,-,)/g' $dir/1882.torfhildur.nar-fic.psd # .748

# 1883.voggur.nar-fic.psd
sed -i "" 's/(, -)/(, ,-,)/g' $dir/1883.voggur.nar-fic.psd # .16 o.fl.

# 1888.grimur.nar-fic.psd
sed -i "" 's/(IP-MAT=1 (NP-SBJ (N-N verðið-verð)/(IP-MAT=1 (NP-SBJ (N-N verð\$-verð)/g' $dir/1888.grimur.nar-fic.psd # .20
sed -i "" 's/(IP-SMC (NP-SBJ \*)/(IP-SMC (NP-SBJ )/g' $dir/1888.grimur.nar-fic.psd # .28
sed -i "" 's/(NS-N augun-auga) (D-N \$n-hinn)/(NS-N augu$-auga) (D-N $n-hinn)/g' $dir/1888.grimur.nar-fic.psd # .280
sed -i "" 's/(, -)/(, ,-,)/g' $dir/1888.grimur.nar-fic.psd # .202 o.fl.
sed -i "" 's/(. -))/(. .-.))/g' $dir/1888.grimur.nar-fic.psd # .256 o.fl.

# 1888.vordraumur.nar-fic.psd
sed -i "" 's/(IP-SUB-PRN=3 (CONJ og-og)/(IP-SUB-PRN (CONJ og-og)/g' $dir/1888.vordraumur.nar-fic.psd # .46
sed -i "" 's/	  (NP-SBJ \*con\*)/	  (NP-SBJ )/g' $dir/1888.vordraumur.nar-fic.psd # .400

# 1902.fossar.nar-fic.psd
sed -i "" 's/(PP (P -))//' $dir/1902.fossar.nar-fic.psd # .879
sed -i "" 's/(, -)/(, ,-,)/g' $dir/1902.fossar.nar-fic.psd # .92 o.fl.
sed -i "" 's/(IP-INF-PRN-ELAB (TO \*)/(IP-INF-PRN-ELAB (TO )/g' $dir/1902.fossar.nar-fic.psd # .140
sed -i "" 's/(. -)/(. .-.)/g' $dir/1902.fossar.nar-fic.psd # .510 o.fl.
sed -i "" 's/(, -----)/(, ,-,)/g' $dir/1902.fossar.nar-fic.psd # .822
sed -i "" 's/(- -)//g' $dir/1902.fossar.nar-fic.psd # .872 o.fl.
sed -i "" 's/(PP (P -))//g' $dir/1902.fossar.nar-fic.psd # .879
sed -i "" 's/(NUM-N -)//g' $dir/1902.fossar.nar-fic.psd # .881
sed -i "" 's/(IP-INF-PRN-ELAB (TO \*)/(IP-INF-PRN-ELAB (TO )/g' $dir/1902.fossar.nar-fic.psd # .1024

# 1907.leysing.nar-fic.psd
sed -i "" 's/(IP-MAT-1 (NP-SBJ (D-N Hinir-hinn)/(IP-MAT (NP-SBJ (D-N Hinir-hinn)/' $dir/1907.leysing.nar-fic.psd # .455
sed -i "" 's/(IP-SMC=1 (NP-SBJ (N-N öskuhaugur$-öskuhaugur) (D-N $inn-hinn))/(IP-SMC (NP-SBJ (N-N öskuhaugur$-öskuhaugur) (D-N $inn-hinn))/' $dir/1907.leysing.nar-fic.psd # .455
sed -i "" 's/(IP-MAT=1 (NP-SBJ (NS-N vindhanar$-vindhani) (D-N $nir-hinn))/(IP-MAT (NP-SBJ (NS-N vindhanar$-vindhani) (D-N $nir-hinn))/' $dir/1907.leysing.nar-fic.psd # .455
sed -i "" 's/( (IP-MAT (, -))\n  (ID 1907.LEYSING.NAR-FIC,.1311))//' $dir/1907.leysing.nar-fic.psd # .1311
sed -i "" 's/(TO \*)/(TO )/' $dir/1907.leysing.nar-fic.psd # .1458

# 1908.ofurefli.nar-fic.psd
sed -i "" 's/(CP-QUE-PRN (CP-QUE=1 (WQ hvort-hvort)/(CP-QUE-PRN (CP-QUE (WQ hvort-hvort)/' $dir/1908.ofurefli.nar-fic.psd # .1115

# 1920.arin.rel-ser.psd
sed -i "" 's/(IP-SUB-PRN=4 (CONJ og-og)/(IP-SUB-PRN (CONJ og-og)/g' $dir/1920.arin.rel-ser.psd # .839

# 1985.margsaga.nar-fic.psd
sed -i "" 's/(NP-ADV (D+N-D hinumegin-hinumeginn)/(NP-ADV (N+D-D hinumegin-hinumeginn)/g' $dir/1985.margsaga.nar-fic.psd # .1173

# 1985.sagan.nar-fic.psd
sed -i "" 's/(NP-SBJ \$ðu-þú)/(NP-SBJ (PRO-N \$ðu-þú))/g' $dir/1985.sagan.nar-fic.psd # .494
sed -i "" 's/(NP (N-A skrána-skrá)/(NP (N-A skrá\$-skrá)/g' $dir/1985.sagan.nar-fic.psd # .628
sed -i "" 's/(ADV einu\$-einu)/(ADV einu\$-einu)/g' $dir/1985.sagan.nar-fic.psd # .693
sed -i "" 's/BEBI er-vera/BEPI er-vera/g' $dir/1985.sagan.nar-fic.psd # .772
sed -i "" 's/(N-N \$ið-hinn)/(D-N \$ið-hinn)/g' $dir/1985.sagan.nar-fic.psd # .773
sed -i "" 's/(PP (P af\.-af)/(PP (P af-af)/g' $dir/1985.sagan.nar-fic.psd # .846
# sed -i "" 's///g' $dir/1985.sagan.nar-fic.psd # .1287
sed -i "" 's/(PP (P t.$-t)/(PP (P t.\$-til)/g' $dir/1985.sagan.nar-fic.psd # .1352
sed -i "" 's/(NP (N-G \$d.-d)))/(NP (N-G $d.-dæmis)))/g' $dir/1985.sagan.nar-fic.psd # .1352
sed -i "" 's/(N-N Þula\$-þula) (N-N \$n-hinn))/(N-N Þula\$-þula) (D-N \$n-hinn))/g' $dir/1985.sagan.nar-fic.psd # .1416
sed -i "" 's/(NS-A svefnpoka\$-svefnpoki) (N-A \$na-na))/(NS-A svefnpoka\$-svefnpoki) (D-A \$na-na))/g' $dir/1985.sagan.nar-fic.psd # .1487
sed -i "" 's/(N-N stjúpa\$-stjúpa) (N-N \$n-hinn))/(N-N stjúpa\$-stjúpa) (D-N \$n-hinn))/g' $dir/1985.sagan.nar-fic.psd # .1520
sed -i "" 's/(D-N tal\$-tal) (N-N \$ið-hinn))/(N-N tal\$-tal) (D-N \$ið-hinn))/g' $dir/1985.sagan.nar-fic.psd # .1751

# 2008.mamma.nar-fic.psd
sed -i "" 's/^ (IP-MAT (NP-SBJ (PRO-N Við-ég))/( (IP-MAT (NP-SBJ (PRO-N Við-ég))/g' $dir/2008.mamma.nar-fic.psd # .1
sed -i "" 's/(ID 2008.MAMMA.NAR-FIC,.1)/(ID 2008.MAMMA.NAR-FIC,.1))/g' $dir/2008.mamma.nar-fic.psd # .1
sed -i "" 's/(CODE {COM:threedots})/(. .-.)/g' $dir/2008.mamma.nar-fic.psd # .405
sed -i "" 's/(, -)//g' $dir/2008.mamma.nar-fic.psd # .588
sed -i "" 's/(VBDI Heyr\$/(VBI Heyr\$/g' $dir/2008.mamma.nar-fic.psd # .784
sed -i "" 's/Kaupmannahafnar\./Kaupmannahafnar/g' $dir/2008.mamma.nar-fic.psd # .876
sed -i "" 's/(NP-OB1 (NS-A augun-auga)/(NP-OB1 (NS-A augu\$-auga)/g' $dir/2008.mamma.nar-fic.psd # .1129
sed -i "" 's/\$vel\$/\$vel/g' $dir/2008.mamma.nar-fic.psd # .1286
sed -i "" 's/PRO-N ðu-þú/PRO-N $ðu-þú/' $dir/2008.mamma.nar-fic.psd # .1289
sed -i "" 's/(NP-SBJ (PRO-N \$di-þú))//g' $dir/2008.mamma.nar-fic.psd # .1393
sed -i "" 's/(VBI komi-\$)//g' $dir/2008.mamma.nar-fic.psd # .1393
sed -i "" 's/(NP-SBJ (PRO-N \$di-þú))/(NP-SBJ (PRO-N \$di-þú))/g' $dir/2008.mamma.nar-fic.psd # .1393
# sed -i "" 's/sofandi\./sofandi/g' $dir/2008.mamma.nar-fic.psd # .1746
sed -i "" 's/( (VAG sofandi\.-sofa))//g' $dir/2008.mamma.nar-fic.psd # .1746 (09.03.20: line removed instead of edited)
sed -i "" 's/kallinn\./kallinn/g' $dir/2008.mamma.nar-fic.psd # .1757
sed -i "" 's/Já\./Já/g' $dir/2008.mamma.nar-fic.psd # .1757
sed -i "" 's/hahaha\./hahaha/g' $dir/2008.mamma.nar-fic.psd # .1791
sed -i "" 's/(VBI Koddu-koma)/(VBI Kod\$-koma)/g' $dir/2008.mamma.nar-fic.psd # .1811
sed -i "" 's/(VBI koddu-koma)/(VBI kod\$-koma)/g' $dir/2008.mamma.nar-fic.psd # .1812, .1813

# 2008.ofsi.nar-sag.psd
# sed -i "" '13057, 13058d' $dir/2008.ofsi.nar-sag.psd # .622 Not completely sure why this is here.
sed -i "" 's/\$hitta)/hitta)/g' $dir/2008.ofsi.nar-sag.psd # .313
sed -i "" 's/(CONJP-4 (CONJP eða-eða)/(CONJP-4 (CONJ eða-eða)/g' $dir/2008.ofsi.nar-sag.psd # .318
sed -i "" 's/(N-A \$veginn-vegur))/(N-A \$veg\$-vegur) (D-A \$inn-hinn))/g' $dir/2008.ofsi.nar-sag.psd # .442
sed -i "" 's/(Q-A nokkurntíma-nokkurntími) (N-A \$tíma-tími))/(Q-A nokkurn\$-nokkur) (N-A $tíma-tími))/g' $dir/2008.ofsi.nar-sag.psd # .450
sed -i "" 's/(NRP-N skarði/(NPR-N skarði/g' $dir/2008.ofsi.nar-sag.psd # .734
sed -i "" 's/(VBPI tilheyrum-tilheyra)/(VBPI $heyrum-tilheyra)/' $dir/2008.ofsi.nar-sag.psd # .1152

echo "Done"

# sed -i "" 's///g' $dir/ # .
# sed -i "" 's///g' $dir/ # .
# sed -i "" 's///g' $dir/ # .


# list of files in order (for reference)

# 1150.firstgrammar.sci-lin.psd
# 1150.homiliubok.rel-ser.psd
# 1210.jartein.rel-sag.psd
# 1210.thorlakur.rel-sag.psd
# 1250.sturlunga.nar-sag.psd
# 1250.thetubrot.nar-sag.psd
# 1260.jomsvikingar.nar-sag.psd
# 1270.gragas.law-law.psd
# 1275.morkin.nar-his.psd
# 1300.alexander.nar-sag.psd
# 1310.grettir.nar-sag.psd
# 1325.arni.nar-sag.psd
# 1350.bandamennM.nar-sag.psd
# 1350.finnbogi.nar-sag.psd
# 1350.marta.rel-sag.psd
# 1400.gunnar.nar-sag.psd
# 1400.gunnar2.nar-sag.psd
# 1400.viglundur.nar-sag.psd
# 1450.bandamenn.nar-sag.psd
# 1450.ectorssaga.nar-sag.psd
# 1450.judit.rel-bib.psd
# 1450.vilhjalmur.nar-sag.psd
# 1475.aevintyri.nar-rel.psd
# 1480.jarlmann.nar-sag.psd
# 1525.erasmus.nar-sag.psd
# 1525.georgius.nar-rel.psd
# 1540.ntacts.rel-bib.psd
# 1540.ntjohn.rel-bib.psd
# 1593.eintal.rel-oth.psd
# 1611.okur.rel-oth.psd
# 1628.olafuregils.bio-tra.psd
# 1630.gerhard.rel-oth.psd
# 1650.illugi.nar-sag.psd
# 1659.pislarsaga.bio-aut.psd
# 1661.indiafari.bio-tra.psd
# 1675.armann.nar-fic.psd
# 1675.magnus.bio-oth.psd
# 1675.modars.nar-fic.psd
# 1680.skalholt.nar-rel.psd
# 1720.vidalin.rel-ser.psd
# 1725.biskupasogur.nar-rel.psd
# 1745.klim.nar-fic.psd
# 1790.fimmbraedra.nar-sag.psd
# 1791.jonsteingrims.bio-aut.psd
# 1830.hellismenn.nar-sag.psd
# 1835.jonasedli.sci-nat.psd
# 1850.piltur.nar-fic.psd
# 1859.hugvekjur.rel-ser.psd
# 1861.orrusta.nar-fic.psd
# 1882.torfhildur.nar-fic.psd
# 1883.voggur.nar-fic.psd
# 1888.grimur.nar-fic.psd
# 1888.vordraumur.nar-fic.psd
# 1902.fossar.nar-fic.psd
# 1907.leysing.nar-fic.psd
# 1908.ofurefli.nar-fic.psd
# 1920.arin.rel-ser.psd
# 1985.margsaga.nar-fic.psd
# 1985.sagan.nar-fic.psd
# 2008.mamma.nar-fic.psd
# 2008.ofsi.nar-sag.psd
