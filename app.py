import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///albums.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def home():

    # ratingf = db.execute("SELECT title, artist, rating FROM fantano")
    # ratingm = db.execute("SELECT title, artist, CriticScore FROM metacritic")

    # newrating =

    # for rating in ratingm:

    tops = db.execute(
        "SELECT DISTINCT fantano.title, fantano.artist, fantano.project_art FROM fantano JOIN metacritic ON fantano.title LIKE metacritic.title WHERE cast(fantano.rating AS Float) > 7.0 AND metacritic.CriticScore > 80 LIMIT 100")
    covers = db.execute(
        "SELECT project_art FROM fantano"
    )

    return render_template("home.html", tops=tops, covers=covers)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        # make sure username field is filled
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # make sure password field is filled
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # make sure the two passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords given don't match", 400)

        try:
            # get the new user id
            id = db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", request.form.get(
                "username"), generate_password_hash(request.form.get("password")))

        # make sure username is unique
        except ValueError:
            return apology("Username is taken", 400)

        # get session id
        session["user_id"] = id

        flash("Registered!")

        # send to home page
        return redirect("/")

    else:

        # make register.html
        return render_template("register.html")


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    """Allow user to change password"""

    if request.method == "POST":

        # check that username field is filled
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # check that password field is filled
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # check that new password field is filled
        elif not request.form.get("newpassword"):
            return apology("must provide a new password", 403)

        # store SQL line in a variable
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # get the user id
        session["user_id"] = rows[0]["id"]

        # update the password field in users
        db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(
            request.form.get("newpassword")), session["user_id"])

        # maintain same session id
        session["user_id"] = rows[0]["id"]

        flash("Password changed!")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        # make account.html
        return render_template("account.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        name = request.form.get("name")
        artist = request.form.get("artist")
        year = request.form.get("year")
        db.execute("INSERT INTO albums (name, artist, year) VALUES(?, ?)", name, artist, year)
        return redirect("/")

    else:

        albums = db.execute("SELECT * FROM albums")
        return render_template("index.html", albums=albums)

# @app.route("/top")
# def top():
#     """Show top albums for each genre"""
#     topalt = db.execute(
#         "SELECT DISTINCT fantano.title, fantano.artist, fantano.project_art FROM fantano JOIN metacritic ON fantano.title LIKE metacritic.title WHERE cast(fantano.rating AS Float) > 7.0 AND metacritic.CriticScore > 80 LIMIT 100")


# @app.route("/myalbums")
# @login_required
# def myalbums():
#     """Show history of transactions"""

#     # store SQL line in a variable
#     albums = db.execute(
#         "SELECT * FROM transactions WHERE user_id = ?", session["user_id"])

#     # make history.html
#     return render_template("history.html", transactions=transactions)
