from collections import namedtuple


class TupleMixin(object):

    def __new__(cls, *args, **kwargs):
        if not kwargs:
            return super(TupleMixin, cls).__new__(cls, *args, **kwargs)

        defaults = {f: None for f in cls._fields}

        defaults.update({k: v for k, v in kwargs.items() if k in cls._fields})
        return super(TupleMixin, cls).__new__(cls, *args, **defaults)


class Config(TupleMixin, namedtuple(
    'Config',
        'api_token api_secret user_id wallet_uuid wallet_id mnemonics '
        'db_path')):
    __slots__ = ()


class CreateWalletResult(TupleMixin, namedtuple(
    'CreateWalletResult',
        'wallet_id success error_message')):
    __slots__ = ()


class UserPackage(TupleMixin, namedtuple(
    'UserPackage',
        'id title code')):
    __slots__ = ()


class UserCompany(TupleMixin, namedtuple(
    'UserCompany',
        'id code title')):
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
