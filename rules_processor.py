import json
import sqlite3
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from email_actions import *
from email.utils import parsedate_to_datetime
import pytz
import re
from tqdm import tqdm



def apply_rule_condition(email, condition):

    field, predicate, value = condition['field'], condition['predicate'], condition['value']
    
    if field == "subject":
        if predicate == "contains" and value in email['subject']:
            return True
        elif predicate == "equals" and value == email['subject']:
            return True
        

    elif field == "from":
        matches = re.findall(r'<(.*?)>', email['from'])
        if matches:
            if predicate == "equals" and value == matches[0]:
                return True
        else:
            if predicate == "equals" and value == email['from']:
                return True
    elif field == "to":
        if predicate == "contains" and value in email['to']:
            return True
    elif field == "date_received":
        try:
            email_date = parsedate_to_datetime(email['date_received'])
            condition_date = datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=pytz.UTC)

            if predicate == "before" and email_date < condition_date:
                return True
            elif predicate == "after" and email_date > condition_date:
                return True
        except ValueError as e:
            print(f"Error parsing date: {e}")

    # Add conditions for other fields like 'to', 'date_received', etc.
    return False

def apply_rule(email, rule):

    if rule['overall_predicate'] == 'all':
        return all(apply_rule_condition(email, condition) for condition in rule['conditions'])
    else:
        return any(apply_rule_condition(email, condition) for condition in rule['conditions'])

def gmail_service():
    creds = Credentials.from_authorized_user_file('token.json')
    return build('gmail', 'v1', credentials=creds)


def execute_action(email_id, action):
    service = gmail_service()
    # Using the Gmail API
    if action['action'] == 'mark_as_read':
        service.users().messages().modify(
            userId='me', 
            id=email_id, 
            body={'removeLabelIds': ['UNREAD']}
        ).execute()
    elif action['action'] == 'mark_as_unread':
        service.users().messages().modify(
            userId='me', 
            id=email_id, 
            body={'addLabelIds': ['UNREAD']}
        ).execute()

    elif action['action'] == 'archive':
        service.users().messages().modify(
            userId='me', 
            id=email_id, 
            body={'removeLabelIds': ['INBOX']}
        ).execute()
    elif action['action'] == 'add_star':
        service.users().messages().modify(
            userId='me', 
            id=email_id, 
            body={'addLabelIds': ['STARRED']}
        ).execute()
    elif action['action'] == 'move_to_folder':
        folder_name = action.get('folder_name')
        label_id = get_label_id_by_name(service, folder_name)
        service.users().messages().modify(
            userId='me', 
            id=email_id, 
            body={'addLabelIds': [label_id]}
        ).execute()
    elif action['action'] == 'forward_to':
        forward_email(service, email_id, action['email_address'])
    
    print(f"\n\n ----------->  Action '{action['action']}' executed for email ID: {email_id} <-----------")

def display_rules(rules):
    for i, rule in enumerate(rules, 1):
        conditions = ' AND '.join([f"{cond['field']} {cond['predicate']} '{cond['value']}'" for cond in rule['conditions']])
        actions = ', '.join([action['action'] for action in rule['actions']])
        print(f"{i}. If {rule['overall_predicate']} of the following conditions are met: ---> for example : {conditions}, then **** {actions} ****.")

def get_user_input_for_rule(rule):
    user_conditions = []
    for condition in rule['conditions']:
        value = input(f"Enter the value for {condition['field']} {condition['predicate']}: ")
        user_conditions.append({**condition, 'value': value})

    user_actions = rule['actions'] 

    return {'conditions': user_conditions, 'overall_predicate': rule['overall_predicate'], 'actions': user_actions}

def apply_rules(user_rule):
    conn = sqlite3.connect('emails.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM emails")
    emails = cursor.fetchall()

    for email in tqdm(emails, desc="Processing emails"):
        email_dict = {'subject': email[4], 'from': email[2],'to': email[3], 'date_received': email[5]}
        if apply_rule(email_dict, user_rule):
            for action in user_rule['actions']:
                execute_action(email[1], action)

# Load rules from JSON
# with open('rules.json') as f:
#     rules = json.load(f)

# # Display rules for the user to choose
# display_rules(rules)

# # Ask the user to select a rule
# rule_number = int(input("Enter the number of the rule you want to customize and apply: ")) - 1
# selected_rule = rules[rule_number]

# # Get user input for the values of the conditions for the selected rule
# user_rule = get_user_input_for_rule(selected_rule)

# # Apply the rule with user input
# apply_rules(user_rule)

if __name__ == '__main__':
    # Load rules from JSON
    with open('rules.json') as f:
        rules = json.load(f)

    # Display rules for the user to choose
    display_rules(rules)

    # Ask the user to select a rule
    rule_number = int(input("Enter the number of the rule you want to customize and apply: ")) - 1
    selected_rule = rules[rule_number]

    # Get user input for the values of the conditions for the selected rule
    user_rule = get_user_input_for_rule(selected_rule)

    # Apply the rule with user input
    apply_rules(user_rule)