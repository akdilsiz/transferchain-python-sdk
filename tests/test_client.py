import os
import time
import shutil
import tempfile
import unittest
from pathlib import Path
from transferchain.client import TransferChain


class TestClientMethods(unittest.TestCase):

    def create_dummy_file(self):
        dir_path = tempfile.mkdtemp()
        file_path = os.path.join(dir_path, 'transferchain_test_data.dat')
        with open(file_path, 'wb') as f:
            f.write(os.urandom(1024).hex().encode('utf-8'))
        return dir_path, file_path

    def setUp(self):
        db_path = os.path.join(os.getcwd(), 'tc.db')
        if os.path.exists(db_path):
            os.remove(db_path)
        self.tc = TransferChain()
        # save_user in add_user, pass!
        self.tc.add_master_user()
        user_result = self.tc.add_user()

        self.assertEqual(True, user_result.success)
        self.assertEqual(2, len(self.tc.users))  # master and sub user
        self.user = user_result.data

        self.tc.users = {}
        self.tc.load_users()
        self.assertEqual(2, len(self.tc.users))  # master and sub user

    def test_transfer(self):
        dir_path, file_path = self.create_dummy_file()
        # transfer
        transfer_result = self.tc.transfer_files(
            files=[file_path],
            sender_user_id=self.user.id,
            recipient_addresses=[
                self.user.random_address().Key['Address']
            ],
            note='test note')
        self.assertEqual(True, transfer_result.success)
        shutil.rmtree(dir_path)

    def test_delete_recevied(self):
        dir_path, file_path = self.create_dummy_file()
        # transfer
        transfer_result = self.tc.transfer_files(
            files=[file_path],
            sender_user_id=self.user.id,
            recipient_addresses=[
                self.user.random_address().Key['Address']
            ],
            note='test note')
        self.assertEqual(True, transfer_result.success)
        # transfer received delete
        recevied_delete_result = self.tc.transfer_received_delete(
            self.user.id, uuid=transfer_result.data[0].data.uuid, tx_id="")
        self.assertEqual(True, recevied_delete_result.success,
                         recevied_delete_result.error_message)
        shutil.rmtree(dir_path)

    def test_transfer_download(self):
        dir_path, file_path = self.create_dummy_file()
        transfer_result = self.tc.transfer_files(
            files=[file_path],
            sender_user_id=self.user.id,
            recipient_addresses=[
                self.user.random_address().Key['Address']
            ],
            note='test note')
        self.assertEqual(True, transfer_result.success)

        # transfer download test
        transfer_sent_obj = transfer_result.data[0].data
        download_result = self.tc.transfer_download(
            file_uid=transfer_sent_obj.uuid,
            slots=transfer_sent_obj.slots,
            file_size=transfer_sent_obj.size,
            file_name=transfer_sent_obj.filename,
            key_aes=transfer_sent_obj.keyAES,
            key_hmac=transfer_sent_obj.KeyHMAC,
            destination=tempfile.tempdir
        )
        self.assertEqual(True, download_result.success)
        path = Path(tempfile.tempdir).joinpath(transfer_sent_obj.filename)
        self.assertEqual(True, path.exists())
        shutil.rmtree(dir_path)

    def test_sent_delete(self):
        dir_path, file_path = self.create_dummy_file()
        transfer_result = self.tc.transfer_files(
            files=[file_path],
            sender_user_id=self.user.id,
            recipient_addresses=[
                self.user.random_address().Key['Address']
            ],
            note='test note')
        self.assertEqual(True, transfer_result.success)
        # transfer sent delete
        sent_delete_result = self.tc.transfer_sent_delete(
            self.user.id, transfer_sent_obj=transfer_result.data[0].data)
        self.assertEqual(True, sent_delete_result.success,
                         sent_delete_result.error_message)
        shutil.rmtree(dir_path)

    def test_cancel_upload(self):
        dir_path, file_path = self.create_dummy_file()
        transfer_result = self.tc.transfer_files(
            files=[file_path],
            sender_user_id=self.user.id,
            recipient_addresses=[
                self.user.random_address().Key['Address']
            ],
            note='test note')
        self.assertEqual(True, transfer_result.success)
        transfer_slots = transfer_result.data[0].data.slots
        cancel_result = self.tc.transfer_cancel(transfer_slots)
        self.assertEqual(True, cancel_result.success,
                         cancel_result.error_message)
        shutil.rmtree(dir_path)


class TestClientWithRestoreMethods(unittest.TestCase):

    def create_dummy_file(self):
        dir_path = tempfile.mkdtemp()
        file_path = os.path.join(dir_path, 'transferchain_test_data.dat')
        with open(file_path, 'wb') as f:
            f.write(os.urandom(1024).hex().encode('utf-8'))
        return dir_path, file_path

    def setUp(self):
        db_path = os.path.join(os.getcwd(), 'tc.db')
        if os.path.exists(db_path):
            os.remove(db_path)

        self.tc = TransferChain()
        self.tc.add_master_user()
        self.tc.users = {}
        self.master_user = None

    def test_restore_master_user(self):
        self.assertEqual(self.tc.users, {}, 'User should be empty')
        time.sleep(2)
        result = self.tc.restore_master_user()
        self.assertEqual(True, result.success, result.error_message)
        self.assertNotEqual(self.tc.users, {}, 'restore error')

    def test_restore_sub_users(self):
        time.sleep(5)

        result = self.tc.restore_master_user()
        self.assertEqual(True, result.success, result.error_message)
        self.assertNotEqual(self.tc.users, {}, 'restore error')
        time.sleep(5)

        user_result = self.tc.add_user()
        self.assertEqual(True, user_result.success)
        self.assertEqual(2, len(self.tc.users))
        time.sleep(5)
        # pop user
        user = self.tc.users.pop(user_result.data.id)
        self.assertEqual(1, len(self.tc.users))

        result = self.tc.restore_sub_users()
        self.assertEqual(True, result.success)
        self.assertEqual(2, len(self.tc.users))
        self.assertEqual(True, user.id in self.tc.users.keys())
