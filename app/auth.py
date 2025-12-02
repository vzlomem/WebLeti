from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from .models import User, users
from flask_babel import _

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and User(username).check_password(password):
            user = User(username)
            login_user(user)
            flash(_("Вы успешно вошли"), "success")
            return redirect(
                url_for("contents.index", lang=request.form.get("lang", "ru"))
            )
        else:
            flash(_("Неверное имя пользователя или пароль"), "danger")

    return render_template("login.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash(_("Вы вышли из системы"), "info")
    return redirect(url_for("auth.login"))
