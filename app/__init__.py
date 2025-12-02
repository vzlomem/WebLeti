from flask import Flask, request, url_for
from flask_babel import Babel


def url_for_lang(endpoint, **values):
    values.setdefault('lang', request.args.get('lang', 'en'))
    return url_for(endpoint, **values)


def get_locale():
    return request.args.get('lang', 'en')


def create_app():
    app = Flask(__name__)

    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

    babel = Babel()
    babel.init_app(app, locale_selector=get_locale)
    
    app.jinja_env.globals['url_for_lang'] = url_for_lang

    from . import routes
    app.register_blueprint(routes.bp)

    return app

