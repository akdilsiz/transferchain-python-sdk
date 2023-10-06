import uuid
import json
from transferchain.db import DB
from transferchain.logger import get_logger
from transferchain.config import create_config
from transferchain.crypt import crypt
from transferchain.datastructures import Result, DataAddress
from transferchain.addresses import generate_user_addresses
from transferchain.transfer import Transfer
from transferchain.storage import Storage


logger = get_logger(__file__)


class TransferChain(object):

    def __init__(self, *args, **kwargs):
        self.config = create_config()
        self.db = DB(self.config.db_path)
        self.transfer_service = Transfer(self.config)
        self.storage_service = Storage(self.config)
        self.users = {}

    def add_user(self):
        sub_user_id = str(uuid.uuid4())
        result = generate_user_addresses(
            self.config.user_id, self.config.mnemonics, sub_user_id)
        if result.success is False:
            return result
        self.save_user_addresses(sub_user_id, result.data)

        self.users[sub_user_id] = result.data
        return Result(
            success=True,
            data={
                'sub_user_id': sub_user_id,
                'master_address': result.data[0].key['address']
            })

    def transfer_file(self, file_path, sender_user_id,
                      recipient_user_id, note):
        return self.transfer_service.transfer_file(
            file_path, sender_user_id, recipient_user_id, note)

    def load_users(self):
        users = self.db.get_all()
        for user_id, data in users.items():
            addresses = json.loads(crypt.decrypt_byte(
                data, self.config.mnemonics))
            items = []
            for address in addresses:
                items.append(DataAddress(**address))
            self.users[user_id] = items
        return self.users

    def save_user_addresses(self, sub_user_id, sub_user_addresses):
        data = []
        for address in sub_user_addresses:
            data.append(address.to_json())
        enc_data = crypt.encrypt_byte(
            json.dumps(data).encode('utf-8'),
            self.config.mnemonics)
        self.db.set(sub_user_id, enc_data)
