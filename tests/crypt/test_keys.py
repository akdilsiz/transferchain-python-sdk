import unittest
from transferchain.crypt import keys


class TestKeysMethods(unittest.TestCase):

    def seed(self):
        return 'd02552defcf487c2e8c623925479d079f203bf8ab945ceb97f4cc30c42bf75e3' # noqa

    def test_generate_ed25519_keypair_from_seed(self):
        seed = self.seed()
        priv_key_ed, pub_key = keys.generate_ed25519_keypair_from_seed(seed)

        self.assertEqual(priv_key_ed, seed)
        self.assertEqual(
            pub_key,
            '12fb9d6b64cfa8eb3ca04a029fd7f8aac410320abbe3e0a784b50185338fffe7')

    def test_curve25519_scalar_base_mult(self):
        r1 = keys.curve25519_scalar_base_mult(self.seed())
        expect = 'f1a858e58cc3c6e455224cdbc7e7719abd8f1107706bf9253f5551e5144b8e2d'  # noqa
        self.assertEqual(r1, expect)

    def test_base58_encode(self):
        result = keys.base58_encode(b'test'.hex())
        self.assertEqual('3yZe7d', result)

    def test_generate_keys(self):
        seed = self.seed()
        seed58 = 'F1Wp1F75u4v9weyVAEfTMfKQUuATN3DP5az63ALLSXo8'
        result = keys.generate_keys(seed)
        self.assertEqual(result['Seed'], seed)
        self.assertEqual(result['Seed58'], seed58)
