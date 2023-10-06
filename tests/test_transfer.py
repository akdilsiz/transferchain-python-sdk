import os
import tempfile
import unittest
from transferchain.transfer import Transfer
from transferchain.config import create_config


class TestTransferMethods(unittest.TestCase):

    def test_db(self):
        config = create_config()
        tc = Transfer(config)
        # tc.transfer_file()
        new_file, filename = tempfile.mkstemp()
        os.write(new_file, b"content")
        os.close(new_file)
