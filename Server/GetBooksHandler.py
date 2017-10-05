import os
import tornado.websocket
import logging
import sqlite3
from URIParser import *
from elasticsearch import Elasticsearch

database_dir = "C:\\databases"
users_db = os.path.join(database_dir, "users.db")
gClient = Elasticsearch([{'host': 'localhost', 'port': 9200}])
gElasticIndex = "books"

class GetBooksHandler(tornado.web.RequestHandler):
    def _getCategoryCounts(self, docType):
        self.set_header("Access-Control-Allow-Origin", "*")
        _body = {
            "size": 0,
            "aggs": {
                "distinct_categories": {
                    "terms": {
                        "field": "category.keyword",
                        "size": 1000
                    }
                }
            }
        }
        elasticResp = gClient.search(index=gElasticIndex, doc_type=docType, body=_body)
        catret = []
        for cat in elasticResp["aggregations"]["distinct_categories"]["buckets"]:
            catret.append({'name': cat["key"], 'count': cat["doc_count"]})

    def _getBooks(self, category, docType):
        self.set_header("Access-Control-Allow-Origin", "*")
        if category == 'recent':
            _body = { "sort": {"timestamp": "asc"}, "size": 5 }
        else:
            _body = {
                "sort": {"timestamp": "asc"},
                "query": {
                    "query_string": {
                        "query": category,
                        "fields": ["category"] # search in this field
                    }
                }
            }
        elasticResp = gClient.search(index=gElasticIndex, doc_type=docType, body=_body)
        ret = {}
        if elasticResp['hits']['total']:
            for book in elasticResp['hits']['hits']:
                if category not in ret: # have to handle multi category
                    ret[category] = []

                imagePath = book['_source']['image_filepath']
                imagePath = os.path.relpath(imagePath, database_dir)
                imagePath.replace("\\", "/")
                ret[category].append({"author": book['_source']['author'],
                                      "title": book['_source']['title'],
                                      #"img": "%s/%s" % (r['user'], row[4]),
                                      "img" : imagePath
                                    })

    def get(self,info):
        self.set_header("Access-Control-Allow-Origin", "*")
        logging.info("GET /getbooks")
        uriparser = URIParser()
        r = uriparser.parse(info)['dict']
        username = r['user']
        category = r['cat']
        print("Getting books for %s of category %s" % (username, category))
        docType=username+gElasticIndex
        #ret = self._getBooks(category, docType) #somehow this is not working
        if category == 'recent':
            _body = { "sort": {"timestamp": "desc"}, "size": 5 }
        else:
            _body = {
                "sort": {"timestamp": "desc"},
                "query": {
                    "query_string": {
                        "query": category,
                        "fields": ["category"] # search in this field
                    }
                }
            }
        elasticResp = gClient.search(index=gElasticIndex, doc_type=docType, body=_body)
        ret = {}
        if elasticResp['hits']['total']:
            for book in elasticResp['hits']['hits']:
                if category not in ret: # have to handle multi category
                    ret[category] = []

                imagePath = book['_source']['image_filepath']
                imagePath = os.path.relpath(imagePath, database_dir)
                imagePath.replace("\\", "/")
                ret[category].append({"author": book['_source']['author'],
                                      "title": book['_source']['title'],
                                      "id" : book['_id'],
                                      "img" : imagePath
                                    })
        #catret = self._getCategoryCounts(docType)

        # This part has to be sent everytime? is it necessary?
        _body = {
            "size": 0,
            "aggs": {
                "distinct_categories": {
                    "terms": {
                        "field": "category.keyword",
                        "size": 1000
                    }
                }
            }
        }
        elasticResp = gClient.search(index=gElasticIndex, doc_type=docType, body=_body)
        catret = []
        for cat in elasticResp["aggregations"]["distinct_categories"]["buckets"]:
            catret.append({'name': cat["key"], 'count': cat["doc_count"]})
        self.write({'books': ret,
                    'categories': catret})
'''
class GetBooksHandler(tornado.web.RequestHandler):
    def get(self, info):
        self.set_header("Access-Control-Allow-Origin", "*")
        logging.info("GET /getbooks")
        global users_db
        global database_dir
        uriparser = URIParser()
        r = uriparser.parse(info)['dict']
        print ("Getting books for %s of category %s" %(r['user'], r['cat']))
        
        user_dir = os.path.join(database_dir, r['user'])
        user_db = os.path.join(user_dir, r['user'] + ".db")
        conn = sqlite3.connect(user_db)
        if (r['cat'] == 'recent'):
            q = "SELECT * FROM books ORDER BY timestamp DESC LIMIT 5";
        else:
            q = "SELECT * FROM books WHERE category='%s' ORDER BY timestamp DESC" % r['cat']
        cursor = conn.cursor().execute(q)
        ret = {}
        for row in cursor.fetchall():
            cat = row[3]
            if (cat not in ret):
                ret[cat] = []
            ret[cat].append( {"author" : row[1],
                              "title" : row[2],
                               "img": "%s/%s" % (r['user'],row[4]),
                              } )
        
        q = "SELECT category, count(*) FROM books GROUP BY category";
        cursor = conn.cursor().execute(q)
        catret = []
        for row in cursor.fetchall():
            catret.append({'name': row[0], 'count': row[1]})

        self.write({'books': ret,
                    'categories': catret})
'''