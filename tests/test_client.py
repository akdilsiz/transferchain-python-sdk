import os
import tempfile
import shutil
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
        os.remove(os.path.join(os.getcwd(), 'tc.db'))
        self.tc = TransferChain()
        # save_user in add_user, pass!
        user_result = self.tc.add_user()

        self.assertEqual(True, user_result.success)
        self.assertEqual(1, len(self.tc.users))
        self.user = user_result.data

        self.tc.users = {}
        self.tc.load_users()
        self.assertEqual(1, len(self.tc.users))

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

    def test_download(self):
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


if __name__ == '__main__':
    unittest.main()
