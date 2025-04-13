from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
import db

def create_user(password, username):
    password_hash = generate_password_hash(password)
    sql = """INSERT INTO users (username, password_hash)
            VALUES (?, ?)"""
    db.execute(sql, [username, password_hash])

def check_login(password, username):
    sql = """SELECT id, password_hash
            FROM users
             WHERE username = ?"""
    result = db.query(sql, [username])
    
    if len(result) == 1:
        user_id, password_hash = result[0]
        if check_password_hash(password_hash, password):
            return user_id
    return None

def get_user(user_id):
    sql = """SELECT username
            FROM users
             WHERE id = ?"""
    query = db.query(sql, [user_id])
    return query[0] if query else None

def get_events(user_id):
    sql = """SELECT e.id, e.date, e.time
            FROM events e
             WHERE e.user_id = ?
            GROUP BY e.id
             ORDER BY e.date, e.time"""
    return db.query(sql, [user_id])

def get_latest_events(user_id, date = date.today(), limit = 5):
    sql = """SELECT e.id, l.name, e.size, e.time, e.date, u.username, e.user_id
            FROM events e, locations l, users u
             WHERE e.location_id = l.id
            AND e.user_id = u.id
             AND e.user_id = ?
            AND e.date >= ?
             GROUP BY e.id
            ORDER BY e.date, e.time
             LIMIT ?"""
    return db.query(sql, [user_id, date, limit])