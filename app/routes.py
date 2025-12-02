from flask import Blueprint, render_template, request
from flask_login import login_required
from flask_babel import _

bp = Blueprint("contents", __name__)

# --- Главная страница ---
@bp.route("/")
def index():
    return render_template("index.html")


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
        {
            "id": 1,
            "name": _("Улыбка"),
            "genre": "horror",
            "status": _("Просмотрено")
        },

        {
            "id": 2,
            "name": _("Матрица"),
            "genre": "sci-fi",
            "status": _("Просмотрено")
        },
        
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
            "status": _("Не просмотрено")
        }
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

    return render_template("series.html", series_list=series_list, 
                           genre=series_genre)
