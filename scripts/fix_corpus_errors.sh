#!/bin/bash

'''
fix_corpus_error.sh
22.07.19
Hinrik Hafsteinsson
Þórunn Arnardóttir

Script for fixing various presumed errors in IcePaHC corpus files (.psd)

Any machine-specific paths must be specified before use
'''

dir="./testing/corpora/icepahc-v0.9/psd"

# 1150.homiliubok.rel-ser.psd
sed -i "" 's/(WADJ hversu-hversu)/(WADV hversu-hversu)/g' $dir/1150.homiliubok.rel-ser.psd # .105
sed -i "" 's/(VBI \$gef-gefa)/(VBI \$gef\$-gefa)/g' $dir/1150.homiliubok.rel-ser.psd # .1648
sed -i "" 's/(NP-SBJ \$tu-þú)/(NP-SBJ (PRO-N \$tu-þú))/g' $dir/1150.homiliubok.rel-ser.psd # .246
sed -i "" 's/(NP-ADT járnum-járna)/(NP-ADT (NS-D járnum-járn))/g' $dir/1150.homiliubok.rel-ser.psd # .410

# 1250.sturlunga.nar-sag.psd
sed -i "" 's/NP-A/NS-A/g' $dir/1250.sturlunga.nar-sag.psd # 135.1604
sed -i "" 's/(IP-SUB (ADVP-OC/(IP-SUB (ADVP-LOC/g' $dir/1250.sturlunga.nar-sag.psd # 448.2121
sed -i "" 's/(NP-SBJ $tu-þú)/(NP-SBJ (PRO-N $tu-þú))/g' $dir/1250.sturlunga.nar-sag.psd # 393.186, 419.994, 421.1061, 423.1171

# 1325.arni.nar-sag.psd
sed -i "" 's/IP-SUB-=17/IP-SUB=17/g' $dir/1325.arni.nar-sag.psd # .927

# 1350.bandamennM.nar-sag.psd
sed -i "" 's/NP-AB1/NP-OB1/g' $dir/1350.bandamennM.nar-sag.psd # .558
sed -i "" 's/IP-SUB-SPE3/IP-SUB-SPE-3/g' $dir/1350.bandamennM.nar-sag.psd # .961
sed -i "" 's/D-N $ðu/PRO-N $ðu/g' $dir/1350.bandamennM.nar-sag.psd # .886
sed -i "" 's/D-N $tu/PRO-N $tu/g' $dir/1350.bandamennM.nar-sag.psd # .909

# 1450.ectorssaga.nar-sag.psd
sed -i "" 's/(ADJP-OC/ADJP-LOC/g' $dir/1450.ectorssaga.nar-sag.psd # .1853

# 1450.vilhjalmur.nar-sag.psd
sed -i "" 's/(NP-SBJ $tu-þú)/(NP-SBJ (PRO-N $tu-þú))/g' $dir/1450.vilhjalmur.nar-sag.psd # .254
sed -i "" 's/(IP-SUB-SPE (NP-SBJ $ú-þú)/(IP-SUB-SPE (NP-SBJ (PRO-N $ú-þú))/g' $dir/1450.vilhjalmur.nar-sag.psd # .774
sed -i "" 's/(IP-INF-SPE (NP-OB2 ICH*-1)/(IP-INF-SPE (NP-OB2 *ICH*-1)/g' $dir/1450.vilhjalmur.nar-sag.psd # .1008
sed -i "" 's/(NS-N rifin-rifinn)/(NS-N rif\$-rif)/g' $dir/1450.vilhjalmur.nar-sag.psd # 87.1768

# 1525.erasmus.nar-sag.psd
sed -i "" 's/(NP-SBJ $tu-þú)/(NP-SBJ (PRO-N $tu-þú))/g' $dir/1525.erasmus.nar-sag.psd # .88

# 1525.georgius.nar-rel.psd
sed -i "" 's/NPÖ-SBJ/NP-SBJ/g' $dir/1525.georgius.nar-rel.psd # .392

# 1540.ntjohn.rel-bib.psd
sed -i "" 's/(NP-SBJ ekki-ekkert)/(NP-SBJ (Q-N ekki-ekkert))/g' $dir/1540.ntjohn.rel-bib.psd # .414
sed -i "" 's/(NP-SBJ $tu-þú)/(NP-SBJ (PRO-N $tu-þú))/g' $dir/1540.ntjohn.rel-bib.psd # .1147, .1148, .1394

# 1861.orrusta.nar-fic.psd
sed -i "" 's/(N-N brynjan-brynja)/(N-N brynja\$-brynja)/g' $dir/1861.orrusta.nar-fic.psd # .433

# 1882.torfhildur.nar-fic.psd
sed -i "" 's/IP-SUB-SUB/IP-SUB/g' $dir/1882.torfhildur.nar-fic.psd # .1983

# 1985.sagan.nar-fic.psd
sed -i "" 's/BEBI er-vera/BEPI er-vera/g' $dir/1985.sagan.nar-fic.psd # .772

# 2008.mamma.nar-fic.psd
sed -i "" 's/(VBDI Heyr\$/(VBI Heyr\$/g' $dir/2008.mamma.nar-fic.psd # .784
sed -i "" 's/(VBI koddu-koma)/(VBI kod$-koma)/g' $dir/2008.mamma.nar-fic.psd # .1811, .1812, .1813

# sed -i "" 's///g' $dir/
# sed -i "" 's///g' $dir/
# sed -i "" 's///g' $dir/
