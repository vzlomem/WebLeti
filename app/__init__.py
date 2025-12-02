from flask import Flask, request, url_for, render_template
from flask_babel import Babel
from flask_login import LoginManager
from config import Config
from .models import User, users
from .auth import bp as auth_bp
from .routes import bp as contents_bp


def url_for_lang(endpoint, **values):
    values.setdefault("lang", request.args.get("lang", "en"))
    return url_for(endpoint, **values)


def get_locale():
    return request.args.get("lang", "en")


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager = LoginManager(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = (
        "Необходимо авторизоваться для получения доступа к странице."
    )

    @login_manager.user_loader
    def load_user(user_id):
        if user_id in users:
            return User(user_id)
        return None

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    app.config["BABEL_DEFAULT_LOCALE"] = "en"
    app.config["BABEL_TRANSLATION_DIRECTORIES"] = "translations"

    babel = Babel()
    babel.init_app(app, locale_selector=get_locale)

    app.jinja_env.globals["url_for_lang"] = url_for_lang

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(contents_bp)
    return app
