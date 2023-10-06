import unittest
from transferchain.crypt import bip39
from transferchain.addresses import (
    get_user_password, generate_user_addresses)


class TestAddressesMethods(unittest.TestCase):

    def test_get_user_password(self):
        result = get_user_password(1, 1)
        self.assertEqual('user-1-1', result)

    def test_generate_user_addresses(self):
        mnemonics = bip39.create_mnomonics()
        result = generate_user_addresses(1, mnemonics, 2)
        self.assertEqual(True, result.success)
