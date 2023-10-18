import os
import tempfile
import shutil
import unittest
from transferchain.client import TransferChain


class TestClientMethods(unittest.TestCase):

    def create_dummy_file(self):
        dir_path = tempfile.mkdtemp()
        file_path = os.path.join(dir_path, 'transfer_test_data.dat')
        with open(file_path, 'wb') as f:
            f.write(os.urandom(1024).hex().encode('utf-8'))
        return dir_path, file_path

    def test_client(self):
        tc = TransferChain()

        # save_user in add_user, pass!
        user_result = tc.add_user()
        self.assertEqual(True, user_result.success)
        self.assertEqual(1, len(tc.users))

        tc.users = {}
        tc.load_users()
        self.assertEqual(1, len(tc.users))

        dir_path, file_path = self.create_dummy_file()
        # transfer
        transfer_result = tc.transfer_files(
            files=[file_path],
            sender_user_id=user_result.data.id,
            recipient_addresses=[
                user_result.data.addresses[1].Key['Address']
            ],
            note='test note')
        self.assertEqual(True, transfer_result.success)

        shutil.rmtree(dir_path)
