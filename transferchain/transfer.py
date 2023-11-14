import os
import uuid
import shutil
import tempfile
import queue
import threading
import datetime
from pathlib import Path
import grpc
from transferchain import constants
from transferchain import blockchain
from transferchain.utils import datetime_to_str
from transferchain.crypt import crypt
from transferchain.datastructures import (
    Result, DataTransfer, TransferSent, TransferDelete,
    TransferReceiveDelete)
from transferchain.grpc_client import get_client
from transferchain.protobuf import service_pb2 as pb
from transferchain.transaction import create_transaction


class Transfer(object):
    '''Transfer processes are managed by the functions in this class.'''

    def __init__(self, config):
        self.config = config

    def download_sent(self, file_uid, slots, file_size, file_name,
                      key_aes, key_hmac, destination):
        '''
        Download transfer file.

        Parameters:
            file_uid (str):
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
        ````
        from transferchain.client import TransferChain
        from transferchain.transfer import Transfer
        from transferchain.config import create_config

        config = create_config()
        tc = TransferChain(config)
        tc.add_master_user()
        user_info_result = tc.add_user()
        user = user_info_result.data

        sender = user.random_address()

        transfer = Transfer(config)
        file_path = '/tmp/your-test-file'

        result = transfer.upload(
            files=[file_path],
            sender=sender,
            recipient_addresses=[sender.Key['Address']])

        transfer_sent_obj = result.data[0].data
        download_result = transfer.download_sent(
            file_uid=transfer_sent_obj.uuid,
            slots=transfer_sent_obj.slots,
            file_size=transfer_sent_obj.size,
            file_name=transfer_sent_obj.filename,
            key_aes=transfer_sent_obj.keyAES,
            key_hmac=transfer_sent_obj.KeyHMAC,
            destination=tempfile.tempdir)
        ````
        '''
        assert file_uid != "", "invalid file_uuid"
        assert len(slots) > 0, "invalid slots"
        assert file_size > 0, "invalid file_size"
        assert file_name != "", "invalid file_name"
        assert key_aes != "", "invalid key_aes"
        assert key_hmac != "", "invalid key_hmac"
        assert destination != "", "invalid destination"
        destination_path = Path(destination)

        assert destination_path.exists(), 'destination does not exist'
        assert destination_path.is_dir(), 'destination must be a folder'
        destination_file = destination_path.joinpath(file_name)

        grpc_client = get_client()
        meta_data = [
            ("user-id", str(self.config.user_id)),
            ("user-api-token", self.config.api_token),
            ("user-api-secret", self.config.api_secret)
        ]
        try:
            file_chunks = grpc_client.Download(pb.DownloadRequest(
                uuid=file_uid,
                Slots=slots,
                WalletID=self.config.wallet_id,
                UserID=self.config.user_id,
                opCode=pb.UploadOpCode.Transfer,
            ), metadata=meta_data)
        except grpc.RpcError as e:
            error_message = 'download error:{}'.format(e.details())
            e.cancel()
            return Result(success=False, error_message=error_message)

        in_file_uid = str(uuid.uuid4())
        in_file_tmp_folder = tempfile.mkdtemp()
        in_file_path = os.path.join(in_file_tmp_folder, in_file_uid)
        totalWrite = 0
        with open(in_file_path, 'ab') as in_file:
            for fc in file_chunks:
                totalWrite + in_file.write(fc.chunk)

        with open(in_file_path, 'rb') as in_file:
            with destination_file.open(mode='wb') as out_file:
                try:
                    crypt.decrypt_aesctr_with_hmac(
                        in_file, out_file, key_aes.encode('utf-8'),
                        key_hmac.encode('utf-8'))
                except Exception as e:
                    return Result(sucess=False, error_message=str(e))
        return Result(success=True)

    def delete_received_transfer(self, user, uuid, tx_id=""):
        '''
        Delete received transfer

        Parameters:
            user (datastructures.User):
                datastructures.User object

            uuid (str):
                transfer uuid

            tx_id:
                transfer transaction id. optional

        Returns:
            Result object

        Example:
            -
        ````
        from transferchain.client import TransferChain
        from transferchain.transfer import Transfer
        from transferchain.config import create_config

        config = create_config()
        tc = TransferChain(config)
        tc.add_master_user()
        user_info_result = tc.add_user()
        user = user_info_result.data

        sender = user.random_address()

        transfer = Transfer(config)
        file_path = '/tmp/your-test-file'

        result = transfer.upload(
            files=[file_path],
            sender=sender,
            recipient_addresses=[sender.Key['Address']])
        delete_result = transfer.delete_received_transfer(
            user=user,
            uuid=transfer_result.data[0].data.uuid))
        ````
        '''
        user_first_address = user.random_address()
        user_second_address = user.random_address()
        tx_data = TransferReceiveDelete(
            UUID=uuid,
            TxID=tx_id,
            Typ=constants.TRANSFER_TYPE_SENT,
            Timestamp=datetime_to_str(datetime.datetime.now()))
        tx = create_transaction(
            constants.TX_TYPE_TRANSFER_RECIEVE_DELETE,
            user_first_address.Key,
            user_second_address.Key['Address'],
            tx_data)
        result = blockchain.broadcast(tx)
        if result.success is False:
            return Result(
                success=False,
                error_message='Transfer recevied delete received is not published on the blockchain.') # noqa
        return Result(success=True)

    def _delete_slot(self, slot_dict, result_queue):
        '''Delete single Slot'''
        grpc_client = get_client()
        meta_data = [
            ("user-id", str(self.config.user_id)),
            ("user-api-token", self.config.api_token),
            ("user-api-secret", self.config.api_secret)
        ]
        slot = pb.UploadSlot(
            UUID=slot_dict.get('UUID'),
            BaseUUID=slot_dict.get('BaseUUID'),
            StorageService=slot_dict.get('StorageService'),
            Address=slot_dict.get('Address'),
            Size=slot_dict.get('Size'),
            SizeRL=slot_dict.get('SizeRL'),
            StorageCode=slot_dict.get('StorageCode'),
            userID=slot_dict.get('userID'))
        result = Result(success=True)
        try:
            grpc_client.Delete(pb.DeleteRequest(
                uuid=slot.UUID,
                StorageCode=slot.StorageCode,
                WalletID=self.config.wallet_id,
                slot=slot,
                opCode=pb.UploadOpCode.Transfer,
                UserID=self.config.user_id
            ), metadata=meta_data)
        except grpc.RpcError as e:
            error_message = 'delete error:{}'.format(e.details())
            result = Result(success=False, error_message=error_message)
        result_queue.put(result)
        return result

    def delete_sent_transfer(self, user, transfer_sent_obj):
        '''
        Delete sent transfer

        Parameters:
            user (datastructures.User):
                datastructures.User object

            transfer_sent_obj (datastructures.TransferSent):
                datastructures.TransferSent

        Returns:
            Result object

        Example:
            -
        ````
        from transferchain.client import TransferChain
        from transferchain.transfer import Transfer
        from transferchain.config import create_config

        config = create_config()
        tc = TransferChain(config)
        tc.add_master_user()
        user_info_result = tc.add_user()
        user = user_info_result.data

        sender = user.random_address()

        transfer = Transfer(config)
        file_path = '/tmp/your-test-file'

        transfer_result = transfer.upload(
            files=[file_path],
            sender=sender,
            recipient_addresses=[sender.Key['Address']])
        transfer_sent_obj = transfer_result.data[0].data

        delete_result = transfer.delete_sent_transfer(
            user=user, transfer_sent_obj=transfer_sent_obj)
        ````
        '''
        result_queue = queue.Queue()
        threads = []

        user_first_address = user.random_address()
        user_second_address = user.random_address()

        for slot_dict in transfer_sent_obj.slots:
            t = threading.Thread(
                target=self._delete_slot, args=(slot_dict, result_queue))
            threads.append(t)

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        error_messages = ''
        for i in range(len(threads)):
            result = result_queue.get()
            if result.success is False:
                error_messages += result.error_messages
        if error_messages:
            return Result(success=False, error_messages=error_messages)

        tx_data = TransferDelete(
            UUID=transfer_sent_obj.uuid,
            TxID=transfer_sent_obj.txId,
            FileName=transfer_sent_obj.filename,
            Typ=constants.TRANSFER_TYPE_SENT,
            Timestamp=datetime_to_str(datetime.datetime.now()))

        error_result = None
        if transfer_sent_obj.receivedAddresses:
            for received in transfer_sent_obj.receivedAddresses:
                tx = create_transaction(
                    constants.TX_TYPE_TRANSFER_CANCEL, user_first_address.Key,
                    received, tx_data)
                broadcast_result = blockchain.broadcast(tx)
                if broadcast_result.success is False:
                    error_result = Result(
                        success=False,
                        error_message='Transfer delete is not published on the blockchain.') # noqa
        else:
            tx = create_transaction(
                constants.TX_TYPE_TRANSFER_CANCEL, user_first_address.Key,
                transfer_sent_obj.ReceivedAddress, tx_data)
            broadcast_result = blockchain.broadcast(tx)
            if broadcast_result.success is False:
                error_result = Result(
                    success=False,
                    error_message='Transfer delete is not published on the blockchain.') # noqa
        tx = create_transaction(
            constants.TX_TYPE_TRANSFER_CANCEL, user_first_address.Key,
            user_second_address.Key['Address'], tx_data)
        broadcast_result = blockchain.broadcast(tx)
        if broadcast_result.success is False:
            error_result = Result(
                success=False,
                error_message='Transfer delete is not published on the blockchain.') # noqa

        if error_result:
            return error_result
        return Result(success=True)

    def upload(self, files, sender, recipient_addresses, note, callback=None):
        '''
        File transfer

        Parameters:
           files:
               list of files

           sender:
               datastructures.User.addresses.Address

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
        ````
        from transferchain.client import TransferChain
        from transferchain.transfer import Transfer
        from transferchain.config import create_config

        config = create_config()
        tc = TransferChain(config)
        tc.add_master_user()
        user_info_result = tc.add_user()
        user = user_info_result.data

        sender = user.random_address()

        transfer = Transfer(config)
        file_path = '/tmp/your-test-file'

        transfer_result = transfer.upload(
            files=[file_path],
            sender=sender,
            recipient_addresses=[sender.Key['Address']])
        ````
        '''
        assert list == type(recipient_addresses), 'recipient adddress must be list' # noqa
        assert len(recipient_addresses) > 0, 'recipient_addresses is required'
        assert len(files) > 0, 'files required'

        if callback is not None:
            assert callable(callback), 'callback is not a function'

        base_file_names = []
        total_file_size = 0
        for file_path in files:
            file_info = os.stat(file_path)
            base_file_names.append(os.path.basename(file_path))
            total_file_size += file_info.st_size

        grpc_client = get_client()
        meta_data = [
            ("user-id", str(self.config.user_id)),
            ("user-api-token", self.config.api_token),
            ("user-api-secret", self.config.api_secret)
        ]

        try:
            init_result = grpc_client.TransferInitV2(
                pb.TransferInitRequest(
                    files=base_file_names,
                    totalSize=total_file_size,
                    opCode=pb.UploadOpCode.Transfer,
                    userID=self.config.user_id,
                    walletID=self.config.wallet_id,
                    recipientCount=len(recipient_addresses),
                    transferOpCode=pb.TransferOpCode.Normal,
                    notes=note,
                    paths=files,
                    DeleteAfter=7 * 24
                ), metadata=meta_data)
        except grpc.RpcError as e:
            error_message = "transfer init request error: {}".format(
                e.details())
            return Result(success=False, error_message=error_message)

        transfer_process_uuid = str(uuid.uuid4())

        threads = []
        result_queue = queue.Queue()
        for file_path in files:
            t = threading.Thread(
                target=self.upload_single_file, args=(
                    pb.UploadOpCode.Transfer,
                    init_result.SessionID,
                    init_result.BaseUUIDs,
                    transfer_process_uuid,
                    sender,
                    recipient_addresses,
                    note,
                    file_path,
                    callback,
                    result_queue
                ))
            threads.append(t)

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        results = []
        for result in range(len(threads)):
            results.append(result_queue.get())

        try:
            grpc_client.TransferFinishV2(
                pb.TransferFinishRequest(
                    SessionID=init_result.SessionID,
                    UserID=self.config.user_id,
                    WalletID=self.config.wallet_id), metadata=meta_data)
        except grpc.RpcError as e:
            # cancel uploads
            for result in results:
                slots = result.data['slots']
                self.cancel_upload(slots, pb.UploadOpCode.Transfer)
            error_message = "transfer finish request error: {}".format(
                e.details())
            return Result(success=False, error_message=error_message)
        return Result(success=True, data=results)

    def upload_single_file(self, op_code, session_id, base_uuid_map,
                           process_uuid, sender, recipients, note,
                           file_path, callback, result_queue):
        '''
        Single file upload. The transfer.upload function uses this.

        Parameters:
           op_code:
               pb.UploadOpCode.<Transfer|Storage>

           session_id:
               pb.TransferInitResponse.SessionID

           base_uuid_map:
               pb.TransferInitResponse.BaseUUIDs

           process_uuid:
               random uuid

           sender:
               datastructures.User.addresses.Address

           recipients:
               list of recipient addresses.
               datastructures.Address.Key['Address']

           note:
               transfer note

           file_path:
               transfer file path

           callback:
               callback is a function, and take the result parameter

           result_queue:
               queue.Queue object

        Returns:
            Result object, payload is [datastructures.TransferSent]

        Example:
            -
        '''
        tmp_folder = tempfile.mkdtemp()
        aes_key = crypt.generate_encrypt_key(32).encode('utf-8')
        hmac_key = crypt.generate_encrypt_key(32).encode('utf-8')

        out_file_uuid = str(uuid.uuid4())
        out_file_path = os.path.join(tmp_folder, out_file_uuid)
        with open(out_file_path, 'ab') as outfile:
            with open(file_path, 'rb') as infile:
                crypt.encrypt_aesctr_with_hmac(
                    infile, outfile, aes_key, hmac_key)

        out_file_info = os.stat(out_file_path)

        file_uuid = base_uuid_map[file_path]
        meta_data = [
            ("user-id", str(self.config.user_id)),
            ("user-api-token", self.config.api_token),
            ("user-api-secret", self.config.api_secret),
            ("uuid", file_uuid),
            ("baseuuid", file_uuid),
            ("sessionid", session_id)
        ]

        grpc_client = get_client()
        upload_init_result = grpc_client.UploadInitV2(
            pb.UploadInitRequest(
                sessionID=session_id,
                fileName=file_path,
                fileSize=out_file_info.st_size,
                opCode=pb.UploadOpCode.Transfer,
                userID=self.config.user_id,
                walletID=self.config.wallet_id,
                DeleteAfter=7 * 24,
                recipientCount=len(recipients),
                transferOpCode=pb.TransferOpCode.Normal,
                senderAddress=sender.Key['Address']
            ), metadata=meta_data)

        out_file = open(out_file_path, 'rb')
        tweezers = {"total_write": 0}
        error_result = None
        for slot_index, slot in enumerate(upload_init_result.Slots):
            is_last_slot = slot_index == len(upload_init_result.Slots) - 1
            payloads = self.prepare_slot_upload_request(
                session_id=session_id,
                out_file=out_file,
                slot=slot,
                is_last_slot=is_last_slot,
                file_stat=out_file_info,
                tweezers=tweezers
            )
            error = ""
            try:
                upload_basic_result = grpc_client.UploadBasicV4(
                    payloads, metadata=meta_data)
                status_code = upload_basic_result.statusCode
                if status_code != 1:
                    error = f"upload result is not ok. result code:{status_code}" # noqa
            except grpc.RpcError as e:
                error = e.details()
                e.cancel()
            except Exception as e:
                error = str(e)

            if error:
                error_result = Result(success=False, error_message=error,
                                      data=file_path)
                break

        out_file.close()
        shutil.rmtree(tmp_folder)

        if error_result:
            self.cancel_upload(upload_init_result.Slots, op_code)
            if callback:
                callback(error_result)
            result_queue.put(error_result)
            return error_result

        upload_date = datetime.datetime.now()
        end_time = upload_date + datetime.timedelta(hours=7 * 24)
        file_name = os.path.basename(file_path)
        slots = []
        for slot in upload_init_result.Slots:
            slots.append({
                'BaseUUID': slot.BaseUUID,
                'UUID': slot.UUID,
                'StorageService': slot.StorageService,
                'Address': slot.Address,
                'Size': slot.Size,
                'SizeRL': slot.SizeRL,
                'StorageCode': slot.StorageCode,
                'userID': slot.userID})

        for recipient in recipients:
            tx_data = DataTransfer(
                SenderMasterAddress=sender.MasterAddress,
                ReceivedAddress=recipient,
                UUID=upload_init_result.BaseUUID,
                FileName=file_name,
                Size=out_file_info.st_size,
                Slots=slots,
                KeyAES=aes_key.decode("utf-8"),
                KeyHMAC=hmac_key.decode("utf-8"),
                Message=note,
                StorageCode=upload_init_result.StorageCode,
                Address=upload_init_result.Address,
                UploadDate=datetime_to_str(upload_date),
                EndTime=datetime_to_str(end_time),
                Typ=constants.TransferNormal)
            tx = create_transaction(
                constants.TX_TYPE_TRANSFER, sender.Key, recipient, tx_data)
            broadcast_result = blockchain.broadcast(tx)
            if broadcast_result.success is False:
                error_result = Result(success=False, error_message='The transfer is not published on the blockchain.') # noqa
                self.cancel_upload(upload_init_result.Slots, op_code)
                if callback:
                    callback(error_result)
                result_queue.put(error_result)
                return error_result

        tx_data = DataTransfer(
            UUID=upload_init_result.BaseUUID,
            FileName=file_name,
            Size=out_file_info.st_size,
            Slots=slots,
            KeyAES=aes_key.decode("utf-8"),
            KeyHMAC=hmac_key.decode("utf-8"),
            Message=note,
            StorageCode=upload_init_result.StorageCode,
            Address=upload_init_result.Address,
            UploadDate=datetime_to_str(upload_date),
            EndTime=datetime_to_str(end_time),
            ReceivedAddress=recipients[0],
            ReceivedAddresses=recipients,
            Typ=constants.TransferSent)
        tx = create_transaction(
            constants.TX_TYPE_TRANSFER, sender.Key, sender.Key['Address'],
            tx_data)
        broadcast_result = blockchain.broadcast(tx)
        if broadcast_result.success is False:
            self.cancel_upload(upload_init_result.Slots, op_code)
            error_result = Result(success=False, error_message='The transfer is not published on the blockchain.') # noqa
            self.cancel_upload(upload_init_result.Slots, op_code)
            if callback:
                callback(error_result)
            result_queue.put(error_result)
            return error_result

        transfer_sent = TransferSent(
            filename=os.path.basename(file_path),
            uuid=upload_init_result.BaseUUID,
            txId="",
            senderAddress=sender.Key['Address'],
            senderMasterAddress=sender.MasterAddress,
            ReceivedAddress=recipients[0],
            receivedAddresses=recipients,
            size=out_file_info.st_size,
            uploadDate=datetime_to_str(upload_date),
            endTime=datetime_to_str(end_time),
            keyAES=aes_key.decode("utf-8"),
            KeyHMAC=hmac_key.decode("utf-8"),
            address=upload_init_result.Address,
            storage_code=upload_init_result.StorageCode,
            slots=slots)
        result = Result(success=True, data=transfer_sent)
        if callback:
            callback(result)
        result_queue.put(result)
        return result

    def prepare_slot_upload_request(
            self, session_id, out_file, slot,
            is_last_slot, file_stat, tweezers):

        '''
        Generate UploadV3Request payloads

        Parameters:

           session_id:
               pb.TransferInitResponse.SessionID

           out_file:
               opened file object

           slot:
               pb.UploadSlot

           is_last_slot:
               bool

           file_stat:
               target file stat. os.stat

           tweezers:
               dict. total_write key is required

        Returns:
           Generator

        Example:
            -
        '''
        chunk_size = constants.UPLOAD_CHUNK_SIZE

        slot_upload_size = 0
        total_read = 0
        buff_size = chunk_size
        while True:
            if total_read + chunk_size > slot.Size:
                if is_last_slot:
                    buff_size = file_stat.st_size - tweezers['total_write']
                else:
                    buff_size = slot.Size - total_read

            data = out_file.read(buff_size)
            if not data:
                break

            total_read += buff_size
            tweezers['total_write'] += buff_size
            slot_upload_size += buff_size
            payload = pb.UploadV3Request(
                Chunk=data,
                Slot=slot,
                LastSlot=is_last_slot,
            )

            yield payload
            if total_read >= slot.Size:
                total_read = 0
                break

    def cancel_upload(self, slots, op_code):
        '''
        Cancel Upload

        Parameters:
           slots:
               list of pb.UploadSlot

           op_code:
               pb.UploadOpCode.<Transfer|Storage>

        Returns:
            Result object

        Example:
            -
        ````
        from transferchain.client import TransferChain
        from transferchain.transfer import Transfer
        from transferchain.config import create_config
        from transferchain.protobuf import service_pb2 as pb
        config = create_config()
        tc = TransferChain(config)
        tc.add_master_user()
        user_info_result = tc.add_user()
        user = user_info_result.data

        sender = user.random_address()

        transfer = Transfer(config)
        file_path = '/tmp/your-test-file'

        transfer_result = transfer.upload(
            files=[file_path],
            sender=sender,
            recipient_addresses=[sender.Key['Address']])
        slots = transfer_result.data[0].data.slots
        cancel_result = transfer.cancel_upload(slots, pb.UploadOpCode.Transfer)
        ````
        '''

        grpc_client = get_client()
        meta_data = [
            ("user-id", str(self.config.user_id)),
            ("user-api-token", self.config.api_token),
            ("user-api-secret", self.config.api_secret)
        ]
        for slot_dict in slots:
            slot = pb.UploadSlot(
                UUID=slot_dict.get('UUID'),
                BaseUUID=slot_dict.get('BaseUUID'),
                StorageService=slot_dict.get('StorageService'),
                Address=slot_dict.get('Address'),
                Size=slot_dict.get('Size'),
                SizeRL=slot_dict.get('SizeRL'),
                StorageCode=slot_dict.get('StorageCode'),
                userID=slot_dict.get('userID'))
            try:
                grpc_client.DeleteV2(pb.DeleteRequest(
                    uuid=slot.UUID,
                    StorageCode=slot.StorageCode,
                    WalletID=self.config.wallet_id,
                    slot=slot,
                    opCode=op_code,
                    UserID=self.config.user_id
                ), metadata=meta_data)
            except grpc.RpcError as e:
                error_message = 'cancel upload error:{}'.format(e.details())
                return Result(success=False, error_message=error_message)
        return Result(success=True)
