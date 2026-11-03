import datetime as dt
from flask import Flask

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    from .routes.pages import bp as pages_bp
    from .routes.api import bp as api_bp
    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.context_processor
    def inject_globals():
        return {"MONTHS": MONTHS, "now_m": dt.date.today().month}

    return app
