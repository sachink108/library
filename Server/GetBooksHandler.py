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
        elif category == 'favorite':
            _body = {
                "sort": {"timestamp": "desc"},
                "query": {
                    "query_string": {
                        "query": "true",
                        "fields": ["favourite"]  # search in this field
                    }
                }
            }
        elif category == 'current':
            _body = {
                "sort": {"timestamp": "desc"},
                "query": {
                    "query_string": {
                        "query": "true",
                        "fields": ["current"]  # search in this field
                    }
                }
            }
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
                                      "img" : imagePath,
                                      "favourite" : book['_source']['favourite'],
                                      "current": book['_source']['current']
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
