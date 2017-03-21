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
#https://technobeans.com/2012/09/17/tornado-file-uploads/
'''
import tornado
import tornado.ioloop
import tornado.web
import os, uuid

__UPLOADS__ = "uploads/"

class Userform(tornado.web.RequestHandler):
    def get(self):
        self.render("fileuploadform.html")


class Upload(tornado.web.RequestHandler):
    def post(self):
        fileinfo = self.request.files['filearg'][0]
        print "fileinfo is", fileinfo
        fname = fileinfo['filename']
        extn = os.path.splitext(fname)[1]
        cname = str(uuid.uuid4()) + extn
        fh = open(__UPLOADS__ + cname, 'w')
        fh.write(fileinfo['body'])
        self.finish(cname + " is uploaded!! Check %s folder" %__UPLOADS__)


application = tornado.web.Application([
        (r"/", Userform),
        (r"/upload", Upload),
        ], debug=True)


if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

<html>
<head> 
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/> 
<title>Upload Form</title>
</head>
<body>
<p><h1>Select & Upload</h1></p>
<form enctype="multipart/form-data" action="/upload" method="post">
File: <input type="file" name="filearg" />
<br />
<br />
<input type="submit" value="upload" />
</form>
'''





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
        
