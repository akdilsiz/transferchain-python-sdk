import unittest
from transferchain.config import create_config


class TestConfigMethods(unittest.TestCase):

    def test_create_config_valid(self):
        config = create_config()
        self.assertIsNotNone(config.api_token)
        self.assertIsNotNone(config.api_secret)
        self.assertIsNotNone(config.wallet_id)
        self.assertIsNotNone(config.wallet_uuid)
        self.assertIsNotNone(config.user_id)
        self.assertIsNotNone(config.mnemonics)
        self.assertIsNotNone(config.db_path)
