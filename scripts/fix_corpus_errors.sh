#!/bin/bash

'''
fix_corpus_error.sh
22.07.19
Hinrik Hafsteinsson
Þórunn Arnardóttir

Script for fixing various presumed errors in IcePaHC corpus files (.psd)

Any machine-specific paths must be specified before use
'''

# dir="./testing/corpora/icepahc-v0.9/psd"
dir="./testing/corpora/icecorpus/psd"

# 1150.homiliubok.rel-ser.psd
sed -i "" 's/(WADJ hversu-hversu)/(WADV hversu-hversu)/g' $dir/1150.homiliubok.rel-ser.psd # .105
sed -i "" 's/(VBI \$gef-gefa)/(VBI \$gef\$-gefa)/g' $dir/1150.homiliubok.rel-ser.psd # .1648
sed -i "" 's/(NP-SBJ \$tu-þú)/(NP-SBJ (PRO-N \$tu-þú))/g' $dir/1150.homiliubok.rel-ser.psd # .246
sed -i "" 's/(NP-ADT járnum-járna)/(NP-ADT (NS-D járnum-járn))/g' $dir/1150.homiliubok.rel-ser.psd # .410

#1210.jartein.rel-sag.psd
sed -i "" 's/(IP-MAT-KOMINN/(IP-MAT/' $dir/1210.jartein.rel-sag.psd # .321
sed -i "" 's/(N-A sylgju\$)/(N-A sylgju\$-sylgja)/' $dir/1210.jartein.rel-sag.psd # .552

# 1250.sturlunga.nar-sag.psd
sed -i "" 's/NP-A/NS-A/g' $dir/1250.sturlunga.nar-sag.psd # 135.1604
sed -i "" 's/(IP-SUB (ADVP-OC/(IP-SUB (ADVP-LOC/g' $dir/1250.sturlunga.nar-sag.psd # 448.2121
sed -i "" 's/(NP-SBJ \$tu-þú)/(NP-SBJ (PRO-N \$tu-þú))/g' $dir/1250.sturlunga.nar-sag.psd # 393.186, 419.994, 421.1061, 423.1171
sed -i "" 's/(WNP-N-1 hver-hver/(WNP-1 (WPRO-N hver-hver)/' $dir/1250.sturlunga.nar-sag.psd # 427.1265

#1250.thetubrot.nar-sag.psd
sed -i "" 's/(NP-PRN-LL/(NP-PRN/' $dir/1250.thetubrot.nar-sag.psd # .151

# 1310.grettir.nar-sag.psd
sed -i "" 's/(N-S/(N-G/g' $dir/1310.grettir.nar-sag.psd # .95

# 1325.arni.nar-sag.psd
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
sed -i "" 's/(NP-SBJ \$ú-þú)/(NP-SBJ (PRO-N \$tu-þú))/g' $dir/1350.finnbogi.nar-sag.psd # .890
sed -i "" 's/(NP-PRN Rauður-rauður)/(NPR-N Rauður-rauður)/g' $dir/1350.finnbogi.nar-sag.psd # .1986
sed -i "" 's/(CP-COM/(NP-COM/' $dir/1350.finnbogi.nar-sag.psd # .2073

# 1450.ectorssaga.nar-sag.psd
sed -i "" 's/(ADJP-OC/(ADJP-LOC/g' $dir/1450.ectorssaga.nar-sag.psd # .1853

# 1450.vilhjalmur.nar-sag.psd
sed -i "" 's/(NP-SBJ \$tu-þú)/(NP-SBJ (PRO-N \$tu-þú))/g' $dir/1450.vilhjalmur.nar-sag.psd # .254
sed -i "" 's/(IP-SUB-SPE (NP-SBJ \$ú-þú)/(IP-SUB-SPE (NP-SBJ (PRO-N \$ú-þú))/g' $dir/1450.vilhjalmur.nar-sag.psd # .774
sed -i "" 's/(NP-OB2 ICH\*-1)/(NP-OB2 \*ICH\*-1)/g' $dir/1450.vilhjalmur.nar-sag.psd # .1008
sed -i "" 's/(NS-N rifin-rifinn)/(NS-N rif\$-rif)/g' $dir/1450.vilhjalmur.nar-sag.psd # 87.1768

