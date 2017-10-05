import os
import tornado.websocket
import logging
from URIParser import *
from elasticsearch import Elasticsearch

database_dir = "C:\\databases"
users_db = os.path.join(database_dir, "users.db")
gClient = Elasticsearch([{'host': 'localhost', 'port': 9200}])
gElasticIndex = "books"

class DeleteBookHandler(tornado.web.RequestHandler):
    def post(self, info):
        self.set_header("Access-Control-Allow-Origin", "*")
        logging.info("DELETE /getbooks")
        uriparser = URIParser()
        r = uriparser.parse(info)['dict']
        username = r['user']
        book_id = r['book_id']
        print("Deleting book with id %s of user %s" % (book_id, username))
        docType = username + gElasticIndex
        elasticResp = gClient.delete(index=gElasticIndex, doc_type=docType, id=book_id)
        ret = {}
        if elasticResp["result"] == "deleted":
            self.write({'status': "OK"})
        else:
            self.write({'status': "NOK"})
