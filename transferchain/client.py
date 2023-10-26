import uuid
import json
from transferchain.db import DB
from transferchain.logger import get_logger
from transferchain.config import create_config
from transferchain.crypt import crypt
from transferchain.datastructures import (
    Result, Address, User)
from transferchain.addresses import generate_user_addresses
from transferchain.transfer import Transfer
from transferchain.storage import Storage
from transferchain.protobuf import service_pb2 as pb

logger = get_logger(__file__)


class TransferChain(object):

    def __init__(self, *args, **kwargs):
        self.config = create_config()
        self.db_path = kwargs.get('db_path') or self.config.db_path
        self.db = DB(self.db_path)
        self.transfer_service = Transfer(self.config)
        self.storage_service = Storage(self.config)
        self.users = {}

    def add_user(self):
        sub_user_id = str(uuid.uuid4())
        result = generate_user_addresses(
            self.config.user_id, self.config.mnemonics, sub_user_id)
        if result.success is False:
            return result

        self.save_user(sub_user_id, result.data)
        self.users[sub_user_id] = result.data
        return Result(success=True, data=result.data)

    def get_user(self, user_id):
        return self.users[user_id]

    def load_users(self):
        users = self.db.get_all()
        for user_id, data in users.items():
            user_data = json.loads(crypt.decrypt_byte(
                data, self.config.mnemonics))
            addresses = []
            for address in user_data.pop('addresses'):
                addresses.append(Address(**address))
            user_data['addresses'] = addresses
            self.users[user_id] = User(**user_data)
        return self.users

    def save_user(self, sub_user_id, user):
        user_dict = user._asdict()
        addresses = []
        for address in user_dict.pop('addresses'):
            addresses.append(address._asdict())
        user_dict['addresses'] = addresses
        enc_data = crypt.encrypt_byte(
            json.dumps(user_dict).encode('utf-8'),
            self.config.mnemonics)
        self.db.set(sub_user_id, enc_data)

    def transfer_files(self, files, sender_user_id,
                       recipient_addresses, note, callback=None):
        user = self.get_user(sender_user_id)
        sender_user_address = user.random_address()
        return self.transfer_service.upload(
            files, sender_user_address, recipient_addresses, note, callback)

    def transfer_received_delete(self, user_id, uuid, tx_id=None):
        # tx_id is not necessary
        return self.transfer_service.delete_received_transfer(
            user=self.get_user(user_id), uuid=uuid, tx_id=tx_id)

    def transfer_sent_delete(self, user_id, transfer_sent_obj):
        # transfer_sent_obj->datastructers.TransferSent
        return self.transfer_service.delete_sent_transfer(
            user=self.get_user(user_id), transfer_sent_obj=transfer_sent_obj)

    def transfer_cancel(self, file_slots):
        return self.transfer_service.cancel_upload(
            file_slots, pb.UploadOpCode.Transfer)

    def transfer_download(self, file_uid, slots, file_size, file_name,
                          key_aes, key_hmac, destination):
        return self.transfer_service.download_sent(
            file_uid, slots, file_size, file_name,
            key_aes, key_hmac, destination)

    def storage_upload(self, user_id, files, callback=None):
        return self.storage_service.upload(
            user=self.get_user(user_id), files=files, callback=callback)

    def storage_cancel(self, file_slots):
        return self.storage_service.cancel_upload(
            file_slots, pb.UploadOpCode.Storage)

    def storage_delete(self, user_id, storage_result):
        # storage_result->datastructers.StorageResult
        return self.storage_service.delete(
            user=self.get_user(user_id), storage_result_object=storage_result)
