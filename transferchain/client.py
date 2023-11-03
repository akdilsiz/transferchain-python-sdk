import uuid
import json
from transferchain import restore
from transferchain.db import DB
from transferchain.logger import get_logger
from transferchain.config import create_config
from transferchain.crypt import crypt, bip39
from transferchain.datastructures import (
    Result, Address, User)
from transferchain.addresses import (
    generate_user_addresses, generate_sub_user_addresses,
    get_user_password)
from transferchain.transfer import Transfer
from transferchain.storage import Storage
from transferchain.protobuf import service_pb2 as pb


logger = get_logger(__file__)


class TransferChain(object):
    '''
    It is the library's interface created for developers.
    You can give `db_path` from outside when creating the TransferChain
    instance.If you do not, it creates its own db as tc.db in the folder
    where it is run.The user's master addresses and sub user addresses
    are kept in this db.
    '''
    def __init__(self, *args, **kwargs):
        self.config = create_config()
        self.db_path = kwargs.get('db_path') or self.config.db_path
        self.db = DB(self.db_path)
        self.transfer_service = Transfer(self.config)
        self.storage_service = Storage(self.config)
        self.users = {}

        self.master_user = None

    def add_master_user(self):
        """
        If there are no mnemonics in the config, be sure to call this
        function to create the mnemonic and define the master user.

        Returns:
            Result object, payload is datastructures.User

        Example:
            -
        ```
        from transferchain.client import TransferChain
        tc = TransferChain()
        result = tc.add_master_user()
        user = result.data
        ```
        """
        mnemonics = bip39.create_mnomonics()
        result = generate_user_addresses(self.config.user_id, mnemonics)
        if result.success is False:
            return result

        user = result.data
        logger.info("Mnemonics-> %s" % mnemonics)
        self.config = self.config._replace(mnemonics=mnemonics)
        self.save_user(str(self.config.user_id), user)
        self.users[str(self.config.user_id)] = user
        self.master_user = user
        return Result(success=True, data=user)

    def restore_sub_users(self):
        """
        If you have mnemonics and have created a master user,
        call this function to fetch your sub users from
        the blockchain and write them to the db.

        Returns:
            Result object, payload is [datastructures.User...]

        Example:
            -
        ```
        from transferchain.client import TransferChain
        tc = TransferChain()
        result = tc.restore_master_user()
        if result.success
            tc.restore_sub_users()  # master user is required for this
        ```
        """
        user_password = get_user_password(self.config.user_id)
        result = restore.restore_sub_user_with_mnemonics(
            self.config.mnemonics, user_password, self.config.user_id)
        if result.success is False:
            return result
        for user in result.data:
            self.save_user(str(user.id), user)
            self.users[str(user.id)] = user
        return result

    def restore_master_user(self):
        """
        If you added your mnemonics to the config and want
        to pull the master user from the blockchain,
        call this function.

        Returns:
            Result object, payload is datastructures.User...

        Example:
            -
        ```
        from transferchain.client import TransferChain
        tc = TransferChain()
        result = tc.restore_master_user()
        ```
        """
        user_password = get_user_password(self.config.user_id)
        result = restore.restore_master_with_mnemonics(
            self.config.mnemonics, user_password, self.config.user_id)
        if result.success is False:
            return result
        user = result.data
        self.master_user = user
        self.save_user(str(self.config.user_id), user)
        self.users[str(self.config.user_id)] = user
        return result

    def add_user(self):
        """
        Use this function to add sub users under the master
        user you created.Before calling this, make sure you
        have mnemonics and the master user is defined.

        Returns:
            Result object, payload is datastructures.User...

        Example:
            -
        ```
        from transferchain.client import TransferChain
        tc = TransferChain()
        result = tc.add_master_user()
        user_result = tc.add_user()
        user_object = user_result.data
        ```
        """
        # master user check
        assert self.master_user is not None, 'you need the master user! '\
            'if you dont have mnemonics call the add_master_user, '\
            'if mnemonics already exists, call the restore_master_user.'
        sub_user_id = str(uuid.uuid4())
        master_user_address = self.master_user.master_address
        result = generate_sub_user_addresses(
            self.config.user_id, master_user_address,
            self.config.mnemonics, sub_user_id)
        if result.success is False:
            return result

        self.save_user(sub_user_id, result.data)
        self.users[sub_user_id] = result.data
        return Result(success=True, data=result.data)

    def get_user(self, user_id):
        """
        Return a user object

        Parameters:
            user_id (str):
                sub user id (uuid)

        Returns:
            A datastructures.User

        Example:
            -
        ```
        from transferchain.client import TransferChain
        tc = TransferChain()
        result = tc.add_master_user()
        user_result = tc.add_user()
        user_object = user_result.data
        user = tc.get_user(user_object.id)
        ```
        """
        return self.users[user_id]

    def load_users(self):
        """
        When creating the TransferChain instance,
        this function should be used to retrieve
        users from the db and import them into the instance.

        Returns:
            [datastructures.User]

        Example:
            -
        ```
        from transferchain.client import TransferChain
        tc = TransferChain()
        tc.load_users()
        ```
        """

        users = self.db.get_all()
        for user_id, data in users.items():
            user_data = json.loads(crypt.decrypt_byte(
                data, self.config.mnemonics))
            addresses = []
            for address in user_data.pop('addresses'):
                addresses.append(Address(**address))
            user_data['addresses'] = addresses
            user = User(**user_data)
            self.users[user_id] = user
            if user.master:
                self.master_user = user
        return self.users

    def save_user(self, sub_user_id, user):
        """
        Use this function to add sub users under the master
        user you created.Before calling this, make sure you
        have mnemonics and the master user is defined.

        Parameters:
           sub_user_id(str):
               sub user uuid
           user:
               datastructures.User

        Returns:
            Result object, payload is datastructures.User...

        Example:
            -
        ```
        from transferchain.client import TransferChain
        tc = TransferChain()
        result = tc.add_master_user()
        user_result = tc.add_user()
        user_object = user_result.data
        tc.save_user(user_object.id, user_object)
        ```
        """
        user_dict = user._asdict()
        addresses = []
        for address in user_dict.pop('addresses'):
            addresses.append(address._asdict())
        user_dict['addresses'] = addresses
        enc_data = crypt.encrypt_byte(
            json.dumps(user_dict).encode('utf-8'),
            self.config.mnemonics)
        self.db.set(sub_user_id, enc_data)

    def transfer_files(self, files, sender_user_id,
                       recipient_addresses, note, callback=None):
        """
        It takes the files as a list and sends them from
        the sender to the recipient user. Callback is optional,
        but if you give it, it is called by taking the result of
        each uploaded file as a parameter. There is a TransferSent
        object in the result. Save these objects so that you can
        delete them later or take another action.

        Parameters:
           files:
               list of files

           sender_user_id:
               datastructures.User

           recipient_addresses:
               datastructures.User.addresses[random].Key['Address']

           note:
               text note

           callback:
               callback is a function, and take the result parameter

        Returns:
            Result object, payload is [datastructures.TransferSent]

        Example:
            -
        ```
        from transferchain.client import TransferChain

        def callback(result):
            pass

        file_path = "/tmp/full_file.path"
        tc = TransferChain()
        tc.add_master_user()
        user_result = tc.add_user()
        user = user_result.data
        transfer_result = tc.transfer_files(
            files=[file_path],
            sender_user_id=user.id,
            recipient_addresses=[
                user.random_address().Key['Address']
            ],
            note='test note',
            callback=callback)
        ```
        """

        user = self.get_user(sender_user_id)
        sender_user_address = user.random_address()
        return self.transfer_service.upload(
            files, sender_user_address, recipient_addresses, note, callback)

    def transfer_received_delete(self, user_id, uuid, tx_id=None):
        """
        Deletes the transfer whose information is given.broadcast only.

        Parameters:
           user_id:
               sub user id is uuid

           uuid:
               transfer uuid

           tx_id ( optional ):
               transfer transaction id

        Returns:
            Result object

        Example:
            -
        ```
        from transferchain.client import TransferChain

        def callback(result):
            pass

        file_path = "/tmp/full_file.path"
        tc = TransferChain()
        tc.add_master_user()
        user_result = tc.add_user()
        user = user_result.data
        transfer_result = tc.transfer_files(
            files=[file_path],
            sender_user_id=user.id,
            recipient_addresses=[
                user.random_address().Key['Address']
            ],
            note='test note',
            callback=callback)

        recevied_delete_result = tc.transfer_received_delete(
            user.id, uuid=transfer_result.data[0].data.uuid, tx_id="")
        ```
        """
        # tx_id is not necessary
        return self.transfer_service.delete_received_transfer(
            user=self.get_user(user_id), uuid=uuid, tx_id=tx_id)

    def transfer_sent_delete(self, user_id, transfer_sent_obj):
        """
        Deletes the transfer whose information is given.

        Parameters:
           user_id:
               sub user id is uuid

           transfer_sent_obj:
               datastructures.TransferSent

        Returns:
            Result object

        Example:
            -
        ```
        from transferchain.client import TransferChain

        file_path = "/tmp/full_file.path"
        tc = TransferChain()
        tc.add_master_user()
        user_result = tc.add_user()
        user = user_result.data
        transfer_result = tc.transfer_files(
            files=[file_path],
            sender_user_id=user.id,
            recipient_addresses=[
                user.random_address().Key['Address']
            ],
            note='test note')
        sent_delete_result = tc.transfer_sent_delete(
            user.id, transfer_sent_obj=transfer_result.data[0].data)
        ```
        """
        # transfer_sent_obj->datastructures.TransferSent
        return self.transfer_service.delete_sent_transfer(
            user=self.get_user(user_id), transfer_sent_obj=transfer_sent_obj)

    def transfer_cancel(self, file_slots):
        """
        Cancels the specified slot.

        Parameters:
           file_slots
               datastructures.TransferSent.slots

        Returns:
            Result object

        Example:
            -
        ```
        from transferchain.client import TransferChain

        file_path = "/tmp/full_file.path"
        tc = TransferChain()
        tc.add_master_user()
        user_result = tc.add_user()
        user = user_result.data
        transfer_result = tc.transfer_files(
            files=[file_path],
            sender_user_id=user.id,
            recipient_addresses=[
                user.random_address().Key['Address']
            ],
            note='test note')
        transfer_slots = transfer_result.data[0].data.slots
        cancel_result = tc.transfer_cancel(transfer_slots)
        ```
        """
        return self.transfer_service.cancel_upload(
            file_slots, pb.UploadOpCode.Transfer)

    def transfer_download(self, file_uid, slots, file_size, file_name,
                          key_aes, key_hmac, destination):
        """
        Download transfer file.

        Parameters:
           file_uid:
               datastructures.TransferSent.uuid

           slots:
               datastructures.TransferSent.slots

           file_size:
               datastructures.TransferSent.size

           file_name:
               datastructures.TransferSent.filename

           key_aes:
               datastructures.TransferSent.keyAES

           key_hmac:
               datastructures.TransferSent.keyHMAC

           destination:
               destination path

        Returns:
            Result object

        Example:
            -
        ```
        from transferchain.client import TransferChain

        file_path = "/tmp/full_file.path"
        tc = TransferChain()
        tc.add_master_user()
        user_result = tc.add_user()
        user = user_result.data
        transfer_result = tc.transfer_files(
            files=[file_path],
            sender_user_id=user.id,
            recipient_addresses=[
                user.random_address().Key['Address']
            ],
            note='test note')
        transfer_sent_obj = transfer_result.data[0].data
        download_result = tc.transfer_download(
            file_uid=transfer_sent_obj.uuid,
            slots=transfer_sent_obj.slots,
            file_size=transfer_sent_obj.size,
            file_name=transfer_sent_obj.filename,
            key_aes=transfer_sent_obj.keyAES,
            key_hmac=transfer_sent_obj.KeyHMAC,
            destination=tempfile.tempdir
        )
        ```
        """
        return self.transfer_service.download_sent(
            file_uid, slots, file_size, file_name,
            key_aes, key_hmac, destination)

    def storage_upload(self, user_id, files, callback=None):
        """
        It takes the files as a list and sends them from
        the own storage. Callback is optional,
        but if you give it, it is called by taking the result of
        each uploaded file as a parameter. There is a StorageResult
        object in the result. Save these objects so that you can
        delete them later or take another action.

        Parameters:
           user_id:
              user id

           files:
               list of files

           callback:
               callback is a function, and take the result parameter

        Returns:
            Result object, payload is [datastructures.StorageResult]

        Example:
            -
        ```
        from transferchain.client import TransferChain

        def callback(result):
            pass

        file_path = "/tmp/full_file.path"
        tc = TransferChain()
        tc.add_master_user()
        user_result = tc.add_user()
        user = user_result.data
        storage_result = tc.storage_upload(
            files=[file_path],
            user=user,
            callback=callback)
        ```
        """

        return self.storage_service.upload(
            user=self.get_user(user_id), files=files, callback=callback)

    def storage_cancel(self, file_slots):
        """
        Cancels the specified slot.

        Parameters:
           file_slots
               datastructures.StorageResult.slots

        Returns:
            Result object

        Example:
            -
        ```
        from transferchain.client import TransferChain

        file_path = "/tmp/full_file.path"
        tc = TransferChain()
        tc.add_master_user()
        user_result = tc.add_user()
        user = user_result.data
        storage_result = tc.storage_upload(files=[file_path], user=user)
        storage_slots = storage_result.data[0].data.slots
        cancel_result = tc.storage_cancel(storage_slots)
        ```
        """
        return self.storage_service.cancel_upload(
            file_slots, pb.UploadOpCode.Storage)

    def storage_delete(self, user_id, storage_result):
        """
        Deletes the storage whose information is given.

        Parameters:
           user_id:
               sub user id is uuid

           storage_result:
               datastructures.StorageResult

        Returns:
            Result object

        Example:
            -
        ```
        from transferchain.client import TransferChain

        file_path = "/tmp/full_file.path"
        tc = TransferChain()
        tc.add_master_user()
        user_result = tc.add_user()
        user = user_result.data
        storage_result = tc.storage_upload(files=[file_path], user=user)
        sent_delete_result = tc.storage_delete(
            user.id, storage_result=storage_result.data[0].data)
        ```
        """
        # storage_result->datastructures.StorageResult
        return self.storage_service.delete(
            user=self.get_user(user_id), storage_result_object=storage_result)

    def storage_download(self, file_uid, slots, file_size, file_name,
                         key_aes, key_hmac, destination):
        """
        Download storage file.

        Parameters:
           file_uid:
               datastructures.StorageResult.uuid

           slots:
               datastructures.StorageResult.slots

           file_size:
               datastructures.StorageResult.size

           file_name:
               datastructures.StorageResult.filename

           key_aes:
               datastructures.StorageResult.keyAES

           key_hmac:
               datastructures.StorageResult.keyHMAC

           destination:
               destination path

        Returns:
            Result object

        Example:
            -
        ```
        from transferchain.client import TransferChain

        file_path = "/tmp/full_file.path"
        tc = TransferChain()
        tc.add_master_user()
        user_result = tc.add_user()
        user = user_result.data

        storage_result = tc.storage_upload(files=[file_path], user=user)

        storage_result_obj = storage_result.data[0].data
        download_result = tc.storage_download(
            file_uid=storage_result_obj.uuid,
            slots=storage_result_obj.slots,
            file_size=storage_result_obj.size,
            file_name=storage_result_obj.filename,
            key_aes=storage_result_obj.keyAES,
            key_hmac=storage_result_obj.KeyHMAC,
            destination=tempfile.tempdir
        )
        ```
        """
        return self.transfer_service.download_sent(
            file_uid, slots, file_size, file_name,
            key_aes, key_hmac, destination)
