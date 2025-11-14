import os
import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these SCOPES, delete the file token.json
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print('Message Id: %s' % message['id'])
        return message
    except Exception as error:
        print(f'An error occurred: {error}')
        return None

def create_message(to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}

def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('google_auth.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)
        message = create_message(
            to='recipient@example.com',
            subject='Test Subject',
            message_text='Hello from Python!'
        )
        send_message(service, 'me', message)
    except Exception as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()
