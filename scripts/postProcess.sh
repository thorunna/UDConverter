#!/usr/bin/env bash

'''
01.08.19
Hinrik Hafsteinsson
Þórunn Arnardóttir

Script for postprocessing IcePaHC Conll-U files
Machine-specific paths must be specified before use
'''


dir="./testing/CoNLLU_output"

for file in $dir/*; do
  echo "Working on file: ${file##*/}"
  # TODO:
  #   - ADD SCRIPT FOR renaming abbrevations to correct tokens/lemmas in:
  #       1725.biskupasogur.nar-rel.psd ('Þ.b.')
  #       1985.sagan.nar-fic.conllu ('m.a.s.')
  #       1985.margsaga.nar-fic.conllu ('amk')
  #       1920.arin.rel-ser.conllu ('þ.e.a.s.')
  #   - Possibly remove $ from CoNLLU files in 'því$ $að' and 'þó$ $að'
  #     in e.g. 1260.jomsvikingar.nar-sag.conllu
  #   - Join ON clitics (e.g. þar$ $s = þar sem) in same manner as verb clitics
  #       Along with this:
  #        - Þann$ $veg in 1525.erasmus.nar-sag.conllu
  #   - ONE+Q-G changed to ADV (and possibly others) if joined ('einhversstaðar')
  python3 scripts/join_verb_clitics.py $file
done
