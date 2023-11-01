import unittest
from transferchain.crypt import bip39
from transferchain.addresses import (
    get_user_password, generate_user_addresses,
    generate_sub_user_addresses)


class TestAddressesMethods(unittest.TestCase):

    def test_get_user_password_valid_s1(self):
        result = get_user_password(1, 1)
        self.assertEqual('user-1-1', result)

    def test_get_user_password_valid_s2(self):
        result = get_user_password(1)
        self.assertEqual('user-1', result)

    def test_get_user_password_invalid(self):
        result = get_user_password(1, 1)
        self.assertNotEqual('user-1-2', result)

    def test_generate_sub_user_addresses_valid(self):
        mnemonics = bip39.create_mnomonics()
        result = generate_user_addresses(1, mnemonics)
        self.assertEqual(True, result.success)

        master_address = result.data.master_address
        result = generate_sub_user_addresses(1, master_address, mnemonics, 2)
        self.assertEqual(True, result.success)

    def test_generate_sub_user_addresses_invalid(self):
        mnemonics = bip39.create_mnomonics()
        result = generate_user_addresses(1, mnemonics)
        self.assertEqual(True, result.success)

        master_address = result.data.master_address
        result = generate_sub_user_addresses(1, master_address, mnemonics, 2)
        self.assertNotEqual(False, result.success)

    def test_generate_user_addresses_valid(self):
        mnemonics = bip39.create_mnomonics()
        result = generate_user_addresses(1, mnemonics)
        self.assertEqual(True, result.success)
