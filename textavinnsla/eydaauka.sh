#!/bin/bash

#Eyða auðri línu
sed -i '/^$/d' ../../icecorpus/finished/*.psd
#Eyða línu sem inniheldur '(ID'
sed -i '/(ID/d' ../../icecorpus/finished/*.psd
#Eyða öllum '( '
sed -i 's/( //g' ../../icecorpus/finished/*.psd