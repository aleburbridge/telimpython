import sqlite3

connection = sqlite3.connect('./backend/database/test.db')

cursor = connection.cursor()

#TODO: clean up old lobbies
#TODO: make sure players wihtin lobby cannot have same name
cursor.execut('''CREATE TABLE IF NOT EXISTS players
              (first_name TEXT, last_nameTEST)''')

cursor.close()
connection.close()