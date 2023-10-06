import uuid
import unittest
import datetime
from transferchain import utils


class TestUtilsMethods(unittest.TestCase):

    def test_datetime_formating_valid(self):
        result = utils.datetime_formating('2023-09-21T09:07:57.620532Z')
        is_datetime = isinstance(result, datetime.datetime)
        self.assertEqual(True, is_datetime)

    def test_datetime_formating_invalid(self):
        with self.assertRaises(Exception):
            utils.datetime_formating('2023-09-21 09:07')

    def test_is_valid_uuid_valid(self):
        result = utils.is_valid_uuid(str(uuid.uuid4()))
        self.assertEqual(True, result)

    def test_is_valid_uuid_invalid(self):
        result = utils.is_valid_uuid('test')
        self.assertNotEqual(True, result)
