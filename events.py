import db

def get_events():
    sql = """SELECT e.id, l.name, e.size, e.time, u.username
            FROM events e, locations l, users u
             WHERE e.location_id = l.id
            GROUP BY e.id
             ORDER BY e.id DESC"""
    return db.query(sql)

def get_event(event_id):
    sql = """SELECT e.id, l.name, l.address, e.size, e.time, u.username
            FROM events e, locations l, users u
             WHERE e.location_id = l.id 
            AND e.id = ?"""
    return db.query(sql, [event_id])[0]


def add_event(size, time, date, user_id, location_id):
    sql = """INSERT INTO events (size, time, date, user_id, location_id)
            VALUES (?,?,?,?,?)"""
    db.execute(sql, [size, time, date, user_id, location_id])
    return db.last_insert_id()
