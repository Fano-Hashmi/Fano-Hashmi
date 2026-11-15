import json
import re
from datetime import datetime
from pathlib import Path
import requests
from bs4 import BeautifulSoup

USERNAME = "Fano-Hashmi"
URL = f"https://github.com/users/{USERNAME}/contributions"
OUT = Path(__file__).resolve().parent.parent / "data/contributions.json"


def main():
    resp = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    tooltips = {}
    for tip in soup.find_all("tool-tip"):
        for_id = tip.get("for")
        if for_id:
            m = re.search(r"(\d+)\s+contribution", tip.get_text(strip=True))
            tooltips[for_id] = int(m.group(1)) if m else 0

    days = []
    for td in soup.select("td.ContributionCalendar-day[data-date]"):
        days.append({
            "date": td["data-date"],
            "level": int(td.get("data-level", 0)),
            "count": tooltips.get(td.get("id", ""), int(td.get("data-level", 0))),
        })

    days.sort(key=lambda x: x["date"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "username": USERNAME,
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "total_contributions": sum(d["count"] for d in days),
        "days": days,
    }, indent=2), encoding="utf-8")
    print(f"Saved {len(days)} days")


if __name__ == "__main__":
    main()
