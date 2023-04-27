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

colorama.init()


with open("name.txt", "r") as f:
    names = [x.strip() for x in f.readlines()]

with open("last.txt", "r") as f:
    lastnames = [x.strip() for x in f.readlines()]

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
    

def vote():
    email = json.loads(requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1").content.decode())
    email = email[0]
    print(f"[INFO] Email: {email}")
    username, server = email.split("@")

    make_vote(email)

    url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={username}&domain={server}"
    mail_id = None

    for i in range(5):
        if i >= 5:
            print(f"{Fore.RED + Style.BRIGHT}[FAIL]{Style.RESET_ALL} Mail not Received")
            return False

        inbox = json.loads(requests.get(url).content.decode())
        if inbox:
            mail_id = inbox[0]["id"]
            print(f"{Fore.GREEN + Style.BRIGHT}[SUCCESS]{Style.RESET_ALL} Got email with id:", mail_id)
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
        print(f"{Fore.GREEN + Style.BRIGHT}[SUCCESS]{Style.RESET_ALL} Voted!")
    else:
        print(f"{Fore.RED + Style.BRIGHT}[FAIL]{Style.RESET_ALL} Not Voted!")

goal = 5

for i in range(goal):
    start = datetime.now()
    vote()
    took = (datetime.now() - start).total_seconds()
    if took != 0:
        print(f"{Fore.MAGENTA + Style.BRIGHT}[SPEED]{Style.RESET_ALL} {round(60/took, 2)} votes per minute")
    time.sleep(1)
