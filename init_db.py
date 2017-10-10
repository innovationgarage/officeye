import sqlite3
import db_tools as db

db_file = 'db/pyolo.db'
db.create_connection(db_file)
db.initialize_tables(db_file)
