import requests
import json
import time
from bs4 import BeautifulSoup as bs
import urllib3
import random
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import colorama
from colorama import Fore, Back, Style
from termcolor import colored

from datetime import datetime

from concurrent.futures import ThreadPoolExecutor

colorama.init()

names = "Nowak;Kowalski;Wiśniewski;Dąbrowski;Lewandowski;Wójcik;Kamiński;Kowalczyk;Zieliński;Szymański;Woźniak;Kozłowski;Jankowski;Wojciechowski;Kwiatkowski;Kaczmarek;Mazur;Krawczyk;Piotrowski;Grabowski;Nowakowski;Pawłowski;Michalski;Nowicki;Adamczyk;Dudek;Zając;Wieczorek;Jabłoński;Król;Majewski;Olszewski;Jaworski;Wróbel;Malinowski;Pawlak;Witkowski;Walczak;Stępień;Górski;Rutkowski;Michalak;Sikora;Ostrowski;Baran;Duda;Szewczyk;Tomaszewski;Pietrzak;Marciniak;Wróblewski;Zalewski;Jakubowski;Jasiński;Zawadzki;Sadowski;Bąk;Chmielewski;Włodarczyk;Borkowski;Czarnecki;Sawicki;Sokołowski;Urbański;Kubiak;Maciejewski;Szczepański;Kucharski;Wilk;Kalinowski;Lis;Mazurek;Wysocki;Adamski;Kaźmierczak;Wasilewski;Sobczak;Czerwiński;Andrzejewski;Cieślak;Głowacki;Zakrzewski;Kołodziej;Sikorski;Krajewski;Gajewski;Szymczak;Szulc;Baranowski;Laskowski;Brzeziński;Makowski;Ziółkowski;Przybylski".split(";")
lastnames = "Ada;Adalbert;Adam;Adela;Adelajda;Adrian;Aga;Agata;Agnieszka;Albert;Alberta;Aldona;Aleksander;Aleksandra;Alfred;Alicja;Alina;Amadeusz;Ambroży;Amelia;Anastazja;Anastazy;Anatol;Andrzej;Aneta;Angelika;Angelina;Aniela;Anita;Anna;Antoni;Antonina;Anzelm;Apolinary;Apollo;Apolonia;Apoloniusz;Ariadna;Arkadiusz;Arkady;Arlena;Arleta;Arletta;Arnold;Arnolf;August;Augustyna;Aurela;Aurelia;Aurelian;Aureliusz;Balbina;Baltazar;Barbara;Bartłomiej;Bartosz;Bazyli;Beata;Benedykt;Benedykta;Beniamin;Bernadeta;Bernard;Bernardeta;Bernardyn;Bernardyna;Błażej;Bogdan;Bogdana;Bogna;Bogumił;Bogumiła;Bogusław;Bogusława;Bohdan;Bolesław;Bonawentura;Bożena;Bronisław;Broniszław;Bronisława;Brunon;Brygida;Cecyl;Cecylia;Celestyn;Celestyna;Celina;Cezary;Cyprian;Cyryl;Dalia;Damian;Daniel;Daniela;Danuta;Daria;Dariusz;Dawid;Diana;Dianna;Dobrawa;Dominik;Dominika;Donata;Dorian;Dorota;Dymitr;Edmund;Edward;Edwin;Edyta;Egon;Eleonora;Eliasz;Eligiusz;Eliza;Elwira;Elżbieta;Emanuel;Emanuela;Emil;Emilia;Emilian;Emiliana;Ernest;Ernestyna;Erwin;Erwina;Eryk;Eryka;Eugenia;Eugeniusz;Eulalia;Eustachy;Ewelina;Fabian;Faustyn;Faustyna;Felicja;Felicjan;Felicyta;Feliks;Ferdynand;Filip;Franciszek;Franciszek;Salezy;Franciszka;Fryderyk;Fryderyka;Gabriel;Gabriela;Gaweł;Genowefa;Gerard;Gerarda;Gerhard;Gertruda;Gerwazy;Godfryd;Gracja;Gracjan;Grażyna;Greta;Grzegorz;Gustaw;Gustawa;Gwidon;Halina;Hanna;Helena;Henryk;Henryka;Herbert;Hieronim;Hilary;Hipolit;Honorata;Hubert;Ida;Idalia;Idzi;Iga;Ignacy;Igor;Ildefons;Ilona;Inga;Ingeborga;Irena;Ireneusz;Irma;Irmina;Irwin;Ismena;Iwo;Iwona;Izabela;Izolda;Izyda;Izydor;Jacek;Jadwiga;Jagoda;Jakub;;Jan;;Janina;January;Janusz;Jarema;Jarogniew;Jaromir;Jarosław;Jarosława;Jeremi;Jeremiasz;Jerzy;Jędrzej;Joachim;Joanna;Jolanta;Jonasz;Jonatan;Jowita;Józef;Józefa;Józefina;Judyta;Julia;Julian;Julianna;Julita;Juliusz;Justyn;Justyna;Kacper;Kaja;Kajetan;Kalina;Kamil;Kamila;Karina;Karol;Karolina;Kacper;Kasper;Katarzyna;Kazimiera;Kazimierz;Kinga;Klara;Klarysa;Klaudia;Klaudiusz;Klaudyna;Klemens;Klementyn;Klementyna;Kleopatra;Klotylda;Konrad;Konrada;Konstancja;Konstanty;;Konstantyn;Kordelia;Kordian;Kordula;Kornel;Kornelia;Kryspin;Krystian;Krystyn;Krystyna;Krzysztof;Ksenia;Kunegunda;Laura;Laurenty;Laurentyn;Laurentyna;Lech;Lechosław;Lechosława;Leokadia;Leon;Leonard;Leonarda;Leonia;Leopold;Leopoldyna;Lesław;Lesława;Leszek;Lidia;Ligia;Lilian;Liliana;Lilianna;Lilla;Liwia;Liwiusz;Liza;Lolita;Longin;Loretta;Luba;Lubomir;Lubomira;Lucja;Lucjan;Lucjusz;Lucyna;Ludmiła;Ludomił;Ludomir;Ludosław;Ludwik;Ludwika;Ludwina;Luiza;Lukrecja;Lutosław;Łucja;Łucjan;Łukasz;Maciej;Madlena;Magda;Magdalena;;Makary;Maksym;Maksymilian;Malina;Malwin;Malwina;Małgorzata;Manfred;Manfreda;Manuela;Marcel;Marcela;Marceli;Marcelina;Marcin;Marcjan;Marcjanna;Marcjusz;Marek;Margareta;Maria;MariaMagdalena;Marian;Marianna;Marietta;Marina;Mariola;Mariusz;Marlena;Marta;Martyna;Maryla;Maryna;Marzanna;Marzena;Mateusz;Matylda;Maurycy;Melania;Melchior;Metody;Michalina;Michał;Mieczysław;Mieczysława;Mieszko;Mikołaj;Milena;Miła;Miłosz;Miłowan;Miłowit;Mira;Mirabella;Mirella;Miron;Mirosław;Mirosława;Modest;Monika;Nadia;Nadzieja;Napoleon;Narcyz;Narcyza;Nastazja;Natalia;Natasza;Nikita;Nikodem;Nina;Nora;Norbert;Norberta;Norma;Norman;Oda;Odila;Odon;Ofelia;Oksana;Oktawia;Oktawian;Olaf;Oleg;Olga;Olgierd;Olimpia;Oliwia;Oliwier;Onufry;Orfeusz;Oskar;Otto;Otylia;Pankracy;Parys;Patrycja;Patrycy;Patryk;Paula;Paulina;Paweł;Pelagia;Petronela;Petronia;Petroniusz;Piotr;Pola;Polikarp;Protazy;Przemysław;Radomił;Radomiła;Radomir;Radosław;Radosława;Radzimir;Rafael;Rafaela;Rafał;Rajmund;Rajmunda;Rajnold;Rebeka;Regina;Remigiusz;Rena;Renata;Robert;Roberta;Roch;Roderyk;Rodryg;Rodryk;Roger;Roksana;Roland;Roma;Roman;Romana;Romeo;Romuald;Rozalia;Rozanna;Róża;Rudolf;Rudolfa;Rudolfina;Rufin;Rupert;Ryszard;Ryszarda;Sabina;Salomea;Salomon;Samuel;Samuela;Sandra;Sara;Sawa;Sebastian;Serafin;Sergiusz;Sewer;Seweryn;Seweryna;Sędzisław;Sędziwoj;Siemowit;Sława;Sławomir;Sławomira;Sławosz;Sobiesław;Sobiesława;Sofia;Sonia;Stanisław;Stanisława;Stefan;Stefania;Sulimiera;Sulimierz;Sulimir;Sydonia;Sykstus;Sylwan;Sylwana;Sylwester;Sylwia;Sylwiusz;Symeon;Szczepan;Szczęsna;Szczęsny;Szymon;Ścibor;Świętopełk;Tadeusz;Tamara;Tatiana;Tekla;Telimena;Teodor;Teodora;Teodozja;Teodozjusz;Teofil;Teofila;Teresa;Tobiasz;Toma;Tomasz;Tristan;Trojan;Tycjan;Tymon;Tymoteusz;Tytus;Unisław;Ursyn;Urszula;Violetta;Wacław;Wacława;Waldemar;Walenty;Walentyna;Waleria;Walerian;Waleriana;Walery;Walter;Wanda;Wasyl;Wawrzyniec;Wera;Werner;Weronika;Wieńczysła;Wiesław;Wiesława;Wiktor;Wiktoria;Wilhelm;Wilhelmina;Wilma;Wincenta;Wincenty;Wińczysła;Wiola;Wioletta;Wirgiliusz;Wirginia;Wirginiusz;Wisław;Wisława;Wit;Witalis;Witold;Witolda;Witołd;Witomir;Wiwanna;Władysława;Władysław;Włodzimierz;Włodzimir;Wodzisław;Wojciech;Wojciecha;Zachariasz;Zbigniew;Zbysław;Zbyszko;Zdobysław;Zdzisław;Zdzisława;Zenobia;Zenobiusz;Zenon;Zenona;Ziemowit;Zofia;Zula;Zuzanna;Zygfryd;Zygmunt;Zyta;Żaklina;Żaneta;Żanna;Żelisław;Żytomir".split(";")

