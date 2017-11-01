import os
import uuid
import time
import tornado.web
import base64
import datetime
from elasticsearch import Elasticsearch
import boto3

#database_dir = "C:\\databases"
database_dir = os.path.join(os.path.dirname(__file__), 'static')
database_dir = os.path.join(database_dir, 'img')

gClient = Elasticsearch([{'host': 'localhost', 'port': 9200}])
gElasticIndex = "books"
gS3Bucket = "my-library_1508745849196"

#http://docs.aws.amazon.com/AmazonS3/latest/dev/example-bucket-policies.html
class AddBookHandler(tornado.web.RequestHandler):
    def _saveImage(self, request):
        user_id = self.get_body_argument("user_id", default=None, strip=False)

        if (len(self.request.files.keys()) > 0):  # desktop
            fileinfo = self.request.files['0'][0]
            filename = fileinfo['filename']
            imgData = fileinfo['body']
        else:  # mobile
            filename = str(uuid.uuid4()) + ".jpg"
            imgData = self.get_body_argument("0", default=None, strip=False)
            imgData = base64.decodebytes(bytes(imgData, 'utf-8'))

        if os.environ['LIBRARY_IMAGE_STORE'] == 'LOCAL_STORE':
            return self._saveImageToLocal(filename, imgData, user_id)
        else:
            return self._saveImageToS3(filename, imgData, user_id)

    def _saveImageToS3(self, filename, imgData, userId):
        imgfilename = userId + "/" + filename
        s3 = boto3.resource('s3')
        s3.Bucket(gS3Bucket).put_object(Key=imgfilename, Body=imgData)

        imgurl = "https://s3.amazonaws.com" + "/" + gS3Bucket + "/" +imgfilename;
        return imgurl

    def _saveImageToLocal(self, filename, imgData, userId):
        userdir = userId + "_es"
        userdir = os.path.join(database_dir, userdir)

        if not os.path.exists(userdir):
            os.makedirs(userdir)

        ofile = os.path.join(userdir, filename)
        fh = open(ofile, 'wb')
        fh.write(imgData)
        #imageUrl = "http://localhost:9000/static/" + userId + "_es/" + filename #crap coding
        imageUrl = "http://localhost:9000/img/" + userId + "_es/" + filename #crap coding
        return imageUrl

    def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        user_id = self.get_body_argument("user_id", default=None, strip=False)
        title = self.get_body_argument("title", default=None, strip=False)
        author = self.get_body_argument("author", default=None, strip=False)
        category = self.get_body_argument("category", default=None, strip=False)

        imageUrl = self._saveImage(self.request) # should return an error is image is not provided, can chck this in js?
        docType = user_id + gElasticIndex
        current_milli_time = lambda: int(round(time.time() * 1000))
        curTime = current_milli_time()
        hCurTime = datetime.datetime.fromtimestamp(curTime / 1000.0).strftime("%A, %d. %B %Y %I:%M %p")

        _body = {'title': title,
                 'author': author,
                 'category': category,
                 'image_filepath': imageUrl,
                 'timestamp':curTime,
                 "h_timestamp": hCurTime,
                 "favourite" : False,
                 "current" : False,
                 }
        elasticResp = gClient.index(index=gElasticIndex, doc_type=docType, body=_body, id=None)
        print(elasticResp)

        self.finish({"status": "OK", "resp" : elasticResp})
