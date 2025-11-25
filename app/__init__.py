from flask import Flask, request
from flask_babel import Babel


def get_locale():
    return request.args.get('lang', 'en')


def create_app():
    app = Flask(__name__)

    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

    babel = Babel(app, locale_selector=get_locale)

    from . import routes
    app.register_blueprint(routes.bp)

    return app

