import json
import gzip
from collections import namedtuple
from transferchain.mixins import TupleMixin

'''
broadcast datasi, blockchain'e gonderilen datadir ve bu datayi karsilayan
servis json payload'i camel case/snake cast/pascal case olarak karisik
bir sekilde handle ediyor. Bu sebeple basinda '# broadcast data' yazan
namedtupllar pythonic degildir!
'''


class Result(TupleMixin, namedtuple(
        'Result', 'success error_message data')):
    __slots__ = ()


# generate user address result
class User(TupleMixin, namedtuple(
        'User', 'id parent_user_id master_address addresses')):
    __slots__ = ()


# broadcast data
class DataTransfer(TupleMixin, namedtuple(
        'DataTransfer',
        'SenderMasterAddress UUID FileName Size Slots KeyAES KeyHMAC '
        'Message StorageCode Address UploadDate EndTime Typ '
        'ReceivedAddress')):
    __slots__ = ()


# broadcast data
class TransferSent(TupleMixin, namedtuple(
        'DataTransferSent',
        'filename uuid txId senderAddress senderMasterAddress '
        'receivedAddresses size uploadDate endTime keyAES KeyHMAC '
        'address storage_code slots ReceivedAddress')):
    __slots__ = ()


# broadcast data
class TransferReceiveDelete(TupleMixin, namedtuple(
        'TransferReceiveDelete', 'UUID TxID Typ Timestamp')):
    __slots__ = ()


# broadcast data
class TransferDelete(TupleMixin, namedtuple(
        'TransferDelete', 'UUID TxID FileName Typ Timestamp')):
    __slots__ = ()


# broadcast data
class Address(TupleMixin, namedtuple(
        'Address', 'Key Mnemonics Master UserID MasterAddress')):
    __slots__ = ()


# broadcast data
class Addresses(TupleMixin, namedtuple(
        'Addresses', 'UserID Addresses')):
    __slots__ = ()

    def dump(self, *args, **kwargs):
        data = {k: getattr(self, k) for k in self._fields}
        return gzip.compress(json.dumps(data).encode('utf-8'))


# config
class Config(TupleMixin, namedtuple(
        'Config',
        'api_token api_secret user_id wallet_uuid wallet_id mnemonics '
        'db_path')):
    __slots__ = ()


# wallet result
class CreateWalletResult(TupleMixin, namedtuple(
        'CreateWalletResult', 'wallet_id success error_message')):
    __slots__ = ()


# wallet result
class UserPackage(TupleMixin, namedtuple('UserPackage', 'id title code')):
    __slots__ = ()


# wallet result
class UserCompany(TupleMixin, namedtuple('UserCompany', 'id code title')):
    __slots__ = ()


# wallet result
class WalletUser(TupleMixin, namedtuple(
        'WalletUser',
        'id uuid type username is_active is_suspended full_name email mobile '
        'role_code role_title last_hash old_hash confirmation_code package '
        'account_create_code password_reset_code created_at updated_at '
        'company status')):
    __slots__ = ()


# wallet result
class WalletInfoResult(TupleMixin, namedtuple(
        'WalletInfoResult',
        'id created_at updated_at user success error_message')):
    __slots__ = ()
