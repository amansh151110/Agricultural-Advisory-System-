# Kisan Advisor — Agricultural Crop Advisory System

Flask + vanilla HTML/CSS/JS. Crop calendar, per-crop guides, pest and disease finder, weather-based farm advice.

## Run
    python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    python run.py          # http://127.0.0.1:5000
    pytest                 # optional: pip install pytest

## Structure
    run.py                    entry point
    config.py                 settings
    app/__init__.py           app factory, blueprints, template globals
    app/routes/pages.py       HTML pages (/, /crop/<id>, /weather, /doctor)
    app/routes/api.py         JSON API (/api/crops, /api/diseases, /api/advisory)
    app/services/advisory.py  crop data access, season status, symptom search
    app/services/weather.py   Open-Meteo forecast + rule-based farm advice
    app/data/crops.json       knowledge base (edit this to add crops)
    app/templates/            Jinja pages (_cal.html = calendar macros)
    app/static/css|js/        styling and page scripts
    tests/                    API and page tests

## Roadmap
1. MVP (done): crop calendar, crop guides, crop doctor, 7-day weather advice
2. Data: move crops.json to SQLite/PostgreSQL with SQLAlchemy; add 50+ crops, state-wise varieties
3. Accounts: farmer profiles, saved fields, SMS/WhatsApp alerts for sowing windows and rain
4. Smarter advice: soil-test input, NPK calculator, mandi price feed, image-based disease detection
5. Reach: Hindi and regional-language UI (Flask-Babel), PWA offline mode, Docker + gunicorn deployment
