#import sys
#sys.path.append('/home/wade/projects/transferchain-python-sdk')

import os
import tempfile
import unittest
import shutil
from datetime import datetime
from transferchain import utils
from transferchain import constants
from transferchain.client import TransferChain
from transferchain.transfer import Transfer
from transferchain.config import create_config
from transferchain.protobuf import service_pb2 as pb
from transferchain.datastructures import (
    TransferReceiveDelete)


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
        user = self.create_test_user(config)
        sender = user.data.addresses[1]
        transfer = Transfer(config)
        dir_path, file_path = self.create_dummy_file()

        def callback(result):
            self.assertEqual(True, result.success)

        result = transfer.upload(
            files=[file_path],
            sender=sender,
            recipient_addresses=[sender.Key['Address']],
            note="test transfer",
            callback=callback)
        self.assertEqual(True, result.success)
        shutil.rmtree(dir_path)

    def test_delete_received_transfer_is_valid(self):
        config = create_config()
        user = self.create_test_user(config)
        sender = user.data.addresses[1]
        transfer = Transfer(config)
        dir_path, file_path = self.create_dummy_file()

        transfer_result = transfer.upload(
            files=[file_path],
            sender=sender,
            recipient_addresses=[sender.Key['Address']],
            note="test transfer")
        self.assertEqual(True, transfer_result.success)

        tx_data = TransferReceiveDelete(
            UUID=transfer_result.data[0].data.uuid,
            TxID="",
            Typ=constants.TRANSFER_TYPE_SENT,
            Timestamp=utils.datetime_to_str(datetime.now())
        )
        delete_result = transfer.delete_received_transfer(
            user_first_address=user.data.addresses[1],
            user_second_address=user.data.addresses[2],
            tx_data=tx_data
        )
        self.assertEqual(True, delete_result.success)
        shutil.rmtree(dir_path)

    def test_delete_sent_transfer_is_valid(self):
        config = create_config()
        user = self.create_test_user(config)
        sender = user.data.addresses[1]
        transfer = Transfer(config)
        dir_path, file_path = self.create_dummy_file()

        transfer_result = transfer.upload(
            files=[file_path],
            sender=sender,
            recipient_addresses=[sender.Key['Address']],
            note="test transfer")
        self.assertEqual(True, transfer_result.success)

        transfer_sent_obj = transfer_result.data[0].data

        delete_result = transfer.delete_sent_transfer(
            user_first_address=user.data.addresses[1],
            user_second_address=user.data.addresses[2],
            transfer_sent_obj=transfer_sent_obj
        )
        self.assertEqual(True, delete_result.success)
        shutil.rmtree(dir_path)

    def test_transfer_file_is_invalid(self):
        config = create_config()
        user = self.create_test_user(config)
        sender = user.data.addresses[1]
        transfer = Transfer(config)
        dir_path, file_path = self.create_dummy_file()

        with self.assertRaises(Exception):
            # wrong files value
            transfer.upload(
                files=file_path,
                sender=sender,
                recipient_addresses=[
                    sender.Key['Address']
                ],
                note="test transfer")

        with self.assertRaises(Exception):
            # wrong files value
            transfer.upload(
                files=[],
                sender=sender,
                recipient_addresses=[
                    sender.Key['Address']
                ],
                note="test transfer")

        with self.assertRaises(Exception):
            # wrong recipient
            transfer.upload(
                files=[file_path],
                sender=sender,
                recipient_addresses=sender.Key['Address'],
                note="test transfer")

        shutil.rmtree(dir_path)

    def test_cancel_upload_is_valid(self):
        config = create_config()
        user = self.create_test_user(config)
        sender = user.data.addresses[1]
        transfer = Transfer(config)
        dir_path, file_path = self.create_dummy_file()

        result = transfer.upload(
            files=[file_path],
            sender=sender,
            recipient_addresses=[sender.Key['Address']],
            note="test transfer")
        self.assertEqual(True, result.success)
        slots = result.data[0].data.slots
        cancel_result = transfer.cancel_upload(slots, pb.UploadOpCode.Transfer)
        self.assertEqual(True, cancel_result.success,
                         cancel_result.error_message)
        shutil.rmtree(dir_path)

    def test_cancel_upload_is_invalid(self):
        config = create_config()
        user = self.create_test_user(config)
        sender = user.data.addresses[1]
        transfer = Transfer(config)
        dir_path, file_path = self.create_dummy_file()

        result = transfer.upload(
            files=[file_path],
            sender=sender,
            recipient_addresses=[sender.Key['Address']],
            note="test transfer")
        self.assertEqual(True, result.success)
        slots = [{}]
        cancel_result = transfer.cancel_upload(slots, pb.UploadOpCode.Transfer)
        self.assertEqual(False, cancel_result.success,
                         cancel_result.error_message)
        shutil.rmtree(dir_path)


if __name__ == '__main__':
    unittest.main()
