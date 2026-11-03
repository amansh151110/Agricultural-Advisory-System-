from flask import Blueprint, render_template, abort
import datetime as dt
from ..services import advisory, weather

bp = Blueprint("pages", __name__)


@bp.get("/")
def index():
    m = dt.date.today().month
    crops = advisory.list_crops()
    return render_template("index.html", crops=crops,
                           sow=[c for c in crops if m in c["sow"]],
                           harvest=[c for c in crops if m in c["harvest"]])


@bp.get("/crop/<crop_id>")
def crop(crop_id):
    c = advisory.get_crop(crop_id)
    return render_template("crop.html", c=c) if c else abort(404)


@bp.get("/weather")
def weather_page():
    return render_template("weather.html", cities=list(weather.CITIES), crops=advisory.CROPS)


@bp.get("/doctor")
def doctor():
    return render_template("doctor.html")
