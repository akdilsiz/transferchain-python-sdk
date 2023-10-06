import unittest
from transferchain.client import TransferChain


class TestClientMethods(unittest.TestCase):

    def test_client(self):
        tc = TransferChain()

        # save_user_addresses in add_user, pass!
        user_result = tc.add_user()
        self.assertEqual(True, user_result.success)
        self.assertEqual(1, len(tc.users))

        tc.users = {}
        tc.load_users()
        self.assertEqual(1, len(tc.users))
