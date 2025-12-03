from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    make_response,
    session,
)
from flask_login import login_required
from flask_babel import _
from datetime import datetime


bp = Blueprint("contents", __name__)


@bp.route("/")
def index():
    return render_template('index.html')


@bp.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        favorite_genre = request.form.get("favorite_genre", "Не выбран")
        email = request.form.get("email", "").strip()

        # Сохраняем данные в cookies
        resp = make_response(redirect(url_for("contents.result")))
        resp.set_cookie("user_name", username, max_age=60 * 60 * 24 * 7)  # на 7 дней
        resp.set_cookie("favorite_genre", favorite_genre, max_age=60 * 60 * 24 * 7)
        resp.set_cookie("email", email, max_age=60 * 60 * 24 * 7)

        # Сохраняем количество визитов и время последнего посещения в сессии
        user_counts = session.get("user_visit_counts", {})
        user_counts[username] = user_counts.get(username, 0) + 1
        session["user_visit_counts"] = user_counts
        session["last_visit"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return resp

    saved_username = request.cookies.get("user_name", "")
    saved_genre = request.cookies.get("favorite_genre", "Не выбран")
    saved_email = request.cookies.get("email", "")

    return render_template(
        "form.html",
        saved_username=saved_username,
        saved_genre=saved_genre,
        saved_email=saved_email,
    )


@bp.route("/result")
def result():
    username = request.cookies.get("user_name", "Аноним")
    favorite_genre = request.cookies.get("favorite_genre", "Не выбран")
    email = request.cookies.get("email", "Не указана")

    user_counts = session.get("user_visit_counts", {})
    visit_count = user_counts.get(username, 0)

    last_visit = session.get("last_visit", "Никогда")

    return render_template(
        "result.html",
        username=username,
        favorite_genre=favorite_genre,
        email=email,
        visit_count=visit_count,
        last_visit=last_visit,
    )


# --- Страница медиатеки ---
@bp.route("/contents")
@login_required
def contents():
    contents_list = [
        {"name": "Фильмы", "url": "films"},
        {"name": "Сериалы", "url": "series"},
    ]
    return render_template("contents.html", contents=contents_list)


@bp.route("/films", methods=["GET"])
@login_required
def films():
    # Список фильмов
    films_list = [
        {"id": 1, "name": _("Улыбка"), "genre": "horror", "status": _("Просмотрено")},
        {"id": 2, "name": _("Матрица"), "genre": "sci-fi", "status": _("Просмотрено")},
        {
            "id": 3,
            "name": _("Очень страшное кино"),
            "genre": "comedy",
            "status": _("Не просмотрено"),
        },
        {
            "id": 4,
            "name": _("Голый пистолет"),
            "genre": "comedy",
            "status": _("Не просмотрено"),
        },
    ]

    # Локализация жанров
    genre_map = {
        "horror": _("Ужасы"),
        "sci-fi": _("Научная фантастика"),
        "comedy": _("Комедия"),
    }

    for film in films_list:
        film["genre_display"] = genre_map.get(film["genre"], film["genre"])

    # --- Фильтрация по выбранным жанрам (через чекбоксы) ---
    selected_genres = request.args.getlist("genre")  # список выбранных жанров
    if selected_genres:
        films_list = [f for f in films_list if f["genre"] in selected_genres]

    # --- Сортировка по имени ---
    sort_order = request.args.get("sort", "asc")
    films_list.sort(key=lambda x: x["name"], reverse=(sort_order == "desc"))

    return render_template(
        "films.html",
        films=films_list,
        selected_genres=selected_genres,
        sort_order=sort_order,
    )


# --- Страница сериалов ---
@bp.route("/series", methods=["GET"])
@login_required
def series():
    series_list = [
        {"id": 1, "name": "Очень странные дела", "genre": "sci-fi"},
        {"id": 2, "name": "Друзья", "genre": "comedy"},
    ]

    # Локализация жанров
    genre_map = {
        "horror": _("Ужасы"),
        "sci-fi": _("Научная фантастика"),
        "comedy": _("Комедия"),
    }

    for s in series_list:
        s["genre_display"] = genre_map.get(s["genre"], s["genre"])

    # Фильтр по жанру
    series_genre = request.args.get("genre", "all")
    if series_genre != "all":
        series_list = [s for s in series_list if s["genre"] == series_genre]

    return render_template("series.html", series_list=series_list, genre=series_genre)
