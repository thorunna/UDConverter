#!/bin/bash

# September 2019
# Hinrik Hafsteinsson
#
# Script for joining tokens 'einu$' and '$sinni' in IcePaHC corpus files.
# Called from 'text_cleanup.sh' script


file=$1

sed -i "" 's/(NP-MSR (ONE-D einu\$-einn) (N-D \$sinni-sinni))/(NP-MSR (ADV einusinni-einusinni))/g' $file
sed -i "" 's/(NP-TMP (ONE-D einu\$-einn) (N-D \$sinni-sinni))/(NP-TMP (ADV einusinni-einusinni))/g' $file
sed -i "" 's/(NP-MSR (ONE-D Einu\$-einn) (N-D \$sinni-sinni))/(NP-MSR (ADV Einusinni-einusinni))/g' $file
sed -i "" 's/(NP-TMP (ONE-D Einu\$-einn) (N-D \$sinni-sinni))/(NP-TMP (ADV Einusinni-einusinni))/g' $file
sed -i "" 's/(NP-MSR (ADV einu\$-einu) (N-D \$sinni-sinni))/(NP-TMP (ADV einusinni-einusinni))/g' $file

(NP-MSR (ADV einu$-einu) (N-D $sinni-sinni))
