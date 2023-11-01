import time
import unittest
from transferchain import restore
from transferchain import constants
from transferchain.addresses import get_user_password
from transferchain.config import create_config
from transferchain.client import TransferChain


class TestRestoreMethods(unittest.TestCase):

    def test_extract_txn(self):
        config = create_config()
        tc = TransferChain(config)
        result = tc.add_master_user()
        self.assertEqual(True, result.success)

        user_password = get_user_password(tc.config.user_id)
        result = restore.restore_master_user(
            tc.config.mnemonics, user_password)
        self.assertEqual(True, result['response'].success)

        txn_result = restore.extract_txn(
            result['response'].result['txs'][0], result['user_keys'])
        self.assertIsNotNone(txn_result)

    def test_restore_master(self):
        config = create_config()
        tc = TransferChain(config)
        result = tc.add_master_user()
        self.assertEqual(True, result.success)

        user_password = get_user_password(tc.config.user_id)
        result = restore.restore_master(
            tc.config.mnemonics, user_password, constants.TX_TYPE_MASTER)
        self.assertEqual(True, result['response'].success)

    def test_restore_master_user(self):
        config = create_config()
        tc = TransferChain(config)
        result = tc.add_master_user()
        self.assertEqual(True, result.success)

        user_password = get_user_password(tc.config.user_id)
        result = restore.restore_master_user(
            tc.config.mnemonics, user_password)
        self.assertEqual(True, result['response'].success)

    def test_restore_sub_user(self):
        config = create_config()
        tc = TransferChain(config)
        result = tc.add_master_user()
        self.assertEqual(True, result.success)

        user_info_result = tc.add_user()
        self.assertEqual(True, user_info_result.success)
        user = user_info_result.data

        user_password = get_user_password(tc.config.user_id)
        result = restore.restore_sub_user(
            tc.config.mnemonics, user_password)
        self.assertEqual(True, result['response'].success)
        txn = restore.extract_txn(
            result['response'].result['txs'][0], result['user_keys'])

        self.assertEqual(txn['SubUserID'], user.id)

    def test_restore_master_user_with_mnemonics(self):
        config = create_config()
        tc = TransferChain(config)
        result = tc.add_master_user()
        self.assertEqual(True, result.success)
        time.sleep(10)
        user_password = get_user_password(tc.config.user_id)
        result = restore.restore_master_with_mnemonics(
            tc.config.mnemonics, user_password, tc.config.user_id)
        self.assertEqual(True, result.success)

    def test_restore_sub_user_with_mnemonics(self):
        config = create_config()
        tc = TransferChain(config)
        result = tc.add_master_user()
        time.sleep(10)
        self.assertEqual(True, result.success)
        user_count = 3
        for i in range(user_count):
            user_info_result = tc.add_user()
            self.assertEqual(True, user_info_result.success)
        time.sleep(10)
        user_password = get_user_password(tc.config.user_id)
        result = restore.restore_sub_user_with_mnemonics(
            tc.config.mnemonics, user_password, tc.config.user_id)
        self.assertEqual(True, result.success)
        self.assertEqual(user_count, len(result.data))
