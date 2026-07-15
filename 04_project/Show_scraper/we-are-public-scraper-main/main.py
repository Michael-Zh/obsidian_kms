# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
from datetime import datetime, date, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# --- CONFIGURATION ---
RESET_CSV = False
EMAIL_SENDER = "boping.m.zhang@gmail.com"
EMAIL_RECEIVER = "boping.m.zhang@gmail.com"
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SCRAPER_API_KEY = os.getenv("SCRAPER_API_KEY")

kw = ['ndt', 'introdans', 'scapino', 'club%20guy', 'carre']
venues = ['internationaal-theater-amsterdam', 'amare-1726', 'theater-bellevue-276', 'frascati-213', 'korzo-501', 'schuur-245', 'stadsschouwburg-haarlem-949', 'tr25-schouwburg', 'theater-ins-blau', 'het-concertgebouw-19', 'carre-51']

event_seen = ['Een vrouw ver vooruit!', 'MEET: DESTINY', 'Sorry not sorry', 'IGNITE', 'En god zag dat het bijna goed was...', 'Double Bill: Finding Places', 'FRANK', 'Sistorhood', 'Moeder van Europa', 'XANUUN']
blockout_days = ["20260306", "20260309"]
file_path = 'results.csv'
columns = ["Keyword", "City", "Disciplines", "Date", "Title", "Artists", "URL", "Venue", "Venue_URL", "Update_date", "blockoutYN"]

# --- FUNCTIONS ---

def convert_dutch_date(date_str):
    now = datetime.now()
    month_map = {"jan": 1, "feb": 2, "mrt": 3, "apr": 4, "mei": 5, "jun": 6,
                 "jul": 7, "aug": 8, "sep": 9, "okt": 10, "nov": 11, "dec": 12}
    ds = date_str.lower().strip()
    if " tot " in ds: ds = ds.split(" tot ")[0].strip()
    target_date, time_part = None, "00:00"
    if "vandaag" in ds: target_date = now
    elif "morgen" in ds: target_date = now + timedelta(days=1)
    time_match = re.search(r"(\d{2}:\d{2})", ds)
    if time_match: time_part = time_match.group(1)
    if not target_date:
        match = re.search(r"(\d{1,2})\s+([a-z]{3})\.?\s+(?:om\s+)?(\d{2}:\d{2})", ds)
        if match:
            day, month_abbr, time_part = int(match.group(1)), match.group(2), match.group(3)
            month = month_map.get(month_abbr)
            if month:
                year = now.year
                if month < now.month and (now.month - month) > 6: year += 1
                target_date = datetime(year, month, day)
    if target_date:
        return f"{target_date.strftime('%Y-%m-%d')} {time_part} {target_date.strftime('%a')}"
    return date_str

def scrape_url(url, source_name, render=False):
    try:
        if SCRAPER_API_KEY:
            api_url = f"http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url={url}"
            if render:
                api_url += "&render=true"
            r = requests.get(api_url, timeout=60)
        else:
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        cards = soup.find_all('div', class_='event-date-card')
        data = []
        for c in cards:
            title_tag = c.find('h3', class_='event-meta__title')
            title = title_tag.get_text(strip=True).replace('⭑', '').strip() if title_tag else ""
            artist_tag = c.find('span', class_='event-meta__artists')
            artist = artist_tag.get_text(strip=True) if artist_tag else ""
            date_tag = c.find('span', class_='event-date')
            iso_date = convert_dutch_date(date_tag.get('title', date_tag.get_text(strip=True))) if date_tag else ""
            genre_tag = c.find('span', class_='event-disciplines')
            genre = genre_tag.get_text(strip=True) if genre_tag else ""
            v_tag = c.find('span', class_='event-venue')
            v_str = v_tag.get_text(strip=True) if v_tag else ""
            venue, city = (v_str.rsplit(',', 1)[0].strip(), v_str.rsplit(',', 1)[1].strip()) if "," in v_str else (v_str, "")
            a_tag = c.find('a', class_='event-date-card__link')
            link = f"https://www.wearepublic.nl{a_tag['href']}" if a_tag else ""
            if not title or not link:
                continue
            data.append({"Keyword": source_name, "City": city, "Disciplines": genre, "Date": iso_date, "Title": title, "Artists": artist, "URL": link, "Venue": venue, "Venue_URL": "", "Update_date": datetime.today().strftime('%Y-%m-%d'), "blockoutYN": False})
        print(f"  {source_name}: {len(data)} events")
        return data
    except Exception as e:
        print(f"  ERROR scraping {url}: {e}")
        return []

def prepare_grouped_html_table(df):
    if df.empty: return "<p style='color: #999; font-style: italic; padding: 10px;'>No events found.</p>"
    city_order = ['Amsterdam', 'Haarlem', 'Amstelveen', 'Den Haag', 'Leiden', 'Rotterdam', 'Utrecht']
    df = df.copy()
    df['city_sort'] = df['City'].apply(lambda c: (city_order.index(c), '') if c in city_order else (len(city_order), c))
    df = df.sort_values(by=['city_sort', 'Disciplines', 'Date']).reset_index(drop=True)
    df = df.drop(columns=['city_sort'])
    html = '<table class="wap-table"><thead><tr><th style="width: 90px;">Date</th><th>Info</th><th>Performance</th></tr></thead><tbody>'
    current_city = None
    for _, row in df.iterrows():
        if row['City'] != current_city:
            current_city = row['City']
            html += f'<tr><td colspan="3" class="city-header">{current_city}</td></tr>'
        d_parts = str(row['Date']).split(' ')
        if len(d_parts) == 3:
            date_cell = f"<strong>{d_parts[0].replace('-', '')}</strong><br><span class='sub-text' style='white-space: nowrap;'>{d_parts[2]} {d_parts[1]}</span>"
        else:
            date_cell = row['Date']
        genre_text = row['Disciplines'] if row['Disciplines'] else "Info"
        v_url = str(row.get('Venue_URL', ''))
        genre_cell = f'<a href="{v_url}" class="venue-link">{genre_text}</a>' if (v_url and v_url.startswith('http')) else genre_text
        artist_str = f"<br><span class='sub-text'>{row['Artists']}</span>" if row['Artists'] else ""
        perf_cell = f'<a href="{row["URL"]}" class="perf-link"><strong>{row["Title"]}</strong></a>{artist_str}'
        html += f'<tr><td style="white-space: nowrap;">{date_cell}</td><td>{genre_cell}</td><td>{perf_cell}</td></tr>'
    return html + '</tbody></table>'

