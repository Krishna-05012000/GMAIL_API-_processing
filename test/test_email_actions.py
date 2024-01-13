
import unittest
from unittest.mock import patch
from email_actions import get_label_id_by_name
class TestEmailActions(unittest.TestCase):

    @patch('googleapiclient.discovery.build')
    def test_get_label_id_by_name(self, mock_build):
        mock_service = mock_build.return_value
        mock_labels = mock_service.users().labels().list().execute.return_value = {
            'labels': [{'id': '123', 'name': 'To-Review'}]
        }

        label_id = get_label_id_by_name(mock_service, 'To-Review')
        self.assertEqual(label_id, '123')

if __name__ == '__main__':
    unittest.main()

