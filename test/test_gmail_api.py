import unittest
from unittest.mock import patch, MagicMock
import gmail_api

class TestGmailApi(unittest.TestCase):

    @patch('gmail_api.Credentials.from_authorized_user_file')
    @patch('gmail_api.InstalledAppFlow.from_client_secrets_file')
    @patch('os.path.exists')
    def test_gmail_authenticate(self, mock_exists, mock_flow, mock_creds):
        mock_exists.return_value = True
        mock_creds.return_value = MagicMock()
        service = gmail_api.gmail_authenticate()
        self.assertIsNotNone(service)

    def test_get_message_body(self):
        payload = {'body': {'data': 'SGVsbG8gd29ybGQ='}} 
        result = gmail_api.get_message_body(payload)
        self.assertEqual(result, 'Hello world')

    @patch('gmail_api.build')
    @patch('gmail_api.insert_email')
    @patch('builtins.input', lambda _: '2022-01-01')
    def test_list_messages_and_store(self, mock_insert_email, mock_build):
        mock_service = mock_build.return_value
        mock_service.users.return_value.messages.return_value.list.return_value.execute.return_value = {'messages': [{'id': '123'}]}
        mock_service.users.return_value.messages.return_value.get.return_value.execute.return_value = {
            'payload': {'headers': [
                {'name': 'Date', 'value': 'Tue, 26 Jul 2022 12:34:56 -0400'},
                # ... other headers ...
            ], 'body': {'data': 'SGVsbG8='}},
            'id': '123'
        }
        gmail_api.list_messages_and_store(mock_service, 'me')
        mock_insert_email.assert_called()


if __name__ == '__main__':
    unittest.main()
