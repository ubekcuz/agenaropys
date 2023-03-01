password = "ily123123"
version = 4

import json
import secmail
import requests
import aminolib
from time import sleep
from bs4 import BeautifulSoup

def onlyDigits(s):
    a = ""
    s = s.lower().replace('s', '5').replace('o', '0').replace('$', '5')
    for i in s:
        if i.isdigit(): a+=i
    return a

def verGet(url):
    req = requests.post("http://woolbot.ix.tc/amino-captcha-ocr/api/v1/autoregister/version")
    if req['v'] > version: print("\n\nNew version available!\nLink: {}\n\n".format(req['l']))

def ocrGet(url):
    while True:
        try:
            req = requests.post("http://woolbot.ix.tc/amino-captcha-ocr/api/v1/predict", json={"url": url})
            # if got too many requests
            try: 
                if req['detail'] == "Too Many Requests":
                    print("[!] Too many requests from OCR's side. Waiting around half minute.")
                    sleep(30)
                    continue
            except: pass
            # if something happened
            try: print(req['WARNING'])
            except: pass
            # return 
            return req.json()['prediction']
        except: print("[!] An error occured on captcha's OCR side. Trying again.")
    
def saveImg(url, name):
    response = requests.get(url)
    with open(f'temp/{name}.png', 'wb') as fp:
        fp.write(response.content)

def gen_email():
    mail = secmail.SecMail()
    email = mail.generate_email()
    return email

def get_message(email):
    try:
        sleep(4)
        f=email
        mail = secmail.SecMail()
        inbox = mail.get_messages(f)
        for Id in inbox.id:
            msg = mail.read_message(email=f, id=Id).htmlBody
            bs = BeautifulSoup(msg, 'html.parser')
            images = bs.find_all('a')[0]
            url = (images['href']+'\n')
            if url is not None: return url
    except:
        pass

def json_append(mail, pswd, devId):
    try:
        with open("accounts.json") as fp: listObj = json.load(fp)
    except:
        with open('accounts.json','a+'): pass
        listObj = list()
    listObj.append({
        "email": mail,
        "password": pswd,
        "device": devId
    })
    with open("accounts.json", 'w') as fp:
        json.dump(listObj, fp, indent=4, separators=(',',': '))
    
def generation_process(count: int, proxy: str = None):
    if proxy in [None, [], (), ""]: proxy = {}
    else: proxy = {"https": proxy}
    
    for i in range(count):
        client = aminolib.Client(proxies=proxy)
        email = gen_email()
        nick = email[:email.find('@')]
                
        while True:
            try:
                req = client.request_verify_code(email=email)
                break
            except Exception as e:
                if "502" in str(e) or "service" in str(e) or "503" in str(e): print(f"[!] 502.")
                elif "403" in str(e): print(f"[!] 403.")
                elif "Too many requests" in str(e):
                    print(f"[!] Too many requests. Try to change proxy.")
                    quit()
                else: print(f"[!] Problem with registration: {e}")

        url = get_message(email).strip()
        print(f"\nCaptcha URL: {url}")
                
        predictCode = ocrGet(url)
        print(f"Predicted code: {predictCode}")

        while True:
            try:
                client.register(nickname=nick, email=email, password=password, verificationCode=predictCode)
                break
            except Exception as e:
                if "502" in str(e) or "service" in str(e) or "503" in str(e): print(f"[!] 502.")
                elif "403" in str(e): print(f"[!] 403.")
                elif "too many requests" in str(e).lower():
                    print(f"[!] Too many requests. Try to change proxy.")
                    quit()
                else: print(f"[!] Problem with registration: {e}")
        json_append(email, password, client.device_id)
        print(f"[V] Account {i+1} ready.")
        
print("AccGen\nv0.4")
generation_process(int(input("Accounts: ")), input("Proxy: "))
quit()
