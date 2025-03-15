import db

def get_courts():
    sql = """SELECT id, name, address
            FROM locations"""
    return db.query(sql)