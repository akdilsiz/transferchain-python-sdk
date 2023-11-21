import json
import gzip
import random
from collections import namedtuple
from transferchain.mixins import TupleMixin


class Result(TupleMixin, namedtuple(
        'Result', 'success error_message data')):
    '''Common result tuple'''
    __slots__ = ()


class User(TupleMixin, namedtuple(
        'User', 'id parent_user_id master_address addresses master')):
    '''Generate user address result'''
    __slots__ = ()

    def random_address(self):
        '''Return random user address'''
        return self.addresses[
            random.randint(1, len(self.addresses) - 1)]


class DataStorage(TupleMixin, namedtuple(
        'DataStorage',
        'UUID FileName Size Slots KeyAES KeyHMAC StorageCode '
        'Address UploadDate')):
    '''Broadcast data'''
    __slots__ = ()


class StorageResult(TupleMixin, namedtuple(
        'StorageResult',
        'uuid filename size senderAddress recipientAddress '
        'txId slots keyAES keyHMAC address storage_code uploadDate')):
    '''Broadcast data'''
    __slots__ = ()


class DataStorageDelete(TupleMixin, namedtuple(
        'DataStorageDelete', 'UUID TxID FileName Timestamp')):
    '''Broadcast data'''
    __slots__ = ()


class DataTransfer(TupleMixin, namedtuple(
        'DataTransfer',
        'SenderMasterAddress UUID FileName Size Slots KeyAES KeyHMAC '
        'Message StorageCode Address UploadDate EndTime Typ '
        'ReceivedAddress')):
    '''Broadcast data'''
    __slots__ = ()


class TransferSent(TupleMixin, namedtuple(
        'DataTransferSent',
        'filename uuid txId senderAddress senderMasterAddress '
        'receivedAddresses size uploadDate endTime keyAES KeyHMAC '
        'address storage_code slots ReceivedAddress')):
    '''Broadcast data'''
    __slots__ = ()


class TransferReceiveDelete(TupleMixin, namedtuple(
        'TransferReceiveDelete', 'UUID TxID Typ Timestamp')):
    '''Broadcast data'''
    __slots__ = ()


class TransferDelete(TupleMixin, namedtuple(
        'TransferDelete', 'UUID TxID FileName Typ Timestamp')):
    '''Broadcast data'''
    __slots__ = ()


class Address(TupleMixin, namedtuple(
        'Address', 'Key Mnemonics Master UserID MasterAddress SubUserID')):
    '''Broadcast data'''
    __slots__ = ()

    def dump(self, *args, **kwargs):
        '''Named tuple to json'''
        excludes = ['MasterAddress']
        data = {k: getattr(self, k) for k in self._fields if k not in excludes}
        return json.dumps(data).encode('utf-8')


class Addresses(TupleMixin, namedtuple(
        'Addresses', 'UserID Addresses')):
    '''Broadcast data'''
    __slots__ = ()

    def dump(self, *args, **kwargs):
        '''Named tuple to json with gzip'''
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
class UserPackage(TupleMixin, namedtuple('UserPackage', 'transfer '
                                         'transfer_size transfer_count '
                                         'transfer_recipient_count messaging '
                                         'messaging_count storage storage_size '
                                         'storage_upload_size share share_size '
                                         'share_count share_recipient_count '
                                         'ipclaim ipclaim_count')):
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
