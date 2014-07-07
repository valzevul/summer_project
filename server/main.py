__author__ = 'AlZimin'

import os
import sqlite3
from flask import *
import decoder
import json

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, "flaskr.db"),
    DEBUG=True,
    SECRET_KEY="development key",
    USERNAME="admin",
    PASSWORD="default"
))
app.config.from_envvar("FLASKR_SETTINGS", silent=True)

def connect_db():
    rv = sqlite3.connect(app.config["DATABASE"])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, "sqlite_db"):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, "sqlite_db"):
        g.sqlite_db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource("schema.sql", mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route("/getArticles", methods=["GET"])
def get_articles():
    db = get_db()
    cur = db.execute("select title, text, id from entries order by id desc")

    handler = decoder.SuperHandler()
    dic = {}
    for el in cur.fetchall():
        dic[el[2]] = handler.call_up_encoding(el[0], el[1])
    return json.dumps(dic)

@app.route("/")
def show_entries():
    db = get_db()
    cur = db.execute("select title, text from entries order by id desc")
    entries = cur.fetchall()
    return render_template("show_entries.html", entries=entries)
        
        
@app.route("/add", methods=["POST"])
def add_entry():
    if not session.get("logged_in"):
        abort(401)
    db = get_db()
    db.execute("insert into entries (title, text) values (?, ?)",
                 [request.form["title"], request.form["text"]])
    db.commit()
    flash("New entry was successfully posted")
    return redirect(url_for("show_entries"))

# @app.route("/remove", methods=["POST"])
# def remove_entry():
#     if not session.get("logged_in"):
#         abort(401)
#     db = get_db()
#     db.session.delete('delete from entries where id=' + entry_id)
#     db.commit()


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form["username"] != app.config["USERNAME"]:
            error = "Invalid username"
        elif request.form["password"] != app.config["PASSWORD"]:
            error = "Invalid password"
        else:
            session["logged_in"] = True
            flash("You were logged in")
            return redirect(url_for("show_entries"))
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("You were logged out")
    return redirect(url_for("show_entries"))

# @app.route('/')
# @app.route('/index')
# def index():
#     return '''
# <html>
#   <head>
#   <style type="text/css">
#   body {
#     color: purple;
#     background-color: #e8e8e8 }
#
#     button{
#     width: 100px;
#     height: 200px;
#     font-size: 200%;
#     background-color: #e8e8e8
# }
#
#   </style>
#     <title>Admin page</title>
#   </head>
#   <body>
#   <button type="button">+</button>
#   <button type="button">-</button>
#   </body>
# </html>
# '''


if __name__ == "__main__":
    app.run( debug = True )