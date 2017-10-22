from googleapiclient import discovery
import httplib2
from oauth2client import client

auth_code = '4/3zW0kXycCqAS1-gh6WFarTd29fXROYnx2R0YgKAKdug'

#auth_code = "crap"
#CLIENT_SECRET_FILE = "C:\\Users\\sachinsk\\Documents\\personal\\progs\\library\\client_id.json"

CLIENT_SECRET_FILE = "C:\\Users\\sachinsk\\Documents\\personal\\progs\\library\\client_secret_416430916426-oghsnp3l7kn652a46kiavtqsf15g6bpj.apps.googleusercontent.com.json"

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