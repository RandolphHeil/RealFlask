# blog.py - controller for our flask blog

#imports

from flask import Flask, render_template, request, session, flash, redirect, url_for, g
from functools import wraps
import sqlite3


#configuration

DATABASE = "blog.db"
USERNAME = "admin"
PASSWORD = "admin"
SECRET_KEY = "f9qlcJtgzjfon2csvPI6u2hPnu5swy8gjEfE"

app = Flask(__name__)

# pulls in app configuration by looking for UPPERCASE variables
app.config.from_object(__name__)

#function used for connecting to database
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

# This function makes sure the user is logged in by comparing "logged_in" to sessions (set in login() )
# Dont really get how the wraps work...
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return test(*args, **kwargs)
        else:
            flash("You need to login first!")
            return redirect(url_for("login"))
    return wrap


# Gets called by login.html and compares username and password
# Sets the session to True if correct ( see login_required() ) and redirects to main()
@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    status_code = 200
    if request.method == "POST":
        if request.form["username"] != app.config["USERNAME"] or \
            request.form["password"] != app.config["PASSWORD"]:
            error = "Invalid Login. Please try again!"
            status_code = 401
        else:
            session["logged_in"] = True
            return redirect(url_for("main"))
    return render_template("login.html", error=error), status_code


# This is where all the posts are displayed; checks if user is logged in through login_required()
# Catches all the posts from the database and passes them to main.html to be displayed
@app.route("/main")
@login_required
def main():
    #Connect do database
    g.db = connect_db()

    #Fetch all the posts from the db
    cur = g.db.execute("SELECT * FROM posts")

    # Create a list of dictionaries with title and post content in each dict
    posts = [dict(title=row[0], post=row[1]) for row in cur.fetchall()]

    # Close connection to Database
    g.db.close()

    # Renders the main template and passes the posts variable we created earlier
    return render_template("main.html", posts=posts)


@app.route("/add", methods=["POST"])
@login_required
def add():
    # Get title and post from main.html through POST, this is to check if they are filled out
    title = request.form["title"]
    post = request.form["post"]

    # Check if all fields are filled in, if not return to main
    if not title or not post:
        flash("All fields are required. Try again!")
        return redirect(url_for("main"))
    else:
        g.db = connect_db()

        # Insert the new title and post into the DB, get the values from the html form
        g.db.execute("INSERT INTO posts (title, post) VALUES (?, ?)", [request.form["title"], request.form["post"]])
        g.db.commit()
        g.db.close()
        flash("New entry was posted!")
        return redirect(url_for("main"))




# Gets called in main.html, closes the session and redirects to login()
@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("You were logged out!")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)