import json
import datetime as dt
from pathlib import Path

_DATA = Path(__file__).resolve().parent.parent / "data" / "crops.json"
CROPS = json.loads(_DATA.read_text(encoding="utf-8"))


def list_crops(season=None, q=None):
    out = CROPS
    if season:
        out = [c for c in out if c["season"].lower() == season.lower()]
    if q:
        q = q.lower()
        out = [c for c in out if q in c["name"].lower() or q in c["hindi"]]
    return out


def get_crop(crop_id):
    return next((c for c in CROPS if c["id"] == crop_id), None)


def status_now(crop, month=None):
    month = month or dt.date.today().month
    if month in crop["sow"]:
        return "sow"
    if month in crop["harvest"]:
        return "harvest"
    return "grow"


def find_problems(q):
    q = (q or "").lower().strip()
    if len(q) < 3:
        return []
    hits = []
    for c in CROPS:
        for p in c["problems"]:
            blob = f'{c["name"]} {p["name"]} {p["symptoms"]}'.lower()
            if all(word in blob for word in q.split()):
                hits.append({"crop": c["name"], "crop_id": c["id"], **p})
    return hits
