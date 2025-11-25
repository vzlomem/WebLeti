from flask import Blueprint, render_template, request
from flask_babel import _


bp = Blueprint('contents', __name__)


@bp.route("/")
def index():
    return render_template('index.html')


@bp.route('/contents')
def contents():
    contents = [
        {'name': _('Фильмы'), 'url': 'films'},
        {'name': _('Сериалы'), 'url': 'series'},
        {'name': _('Книги'), 'url': 'books'}
    ]
    return render_template('contents.html', contents=contents)


@bp.route('/films', methods=['GET'])
def films():
    films = [
        {'id': 1, 'name': _('Улыбка'), 'genre': _('Ужасы')},
        {'id': 2, 'name': _('Матрица'), 'genre': _('Научная фантастика')},
        {'id': 3, 'name': _('Очень страшное кино'), 'genre': _('Комедия')}
    ]

    film_genre = request.args.get('genre')
    if film_genre:
        films = [film for film in films if film['genre'] == film_genre]

    return render_template('films.html', films=films)
