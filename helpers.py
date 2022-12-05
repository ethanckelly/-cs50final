# import relevant libraries
import os
import requests
import urllib.parse

from cs50 import SQL
from flask import redirect, render_template, request, session
from functools import wraps

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///albums.db")

# apology function
def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.
        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s

    # render apology.html
    return render_template("apology.html", top=code, bottom=escape(message)), code


def searched(name):
    # query for just the search results
    results = db.execute(
        "SELECT title,artist FROM metacritic WHERE title LIKE ?", '%'+name+'%')
    # query for the reviews related to the album
    reviews = db.execute(
        "SELECT metacritic.title,metacritic.artist,fantano.project_art,reviews.review,reviews.rating,reviews.displayname "
        "FROM metacritic LEFT JOIN fantano ON metacritic.title LIKE fantano.title "
        "LEFT JOIN reviews ON metacritic.title LIKE reviews.album AND metacritic.artist LIKE reviews.artist WHERE metacritic.title LIKE ? "
        "UNION "
        "SELECT metacritic.title,metacritic.artist,fantano.project_art,reviews.review,reviews.rating,reviews.displayname "
        "FROM reviews LEFT JOIN metacritic ON metacritic.title LIKE reviews.album AND metacritic.artist LIKE reviews.artist "
        "LEFT JOIN fantano ON metacritic.title LIKE fantano.title WHERE metacritic.title LIKE ? ", '%'+name+'%', '%'+name+'%')
    # pass everything to results
    return render_template("results.html", results=results, reviews=reviews)


# check whether the user must be logged in to see this
def login_required(f):
    """
    Decorate routes to require login.
    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
