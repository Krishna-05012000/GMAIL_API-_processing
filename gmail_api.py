from googleapiclient.discovery import build
import os.path
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import tqdm
from database import insert_email
from base64 import urlsafe_b64decode
from datetime import datetime
from email.utils import parsedate_to_datetime
import pytz
from tqdm import tqdm  

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']



def gmail_authenticate():
    creds = None
    # The file token.json stores the user's access and refresh tokens and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save credentials 
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def get_message_body(payload):
    """Extracts the body of the email from the payload"""
    body = None 

    if 'data' in payload['body']:
        body = urlsafe_b64decode(payload['body']['data']).decode('utf-8')
    elif 'parts' in payload:
        for part in payload.get('parts', []):
            if part['mimeType'] in ['text/plain', 'text/html'] and 'data' in part['body']:
                body = urlsafe_b64decode(part['body']['data']).decode('utf-8')
                break  
    if body is None:
        body = "Could not retrieve the message body."

    return body



def list_messages_and_store(service, user_id):
    # Ask the user for the start date
    start_date_str = input("Enter the start date for fetching emails (YYYY-MM-DD): ")
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").replace(tzinfo=pytz.UTC)

    messages = service.users().messages().list(userId=user_id).execute().get('messages', [])

    for message in tqdm(messages, desc="Processing and storing emails"):
        msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
        headers = msg['payload']['headers']
        subject = next((value for value in headers if value['name'] == 'Subject'), {'value': 'No Subject'})['value']
        from_address = next((value for value in headers if value['name'] == 'From'), {'value': 'Unknown'})['value']
        to_address = next((value for value in headers if value['name'] == 'To'), {'value': 'Unknown'})['value']
        date_received_str = next((value for value in headers if value['name'] == 'Date'), {'value': 'Unknown Date'})['value']
        
        # Parse the email date
        date_received = parsedate_to_datetime(date_received_str)
        if date_received.replace(tzinfo=pytz.UTC) >= start_date:
            body = get_message_body(msg['payload'])
            # Insert email into the database using the database module function
            insert_email(message['id'], from_address, to_address, subject, date_received_str, body)


