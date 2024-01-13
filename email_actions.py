import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64

def get_label_id_by_name(service, label_name):
    """Get the Gmail label ID based on the label name."""
    labels_response = service.users().labels().list(userId='me').execute()
    label_id = next((label['id'] for label in labels_response['labels'] if label['name'].lower() == label_name.lower()), None)
    if label_id is None:
        raise ValueError(f"Label '{label_name}' not found.")
    return label_id




def create_message(sender, to, subject, message_text):
    """Create a message for an email."""
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw_message}

def get_mime_message(service, user_id, msg_id):
    """Fetch the MIME Message using the Gmail API."""
    message = service.users().messages().get(userId=user_id, id=msg_id, format='raw').execute()
    msg_raw = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
    mime_msg = email.message_from_bytes(msg_raw)
    return mime_msg

def create_forward_message(original_email, to_email):
    """Create a new MIME message for forwarding."""
    message = MIMEMultipart()
    message['to'] = to_email
    message['subject'] = f"Fwd: {original_email['subject']}"

    # Handling multipart messages
    if original_email.is_multipart():
        for part in original_email.walk():
            # Extract text/plain parts and attach
            if part.get_content_type() == 'text/plain':
                text = part.get_payload(decode=True).decode(part.get_content_charset())
                msg = MIMEText(text)
                message.attach(msg)
                break
    else:
        text = original_email.get_payload(decode=True).decode(original_email.get_content_charset())
        msg = MIMEText(text)
        message.attach(msg)
    
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


def forward_email(service, email_id, to_email):
    original_email = get_mime_message(service, 'me', email_id)
    forward_message = create_forward_message(original_email, to_email)
    send_message(service, 'me', forward_message)

def send_message(service, user_id, message):
    """Send an email message."""
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    except Exception as error:
        print(f'An error occurred: {error}')
