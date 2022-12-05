# importing all of the libraries we need
import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

# importing relevant functions from helpers.py
from helpers import apology, login_required, searched

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///albums.db")


# make sure responses aren't cached
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# creating the homepage
@app.route("/", methods=["GET", "POST"])
def home():

    # query the database to find the top rated albums in our dataset (had to standardize a rating system across metacritic and fantano)
    tops = db.execute(
        "SELECT DISTINCT fantano.title, fantano.artist, fantano.project_art, fantano.rating FROM fantano JOIN metacritic ON fantano.title LIKE metacritic.title ORDER BY ((cast(fantano.rating AS Float)*10) + cast(metacritic.CriticScore AS Float))/2.0 DESC LIMIT 100")

    # query the database for all the links to project art from the fantano table
    covers = db.execute(
        "SELECT project_art FROM fantano LIMIT 50")

    # render the home.html template and return tops and covers
    return render_template("home.html", tops=tops, covers=covers)


# creating the homepage
@app.route("/top", methods=["GET"])
def top():

    # query the database to find the top rated albums in our dataset (had to standardize a rating system across metacritic and fantano)
    hiphops = db.execute(
        "SELECT DISTINCT fantano.title, fantano.artist, fantano.project_art, metacritic.genre, ((cast(fantano.rating AS Float)*10) + cast(metacritic.CriticScore AS Float))/2.0 AS score FROM fantano JOIN metacritic ON fantano.title LIKE metacritic.title WHERE metacritic.genre = 'Hip Hop' ORDER BY ((cast(fantano.rating AS Float)*10) + cast(metacritic.CriticScore AS Float))/2.0 DESC LIMIT 10")

    indierocks = db.execute(
        "SELECT DISTINCT fantano.title, fantano.artist, fantano.project_art, metacritic.genre, ((cast(fantano.rating AS Float)*10) + cast(metacritic.CriticScore AS Float))/2.0 AS score FROM fantano JOIN metacritic ON fantano.title LIKE metacritic.title WHERE metacritic.genre = 'Indie Rock' ORDER BY ((cast(fantano.rating AS Float)*10) + cast(metacritic.CriticScore AS Float))/2.0 DESC LIMIT 10")

    indiepops = db.execute(
        "SELECT DISTINCT fantano.title, fantano.artist, fantano.project_art, metacritic.genre, ((cast(fantano.rating AS Float)*10) + cast(metacritic.CriticScore AS Float))/2.0 AS score FROM fantano JOIN metacritic ON fantano.title LIKE metacritic.title WHERE metacritic.genre = 'Indie Pop' ORDER BY ((cast(fantano.rating AS Float)*10) + cast(metacritic.CriticScore AS Float))/2.0 DESC LIMIT 10")

    altrocks = db.execute(
        "SELECT DISTINCT fantano.title, fantano.artist, fantano.project_art, metacritic.genre, ((cast(fantano.rating AS Float)*10) + cast(metacritic.CriticScore AS Float))/2.0 AS score FROM fantano JOIN metacritic ON fantano.title LIKE metacritic.title WHERE metacritic.genre = 'Alternative Rock' ORDER BY ((cast(fantano.rating AS Float)*10) + cast(metacritic.CriticScore AS Float))/2.0 DESC LIMIT 10")

    sss = db.execute(
        "SELECT DISTINCT fantano.title, fantano.artist, fantano.project_art, metacritic.genre, ((cast(fantano.rating AS Float)*10) + cast(metacritic.CriticScore AS Float))/2.0 AS score FROM fantano JOIN metacritic ON fantano.title LIKE metacritic.title WHERE metacritic.genre = 'Singer-Songwriter' ORDER BY ((cast(fantano.rating AS Float)*10) + cast(metacritic.CriticScore AS Float))/2.0 DESC LIMIT 10")

    poprocks = db.execute(
        "SELECT DISTINCT fantano.title, fantano.artist, fantano.project_art, metacritic.genre, ((cast(fantano.rating AS Float)*10) + cast(metacritic.CriticScore AS Float))/2.0 AS score FROM fantano JOIN metacritic ON fantano.title LIKE metacritic.title WHERE metacritic.genre = 'Pop Rock' ORDER BY ((cast(fantano.rating AS Float)*10) + cast(metacritic.CriticScore AS Float))/2.0 DESC LIMIT 10")

    electronics = db.execute(
        "SELECT DISTINCT fantano.title, fantano.artist, fantano.project_art, metacritic.genre, ((cast(fantano.rating AS Float)*10) + cast(metacritic.CriticScore AS Float))/2.0 AS score FROM fantano JOIN metacritic ON fantano.title LIKE metacritic.title WHERE metacritic.genre = 'Electronic' ORDER BY ((cast(fantano.rating AS Float)*10) + cast(metacritic.CriticScore AS Float))/2.0 DESC LIMIT 10")

    folks = db.execute(
        "SELECT DISTINCT fantano.title, fantano.artist, fantano.project_art, metacritic.genre, ((cast(fantano.rating AS Float)*10) + cast(metacritic.CriticScore AS Float))/2.0 AS score FROM fantano JOIN metacritic ON fantano.title LIKE metacritic.title WHERE metacritic.genre = 'Folk' ORDER BY ((cast(fantano.rating AS Float)*10) + cast(metacritic.CriticScore AS Float))/2.0 DESC LIMIT 10")

    pops = db.execute(
        "SELECT DISTINCT fantano.title, fantano.artist, fantano.project_art, metacritic.genre, ((cast(fantano.rating AS Float)*10) + cast(metacritic.CriticScore AS Float))/2.0 AS score FROM fantano JOIN metacritic ON fantano.title LIKE metacritic.title WHERE metacritic.genre = 'Pop' ORDER BY ((cast(fantano.rating AS Float)*10) + cast(metacritic.CriticScore AS Float))/2.0 DESC LIMIT 10")

    rnbs = db.execute(
        "SELECT DISTINCT fantano.title, fantano.artist, fantano.project_art, metacritic.genre, ((cast(fantano.rating AS Float)*10) + cast(metacritic.CriticScore AS Float))/2.0 AS score FROM fantano JOIN metacritic ON fantano.title LIKE metacritic.title WHERE metacritic.genre = 'R&B' ORDER BY ((cast(fantano.rating AS Float)*10) + cast(metacritic.CriticScore AS Float))/2.0 DESC LIMIT 10")

    # render the home.html template and return tops and covers
    return render_template("top.html", hiphops=hiphops, indierocks=indierocks, indiepops=indiepops, altrocks=altrocks, sss=sss, poprocks=poprocks, electronics=electronics, folks=folks, pops=pops, rnbs=rnbs)


