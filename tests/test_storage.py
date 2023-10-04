import os
import tempfile
import unittest
from transferchain.storage import Storage


class TestStorageMethods(unittest.TestCase):

    def test_storage(self):
        with tempfile.TemporaryDirectory() as tempdir:
            db_path = os.path.join(tempdir, 'test.db')
            storage = Storage(db_path)
            storage.set('test', 'test-value')

            val = storage.get('test')
            self.assertEqual('test-value', val, 'invalid value')
