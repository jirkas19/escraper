Engeto 3 projekt

Program vyhledává a ukládá data z parlamentních voleb 2017.

použité knihovny jsou uvedeny v souboru requirments.txt
k instalaci knihoven použijte v terminálu následující příkaz
pip install -r requirments.txt

Ke spuštění programu je třeba do terminálu zadat tři proměnné.
První je název souboru. (engeto_3.py)
Druhá je url adresa.
Třetí název souboru k ukládání dat. (volby.csv)

Ukázka:
Spuštění programu
do terminálu zadám
python engeto_3.py volby.csv https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=3&xnumnuts=3107

Průběh:
stahuji data z https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=3&xnumnuts=3107
zapisuji data do souboru volby.csv

Částečný výstup:
číslo	      název	      Voliči v seznamu	Vydané obálky	Platné hlasy…
563251	Balkova Lhota	102	              69        	69
563366	Bečice	      63	              52	           52
……
