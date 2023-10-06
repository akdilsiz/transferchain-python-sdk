import os
import tempfile
import unittest
from transferchain.db import DB


class TestDBMethods(unittest.TestCase):

    def test_db(self):
        with tempfile.TemporaryDirectory() as tempdir:
            db_path = os.path.join(tempdir, 'test.db')
            db = DB(db_path)
            db.set('test', 'test-value')

            val = db.get('test')
            self.assertEqual(b'test-value', val, 'invalid value')

            items = db.get_all()
            self.assertEqual(items['test'], b'test-value', 'invalid value')
