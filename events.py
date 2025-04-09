from datetime import date
import db

def get_events(date, page, page_size):
    sql = """SELECT e.id, l.name, e.size, e.time, e.date, u.username
            FROM events e, locations l, users u
             WHERE e.location_id = l.id
            AND e.user_id = u.id
             AND e.date >= ?
            GROUP BY e.id
             ORDER BY e.date, e.time
            LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page-1)
    return db.query(sql, [date, limit, offset])

def courts_events(court_id, date): # currently not in  use
    sql = """SELECT e.id, l.name, e.size, e.time, e.date, u.username
            FROM events e, locations l, users u
             WHERE e.location_id = ?
            AND e.user_id = u.id
             AND e.date > ?
            GROUP BY e.id
             ORDER BY e.date"""
    return db.query(sql, [court_id, date])

def get_events_by_date(dateArg, time, court_id):
    if not time:
        time = "00:00"
    if not dateArg:
        dateArg = date.today()
    if court_id > 0:
        sql = """SELECT e.id, l.name, e.size, e.time, e.date, u.username
                FROM events e, locations l, users u
                 WHERE e.location_id = l.id
                AND e.user_id = u.id
                 AND e.date = ?
                AND e.time >= ?
                 AND e.location_id = ?
                GROUP BY e.id
                 ORDER BY e.date, e.time ASC"""
        return db.query(sql, [dateArg, time, court_id])
    else:
        sql = """SELECT e.id, l.name, e.size, e.time, e.date, u.username
                FROM events e, locations l, users u
                 WHERE e.location_id = l.id
                AND e.user_id = u.id
                 AND e.date = ?
                AND e.time >= ?
                 GROUP BY e.id
                ORDER BY e.date, e.time ASC"""
        return db.query(sql, [dateArg, time])
    

def get_event(event_id):
    sql = """SELECT e.id, l.name, l.address, e.size, e.date, e.time, e.user_id, u.username
            FROM events e, locations l, users u
             WHERE e.location_id = l.id
            AND e.user_id = u.id 
             AND e.id = ?"""
    return db.query(sql, [event_id])[0]

def add_event(size, time, date, user_id, location_id):
    sql = """INSERT INTO events (size, time, date, user_id, location_id)
            VALUES (?,?,?,?,?)"""
    db.execute(sql, [size, time, date, user_id, location_id])
    return db.last_insert_id()

def remove_event(event_id):
    sql = """DELETE 
            FROM events
            WHERE id == ?"""
    db.execute(sql, [event_id])

def update_event(event_id, size, time, date, location_id):
    sql = """UPDATE events
            SET size = ?,
             time = ?,
            date = ?,
             location_id = ?
            WHERE id = ?"""
    db.execute(sql, [size, time, date, location_id, event_id]) 

def add_message(content, user_id, event_id):
    sql = """INSERT INTO messages (content, send_time, user_id, event_id)
            VALUES (?, datetime('now'), ?, ?)"""
    db.execute(sql, [content, user_id, event_id])

def get_messages(event_id):
    sql = """SELECT m.id, m.content, m.send_time, m.user_id, u.username, m.event_id
            FROM messages m, users u
             WHERE m.event_id = ?
            AND u.id = m.user_id"""
    return db.query(sql, [event_id])

def get_message(message_id):
    sql = """SELECT m.id, m.content, m.send_time, m.user_id, u.username, m.event_id
            FROM messages m, users u
             WHERE m.id = ?
            AND u.id = m.user_id"""
    return db.query(sql, [message_id])[0]

def update_message(message_id, content):
    sql = """UPDATE messages
            SET content = ?
             WHERE id = ?"""
    db.execute(sql, [content, message_id])

def event_count():
    sql = """SELECT COUNT(*)
            FROM events"""
    return db.query(sql)[0][0]

def upcoming_event_count(date):
    sql = """SELECT COUNT(*)
            FROM events
             WHERE date >= ?"""
    return db.query(sql, [date])[0][0]