# creates our album page: displays a specific album with it's album art if it exists and it's title and artist. also allows users to review the album
@app.route("/album", methods=["GET", "POST"])
def album():

    if request.method == "POST":

        # check if album title was submitted
        if not request.form.get("atitle"):
            return apology("must provide an album title", 400)

        # check if artist was submitted
        elif not request.form.get("aartist"):
            return apology("must provide an artist", 400)

        # check if rating was submitted
        elif not request.form.get("rating"):
            return apology("must provide rating", 400)

        elif not request.form.get("dname"):
            return apology("must provide display name", 400)

        # insert a new row into the reviews table with the relevant review
        db.execute("INSERT INTO reviews (album, artist, userid, displayname, review, rating) VALUES(?, ?, ?, ?, ?, ?)", request.form.get(
            "atitle"), request.form.get("aartist"), session["user_id"], request.form.get("dname"), request.form.get("review"), request.form.get("rating"))

        # flash a notice that the review was submitted
        flash("Review Submitted!")

        # redirect to homepage
        return redirect("/")

    # render the album.html template
    else:
        return render_template("album.html")

    
@app.route("/suggest", methods=["GET", "POST"])
@login_required
def suggest():
    # necessary form inputs are all there
    if request.method == "POST":
        if not request.form.get("atitle"):
            return apology("must provide an album title", 400)
        elif not request.form.get("aartist"):
            return apology("must provide an artist", 400)
        elif not request.form.get("rating"):
            return apology("must provide rating", 400)

        #insert their review in reviews and their suggested album into both needed tables
        db.execute("INSERT INTO reviews (album, artist, userid, review, rating) VALUES(?, ?, ?, ?, ?)", request.form.get(
            "atitle"), request.form.get("aartist"), session["user_id"], request.form.get("review"), request.form.get("rating"))
        db.execute("INSERT INTO metacritic (artist, title, year, format, label, genre) VALUES(?, ?, ?, ?, ?, ?)", request.form.get(
            "aartist"), request.form.get("atitle"), request.form.get("year"), request.form.get("projecttype"), request.form.get("label"),
            request.form.get("genre"))
        db.execute("INSERT INTO fantano (spotify_id, title, artist, project_type, tracks, project_art, year VALUES(?, ?, ?, ?, ?, ?, ?)", request.form.get("spid"),
            request.form.get("atitle"), request.form.get("aartist"), request.form.get("projecttype"), request.form.get("numtrack"), request.form.get("project_art"),
            request.form.get("year"))

        flash("Review Submitted!")

        return redirect("/")
    else:
        return render_template("suggest.html")

# creates a page to register a user on our website
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        # make sure username field is filled
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # make sure display name field is filled
        elif not request.form.get("displayname"):
            return apology("music provide display name", 400)

        # make sure password field is filled
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # make sure the two passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords given don't match", 400)

        try:
            # get the new user id
            id = db.execute("INSERT INTO users (username, displayname, hash) VALUES(?, ?, ?)", request.form.get(
                "username"), request.form.get("displayname"), generate_password_hash(request.form.get("password")))

        # make sure username is unique
        except ValueError:
            return apology("Username is taken", 400)

        # get session id
        session["user_id"] = id

        # flash a notice that the user is registered
        flash("Registered!")

        # send to homepage
        return redirect("/")

    else:

        # render register.html
        return render_template("register.html")


# creates an account page that allows the user to change their password
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

        # flash notice password has changed
        flash("Password changed!")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        # make account.html
        return render_template("account.html")


# creates a way for users to search for specific albums in our database
@app.route("/search", methods=["GET", "POST"])
def search():

    if request.method == "POST":

        # make sure query field is filled
        if not request.form.get("query"):
            return apology("value not inputted", 403)

        # set query to a variable
        name = request.form.get("query")

        # return name to the search function in searched from helpers.py
        return searched(name)

    # render search.html
    else:
        return render_template("search.html")


# creates a results page that displays results from the search function
@app.route("/results", methods=["GET", "POST"])
def results():

    # render results.html
    return render_template("results.html")


# creates a log in page that allows a preexisting user to log in
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # check that username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # check password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to homepage
        return redirect("/")

    # render login.html
    else:
        return render_template("login.html")


# creates a page that allows a user to log out
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # redirects to homepage
    return redirect("/")
