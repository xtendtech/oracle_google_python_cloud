from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
from google.auth.transport.requests import Request
# If modifying these SCOPES, delete the file token.json
SCOPES =  ["https://www.googleapis.com/auth/youtube.force-ssl"]

def get_videos():
  ...



def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('google_auth.json', SCOPES)
            creds = flow.run_local_server(port=8080,prompt='consent',authorization_prompt_message='Please visit this URL: {url}',open_browser=True)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return( build("youtube", version="v3", credentials=creds))
  
 
if __name__ == '__main__':
 youtube =    main()
youtube.videos().list(
        part="snippet,contentDetails,statistics",
        filter= "q='python'"
    ).execute()