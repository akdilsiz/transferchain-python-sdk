import os
import uuid
import shutil
import tempfile
import queue
import threading
import grpc
from transferchain import constants
from transferchain.datastructures import Result
from transferchain.crypt import crypt
from transferchain.grpc_client import get_client
from transferchain.protobuf import service_pb2 as pb


class Transfer(object):

    def __init__(self, config):
        self.config = config

    def delete(self):
        pass

    def download(self):
        pass

    def transfer_file(self, files, sender_address,
                      recipient_addresses, note, callback=None):
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
                target=self.upload, args=(
                    pb.UploadOpCode.Transfer,
                    init_result.SessionID,
                    init_result.BaseUUIDs,
                    transfer_process_uuid,
                    sender_address,
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

    def upload(self, op_code, session_id, base_uuid_map, process_uuid,
               sender, recipients, note, file_path, callback, result_queue):

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
        upload_init_request = pb.UploadInitRequest(
            sessionID=session_id,
            fileName=file_path,
            fileSize=out_file_info.st_size,
            opCode=pb.UploadOpCode.Transfer,
            userID=self.config.user_id,
            walletID=self.config.wallet_id,
            DeleteAfter=7 * 24,
            recipientCount=len(recipients),
            transferOpCode=pb.TransferOpCode.Normal,
            senderAddress=sender
        )
        upload_init_result = grpc_client.UploadInitV2(
            upload_init_request,
            metadata=meta_data)

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
            result = error_result
        else:
            result = Result(success=True, data={
                'file_path': file_path,
                'slots': upload_init_result.Slots
            })

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
        for slot in slots:
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
