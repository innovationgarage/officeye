import sqlite3

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return None
        
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

def initialize_tables(database):
    sql_create_objects_table = """ CREATE TABLE IF NOT EXISTS objects (
    id integer PRIMARY KEY,
    obj_type text NOT NULL,
    last_event text,
    last_x_left text,
    last_y_left text,
    speed text
    ); """

    sql_create_events_table = """ CREATE TABLE IF NOT EXISTS events (
    id integer PRIMARY KEY,
    model text,
    w_in float,
    h_in float,
    x_left float,
    y_left float,
    x_top float,
    y_top float,
    w_b float,
    h_b float,
    prob float,
    timestamp text,
    obj_id integer NOT NULL,
    FOREIGN KEY (obj_id) REFERENCES objects(id)
    ); """
    
    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        # create objects table
        create_table(conn, sql_create_objects_table)
        # create events table
        create_table(conn, sql_create_events_table)
    else:
        print("Error! cannot create the database connection.")
    
