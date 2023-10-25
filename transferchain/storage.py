import os
import uuid
import queue
import tempfile
import threading
import shutil
from pathlib import Path
import grpc
from transferchain import constants
from transferchain import blockchain
from transferchain.utils import datetime_to_str
from transferchain.crypt import crypt
from transferchain.grpc_client import get_client
from transferchain.protobuf import service_pb2 as pb
from transferchain.transaction import create_transaction
from transferchain.datastructures import (
    Result)


class Storage(object):

    def __init__(self, config):
        self.config = config

    def upload_single_file(self, session_id, base_uuid_maps, process_uuid,
                           user_address, file_object, result_queue, callback):
        aes_key = crypt.generate_encrypt_key(32).encode('utf-8')
        hmac_key = crypt.generate_encrypt_key(32).encode('utf-8')

        tmp_folder = tempfile.mkdtemp()
        out_file_uuid = str(uuid.uuid4())
        out_file = Path(os.path.join(tmp_folder, out_file_uuid))
        with out_file.open(mode='wb') as outfile:
            with in_file.open(mode='rb') as infile:
                crypt.encrypt_aesctr_with_hmac(
                    infile, outfile, aes_key, hmac_key)

        import ipdb;ipdb.set_trace()

        shutil.rmtree(tmp_folder)
        return Result(success=True, data="")

    def upload(self, user_address, files, callback=None):
        assert len(files) <= constants.STORAGE_MAX_FILE_COUNT, \
            'file count exceeded'

        if callback is not None:
            assert callable(callback), 'callback is not a function'

        file_objects = []
        total_file_size = 0
        for file_path in files:
            file_object = Path(file_path)
            if not file_object.exists():
                return Result(success=False, error_message='file does not exist')
            file_objects.append(file_object)
            total_file_size += file_object.stat().st_size

        result_queue = queue.Queue()
        process_uuid = str(uuid.uuid4())
        threads = []

        meta_data = [
            ("user-id", str(self.config.user_id)),
            ("user-api-token", self.config.api_token),
            ("user-api-secret", self.config.api_secret)
        ]
        grpc_client = get_client()
        try:
            init_result = grpc_client.StorageInitV2(
                pb.StorageInitRequest(
                    TotalSize=total_file_size,
                    Paths=files,
                    OpCode=pb.UploadOpCode.Storage,
                    UserID=self.config.user_id,
                    WalletID=self.config.wallet_id,
                    notes="",
                    UID="",
                ), metadata=meta_data)
        except grpc.RpcError as e:
            error_message = "storage init request error: {}".format(
                e.details())
            return Result(success=False, error_message=error_message)

        for file_object in file_objects:
            t = threading.Thread(
                target=self.upload_single_file, args=(
                    init_result.SessionID,
                    init_result.BaseUUIDs,
                    process_uuid,
                    user_address,
                    file_object,
                    result_queue,
                    callback))
            threads.append(t)

        for t in threads:
            t.start()

        for t in threads:
            t.join()
