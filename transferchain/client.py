import uuid
from transferchain.storage import Storage
from transferchain.logger import get_logger
from transferchain.config import create_config
from transferchain.addresses import (
    new_address_with_mnemonics, generate_user_addresses)


logger = get_logger(__file__)


class TransferChain(object):

    def __init__(self, *args, **kwargs):
        self.config = create_config()
        self.storage = Storage(self.config.db_path)

    def add_user(self):
        user_addresses = new_address_with_mnemonics(
            self.config.user_id, self.config.mnemonics)
        sub_user_id = str(uuid.uuid4())
        sub_user_addresses = generate_user_addresses(sub_user_id)
        self.save_user_addresses(sub_user_id, sub_user_addresses)
