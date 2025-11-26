# announcements
a safe, legal, and fully workable approach to send new announcements from your college website to your WhatsApp automatically using a Python script.
1. How the system will work

Your Python script will check the college announcement webpage periodically (e.g., every hour).

It will scrape the announcements (only if website terms allow scraping!).

It compares with previously saved announcements.

If new announcements exist → it sends them to your WhatsApp.

⚠️ Before You Start

Check your college website’s robots.txt or Terms of Service to ensure scraping is allowed.

✅ 2. Detect announcements from the website

You need requests + BeautifulSoup.

import requests
from bs4 import BeautifulSoup

def get_announcements():
    url = "https://yourcollege.edu/announcements"   # change this
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    
    # Update this selector depending on website structure
    items = soup.select(".announcement-item")  

    announcements = []
    for i in items:
        title = i.get_text(strip=True)
        announcements.append(title)
    return announcements

✅ 3. How to send WhatsApp messages automatically
You have two legal options:
OPTION A — Use Twilio WhatsApp API (Most Reliable)

✔ Works 24/7
✔ Official WhatsApp API
✔ Free trial available

Steps:

Create free account → https://www.twilio.com/whatsapp

Get:

ACCOUNT_SID

AUTH_TOKEN

WhatsApp sandbox number

Add your own WhatsApp number to the sandbox.

Python Code:
from twilio.rest import Client

def send_whatsapp(message):
    account_sid = "YOUR_SID"
    auth_token = "YOUR_TOKEN"
    client = Client(account_sid, auth_token)

    client.messages.create(
        from_='whatsapp:+14155238886',  # twilio sandbox number
        body=message,
        to='whatsapp:+91XXXXXXXXXX'     # your number
    )

OPTION B — FREE: Use WhatsApp Web Automation (selenium)

⚠️ Works only if your computer is on
⚠️ Requires QR scan
✔ Free
✔ Sends directly from your WhatsApp

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def send_whatsapp_web(number, text):
    driver = webdriver.Chrome()
    driver.get("https://web.whatsapp.com/")
    input("Scan QR then press ENTER...")

    time.sleep(10)
    driver.get(f"https://web.whatsapp.com/send?phone={number}&text={text}")
    time.sleep(10)
    send_btn = driver.find_element("xpath", "//span[@data-icon='send']")
    send_btn.click()
    driver.quit()

✅ 4. Combine Everything (Full Automation Code)
import time
import json

from twilio.rest import Client
import requests
from bs4 import BeautifulSoup

DATA_FILE = "old_announcements.json"

def load_old():
    try:
        return json.load(open(DATA_FILE))
    except:
        return []

def save_new(data):
    json.dump(data, open(DATA_FILE, "w"))

def get_announcements():
    url = "https://yourcollege.edu/announcements"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select(".announcement-item")

    return [i.get_text(strip=True) for i in items]

def send_whatsapp(text):
    client = Client("SID", "TOKEN")
    client.messages.create(
        from_='whatsapp:+14155238886',
        body=text,
        to='whatsapp:+91XXXXXXXXXX'
    )

if __name__ == "__main__":
    while True:
        old = load_old()
        new = get_announcements()

        fresh = [a for a in new if a not in old]

        for f in fresh:
            send_whatsapp("📢 New Announcement:\n\n" + f)

        if fresh:
            save_new(new)

        time.sleep(3600)   # check every hour

🎉 That’s it! You now have your own WhatsApp announcement bot.
