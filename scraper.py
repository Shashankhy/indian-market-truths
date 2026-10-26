import datetime
import json
import requests
from bs4 import BeautifulSoup
import os

def scrape_today():
    today = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5, minutes=30)))
    date_slug = today.strftime("%B-%d-%Y").lower()
    
    url = f"https://fin.preparoo.app/daystarter-{date_slug}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            return

        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        lead_text = paragraphs[0].text if len(paragraphs) > 0 else "Market update in progress..."
        
        data = {
            "date": today.strftime("%A, %B %d, %Y"),
            "lead_headline": "Evening Market Update",
            "lead_body": f"<p>{lead_text}</p>"
        }

        with open("market_data.json", "w") as f:
            json.dump(data, f)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape_today()
