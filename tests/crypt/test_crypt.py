import unittest
from transferchain.crypt import bip39
from transferchain.crypt import keys
from transferchain.crypt import crypt


class TestAddressMethods(unittest.TestCase):

    def test_asymmetric_encryption_decryption(self):
        message = b'alles gut'
        sender_mnemonics = bip39.create_mnomonics()
        sender = keys.create_keys_with_mnemonic(sender_mnemonics, 'p1')

        recipient_mnemonics = bip39.create_mnomonics()
        recipient = keys.create_keys_with_mnemonic(recipient_mnemonics, 'p2')

        encrypted_data = crypt.encrypt_asymmetric(
            sender['Seed'], recipient['Address'], message)

        decrypted_data = crypt.decrypt_asymmetric(
            sender['Address'], recipient['Seed'], encrypted_data)
        self.assertEqual(message, decrypted_data)

    def test_sign(self):
        expected = '7c37e4276de5cd43a09bf9fb06ec91b6e8714cebf5f8e38a67c004978e03db7b08792bddbb9493c1a01e4fefaeddd6dc5890c16f4c81d68b88043bf037580d02' # noqa
        pks = 'a0c4e141c6273b9cfd0ffd4ac64110b31189b7051066e92e45ba4534a8a12008baa5f1b8e00a76e8342bb31b105c396d423d9e897df7a290e55fca4ba8249c79' # noqa
        result = crypt.sign(pks, b'alles gut')
        self.assertEqual(expected, result.hex())

    def test_verify_sign_valid(self):
        mnemonics = bip39.create_mnomonics()
        keys_ = keys.create_keys_with_mnemonic(mnemonics, 'p2')
        data = b'alles gut'
        sign_key = crypt.sign(keys_['PrivateKeySign'], data)
        result = crypt.verify_sign(keys_['Address'], data, sign_key)
        self.assertEqual(True, result)

    def test_verify_sign_invalid(self):
        mnemonics = bip39.create_mnomonics()
        keys_ = keys.create_keys_with_mnemonic(mnemonics, 'p2')
        data = b'alles gut'
        sign_key = crypt.sign(keys_['PrivateKeySign'], data)
        result = crypt.verify_sign('empty', data, sign_key)
        self.assertEqual(False, result)

    def test_generate_encrypt_key(self):
        result = crypt.generate_encrypt_key(10)
        self.assertEqual(10, len(result))

    def test_encrypt_byte(self):
        message = b'alles gut'
        key = 'secret_key'
        enc_result = crypt.encrypt_byte(message, key)
        dec_result = crypt.decrypt_byte(enc_result, key)
        self.assertEqual(message, dec_result)