# --- EXECUTION ---
if RESET_CSV or not os.path.exists(file_path):
    all_result = pd.DataFrame(columns=columns)
else:
    all_result = pd.read_csv(file_path)
    if 'Venue_URL' not in all_result.columns: all_result['Venue_URL'] = ""

today_data = []
all_urls = (
    [(f"https://www.wearepublic.nl/zoeken?q={q}", q.upper(), False) for q in kw] +
    [(f"https://www.wearepublic.nl/dans", "PAGE_DANS", True)] +
    [(f"https://www.wearepublic.nl/beeldende-kunst", "PAGE_BEELDENDE-KUNST", False)] +
    [(f"https://www.wearepublic.nl/venues/{v}", f"VENUE_{v.upper()}", False) for v in venues]
)
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = {executor.submit(scrape_url, url, name, render): name for url, name, render in all_urls}
    for future in as_completed(futures):
        today_data.extend(future.result())
print(f"TOTAL scraped today: {len(today_data)}")

all_result = pd.concat([all_result, pd.DataFrame(today_data)], ignore_index=True)
all_result = all_result.drop_duplicates(subset=['Title', 'Artists', 'Date', 'Venue'], keep='first')
all_result['temp_date'] = pd.to_datetime(all_result['Date'].str.extract(r'(\d{4}-\d{2}-\d{2})')[0], errors='coerce')
today_dt = pd.to_datetime(date.today())

all_result_final = all_result[all_result['temp_date'] >= today_dt].copy()
all_result_final = all_result_final[~all_result_final['Title'].isin(event_seen)]
if blockout_days:
    b_start = datetime.strptime(blockout_days[0], "%Y%m%d").date()
    b_end = datetime.strptime(blockout_days[1], "%Y%m%d").date()
    all_result_final['blockoutYN'] = all_result_final['temp_date'].dt.date.apply(lambda x: b_start <= x <= b_end if pd.notnull(x) else False)

all_result_final.drop(columns=['temp_date']).to_csv(file_path, index=False)

# --- EMAIL ---
today_str = date.today().strftime("%Y-%m-%d")
new_ev = all_result_final[(all_result_final['Update_date'] == today_str) & (all_result_final['blockoutYN'] == False)]
cities_pref = ['Amsterdam', 'Haarlem', 'Den Haag', 'Leiden', 'Rotterdam', 'Utrecht', 'Amstelveen']
key_city_ev = all_result_final[(all_result_final['City'].str.contains('|'.join(cities_pref), case=False, na=False)) & (all_result_final['blockoutYN'] == False)]
dance_ev = all_result_final[(all_result_final['Disciplines'].str.contains('dans', case=False, na=False)) & (all_result_final['blockoutYN'] == False)]
print(f"new_ev: {len(new_ev)}, key_city_ev: {len(key_city_ev)}, dance_ev: {len(dance_ev)}")

email_style = """<style>
    body { font-family: 'Helvetica', Arial, sans-serif; color: #333; max-width: 750px; margin: 0 auto; }
    h2 { color: #ffffff; background-color: #49003F; padding: 12px; border-left: 8px solid #D1CD33; font-size: 18px; margin-bottom: 5px; }
    .wap-table { border-collapse: collapse; width: 100%; font-size: 13px; margin-bottom: 30px; table-layout: auto; }
    .wap-table th { text-align: left; background-color: #f8f8f8; color: #49003F; padding: 10px; border-bottom: 2px solid #49003F; }
    .wap-table td { padding: 10px; border-bottom: 1px solid #eee; vertical-align: top; }
    .city-header { background-color: #D1CD33 !important; color: #000; font-weight: bold; padding: 8px 10px !important; font-size: 14px; text-transform: uppercase; }
    .sub-text { color: #666; font-size: 11px; line-height: 1.2; }
    .perf-link { color: #49003F; text-decoration: none; }
    .venue-link { color: #C94581; text-decoration: underline; font-weight: bold; }
</style>"""

email_content = f"""<html><head>{email_style}</head><body>
    <h1 style="color: #49003F; text-align: center;">WAP Daily Digest</h1>
    <h2>✨ NEW DISCOVERIES</h2>{prepare_grouped_html_table(new_ev)}
    <h2>📍 SELECTED CITIES</h2>{prepare_grouped_html_table(key_city_ev)}
    <h2>💃 DANCE ONLY</h2>{prepare_grouped_html_table(dance_ev)}
</body></html>"""

if not (new_ev.empty and key_city_ev.empty and dance_ev.empty):
    msg = MIMEMultipart()
    msg['Subject'] = f"WAP Update: {date.today().strftime('%d %b')}"
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg.attach(MIMEText(email_content, 'html'))
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        print("Email sent!")
    except Exception as e:
        print(f"SMTP Error: {e}")
