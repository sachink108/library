import os
import sys
import uuid
import json
import tornado.ioloop
import time
import tornado.web
import base64
import datetime
from URIParser import *
from googleapiclient import discovery
import httplib2
from oauth2client import client

class AuthCodeHandler(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        auth_code = json.loads(self.request.body)['auth_code']
        print (auth_code)
        #self.finish({"status": "OK"})

        #print (self.request.headers)

        # If this request does not have `X-Requested-With` header, this could be a CSRF
        #if not self.request.headers.get('X-Requested-With'):
        #    print("Header error!")
        #    exit(1)
            #abort(403)

        # Set path to the Web application client_secret_*.json file you downloaded from the
        # Google API Console: https://console.developers.google.com/apis/credentials
        #CLIENT_SECRET_FILE = '/path/to/client_secret.json'
        CLIENT_SECRET_FILE = "C:\\Users\\sachinsk\\Documents\\personal\\progs\\library\\client_id.json"

        # Exchange auth code for access token, refresh token, and ID token
        credentials = client.credentials_from_clientsecrets_and_code(
            CLIENT_SECRET_FILE,
            ['https://www.googleapis.com/auth/drive.appdata', 'profile', 'email'],
            auth_code)

        # Call Google API
        http_auth = credentials.authorize(httplib2.Http())
        drive_service = discovery.build('drive', 'v3', http=http_auth)
        appfolder = drive_service.files().get(fileId='appfolder').execute()

        # Get profile info from ID token
        userid = credentials.id_token['sub']
        email = credentials.id_token['email']

        print (userid)
        print (email)
        self.finish({"status": "OK"})
