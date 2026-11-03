import json
import random
import datetime as dt
from urllib.parse import urlencode
from urllib.request import urlopen

CITIES = {
    "Delhi": (28.61, 77.21), "Ludhiana": (30.90, 75.86), "Jaipur": (26.91, 75.79),
    "Lucknow": (26.85, 80.95), "Patna": (25.59, 85.14), "Pune": (18.52, 73.86),
    "Nagpur": (21.15, 79.09), "Hyderabad": (17.39, 78.49),
}
_BASE_TMAX = [22, 26, 32, 38, 41, 38, 33, 32, 33, 33, 29, 24]


def forecast(city):
    """7-day forecast from Open-Meteo (free, no key). Falls back to sample data offline."""
    lat, lon = CITIES[city]
    q = urlencode({"latitude": lat, "longitude": lon, "timezone": "auto", "forecast_days": 7,
                   "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max"})
    try:
        with urlopen("https://api.open-meteo.com/v1/forecast?" + q, timeout=5) as r:
            d = json.load(r)["daily"]
        days = [{"date": d["time"][i], "tmax": d["temperature_2m_max"][i], "tmin": d["temperature_2m_min"][i],
                 "rain": d["precipitation_sum"][i], "wind": d["wind_speed_10m_max"][i]} for i in range(len(d["time"]))]
        return {"city": city, "source": "live", "days": days}
    except Exception:
        today = dt.date.today()
        rnd = random.Random(f"{city}{today}")
        base = _BASE_TMAX[today.month - 1]
        days = []
        for i in range(7):
            tmax = round(base + rnd.uniform(-3, 3), 1)
            days.append({"date": str(today + dt.timedelta(days=i)), "tmax": tmax,
                         "tmin": round(tmax - rnd.uniform(9, 14), 1),
                         "rain": round(rnd.choice([0, 0, 0, 2, 12]), 1), "wind": round(rnd.uniform(6, 28), 1)})
        return {"city": city, "source": "sample", "days": days}


def advice(fc, crop=None):
    days, tips = fc["days"], []
    wet = [d["date"] for d in days if d["rain"] >= 10]
    if wet:
        tips.append({"level": "warn", "text": f"Heavy rain expected on {', '.join(wet)}. Hold irrigation, fertiliser and spraying, and clear field drains."})
    elif sum(d["rain"] for d in days) < 2:
        tips.append({"level": "info", "text": "A dry week ahead. Check soil moisture and schedule irrigation."})
    if any(d["wind"] >= 25 for d in days):
        tips.append({"level": "warn", "text": "Strong winds forecast on some days. Avoid pesticide spraying then; drift wastes product."})
    if any(d["tmax"] >= 38 for d in days):
        tips.append({"level": "warn", "text": "Heat above 38 °C. Irrigate in the evening and mulch to cut soil moisture loss."})
    if any(d["tmin"] <= 5 for d in days):
        tips.append({"level": "warn", "text": "Frost risk at night. Irrigate lightly in the evening and cover nurseries."})
    spray = [d["date"] for d in days if d["rain"] < 1 and d["wind"] < 15]
    if spray:
        tips.append({"level": "ok", "text": f"Good spraying days: {', '.join(spray[:4])}."})
    if crop:
        lo, hi = crop["temp"]
        avg_max = sum(d["tmax"] for d in days) / len(days)
        avg_min = sum(d["tmin"] for d in days) / len(days)
        if avg_max > hi + 3:
            tips.append({"level": "warn", "text": f"Average highs ({avg_max:.0f} °C) are above the {crop['name']} comfort range ({lo}–{hi} °C). Expect heat stress."})
        elif avg_min < lo - 3:
            tips.append({"level": "warn", "text": f"Average lows ({avg_min:.0f} °C) are below the {crop['name']} comfort range ({lo}–{hi} °C). Growth will slow."})
        else:
            tips.append({"level": "ok", "text": f"Temperatures suit {crop['name']} this week."})
    return tips
