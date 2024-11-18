import os
import time
import logging
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GmailMonitor:
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    def __init__(self, credentials_file, token_file, check_interval=30):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.check_interval = check_interval
        self.service = None
        self.seen_message_ids = set()

    def authenticate(self):
        creds = None
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())
        
        self.service = build('gmail', 'v1', credentials=creds)
        logging.info("Authentication was successful")

    def list_new_messages(self):
        try:
            results = self.service.users().messages().list(userId='me', maxResults=10).execute()
            messages = results.get('messages', [])
            if not messages:
                logging.info("No new mails")
                return []

            new_messages = []
            for message in messages:
                msg_id = message['id']
                if msg_id not in self.seen_message_ids:
                    msg = self.service.users().messages().get(userId='me', id=msg_id).execute()
                    payload = msg.get('payload', {})
                    headers = payload.get('headers', [])
                    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "Без темы")
                    new_messages.append({"id": msg_id, "subject": subject})
                    self.seen_message_ids.add(msg_id)
            
            return new_messages
        except HttpError as error:
            logging.error(f"An error occurred while receiving messages: {error}")
            return []

    def monitor_inbox(self, callback=None):
        try:
            logging.info("Launching monitoring of new emails")
            while True:
                new_messages = self.list_new_messages()
                if new_messages and callback:
                    for message in new_messages:
                        callback(message)
                time.sleep(self.check_interval)
        except Exception as e:
            logging.error(f"Error: {e}")
