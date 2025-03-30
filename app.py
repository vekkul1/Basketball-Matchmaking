from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from time import time
import sqlite3
import db
import events
import courts
import config

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    allEvents = events.get_events(date.today())
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
    messages = events.get_messages(event_id)

    return render_template("event.html", event = event, messages = messages)

#, method=["POST"]
@app.route("/new_event", methods=["POST"])
def new_event():
    location_id = request.form["location_id"]
    team_size = request.form["team_size"]
    dateform = request.form["date"]
    timeform = request.form["time"]

    if dateform < str(date.today()):
        return "The event you're trying to create is in the past."

    events.add_event(team_size, timeform, dateform, session["user_id"], location_id)
    return redirect("/")

@app.route("/remove/<int:event_id>")
def remove_event(event_id):
    events.remove_event(event_id)
    return redirect("/")

@app.route("/edit/<int:event_id>", methods=["GET", "POST"])
def edit_event(event_id):
    event = events.get_event(event_id)
    locations = courts.get_courts()
   
    if request.method == "GET":
        return render_template("editEvent.html", event = event, locations = locations)
    
    if request.method == "POST":
        date = request.form["date"]
        time = request.form["time"]
        location = request.form["location_id"]
        team_size = request.form["team_size"]
        events.update_event(event_id,team_size, time, date, location)
        return redirect(f"/event/{event_id}")
    
@app.route("/new_message", methods = ["POST"])
def new_message():
    content = request.form["content"]
    user_id = session["user_id"]
    event_id = request.form["event_id"]

    events.add_message(content, user_id, event_id)
    return redirect(f"/event/{event_id}")

@app.route("/edit/message/<int:message_id>", methods=["GET", "POST"])
def edit_message(message_id):
    messagep = events.get_message(message_id)

    if request.method == "GET":
        return render_template("editMessage.html", message = messagep)
    
    if request.method == "POST":
        content = request.form["content"]
        event_id = request.form["event_id"]
        events.update_message(message_id, content)
        redirect(f"/event/{messagep["event_id"]}")

@app.route("/search_date", methods=["POST"])
def search_date():
    date = request.form["datesort"]
    



