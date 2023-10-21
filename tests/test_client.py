import os
import tempfile
import shutil
import unittest
from pathlib import Path
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
        user_id = user_result.data.id

        tc.users = {}
        tc.load_users()
        self.assertEqual(1, len(tc.users))

        dir_path, file_path = self.create_dummy_file()

        # transfer
        transfer_result = tc.transfer_files(
            files=[file_path],
            sender_user_id=user_id,
            recipient_addresses=[
                user_result.data.addresses[1].Key['Address']
            ],
            note='test note')
        self.assertEqual(True, transfer_result.success)

        # transfer received delete
        recevied_delete_result = tc.transfer_received_delete(
            user_id, uuid=transfer_result.data[0].data.uuid, tx_id="")
        self.assertEqual(True, recevied_delete_result.success,
                         recevied_delete_result.error_message)

        # upload again!
        transfer_result = tc.transfer_files(
            files=[file_path],
            sender_user_id=user_id,
            recipient_addresses=[
                user_result.data.addresses[1].Key['Address']
            ],
            note='test note')
        self.assertEqual(True, transfer_result.success)

        # transfer download test
        transfer_sent_obj = transfer_result.data[0].data
        download_result = tc.transfer_download(
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

        # transfer sent delete
        sent_delete_result = tc.transfer_sent_delete(
            user_id, transfer_sent_obj=transfer_result.data[0].data)
        self.assertEqual(True, sent_delete_result.success,
                         sent_delete_result.error_message)

        shutil.rmtree(dir_path)
