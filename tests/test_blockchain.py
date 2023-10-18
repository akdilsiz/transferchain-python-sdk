import unittest
from transferchain.crypt import bip39
from transferchain.addresses import get_user_password
from transferchain.blockchain import broadcast
from transferchain.crypt import keys
from transferchain.datastructures import Address
from transferchain.transaction import create_transaction
from transferchain import constants


class TestBlockchainMethods(unittest.TestCase):

    def test_broadcast(self):
        user_id = 1
        sub_user_id = 2
        mnemonics = bip39.create_mnomonics()
        user_pass = get_user_password(user_id, sub_user_id)
        user_keys = keys.create_keys_with_mnemonic(mnemonics, user_pass)

        tx_master_address = Address(
            Master=True, Key=user_keys, UserID=user_id, Mnemonics=mnemonics)

        tx = create_transaction(
            constants.TX_TYPE_MASTER, user_keys, user_keys['Address'],
            tx_master_address)
        result = broadcast(tx)
        self.assertEqual(True, result.success)
