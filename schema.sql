CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    image BLOB
);

CREATE TABLE locations ( 
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    address TEXT UNIQUE
);

CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    size INTEGER,
    time TEXT,
    date TEXT,
    user_id INTEGER REFRENCES users,
    location_id INTEGER REFRENCES locations
);

CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    content TEXT,
    send_time TEXT,
    user_id INTEGER REFRENCES users,
    event_id INTEGER REFRENCES events
);

CREATE TABLE signups (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFRENCES users,
    event_id INTEGER REFRENCES events
);

CREATE INDEX idx_event_messages ON messages (event_id);
CREATE INDEX idx_event_signups ON signups (event_id);
