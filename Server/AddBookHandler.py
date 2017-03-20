import os
import sys
import json
import tornado.ioloop
import tornado.web
import logging
import sqlite3
from URIParser import *

database = "G:\\SachinK\progs\sqlite3\databases\library.db";
create_books_table = """ CREATE TABLE IF NOT EXISTS books (
                                        id INTEGER PRIMARY KEY,
                                        user text NOT NULL,
                                        title text NOT NULL,
                                        author text NOT NULL,
                                        image blob
                                    ); """
                                    
# /addbook/
class AddBookHandler(tornado.web.RequestHandler):
    def post(self, book_details):
        self.set_header("Access-Control-Allow-Origin", "*")
        global database
        global create_book_table
        self.write({'status' : "OK"})
        status = ''
        conn = sqlite3.connect(database)
        r = json.loads(self.request.body)
        
        if conn is not None:
            conn.cursor().execute(create_books_table)
            print ("Adding book")
            conn.cursor().execute("INSERT INTO books (user, title, author, image) VALUES (?,?,?,?)", (r['user'], r['title'], r['author'], r['image']))
            conn.commit()
            status = 'added'
        else:
            status = 'error connecting to db'
        self.write({'status' : status})
        
