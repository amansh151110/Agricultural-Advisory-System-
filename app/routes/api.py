from flask import Blueprint, jsonify, request, abort
from ..services import advisory, weather

bp = Blueprint("api", __name__)


@bp.get("/crops")
def crops():
    return jsonify(advisory.list_crops(request.args.get("season"), request.args.get("q")))


@bp.get("/crops/<crop_id>")
def crop(crop_id):
    c = advisory.get_crop(crop_id)
    return jsonify(c) if c else abort(404)


@bp.get("/diseases")
def diseases():
    return jsonify(advisory.find_problems(request.args.get("q")))


@bp.get("/advisory")
def weather_advisory():
    city = request.args.get("city", "Delhi")
    if city not in weather.CITIES:
        return jsonify(error="Unknown city", cities=list(weather.CITIES)), 400
    fc = weather.forecast(city)
    fc["advice"] = weather.advice(fc, advisory.get_crop(request.args.get("crop", "")))
    return jsonify(fc)
