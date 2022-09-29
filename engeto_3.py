"""

projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Jiří Sedlo

email: jirkas1199@seznam.cz

"""
import requests
import csv
import sys
from bs4 import BeautifulSoup as BS


# "url=https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=3&xnumnuts=3107"
def obal():
    if len(sys.argv) != 3:
        print("špatný počet proměnných")
    else:
        hlavni(sys.argv[1], sys.argv[2])


def obsah_obci(urr):
    rr = requests.get(urr)
    # print(rr.status_code]
    soupp = BS(rr.content, 'html.parser')
    data_obce = []
    tab1 = soupp.find_all('td', headers="sa2")
    for i in tab1:
        data_obce.append(i.string)
    tab2 = soupp.find_all('td', headers="sa3")
    for i in tab2:
        b = i.string  # vydané obálky
        data_obce.append(b)
    tab3 = soupp.find_all('td', headers="sa5")
    for i in tab3:
        c = i.string  # platné hlasy
        data_obce.append(c)
    tab4 = soupp.find_all('td', headers="t1sa2 t1sb3")
    for i in tab4:
        strany1 = i.string  # hlasy stran
        data_obce.append(strany1)
    tab5 = soupp.find_all('td', headers="t2sa2 t2sb3")
    for i in tab5:
        strany2 = i.string
        data_obce.append(strany2)
    return data_obce


def prvni_radek_excelu(url1):
    r1 = requests.get(url1)  # stránka s obcemi
    nazvy_sloupcu = []
    soup1 = BS(r1.content, 'html.parser')
    hledejt1 = soup1.select("table.table")[0]
    hl = [a["href"] for a in hledejt1.select("a[href]")]
    link = "https://volby.cz/pls/ps2017nss/" + hl[0]
    r2 = requests.get(link)  # stránka se statistikou z volební oblasti
    soup2 = BS(r2.content, 'html.parser')
    bunka1 = soup1.find('th', id="t1sb1").get_text()  # výtah textu z vyhledaného obsahu
    nazvy_sloupcu.append(bunka1)
    bunka2 = soup1.find('th', id="t1sb2").get_text()
    nazvy_sloupcu.append(bunka2)
    bunka3 = soup2.find('th', id="sa2").get_text()
    b3 = bunka3[:6] + ' ' + bunka3[6:]  # mezera mezi slovy. break tag byl na stránce použit bez mezery
    nazvy_sloupcu.append(b3)
    bunka4 = soup2.find('th', id="sa3").get_text()
    b4 = bunka4[:6] + ' ' + bunka4[6:]
    nazvy_sloupcu.append(b4)
    bunka5 = soup2.find('th', id="sa6").get_text()
    b5 = bunka5[:6] + ' ' + bunka5[6:]
    nazvy_sloupcu.append(b5)
    tab4 = soup2.find_all('td', headers="t1sa1 t1sb2")  # názvy stran z první půle tabulky
    for i in tab4:
        nazvy_sloupcu.append(i.string)
    tab5 = soup2.find_all('td', headers="t2sa1 t2sb2")  # názvy stran z druhé půle tabulky
    for i in tab5:
        nazvy_sloupcu.append(i.string)
    return nazvy_sloupcu


def vytah_obci(url):
    r = requests.get(url)
    print(r.status_code)  # navázané spojení
    soup = BS(r.content, 'html.parser')  # formátuj html
    obce1 = soup.find_all("a", {"class": "cislo"})  # hledej tg tag
    print(obce1)
    hledejt1 = soup.select("table.table")[0]  # hledej první tabulku
    hledejt2 = soup.select("table.table")[1]
    hledejt3 = soup.select("table.table")[2]
    l1 = [a["href"] for a in hledejt1.select("a[href]")]  # vytáhni odkazy z první tabulky
    l2 = [a["href"] for a in hledejt2.select("a[href]")]
    l3 = [a["href"] for a in hledejt3.select("a[href]")]
    links = l1 + l2 + l3
    volby = []
    for i, j in enumerate(links):
        if i % 2 == 0:  # ulož každý druhý odkaz do listu(odkazy jsou po dvou, jeden z x a druhý z id města,
            # x ukazuje na okrsky když jsou, mi potřebujeme odkazy od id
            volby.append(j)

    identificator = soup.find_all("td", class_="cislo")
    obce = soup.find_all("td", class_="overflow_name")
    data_komplet = []
    data_cast = []
    kody_obci = []
    for i in identificator:
        a = i.select("[href]")
        c = str(a)
        kod = c[-11:-5]
        kody_obci.append(kod)

    for (i, j, k) in zip(obce, kody_obci, volby):
        data_cast.append(j)
        data_cast.append(i.string)
        linky = "https://volby.cz/pls/ps2017nss/" + k
        vytah = obsah_obci(linky)
        data_cast.extend(vytah)
        data_komplet.append(data_cast[-31:])  # rádek excelu=31 buňěk
        if str(j) == "552054":
            break
    return data_komplet


def hlavni(url, csv_soubor):
    # hlavní spouštěcí funkce
    pomocna = 1
    if url != "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=3&xnumnuts=3107":
        print("špatná url adresa")
        pomocna = 0
    else:
        pass
    if csv_soubor != "volby.csv":
        print("špatný název souboru k ukládání dat")
        pomocna = 0
    else:
        pass
    if pomocna == 1:
        data = vytah_obci(url)
        hlavicky = prvni_radek_excelu(url)
        zapis(hlavicky, data, csv_soubor)
    else:
        print("ukončuji program")


def zapis(hlava, dat, csv_soubor):
    # zápis dat do csv souboru
    with open(csv_soubor, mode="w", encoding='utf16', newline='') as csv_file:
        writer = csv.writer(csv_file,
                            delimiter='\t')  # tab delimiter pro utf16, pro utf8 delimiter=";"
        writer.writerow(hlava)
        writer.writerows(dat)


if __name__ == "__main__":
    obal()
