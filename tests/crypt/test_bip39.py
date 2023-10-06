import unittest
from transferchain.crypt import bip39


class TestBib39Methods(unittest.TestCase):

    def test_checksum(self):
        r1 = bip39.checksum(b'')
        self.assertEqual(r1, [], 'invalid result')

        r2 = bip39.checksum(b't')
        expect = ['0', '1', '1', '1', '0', '1', '0', '0']
        self.assertEqual(r2, expect, 'invalid result')

    def test_bytes_to_bits(self):
        r1 = bip39.bytes_to_bits(b't')
        expect = ['0', '1', '1', '1', '0', '1', '0', '0']
        self.assertEqual(r1, expect, 'invalid result')

    def test_mnemonics(self):
        r1 = bip39.create_mnomonics()
        self.assertIsNot(r1, '', 'mnemonics are empty')
        self.assertEqual(len(r1.split()), 24, 'incorrect mnemonics count')
