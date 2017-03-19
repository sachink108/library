import sys
import os
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None
    
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():

    database = "G:\\SachinK\progs\sqlite3\databases\users.db";
    create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        id INTEGER PRIMARY KEY,
                                        name text NOT NULL,
                                        password text NOT NULL
                                    ); """

    #database = "C:\\Users\sachinsk\Documents\personal\images_db\images.db"
    database = "G:\\SachinK\progs\sqlite3\databases\library.db";
    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS images (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        image blob NOT NULL
                                    ); """
 
    conn = create_connection(database)
    if conn is not None:
        #create_table(conn, create_users_table)
        #conn.cursor().execute("insert into users (name, password) values ('sachin', 'pass')")
        #conn.commit()
        #cursor = conn.cursor().execute("SELECT id from users where name='sachin' and password='pass'");
        #print (cursor.rowcount)
        #if (cursor.fetchone()):
        #    print ("user exists")
        #else:
        #    print ("User does not exits")
        cursor = conn.cursor().execute("SELECT image from books where user='sachin'");
        
        with open("writeout.jpg", "wb") as imageout:
                imageout.write(cursor.fetchone()[0])
    #exit;
'''
    if conn is not None:
        create_table(conn, sql_create_projects_table)
        with open("LeeChild_MakeMe.jpg", "rb") as imageFile:
            f = imageFile.read()
            b = bytearray(f)
            iq = """INSERT INTO images (id, name, image) 
                    VALUES ('1','LeeChild_MakeMe.jpg',b);
                 """
            conn.cursor().execute(iq)
            
            with open("writeout.jpg", "w") as imageout:
                imageout.write(b)
    else:
        print("Error! cannot create the database connection.")
'''
if __name__ == '__main__':
    main()