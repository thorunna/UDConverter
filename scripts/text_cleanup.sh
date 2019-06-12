#!/bin/bash

# HH Path:
# ./testing/corpora/icepahc-v0.9/psd/*.psd

# ÞA Path:
# ../icecorpus/finished/*.psd

./scripts/rm-code.prl $1 > $2

#Eyða (CODE...)
sed -i "" 's/(CODE[ {}*<>a-zA-Z0-9a-zA-ZþæðöÞÆÐÖáéýúíóÁÉÝÚÍÓ\.$_:-?/]*)//g' $2 #./testing/corpora/icepahc-v0.9/psd_orig/*.psd
#Eyða auðri línu
sed -i "" '/^$/d' $2 #./testing/corpora/icepahc-v0.9/psd_orig/*.psd
#Eyða línu sem inniheldur '(ID'
sed -i "" '/(ID/d' $2 #./testing/corpora/icepahc-v0.9/psd_orig/*.psd
#Eyða öllum '( '
sed -i "" 's/( //g' $2 #./testing/corpora/icepahc-v0.9/psd_orig/*.psd

# sed -i "" 's/) //g' ./testing/corpora/icepahc-v0.9/psd_orig/*.psd