def get_name():
    return f"{random.choice(names)} {random.choice(lastnames)}"

def make_vote(email: str):
    data = {
        "jack": 1,
        "wybor": "95.+Zwierz%C4%99cy+Patrol+SJRW+-+Specjalistyczna+Jednostka+Ratownictwa+Weterynaryjnego+Fundacja",
        "sender_name": get_name().replace(" ", "+"),
        "sender_mail": email,
        "zgoda": 1,
    }

    req = requests.post("https://xyz.um.warszawa.pl/S/S3ktor/form.php", data=data, verify=False)
    if req.status_code != 200:
        print(Fore.YELLOW + Style.BRIGHT + "[WARNING]" + Style.RESET_ALL + " Voted unsuccessfully!")
    else:
        print(f"{Fore.GREEN + Style.BRIGHT}[SUCCESS]{Style.RESET_ALL} Email sent!")
    

def vote(process_id):
    email = json.loads(requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1").content.decode())
    email = email[0]
    print(f"[{process_id}][INFO] Email: {email}")
    username, server = email.split("@")

    make_vote(email)

    url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={username}&domain={server}"
    mail_id = None

    print(f"[{process_id}][INFO] Waiting for email...")
    for i in range(5):
        if i >= 4:
            print(f"{Fore.RED + Style.BRIGHT}[FAIL]{Style.RESET_ALL} Mail not Received")
            return False

        inbox = json.loads(requests.get(url).content.decode())
        if inbox:
            mail_id = inbox[0]["id"]
            print(f"[{process_id}]{Fore.GREEN + Style.BRIGHT}[SUCCESS]{Style.RESET_ALL} Got email with id:", mail_id)
            break
        else:
            time.sleep(1)
    
    content = requests.get(f"https://www.1secmail.com/api/v1/?action=readMessage&login={username}&domain={server}&id={str(mail_id)}")
    content = json.loads(content.content.decode())
    page = content['body']

    soup = bs(page, 'html.parser')
    links = soup.select("a")
    if not links:
        raise Exception("Broken LINK!")
    
    verify_url = links[0]['href']
    # print(f"[INFO] Verify URL: {verify_url}")

    verify_req = requests.get(verify_url, verify=False)
    soup = bs(verify_req.content.decode(), 'html.parser')
    if soup.select("div.big.green"):
        print(f"[{process_id}]{Fore.GREEN + Style.BRIGHT}[SUCCESS]{Style.RESET_ALL} Voted!")
        return True
    else:
        print(f"[{process_id}]{Fore.RED + Style.BRIGHT}[FAIL]{Style.RESET_ALL} Not Voted!")
        return False


count = 0

def make_one():
    global count
    count += 1
    start = datetime.now()
    status = vote(count)
    took = (datetime.now() - start).total_seconds()
    if took != 0:
        print(f"{Fore.MAGENTA + Style.BRIGHT}[SPEED]{Style.RESET_ALL} {round(60/took, 2)} votes per minute")
    time.sleep(1)

with ThreadPoolExecutor(max_workers=5) as executor:
    while True:
        executor.submit(make_one)
        time.sleep(0.25)
