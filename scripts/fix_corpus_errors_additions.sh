#!/bin/bash

echo '''
08.01.21
Hinrik Hafsteinsson
Þórunn Arnardóttir

fix_corpus_error.sh

Script for fixing various presumed errors in additional IcePaHC corpus files (.psd)
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

## Additions2019

# althingi/bo/2014/G-33-4569636.psd
sed -i "" 's/(IP-SUB (IP-SUB=1 (NP-SBJ (N-D fórnfýsi-fórnfýsi)/(IP-SUB (IP-SUB (NP-SBJ (N-D fórnfýsi-fórnfýsi)/g' $dir/G-33-4569636.psd
sed -i "" 's/(IP-SUB=1 (HVPI hefur-hafa)/(IP-SUB (HVPI hefur-hafa)/g' $dir/G-33-4569636.psd

# althingi/bo/2014/G-33-4669345
sed -i "" 's/(IP-INF-PRN-ELAB (TO \*)/(IP-INF-PRN-ELAB (TO )/g' $dir/G-33-4669345.psd

# althingi/bo/2014/G-33-4893594
sed -i "" 's/(IP-INF-PRN-ELAB (TO \*)/(IP-INF-PRN-ELAB (TO )/g' $dir/G-33-4893594.psd

# althingi/bo/2015/G-33-4651739
sed -i "" 's/(IP-INF-PRN=1 (CODE {COM:OB1})/(IP-INF-PRN (CODE {COM:OB1})/g' $dir/G-33-4651739.psd

# althingi/hhg/2013/G-33-4591478
sed -i "" 's/(IP-SUB=1 (ADVP (ADV vissulega-vissulega))/(IP-SUB (ADVP (ADV vissulega-vissulega))/g' $dir/G-33-4591478.psd

# althingi/hhg/2013/G-33-4677138
sed -i "" 's/(CONJP (IP-SUB=2 (ADVP (ADVR heldur-heldur))/(CONJP (IP-SUB (ADVP (ADVR heldur-heldur))/g' $dir/G-33-4677138.psd

# althingi/hhg/2013/G-33-4705680
sed -i "" 's/(IP-SUB-PRN=2 (ADVP-TMP (ADV þá-þá))/(IP-SUB-PRN (ADVP-TMP (ADV þá-þá))/g' $dir/G-33-4705680.psd

# althingi/hhg/2013/G-33-4737686
sed -i "" 's/(IP-INF (TO \*)/(IP-INF (TO )/g' $dir/G-33-4737686.psd

# althingi/hhg/2013/G-33-4833012
sed -i "" 's/(IP-SUB-SPE=2 (MDPI Getum-geta)/(IP-SUB-SPE (MDPI Getum-geta)/g' $dir/G-33-4833012.psd

# althingi/hhg/2013/G-33-4836659
sed -i "" 's/(IP-SUB-PRN=1 (IP-SUB (NP-ADV (OTHER-G annars-annar) (N-G vegar-vegur))/(IP-SUB-PRN (IP-SUB (NP-ADV (OTHER-G annars-annar) (N-G vegar-vegur))/g' $dir/G-33-4836659.psd

# althingi/hhg/2013/G-33-4854491
sed -i "" 's/(IP-SUB-PRN=3 (ADVP (ADV sérstaklega-sérstaklega))/(IP-SUB-PRN (ADVP (ADV sérstaklega-sérstaklega))/g' $dir/G-33-4854491.psd

# althingi/hhg/2013/G-33-4916517
sed -i "" 's/(PP (P \*)/(PP (P )/g' $dir/G-33-4916517.psd

# althingi/hhg/2013/G-33-4916520
sed -i "" 's/(IP-INF (TO \*)/(IP-INF (TO )/g' $dir/G-33-4916520.psd

# althingi/sjs/2013/G-33-4736548
sed -i "" 's/(IP-SUB-PRN=1 (NP-ADV (Q-A alla-allur) (NS-A vega-vegur))/(IP-SUB-PRN (NP-ADV (Q-A alla-allur) (NS-A vega-vegur))/g' $dir/G-33-4736548.psd

# althingi/sjs/2013/G-33-4577317
sed -i "" 's/(IP-INF-PRN-ELAB (TO \*)/(IP-INF-PRN-ELAB (TO )/g' $dir/G-33-4577317.psd

# althingi/sjs/2013/G-33-4594976
sed -i "" 's/(IP-INF-PRN-ELAB (TO \*)/(IP-INF-PRN-ELAB (TO )/g' $dir/G-33-4594976.psd

# althingi/sjs/2013/G-33-4691402
sed -i "" 's/(IP-INF-PRN-ELAB (TO \*)/(IP-INF-PRN-ELAB (TO )/g' $dir/G-33-4691402.psd

# althingi/tkg/2011/G-33-4522153
sed -i "" 's/(IP-SUB-PRN=2 (NEG ekki-ekki)/(IP-SUB-PRN (NEG ekki-ekki)/g' $dir/G-33-4522153.psd
sed -i "" 's/(IP-INF-PRN-ELAB (TO \*)/(IP-INF-PRN-ELAB (TO )/g' $dir/G-33-4522153.psd

# althingi/tkg/2011/G-33-4626061
sed -i "" 's/(IP-INF (TO \*)/(IP-INF (TO )/g' $dir/G-33-4626061.psd

# althingi/tkg/2011/G-33-4659893
sed -i "" 's/									       (CP-THT (C (CODE {að}))//g' $dir/G-33-4659893.psd
sed -i "" 's/										       (IP-SUB (ADJP *T*-2)//g' $dir/G-33-4659893.psd
sed -i "" 's/											       (NP-SBJ *exp*)//g' $dir/G-33-4659893.psd
sed -i "" 's/											       (BEPS (CODE {sé}))))//g' $dir/G-33-4659893.psd

# ruv/esp/2016/G-2-1033175
sed -i "" 's/(IP-INF-SPE-1 (TO \*)/(IP-INF-SPE-1 (TO )/g' $dir/G-2-1033175.psd

# ruv/tgs/2016/G-2-1031601
sed -i "" 's/( (CODE *ZZZ_MISS_CP*)/(/g' $dir/G-2-1031601.psd
