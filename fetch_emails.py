import os.path
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def gmail_authenticate():
    creds = None
    # The file token.json stores the user's access and refresh tokens and created automatically when the authorization flow completes for the first time.
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
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def list_messages(service, user_id):
    # Call the Gmail API to fetch INBOX
    try:
        response = service.users().messages().list(userId=user_id).execute()
        messages = response.get('messages', [])
        return messages
    except Exception as error:
        print(f'An error occurred: {error}')
        return None

# def main():
#     service = gmail_authenticate()
#     messages = list_messages(service, 'me')
#     if not messages:
#         print("No messages found.")
#     else:
#         print("Message IDs:")
#         for message in messages[:10]:  # displaying only first 10 messages
#             print(message['id'])

# if __name__ == '__main__':
#     main()
