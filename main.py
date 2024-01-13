from gmail_api import gmail_authenticate, list_messages_and_store

def main():
    service = gmail_authenticate()
    list_messages_and_store(service, 'me')

if __name__ == '__main__':
    main()
