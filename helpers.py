import os
import requests
import urllib.parse

from cs50 import SQL
from flask import redirect, render_template, request, session
from functools import wraps

db = SQL("sqlite:///albums.db")
url = "https://spotify23.p.rapidapi.com/albums/"

querystring = {"ids":"3IBcauSj5M2A6lTeffJzdv"}

headers = {
	"X-RapidAPI-Key": "7e0c0fb8c7msh5f85dae3076c683p1845b4jsn512cc4e4e4fb",
	"X-RapidAPI-Host": "spotify23.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)



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
    return render_template("apology.html", top=code, bottom=escape(message)), code


def searched(name):
    results = db.execute(
            "SELECT title,artist FROM metacritic WHERE title LIKE ?", '%'+name+'%')
    return render_template("results.html", results=results)


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


def lookup(album):
    """Look up quote for album."""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        url = f"https://spotify23.p.rapidapi.com/albums/"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "Title": quote["Title"],
            "Artist": quote["Artist"],
        }
    except (KeyError, TypeError, ValueError):
        return None
