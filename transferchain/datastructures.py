import json
import gzip
from collections import namedtuple
from transferchain.mixins import TupleMixin


class Result(TupleMixin, namedtuple(
        'Result', 'success error_message data')):
    __slots__ = ()


class DataAddress(TupleMixin, namedtuple(
        'DataAddress', 'key mnemonics master user_id')):
    __slots__ = ()


class DataAddresses(TupleMixin, namedtuple(
        'DataAddresses', 'user_id addresses')):
    __slots__ = ()

    def dump(self, *args, **kwargs):
        payload = {}
        for k in self._fields:
            key = k.title().replace('_', '')
            val = getattr(self, k)
            payload[key] = val
        return gzip.compress(json.dumps(payload).encode('utf-8'))


class DataStorage(TupleMixin, namedtuple(
        'DataStorage', '')):
    __slots__ = ()


class Config(TupleMixin, namedtuple(
        'Config',
        'api_token api_secret user_id wallet_uuid wallet_id mnemonics '
        'db_path')):
    __slots__ = ()


class CreateWalletResult(TupleMixin, namedtuple(
        'CreateWalletResult', 'wallet_id success error_message')):
    __slots__ = ()


class UserPackage(TupleMixin, namedtuple('UserPackage', 'id title code')):
    __slots__ = ()


class UserCompany(TupleMixin, namedtuple('UserCompany', 'id code title')):
    __slots__ = ()


class WalletUser(TupleMixin, namedtuple(
        'WalletUser',
        'id uuid type username is_active is_suspended full_name email mobile '
        'role_code role_title last_hash old_hash confirmation_code package '
        'account_create_code password_reset_code created_at updated_at '
        'company status')):
    __slots__ = ()


class WalletInfoResult(TupleMixin, namedtuple(
        'WalletInfoResult',
        'id created_at updated_at user success error_message')):
    __slots__ = ()
