import sqlite3

def get_db_cursor():
    connection = sqlite3.connect('./backend/database/test.db')
    cursor = connection.cursor()
    return cursor, connection

def create_tables():
    cursor, connection = get_db_cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS players(
                   first_name TEXT, 
                   last_name TEXT, 
                   id INTEGER PRIMARY KEY AUTOINCREMENT
                   )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS rooms(
                  room_code INTEGER PRIMARY KEY AUTOINCREMENT
                   )''')
    connection.commit()
    connection.close()

def database_has_room_code(room_code):
    cursor, connection = get_db_cursor()
    cursor.execute('SELECT 1 FROM rooms WHERE room_code = ?', (room_code,))
    isExisting = cursor.fetchone()
    connection.close()
    return isExisting

def insert_room_code(room_code):
    cursor, connection = get_db_cursor()
    cursor.execute('INSERT INTO rooms (room_code) VALUES (?)', (room_code,))
    connection.commit()
    connection.close()
