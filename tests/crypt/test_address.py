import unittest
from transferchain.crypt import address
from transferchain.crypt import keys


class TestAddressMethods(unittest.TestCase):

    def test_public_key_sign_from_address_valid(self):
        _keys = keys.create_keys_with_mnemonic('test mnemonics', 'password')
        r1 = address.public_key_sign_from_address(_keys['Address'])
        self.assertEqual(r1, _keys['PublicKeySign'])

    def test_public_key_sign_from_address_invalid(self):
        address = "InvalidAddress"
        with self.assertRaises(Exception):
            keys.public_key_sign_from_address(address)

    def test_public_key_encrypt_from_address(self):
        _keys = keys.create_keys_with_mnemonic('test mnemonics', 'password')
        r1 = address.public_key_encrypt_from_address(_keys['Address'])
        self.assertEqual(r1, _keys['PublicKeyEncrypt'])

    def test_public_key_encrypt_from_address_invalid(self):
        address = "InvalidAddress"
        with self.assertRaises(Exception):
            keys.public_key_encrypt_from_address(address)
