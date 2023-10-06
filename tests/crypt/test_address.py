import unittest
from transferchain.crypt import address
from transferchain.crypt import keys


class TestAddressMethods(unittest.TestCase):

    def test_publicK_key_sign_from_address(self):
        _keys = keys.create_keys_with_mnemonic('test mnemonics', 'password')
        r1 = address.public_key_sign_from_address(_keys['address'])
        self.assertEqual(r1, _keys['public_key_sign'])

    def test_public_key_encrypt_from_address(self):
        _keys = keys.create_keys_with_mnemonic('test mnemonics', 'password')
        r1 = address.public_key_encrypt_from_address(_keys['address'])
        self.assertEqual(r1, _keys['public_key_encrypt'])


if __name__ == '__main__':
    unittest.main()
