#!/usr/bin/env python3
"""
בודק מועמדים חדשים ב-hagush.org.il
מריץ ע"י המשימה המתוזמנת בשעה 19:00
"""
import json, csv, os, urllib.request
from datetime import datetime

CSV_PATH = "/sessions/busy-relaxed-bardeen/mnt/דבר/04-תוצאות/candidates.csv"
URL = "https://hagush.org.il/candidates.json"

def load_existing_ids():
    if not os.path.exists(CSV_PATH):
        return set()
    with open(CSV_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return {row["id"] for row in reader}

def fetch_candidates():
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def write_csv(candidates):
    fieldnames = ["id","name","age","home","activities","facebook","linkedin","instagram","x","tiktok","homepage","telegram","youtube","תאריך_איסוף"]
    with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for c in candidates:
            links = c.get("links", {})
            w.writerow({
                "id": c.get("id",""),
                "name": c.get("name",""),
                "age": c.get("age",""),
                "home": c.get("home",""),
                "activities": c.get("activities",""),
                "facebook": links.get("facebook",""),
                "linkedin": links.get("linkedin",""),
                "instagram": links.get("instagram",""),
                "x": links.get("x",""),
                "tiktok": links.get("tiktok",""),
                "homepage": links.get("homepage",""),
                "telegram": links.get("telegram",""),
                "youtube": links.get("youtube",""),
                "תאריך_איסוף": datetime.now().strftime("%Y-%m-%d %H:%M")
            })

if __name__ == "__main__":
    existing = load_existing_ids()
    candidates = fetch_candidates()
    new_ones = [c for c in candidates if c["id"] not in existing]
    
    if new_ones:
        print(f"נמצאו {len(new_ones)} מועמדים חדשים:")
        for c in new_ones:
            print(f"  + {c['name']}")
        write_csv(candidates)
        print(f"הרשימה עודכנה ({len(candidates)} סה\"כ)")
    else:
        print(f"אין חדשים. סה\"כ {len(candidates)} מועמדים.")
