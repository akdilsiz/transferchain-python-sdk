import uuid
import json
import random
from transferchain.db import DB
from transferchain.logger import get_logger
from transferchain.config import create_config
from transferchain.crypt import crypt
from transferchain.datastructures import Result, Address, User
from transferchain.addresses import generate_user_addresses
from transferchain.transfer import Transfer
from transferchain.storage import Storage


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

    def transfer_files(self, files, sender_user_id,
                       recipient_addresses, note):
        user = self.users[sender_user_id]
        sender_user_address = user.addresses[
            random.randint(1, len(user.addresses) - 1)]
        return self.transfer_service.upload(
            files, sender_user_address, recipient_addresses, note)

    def transfer_sent_delete(self, user_id):
        user = self.users[user_id]
        first_user_keys = user.addresses[
            random.randint(1, len(user.addresses) - 1)]
        second_user_keys = user.addresses[
            random.randint(1, len(user.addresses) - 1)]

        tx_id = ""
        tx_uuid = ""
        return self.transfer_service.delete(
            first_user_keys, second_user_keys, tx_id, tx_uuid)

    def transfer_sent_download(self, user_id):
        pass

    def transfer_received_download(self, user_id):
        pass

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
