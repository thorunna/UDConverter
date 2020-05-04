# UD - Samantekt á hugbúnaðinum (06.03.20)
## Keyrsluröð:
Í breytingarferli. Eins og er (06.03.20) annaðhvort:
1. `text_cleanup.sh`
2. `convert.py`
3. `postProcess.sh`

Eða:
1. `text_cleanup.sh`
2. `convert.py`

## Forritseiningar
### `depender.py`
 - Les inn IcePaHC tré og skilar venslagrafi fyrir það (UD-skema) 
### `relations.py`
- Inniheldur fall sem ákvarðar gerð vensla og er notað í depender.py

### `features.py`
**ATH óklárað**
- Finnur UD þætti út frá OTB marki orðs
- Ber saman CoNLL-U skrá og markaða textaskrá hennar og finnur rétt mark á orð
- Þarf að hafa markaðan texta úr hverri IcePaHC skrá fyrir sig til að virka sjá https://github.com/thorunna/UD/tree/master/taggers/tagged
- Ef CoNLL-U textinn breytist efnislega fyrir lok verkefnisins þarf að endurmarka hann. Það er sér skrifta sem undirbýr skrárnar til þess

### `joiners.py`
- Inniheldur föll sem annars vegar sameinar liði og orð í .psd skrám og hins vegar sameinar orð í conllu skrám

### `rules.py`
- Inniheldur reglur sem eru notaðar víðs vegar í öðrum skriftum

## Skriftur
### `convert.py`
- Kallar á depender.py módulinn og skrifar út .conllu skrárnar fyrir hverja IcePaHC skrá
### `text_cleanup.sh` 
- Forvinnur IcePaHC skrárnar og gerir þær tilbúnar fyrir convert.py og depender.
### `join_psd.py`
- Sameinar alls konar liði og orð í .psd skrám með því að kalla á mismunandi föll í joiners.py módulnum
### `postProcess.sh`
- Vinnur úr eftirstöðuatriðum í CoNLL-U skránum

### `join_conllu.py`
- kallar á föll í joiners.py til að sameina orð í CoNLL-U skráum (t.d. Sagnir og snýkla) 
- Í vinnslu: Sameinar setningar í CoNLL-U skrám út frá greinarmerkjum

### `rename_conllu.py`
- Kallar á features.py og setur inn UD-þætti orðs ásamt OTB-marki í síðasta sæti hverrar línu
- Endurnefnir stök orð í CoNLL-U skrám, t.d. sumar skammstafanir 