# 1525.erasmus.nar-sag.psd
sed -i "" 's/(NP-SBJ \$u-þú)/(NP-SBJ (PRO-N \$u-þú))/g' $dir/1525.erasmus.nar-sag.psd # .88

# 1525.georgius.nar-rel.psd
sed -i "" 's/NPÖ-SBJ/NP-SBJ/g' $dir/1525.georgius.nar-rel.psd # .392
sed -i "" 's/(IP-MAT-KOMINN/(IP-MAT/' $dir/1525.georgius.nar-rel.psd # .743

# 1540.ntjohn.rel-bib.psd
sed -i "" 's/(NP-SBJ ekki-ekkert)/(NP-SBJ (Q-N ekki-ekkert))/g' $dir/1540.ntjohn.rel-bib.psd # .414
sed -i "" 's/(NP-SBJ \$tu-þú)/(NP-SBJ (PRO-N \$tu-þú))/g' $dir/1540.ntjohn.rel-bib.psd # .1147, .1148, .1394

#1628.olafuregils.bio-tra.psd
sed -i "" 's/(IP-INF-ZZZ/(IP-INF/' $dir/1628.olafuregils.bio-tra.psd # .205

#1661.indiafari.bio-tra.psd
sed -i "" 's/(IP-MAT-SENT-BEFORE/(IP-MAT/' $dir/1661.indiafari.bio-tra.psd # .845

#1790.fimmbraedra.nar-sag.psd
sed -i "" 's/(NP-SBJ-ZZZ-2SBJ/(NP-SBJ/' $dir/1790.fimmbraedra.nar-sag.psd # .1198

# 1791.jonsteingrims.bio-aut.psd
sed -i "" 's/(NP-SBJ \$ðu-þú)/(NP-SBJ (PRO-N \$ðu-þú))/g' $dir/1791.jonsteingrims.bio-aut.psd # .971

# 1850.piltur.nar-fic.psd
sed -i "" 's/(NP-SBJ \$tu-þú)/(NP-SBJ (PRO-N \$tu-þú))/g' $dir/1850.piltur.nar-fic.psd # .187, .667
sed -i "" 's/(NP-SBJ \$ðu-þú)/(NP-SBJ (PRO-N \$ðu-þú))/g' $dir/1850.piltur.nar-fic.psd # .192

# 1883.voggur.nar-fic.psd
sed -i "" 's/(NPR-G hans-hann)/(PRO-G hans-hann)/g' $dir/1883.voggur.nar-fic.psd # .130

# 1861.orrusta.nar-fic.psd
sed -i "" 's/(N-N brynjan-brynja)/(N-N brynja\$-brynja)/g' $dir/1861.orrusta.nar-fic.psd # .433

# 1882.torfhildur.nar-fic.psd
sed -i "" 's/IP-SUB-SUB/IP-SUB/g' $dir/1882.torfhildur.nar-fic.psd # .1983

# 1985.sagan.nar-fic.psd
sed -i "" 's/BEBI er-vera/BEPI er-vera/g' $dir/1985.sagan.nar-fic.psd # .772
sed -i "" 's/(NP-SBJ \$ðu-þú)/(NP-SBJ (PRO-N \$ðu-þú))/g' $dir/1985.sagan.nar-fic.psd # .494

# 2008.mamma.nar-fic.psd
sed -i "" 's/(VBDI Heyr\$/(VBI Heyr\$/g' $dir/2008.mamma.nar-fic.psd # .784
sed -i "" 's/(VBI koddu-koma)/(VBI kod\$-koma)/g' $dir/2008.mamma.nar-fic.psd # .1811, .1812, .1813

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
