import os
import uuid
import shutil
import tempfile
import queue
import threading
import datetime
import grpc
from transferchain import constants
from transferchain import blockchain
from transferchain.utils import datetime_to_str
from transferchain.crypt import crypt
from transferchain.datastructures import (
    Result, DataTransfer, TransferSent, TransferDelete)
from transferchain.grpc_client import get_client
from transferchain.protobuf import service_pb2 as pb
from transferchain.transaction import create_transaction


class Transfer(object):

    def __init__(self, config):
        self.config = config

    def delete_received_transfer(self, user_first_address,
                                 user_second_address, tx_data):
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
            error_message = 'cancel upload error:{}'.format(e.details())
            result = Result(success=False, error_message=error_message)
        result_queue.put(result)
        return result

    def delete_sent_transfer(self, user_first_address,
                             user_second_address, transfer_sent_obj):
        result_queue = queue.Queue()
        threads = []
        print('marco')
        for slot_dict in transfer_sent_obj.slots:
            t = threading.Thread(
                target=self._delete_slot, args=(slot_dict, result_queue))
            threads.append(t)

        for t in threads:
            t.start()

        for t in threads:
            t.join()
        print('polo')
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

    def download(self, user_id, typ, transfer, destination):
        pass

    def upload(self, files, sender, recipient_addresses, note, callback=None):
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
                    paths=files
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
                grpc_client.Delete(pb.DeleteRequest(
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
