import os
import tempfile
from pathlib import Path
import unittest
import shutil
from transferchain.client import TransferChain
from transferchain.storage import Storage
from transferchain.config import create_config
from transferchain.protobuf import service_pb2 as pb


class TestStorageMethods(unittest.TestCase):

    def create_dummy_file(self):
        dir_path = tempfile.mkdtemp()
        file_path = os.path.join(dir_path, 'storage_test_data.dat')
        with open(file_path, 'wb') as f:
            f.write(os.urandom(1024).hex().encode('utf-8'))
        return dir_path, file_path

    def create_test_user(self, config):
        tc = TransferChain(config)
        tc.add_master_user()
        user_info_result = tc.add_user()
        self.assertEqual(True, user_info_result.success)
        return user_info_result.data

    def test_storage_file_is_valid(self):
        config = create_config()
        user = self.create_test_user(config)
        storage = Storage(config)
        dir_path, file_path = self.create_dummy_file()

        def callback(result):
            self.assertEqual(True, result.success)

        result = storage.upload(
            user=user, files=[file_path], callback=callback)
        self.assertEqual(True, result.success)
        shutil.rmtree(dir_path)

    def test_storage_cancel_is_valid(self):
        config = create_config()
        user = self.create_test_user(config)
        storage = Storage(config)
        dir_path, file_path = self.create_dummy_file()

        def callback(result):
            self.assertEqual(True, result.success)

        result = storage.upload(
            user=user, files=[file_path], callback=callback)
        self.assertEqual(True, result.success)

        slots = result.data[0].data.slots
        cancel_result = storage.cancel_upload(slots, pb.UploadOpCode.Storage)
        self.assertEqual(True, cancel_result.success,
                         cancel_result.error_message)
        shutil.rmtree(dir_path)

    def test_storage_delete_is_valid(self):
        config = create_config()
        user = self.create_test_user(config)
        storage = Storage(config)
        dir_path, file_path = self.create_dummy_file()

        def callback(result):
            self.assertEqual(True, result.success)

        result = storage.upload(
            user=user, files=[file_path], callback=callback)
        self.assertEqual(True, result.success)

        storage_result = result.data[0].data
        cancel_result = storage.delete(user, storage_result)
        self.assertEqual(True, cancel_result.success,
                         cancel_result.error_message)
        shutil.rmtree(dir_path)

    def test_storage_download_is_valid(self):
        config = create_config()
        user = self.create_test_user(config)
        storage = Storage(config)
        dir_path, file_path = self.create_dummy_file()

        def callback(result):
            self.assertEqual(True, result.success)

        result = storage.upload(
            user=user, files=[file_path], callback=callback)
        self.assertEqual(True, result.success)

        storage_reuslt_obj = result.data[0].data
        download_result = storage.download(
            file_uid=storage_reuslt_obj.uuid,
            slots=storage_reuslt_obj.slots,
            file_size=storage_reuslt_obj.size,
            file_name=storage_reuslt_obj.filename,
            key_aes=storage_reuslt_obj.keyAES,
            key_hmac=storage_reuslt_obj.keyHMAC,
            destination=tempfile.tempdir
        )
        self.assertEqual(True, download_result.success)
        path = Path(tempfile.tempdir).joinpath(storage_reuslt_obj.filename)
        self.assertEqual(True, path.exists())
        shutil.rmtree(dir_path)
