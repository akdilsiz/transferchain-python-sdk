import os
import tempfile
import unittest
import shutil
from transferchain.client import TransferChain
from transferchain.transfer import Transfer
from transferchain.config import create_config
from transferchain.protobuf import service_pb2 as pb


class TestTransferMethods(unittest.TestCase):

    def create_dummy_file(self):
        dir_path = tempfile.mkdtemp()
        file_path = os.path.join(dir_path, 'transfer_test_data.dat')
        with open(file_path, 'wb') as f:
            f.write(os.urandom(1024).hex().encode('utf-8'))
        return dir_path, file_path

    def create_test_user(self, config):
        tc = TransferChain(config)
        user_info_result = tc.add_user()
        self.assertEqual(True, user_info_result.success)
        return user_info_result

    def test_transfer_file_is_valid(self):
        config = create_config()
        user_info_result = self.create_test_user(config)
        user_master_address = user_info_result.data['master_address']
        transfer = Transfer(config)
        dir_path, file_path = self.create_dummy_file()

        def callback(result):
            self.assertEqual(True, result.success)

        result = transfer.transfer_file(
            files=[file_path],
            sender_address=user_master_address,
            recipient_addresses=[user_master_address],
            note="test transfer",
            callback=callback)
        self.assertEqual(True, result.success)
        shutil.rmtree(dir_path)

    def test_transfer_file_is_invalid(self):
        config = create_config()
        user_info_result = self.create_test_user(config)
        user_master_address = user_info_result.data['master_address']
        transfer = Transfer(config)
        dir_path, file_path = self.create_dummy_file()

        with self.assertRaises(Exception):
            # wrong files value
            transfer.transfer_file(
                files=file_path,
                sender_address=user_master_address,
                recipient_addresses=[user_master_address],
                note="test transfer")

        with self.assertRaises(Exception):
            # wrong files value
            transfer.transfer_file(
                files=[],
                sender_address=user_master_address,
                recipient_addresses=[user_master_address],
                note="test transfer")

        with self.assertRaises(Exception):
            # wrong recipient
            transfer.transfer_file(
                files=[file_path],
                sender_address=user_master_address,
                recipient_addresses=user_master_address,
                note="test transfer")

        shutil.rmtree(dir_path)

    def test_cancel_upload_is_valid(self):
        config = create_config()
        user_info_result = self.create_test_user(config)
        user_master_address = user_info_result.data['master_address']
        transfer = Transfer(config)
        dir_path, file_path = self.create_dummy_file()

        result = transfer.transfer_file(
            files=[file_path],
            sender_address=user_master_address,
            recipient_addresses=[user_master_address],
            note="test transfer")
        self.assertEqual(True, result.success)
        slots = result.data[0].data['slots']
        cancel_result = transfer.cancel_upload(slots, pb.UploadOpCode.Transfer)
        self.assertEqual(True, cancel_result.success,
                         cancel_result.error_message)
        shutil.rmtree(dir_path)

    def test_cancel_upload_is_invalid(self):
        config = create_config()
        user_info_result = self.create_test_user(config)
        user_master_address = user_info_result.data['master_address']
        transfer = Transfer(config)
        dir_path, file_path = self.create_dummy_file()

        result = transfer.transfer_file(
            files=[file_path],
            sender_address=user_master_address,
            recipient_addresses=[user_master_address],
            note="test transfer")
        self.assertEqual(True, result.success)
        slots = [pb.UploadSlot()]
        cancel_result = transfer.cancel_upload(slots, pb.UploadOpCode.Transfer)
        self.assertEqual(False, cancel_result.success,
                         cancel_result.error_message)
        shutil.rmtree(dir_path)


if __name__ == '__main__':
    unittest.main()
