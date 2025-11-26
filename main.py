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
