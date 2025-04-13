import math
import secrets
import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session, flash
from datetime import date
import events
import courts
import config
import users

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.route("/")
@app.route("/<int:page>")
def index(page = 1):
    page_size = 5
    event_count = events.upcoming_event_count(date.today())
    page_count = max(math.ceil(event_count/page_size), 1)
    
    if page < 1:
        return redirect("/1")
    if page > page_count:
        return redirect(f"/{page_count}")
    
    allEvents = events.get_events(date.today(), page, page_size)
    locations = courts.get_courts()
    return render_template("index.html", page = page, page_count = page_count , allEvents = allEvents, locations = locations)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    
    if request.method == "POST":
        check_csrf()
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if not password1 == password2:
            flash("ERROR: Passwords do not match!")
            return redirect("/singup")
        
        try:
            users.create_user(password1, username)
        except sqlite3.IntegrityError:
            flash("ERROR: User already exists!")
            return redirect("/signup")

        return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(password, username)

        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            flash("ERROR: wrong username or password")
            return redirect("/login")
    
@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    del session["csrf_token"]
    return redirect("/")

@app.route("/event/<int:event_id>")
def show_event(event_id):
    event = events.get_event(event_id)
    messages = events.get_messages(event_id)

    return render_template("event.html", event = event, messages = messages)

#, method=["POST"]
@app.route("/new_event", methods=["POST"])
def new_event():
    check_csrf()
    require_login()

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
    require_login()
    events.remove_event(event_id)
    return redirect("/")

@app.route("/edit/<int:event_id>", methods=["GET", "POST"])
def edit_event(event_id):
    require_login()
    event = events.get_event(event_id)
    locations = courts.get_courts()
   
    if request.method == "GET":
        return render_template("editEvent.html", event = event, locations = locations)
    
    if request.method == "POST":
        check_csrf()
        date = request.form["date"]
        time = request.form["time"]
        location = request.form["location_id"]
        team_size = request.form["team_size"]
        events.update_event(event_id,team_size, time, date, location)
        return redirect(f"/event/{event_id}")
    
@app.route("/new_message", methods = ["POST"])
def new_message():
    check_csrf()
    require_login()
    content = request.form["content"]
    user_id = session["user_id"]
    event_id = request.form["event_id"]

    events.add_message(content, user_id, event_id)
    return redirect(f"/event/{event_id}")

@app.route("/edit/message/<int:message_id>", methods=["GET", "POST"])
def edit_message(message_id):
    require_login()
    messagep = events.get_message(message_id)

    if request.method == "GET":
        return render_template("editMessage.html", message = messagep)
    
    if request.method == "POST":
        check_csrf()
        content = request.form["content"]
        event_id = request.form["event_id"]
        events.update_message(message_id, content)
        return redirect(f"/event/{event_id}")

@app.route("/search")
def search():
    locations = courts.get_courts()
    date = request.args.get("date")
    time = request.args.get("time")
    court_id = request.args.get("court_id")
    if not court_id:
        court_id = 0

    results = events.get_events_by_date(date, time, int(court_id))
    return render_template("search.html", locations=locations, date=date, time=time, court_id=int(court_id), results=results)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    usersAllEvents = users.get_events(user_id)
    usersUpcomingEvents = users.get_latest_events(user_id)
    return render_template("user.html", user=user, events=usersAllEvents, upcoming=usersUpcomingEvents)
