

import unittest
from rules_processor import apply_rule_condition
from email.utils import format_datetime
from datetime import datetime, timezone

class TestRulesProcessor(unittest.TestCase):

    def setUp(self):
        self.email = {
            'subject': 'Meeting Reminder',
            'from': 'boss@example.com',
            'to': 'employee@example.com',
            'date_received': format_datetime(datetime(2022, 7, 21, 17, 0, 0, tzinfo=timezone.utc))
        }

    def test_subject_contains(self):
        condition = {'field': 'subject', 'predicate': 'contains', 'value': 'Meeting'}
        self.assertTrue(apply_rule_condition(self.email, condition))

    def test_subject_equals(self):
        condition = {'field': 'subject', 'predicate': 'equals', 'value': 'Meeting Reminder'}
        self.assertTrue(apply_rule_condition(self.email, condition))

    def test_from_equals(self):
        condition = {'field': 'from', 'predicate': 'equals', 'value': 'boss@example.com'}
        self.assertTrue(apply_rule_condition(self.email, condition))

    def test_date_before(self):
        condition = {'field': 'date_received', 'predicate': 'before', 'value': '2022-08-01'}
        self.assertTrue(apply_rule_condition(self.email, condition))

    def test_date_after(self):
        condition = {'field': 'date_received', 'predicate': 'after', 'value': '2022-01-01'}
        self.assertTrue(apply_rule_condition(self.email, condition))


if __name__ == '__main__':
    unittest.main()
