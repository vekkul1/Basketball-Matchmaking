from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import db
import events
import courts
import config

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    allEvents = events.get_events()
    locations = courts.get_courts()
    return render_template("index.html", allEvents = allEvents, locations = locations)

@app.route("/signup")
def signup():
    return render_template("signup.html", message="")

@app.route("/create", methods = ["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if not password1 == password2:
        return render_template("signup.html", message = "ERROR: Passwords do not match!")
    
    password_hash = generate_password_hash(password1)
    
    try:
        sql = """
                INSERT INTO users (username, password_hash)
                VALUES (?, ?)
              """
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return render_template("signup.html", message = "ERROR: USER ALREADY EXISTS!")
    
    session["user_id"] = db.last_insert_id()
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    sql = """
        SELECT id, password_hash
        FROM users
        WHERE username = ?
    """
    try:
        user_id, password_hash = db.query(sql, [username])[0]
    except:
        return render_template("index.html", message="ERROR: wrong username or password")

    if check_password_hash(password_hash, password):
        session["user_id"] = user_id
        return redirect("/")
    else:
        return render_template("index.html", message="ERROR: wrong username or password")
    
@app.route("/logout")
def logout():
    del session["user_id"]
    return redirect("/")

@app.route("/event/<int:event_id>")
def show_event(event_id):
    event = events.get_event(event_id)
    return render_template("event.html", event = event)

#, method=["POST"]
@app.route("/new_event", methods=["POST"])
def new_event():
    location_id = request.form["location_id"]
    team_size = request.form["team_size"]
    date = request.form["date"]
    time = request.form["time"]
    events.add_event(team_size, time, date, session["user_id"], location_id)
    return f"{location_id} {team_size} {str(date)+' '+str(time)}"
