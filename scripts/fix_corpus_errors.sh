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

# 1150.homiliubok fixes
sed -i "" 's/(VBI \$gef-gefa)/(VBI \$gef\$-gefa)/g' $dir/1150.homiliubok.rel-ser.psd # .1648
sed -i "" 's/(NP-SBJ \$tu-þú)/(NP-SBJ (PRO-N \$tu-þú))/g' $dir/1150.homiliubok.rel-ser.psd # .246
sed -i "" 's/(NP-ADT járnum-járna)/(NP-ADT (NS-D járnum-járn))/g' $dir/1150.homiliubok.rel-ser.psd # .410

# 1250.sturlunga fixes
sed -i "" 's/(IP-SUB (ADVP-OC/IP-SUB (ADVP-LOC/g' $dir/1250.sturlunga.nar-sag.psd # 448.2121

# 1325.arni fixes
sed -i "" 's/IP-SUB-=17/IP-SUB=17/g' $dir/1325.arni.nar-sag.psd # .927

# 1350.bandamenn fixes
sed -i "" 's/NP-AB1/NP-OB1/g' $dir/1350.bandamennM.nar-sag.psd # .558
sed -i "" 's/IP-SUB-SPE3/IP-SUB-SPE-3/g' $dir/1350.bandamennM.nar-sag.psd # .961
sed -i "" 's/D-N $ðu/PRO-N $ðu/g' $dir/1350.bandamennM.nar-sag.psd # .886
sed -i "" 's/D-N $tu/PRO-N $tu/g' $dir/1350.bandamennM.nar-sag.psd # .909

# 1450.ectorssaga fixes
sed -i "" 's/(ADJP-OC/ADJP-LOC/g' $dir/1450.ectorssaga.nar-sag.psd # .1853

# 1450.vilhjalmur fixes
sed -i "" 's/(NS-N rifin-rifinn)/(NS-N rif\$-rif)/g' $dir/1450.vilhjalmur.nar-sag.psd # 87.1768

# 1525.georgius fixes
sed -i "" 's/NPÖ-SBJ/NP-SBJ/g' $dir/1525.georgius.nar-rel.psd # .392

# 1861.orrusta fixes
sed -i "" 's/(N-N brynjan-brynja)/(N-N brynja\$-brynja)/g' $dir/1861.orrusta.nar-fic.psd # .433

# 1882.torfhildur fixes
sed -i "" 's/IP-SUB-SUB/IP-SUB/g' $dir/1882.torfhildur.nar-fic.psd # .1983

# 1985.sagan fixes
sed -i "" 's/BEBI er-vera/BEPI er-vera/g' $dir/1985.sagan.nar-fic.psd # .772

# 2008.mamma fixes
sed -i "" 's/(VBDI Heyr\$/(VBI Heyr\$/g' $dir/2008.mamma.nar-fic.psd # .784
sed -i "" 's/(VBI koddu-koma)/(VBI kod$-koma)/g' $dir/2008.mamma.nar-fic.psd # .1811, .1812, .1813

# sed -i "" 's///g' $dir/
# sed -i "" 's///g' $dir/
# sed -i "" 's///g' $dir/
