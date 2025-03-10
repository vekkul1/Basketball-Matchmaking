from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import db
import config

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods = ["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if not password1 == password2:
        return render_template("created.html", message = "ERROR: Passwords do not match!")
    
    password_hash = generate_password_hash(password1)
    
    try:
        sql = """
                INSERT INTO users (username, password_hash)
                VALUES (?, ?)
              """
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return render_template("created.html", message = "ERROR: USER ALREADY EXISTS!")
    
    session["username"] = username
    return render_template("created.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    sql = """
        SELECT password_hash
        FROM users
        WHERE username = ?
    """
    password_hash = db.query(sql, [username])[0][0]

    if check_password_hash(password_hash, password):
        session["username"] = username
        return redirect("/")
    else:
        return "ERROR: wrong username or password"
    
@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")