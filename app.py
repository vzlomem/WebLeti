from flask import Flask, render_template, url_for, request

app = Flask(__name__)


@app.route("/")
def index():
    print(url_for('index'))
    return render_template('index.html')


@app.route('/contents')
def contents():
    print(url_for('contents'))
    contents = [
        {'name': 'Фильмы', 'url': 'films'},
        {'name': 'Сериалы', 'url': 'series'},
        {'name': 'Книги', 'url': 'books'}
    ]
    return render_template('contents.html', contents=contents)


@app.route('/films', methods=['GET'])
def films():
    print(url_for('films'))
    films = [
        {'id': 1, 'name': 'Улыбка', 'genre': 'Ужасы'},
        {'id': 2, 'name': 'Матрица', 'genre': 'Фантастика'},
        {'id': 3, 'name': 'Очень страшное кино', 'genre': 'Комедия'}
    ]

    film_genre = request.args.get('genre')
    if film_genre:
        films = [film for film in films if film['genre'] == film_genre]

    return render_template('films.html', films=films)



if __name__ == "__main__":
    app.run(debug=True)
