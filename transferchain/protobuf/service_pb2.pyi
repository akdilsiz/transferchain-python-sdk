from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UploadOpCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    Transfer: _ClassVar[UploadOpCode]
    Upload: _ClassVar[UploadOpCode]
    Backup: _ClassVar[UploadOpCode]
    Storage: _ClassVar[UploadOpCode]
    StorageUpload: _ClassVar[UploadOpCode]
    Share: _ClassVar[UploadOpCode]
    Requests: _ClassVar[UploadOpCode]
    NonTransfer: _ClassVar[UploadOpCode]

class TransferOpCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    Normal: _ClassVar[TransferOpCode]
    Sent: _ClassVar[TransferOpCode]
    Non: _ClassVar[TransferOpCode]

class BackupOpCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    DB: _ClassVar[BackupOpCode]

class TransferStatusCodes(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    TransferParameter: _ClassVar[TransferStatusCodes]
    TransferPackageNotFound: _ClassVar[TransferStatusCodes]
    TransferRecipientCount: _ClassVar[TransferStatusCodes]
    TransferLimit: _ClassVar[TransferStatusCodes]
    TransferProviderNotFound: _ClassVar[TransferStatusCodes]
    TransferOK: _ClassVar[TransferStatusCodes]
    TransferNotFound: _ClassVar[TransferStatusCodes]
    TransferInternal: _ClassVar[TransferStatusCodes]

class StorageStatusCodes(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    StorageParameter: _ClassVar[StorageStatusCodes]
    StoragePackageNotFound: _ClassVar[StorageStatusCodes]
    StorageLimit: _ClassVar[StorageStatusCodes]
    StorageProviderNotFound: _ClassVar[StorageStatusCodes]
    StorageOK: _ClassVar[StorageStatusCodes]
    StorageNotFound: _ClassVar[StorageStatusCodes]
    StorageInternal: _ClassVar[StorageStatusCodes]

class UploadStatusCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    Unknown: _ClassVar[UploadStatusCode]
    Ok: _ClassVar[UploadStatusCode]
    Failed: _ClassVar[UploadStatusCode]

class DeleteStatusCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    NotFound: _ClassVar[DeleteStatusCode]
    Deleted: _ClassVar[DeleteStatusCode]
    Fail: _ClassVar[DeleteStatusCode]

class Policy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    Owner: _ClassVar[Policy]
    Write: _ClassVar[Policy]
    Read: _ClassVar[Policy]
    Preview: _ClassVar[Policy]
Transfer: UploadOpCode
Upload: UploadOpCode
Backup: UploadOpCode
Storage: UploadOpCode
StorageUpload: UploadOpCode
Share: UploadOpCode
Requests: UploadOpCode
NonTransfer: UploadOpCode
Normal: TransferOpCode
Sent: TransferOpCode
Non: TransferOpCode
DB: BackupOpCode
TransferParameter: TransferStatusCodes
TransferPackageNotFound: TransferStatusCodes
TransferRecipientCount: TransferStatusCodes
TransferLimit: TransferStatusCodes
TransferProviderNotFound: TransferStatusCodes
TransferOK: TransferStatusCodes
TransferNotFound: TransferStatusCodes
TransferInternal: TransferStatusCodes
StorageParameter: StorageStatusCodes
StoragePackageNotFound: StorageStatusCodes
StorageLimit: StorageStatusCodes
StorageProviderNotFound: StorageStatusCodes
StorageOK: StorageStatusCodes
StorageNotFound: StorageStatusCodes
StorageInternal: StorageStatusCodes
Unknown: UploadStatusCode
Ok: UploadStatusCode
Failed: UploadStatusCode
NotFound: DeleteStatusCode
Deleted: DeleteStatusCode
Fail: DeleteStatusCode
Owner: Policy
Write: Policy
Read: Policy
Preview: Policy

class MessageRequest(_message.Message):
    __slots__ = ["WalletUUID", "UserID", "WalletID", "JWT"]
    WALLETUUID_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    WALLETID_FIELD_NUMBER: _ClassVar[int]
    JWT_FIELD_NUMBER: _ClassVar[int]
    WalletUUID: str
    UserID: int
    WalletID: int
    JWT: str
    def __init__(self, WalletUUID: _Optional[str] = ..., UserID: _Optional[int] = ..., WalletID: _Optional[int] = ..., JWT: _Optional[str] = ...) -> None: ...

class MessageResponse(_message.Message):
    __slots__ = ["statusCode"]
    STATUSCODE_FIELD_NUMBER: _ClassVar[int]
    statusCode: UploadStatusCode
    def __init__(self, statusCode: _Optional[_Union[UploadStatusCode, str]] = ...) -> None: ...

class TransferToUploadRequest(_message.Message):
    __slots__ = ["UUID", "UserID", "Slots", "JWT"]
    UUID_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    SLOTS_FIELD_NUMBER: _ClassVar[int]
    JWT_FIELD_NUMBER: _ClassVar[int]
    UUID: str
    UserID: int
    Slots: _containers.RepeatedCompositeFieldContainer[UploadSlot]
    JWT: str
    def __init__(self, UUID: _Optional[str] = ..., UserID: _Optional[int] = ..., Slots: _Optional[_Iterable[_Union[UploadSlot, _Mapping]]] = ..., JWT: _Optional[str] = ...) -> None: ...

class TransferToStorageRequest(_message.Message):
    __slots__ = ["UUID", "UserID", "Slots", "JWT"]
    UUID_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    SLOTS_FIELD_NUMBER: _ClassVar[int]
    JWT_FIELD_NUMBER: _ClassVar[int]
    UUID: str
    UserID: int
    Slots: _containers.RepeatedCompositeFieldContainer[UploadSlot]
    JWT: str
    def __init__(self, UUID: _Optional[str] = ..., UserID: _Optional[int] = ..., Slots: _Optional[_Iterable[_Union[UploadSlot, _Mapping]]] = ..., JWT: _Optional[str] = ...) -> None: ...

class TransferInitRequest(_message.Message):
    __slots__ = ["files", "totalSize", "opCode", "userID", "walletID", "recipientCount", "transferOpCode", "emails", "notes", "sourceEmail", "UID", "paths", "Non2Non", "NonUID", "URLFlag", "DeleteAfter", "JWT"]
    FILES_FIELD_NUMBER: _ClassVar[int]
    TOTALSIZE_FIELD_NUMBER: _ClassVar[int]
    OPCODE_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    WALLETID_FIELD_NUMBER: _ClassVar[int]
    RECIPIENTCOUNT_FIELD_NUMBER: _ClassVar[int]
    TRANSFEROPCODE_FIELD_NUMBER: _ClassVar[int]
    EMAILS_FIELD_NUMBER: _ClassVar[int]
    NOTES_FIELD_NUMBER: _ClassVar[int]
    SOURCEEMAIL_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    PATHS_FIELD_NUMBER: _ClassVar[int]
    NON2NON_FIELD_NUMBER: _ClassVar[int]
    NONUID_FIELD_NUMBER: _ClassVar[int]
    URLFLAG_FIELD_NUMBER: _ClassVar[int]
    DELETEAFTER_FIELD_NUMBER: _ClassVar[int]
    JWT_FIELD_NUMBER: _ClassVar[int]
    files: _containers.RepeatedScalarFieldContainer[str]
    totalSize: int
    opCode: UploadOpCode
    userID: int
    walletID: int
    recipientCount: int
    transferOpCode: TransferOpCode
    emails: _containers.RepeatedScalarFieldContainer[str]
    notes: str
    sourceEmail: str
    UID: str
    paths: _containers.RepeatedScalarFieldContainer[str]
    Non2Non: bool
    NonUID: str
    URLFlag: bool
    DeleteAfter: int
    JWT: str
    def __init__(self, files: _Optional[_Iterable[str]] = ..., totalSize: _Optional[int] = ..., opCode: _Optional[_Union[UploadOpCode, str]] = ..., userID: _Optional[int] = ..., walletID: _Optional[int] = ..., recipientCount: _Optional[int] = ..., transferOpCode: _Optional[_Union[TransferOpCode, str]] = ..., emails: _Optional[_Iterable[str]] = ..., notes: _Optional[str] = ..., sourceEmail: _Optional[str] = ..., UID: _Optional[str] = ..., paths: _Optional[_Iterable[str]] = ..., Non2Non: bool = ..., NonUID: _Optional[str] = ..., URLFlag: bool = ..., DeleteAfter: _Optional[int] = ..., JWT: _Optional[str] = ...) -> None: ...

class TransferInitResponse(_message.Message):
    __slots__ = ["SessionID", "BaseUUIDs", "UID", "Address", "UserID", "errorCode", "errorMessage"]
    class BaseUUIDsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    SESSIONID_FIELD_NUMBER: _ClassVar[int]
    BASEUUIDS_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    ERRORCODE_FIELD_NUMBER: _ClassVar[int]
    ERRORMESSAGE_FIELD_NUMBER: _ClassVar[int]
    SessionID: str
    BaseUUIDs: _containers.ScalarMap[str, str]
    UID: str
    Address: str
    UserID: int
    errorCode: TransferStatusCodes
    errorMessage: str
    def __init__(self, SessionID: _Optional[str] = ..., BaseUUIDs: _Optional[_Mapping[str, str]] = ..., UID: _Optional[str] = ..., Address: _Optional[str] = ..., UserID: _Optional[int] = ..., errorCode: _Optional[_Union[TransferStatusCodes, str]] = ..., errorMessage: _Optional[str] = ...) -> None: ...

class TransferFinishRequest(_message.Message):
    __slots__ = ["SessionID", "UserID", "WalletID", "Passkey", "Canceled", "Files", "TotalSize", "JWT"]
    SESSIONID_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    WALLETID_FIELD_NUMBER: _ClassVar[int]
    PASSKEY_FIELD_NUMBER: _ClassVar[int]
    CANCELED_FIELD_NUMBER: _ClassVar[int]
    FILES_FIELD_NUMBER: _ClassVar[int]
    TOTALSIZE_FIELD_NUMBER: _ClassVar[int]
    JWT_FIELD_NUMBER: _ClassVar[int]
    SessionID: str
    UserID: int
    WalletID: int
    Passkey: str
    Canceled: bool
    Files: _containers.RepeatedScalarFieldContainer[str]
    TotalSize: int
    JWT: str
    def __init__(self, SessionID: _Optional[str] = ..., UserID: _Optional[int] = ..., WalletID: _Optional[int] = ..., Passkey: _Optional[str] = ..., Canceled: bool = ..., Files: _Optional[_Iterable[str]] = ..., TotalSize: _Optional[int] = ..., JWT: _Optional[str] = ...) -> None: ...

class TransferFinishResponse(_message.Message):
    __slots__ = ["Code", "URL"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    Code: TransferStatusCodes
    URL: str
    def __init__(self, Code: _Optional[_Union[TransferStatusCodes, str]] = ..., URL: _Optional[str] = ...) -> None: ...

class TransferRequest(_message.Message):
    __slots__ = ["SessionID", "Offset", "Chunk", "Slot", "JWT"]
    SESSIONID_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    CHUNK_FIELD_NUMBER: _ClassVar[int]
    SLOT_FIELD_NUMBER: _ClassVar[int]
    JWT_FIELD_NUMBER: _ClassVar[int]
    SessionID: str
    Offset: int
    Chunk: bytes
    Slot: UploadSlot
    JWT: str
    def __init__(self, SessionID: _Optional[str] = ..., Offset: _Optional[int] = ..., Chunk: _Optional[bytes] = ..., Slot: _Optional[_Union[UploadSlot, _Mapping]] = ..., JWT: _Optional[str] = ...) -> None: ...

class TransferResponse(_message.Message):
    __slots__ = ["StatusCode"]
    STATUSCODE_FIELD_NUMBER: _ClassVar[int]
    StatusCode: UploadStatusCode
    def __init__(self, StatusCode: _Optional[_Union[UploadStatusCode, str]] = ...) -> None: ...

class UploadInitRequest(_message.Message):
    __slots__ = ["sessionID", "fileName", "senderAddress", "fileSize", "opCode", "userID", "walletID", "DeleteAfter", "recipientCount", "transferOpCode", "Non2Non", "DownloadLimit", "JWT", "RoomID", "Owner", "PolicyID"]
    SESSIONID_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    SENDERADDRESS_FIELD_NUMBER: _ClassVar[int]
    FILESIZE_FIELD_NUMBER: _ClassVar[int]
    OPCODE_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    WALLETID_FIELD_NUMBER: _ClassVar[int]
    DELETEAFTER_FIELD_NUMBER: _ClassVar[int]
    RECIPIENTCOUNT_FIELD_NUMBER: _ClassVar[int]
    TRANSFEROPCODE_FIELD_NUMBER: _ClassVar[int]
    NON2NON_FIELD_NUMBER: _ClassVar[int]
    DOWNLOADLIMIT_FIELD_NUMBER: _ClassVar[int]
    JWT_FIELD_NUMBER: _ClassVar[int]
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    POLICYID_FIELD_NUMBER: _ClassVar[int]
    sessionID: str
    fileName: str
    senderAddress: str
    fileSize: int
    opCode: UploadOpCode
    userID: int
    walletID: int
    DeleteAfter: int
    recipientCount: int
    transferOpCode: TransferOpCode
    Non2Non: bool
    DownloadLimit: int
    JWT: str
    RoomID: str
    Owner: str
    PolicyID: str
    def __init__(self, sessionID: _Optional[str] = ..., fileName: _Optional[str] = ..., senderAddress: _Optional[str] = ..., fileSize: _Optional[int] = ..., opCode: _Optional[_Union[UploadOpCode, str]] = ..., userID: _Optional[int] = ..., walletID: _Optional[int] = ..., DeleteAfter: _Optional[int] = ..., recipientCount: _Optional[int] = ..., transferOpCode: _Optional[_Union[TransferOpCode, str]] = ..., Non2Non: bool = ..., DownloadLimit: _Optional[int] = ..., JWT: _Optional[str] = ..., RoomID: _Optional[str] = ..., Owner: _Optional[str] = ..., PolicyID: _Optional[str] = ...) -> None: ...

class UploadSlot(_message.Message):
    __slots__ = ["BaseUUID", "UUID", "StorageService", "Address", "Size", "SizeRL", "ProvData", "Data", "UploadData", "StorageCode", "userID", "LastPartSize", "Storage", "ChunkSize"]
    BASEUUID_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    STORAGESERVICE_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    SIZERL_FIELD_NUMBER: _ClassVar[int]
    PROVDATA_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    UPLOADDATA_FIELD_NUMBER: _ClassVar[int]
    STORAGECODE_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    LASTPARTSIZE_FIELD_NUMBER: _ClassVar[int]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    CHUNKSIZE_FIELD_NUMBER: _ClassVar[int]
    BaseUUID: str
    UUID: str
    StorageService: str
    Address: str
    Size: int
    SizeRL: int
    ProvData: bytes
    Data: bytes
    UploadData: bytes
    StorageCode: str
    userID: int
    LastPartSize: int
    Storage: bytes
    ChunkSize: int
    def __init__(self, BaseUUID: _Optional[str] = ..., UUID: _Optional[str] = ..., StorageService: _Optional[str] = ..., Address: _Optional[str] = ..., Size: _Optional[int] = ..., SizeRL: _Optional[int] = ..., ProvData: _Optional[bytes] = ..., Data: _Optional[bytes] = ..., UploadData: _Optional[bytes] = ..., StorageCode: _Optional[str] = ..., userID: _Optional[int] = ..., LastPartSize: _Optional[int] = ..., Storage: _Optional[bytes] = ..., ChunkSize: _Optional[int] = ...) -> None: ...

class UploadInitResponse(_message.Message):
    __slots__ = ["UUID", "Slots", "One", "Address", "UploadData", "Data", "BaseUUID", "StorageService", "StorageCode", "UserID", "errorCode", "errorMessage", "TxsID", "Extra"]
    UUID_FIELD_NUMBER: _ClassVar[int]
    SLOTS_FIELD_NUMBER: _ClassVar[int]
    ONE_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    UPLOADDATA_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    BASEUUID_FIELD_NUMBER: _ClassVar[int]
    STORAGESERVICE_FIELD_NUMBER: _ClassVar[int]
    STORAGECODE_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    ERRORCODE_FIELD_NUMBER: _ClassVar[int]
    ERRORMESSAGE_FIELD_NUMBER: _ClassVar[int]
    TXSID_FIELD_NUMBER: _ClassVar[int]
    EXTRA_FIELD_NUMBER: _ClassVar[int]
    UUID: str
    Slots: _containers.RepeatedCompositeFieldContainer[UploadSlot]
    One: bool
    Address: str
    UploadData: bytes
    Data: bytes
    BaseUUID: str
    StorageService: str
    StorageCode: str
    UserID: int
    errorCode: int
    errorMessage: str
    TxsID: int
    Extra: bytes
    def __init__(self, UUID: _Optional[str] = ..., Slots: _Optional[_Iterable[_Union[UploadSlot, _Mapping]]] = ..., One: bool = ..., Address: _Optional[str] = ..., UploadData: _Optional[bytes] = ..., Data: _Optional[bytes] = ..., BaseUUID: _Optional[str] = ..., StorageService: _Optional[str] = ..., StorageCode: _Optional[str] = ..., UserID: _Optional[int] = ..., errorCode: _Optional[int] = ..., errorMessage: _Optional[str] = ..., TxsID: _Optional[int] = ..., Extra: _Optional[bytes] = ...) -> None: ...

class UploadRequest(_message.Message):
    __slots__ = ["chunk", "SessionID"]
    CHUNK_FIELD_NUMBER: _ClassVar[int]
    SESSIONID_FIELD_NUMBER: _ClassVar[int]
    chunk: bytes
    SessionID: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, chunk: _Optional[bytes] = ..., SessionID: _Optional[_Iterable[str]] = ...) -> None: ...

class UploadResponse(_message.Message):
    __slots__ = ["statusCode"]
    STATUSCODE_FIELD_NUMBER: _ClassVar[int]
    statusCode: UploadStatusCode
    def __init__(self, statusCode: _Optional[_Union[UploadStatusCode, str]] = ...) -> None: ...

class RequestsCreateRequest(_message.Message):
    __slots__ = ["UserID", "UUID", "Expire", "JWT"]
    USERID_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    EXPIRE_FIELD_NUMBER: _ClassVar[int]
    JWT_FIELD_NUMBER: _ClassVar[int]
    UserID: int
    UUID: str
    Expire: str
    JWT: str
    def __init__(self, UserID: _Optional[int] = ..., UUID: _Optional[str] = ..., Expire: _Optional[str] = ..., JWT: _Optional[str] = ...) -> None: ...

class RequestsUpdateRequest(_message.Message):
    __slots__ = ["UserID", "UUID", "Expire", "JWT"]
    USERID_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    EXPIRE_FIELD_NUMBER: _ClassVar[int]
    JWT_FIELD_NUMBER: _ClassVar[int]
    UserID: int
    UUID: str
    Expire: str
    JWT: str
    def __init__(self, UserID: _Optional[int] = ..., UUID: _Optional[str] = ..., Expire: _Optional[str] = ..., JWT: _Optional[str] = ...) -> None: ...

class RequestsResponse(_message.Message):
    __slots__ = ["ErrorCode", "ErrorMessage"]
    ERRORCODE_FIELD_NUMBER: _ClassVar[int]
    ERRORMESSAGE_FIELD_NUMBER: _ClassVar[int]
    ErrorCode: int
    ErrorMessage: str
    def __init__(self, ErrorCode: _Optional[int] = ..., ErrorMessage: _Optional[str] = ...) -> None: ...

class StorageInitRequest(_message.Message):
    __slots__ = ["TotalSize", "Paths", "OpCode", "UserID", "WalletID", "notes", "UID", "Requests", "RequestsUUID", "Expire", "JWT", "RoomID", "Owner", "PolicyID"]
    TOTALSIZE_FIELD_NUMBER: _ClassVar[int]
    PATHS_FIELD_NUMBER: _ClassVar[int]
    OPCODE_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    WALLETID_FIELD_NUMBER: _ClassVar[int]
    NOTES_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    REQUESTS_FIELD_NUMBER: _ClassVar[int]
    REQUESTSUUID_FIELD_NUMBER: _ClassVar[int]
    EXPIRE_FIELD_NUMBER: _ClassVar[int]
    JWT_FIELD_NUMBER: _ClassVar[int]
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    POLICYID_FIELD_NUMBER: _ClassVar[int]
    TotalSize: int
    Paths: _containers.RepeatedScalarFieldContainer[str]
    OpCode: UploadOpCode
    UserID: int
    WalletID: int
    notes: str
    UID: str
    Requests: bool
    RequestsUUID: str
    Expire: str
    JWT: str
    RoomID: str
    Owner: str
    PolicyID: str
    def __init__(self, TotalSize: _Optional[int] = ..., Paths: _Optional[_Iterable[str]] = ..., OpCode: _Optional[_Union[UploadOpCode, str]] = ..., UserID: _Optional[int] = ..., WalletID: _Optional[int] = ..., notes: _Optional[str] = ..., UID: _Optional[str] = ..., Requests: bool = ..., RequestsUUID: _Optional[str] = ..., Expire: _Optional[str] = ..., JWT: _Optional[str] = ..., RoomID: _Optional[str] = ..., Owner: _Optional[str] = ..., PolicyID: _Optional[str] = ...) -> None: ...

class StorageInitResponse(_message.Message):
    __slots__ = ["SessionID", "BaseUUIDs", "UID", "Address", "UserID", "ErrorCode", "ErrorMessage"]
    class BaseUUIDsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    SESSIONID_FIELD_NUMBER: _ClassVar[int]
    BASEUUIDS_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    ERRORCODE_FIELD_NUMBER: _ClassVar[int]
    ERRORMESSAGE_FIELD_NUMBER: _ClassVar[int]
    SessionID: str
    BaseUUIDs: _containers.ScalarMap[str, str]
    UID: str
    Address: str
    UserID: int
    ErrorCode: StorageStatusCodes
    ErrorMessage: str
    def __init__(self, SessionID: _Optional[str] = ..., BaseUUIDs: _Optional[_Mapping[str, str]] = ..., UID: _Optional[str] = ..., Address: _Optional[str] = ..., UserID: _Optional[int] = ..., ErrorCode: _Optional[_Union[StorageStatusCodes, str]] = ..., ErrorMessage: _Optional[str] = ...) -> None: ...

class StorageFinishRequest(_message.Message):
    __slots__ = ["SessionID", "UserID", "WalletID", "opCode", "JWT"]
    SESSIONID_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    WALLETID_FIELD_NUMBER: _ClassVar[int]
    OPCODE_FIELD_NUMBER: _ClassVar[int]
    JWT_FIELD_NUMBER: _ClassVar[int]
    SessionID: str
    UserID: int
    WalletID: int
    opCode: UploadOpCode
    JWT: str
    def __init__(self, SessionID: _Optional[str] = ..., UserID: _Optional[int] = ..., WalletID: _Optional[int] = ..., opCode: _Optional[_Union[UploadOpCode, str]] = ..., JWT: _Optional[str] = ...) -> None: ...

class UploadV3Request(_message.Message):
    __slots__ = ["SessionID", "Offset", "Chunk", "Slot", "LastSlot", "CloseSession", "Progress", "ProcessUUID"]
    SESSIONID_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    CHUNK_FIELD_NUMBER: _ClassVar[int]
    SLOT_FIELD_NUMBER: _ClassVar[int]
    LASTSLOT_FIELD_NUMBER: _ClassVar[int]
    CLOSESESSION_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    PROCESSUUID_FIELD_NUMBER: _ClassVar[int]
    SessionID: str
    Offset: int
    Chunk: bytes
    Slot: UploadSlot
    LastSlot: bool
    CloseSession: bool
    Progress: int
    ProcessUUID: str
    def __init__(self, SessionID: _Optional[str] = ..., Offset: _Optional[int] = ..., Chunk: _Optional[bytes] = ..., Slot: _Optional[_Union[UploadSlot, _Mapping]] = ..., LastSlot: bool = ..., CloseSession: bool = ..., Progress: _Optional[int] = ..., ProcessUUID: _Optional[str] = ...) -> None: ...

class StorageResponse(_message.Message):
    __slots__ = ["Code"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    Code: UploadStatusCode
    def __init__(self, Code: _Optional[_Union[UploadStatusCode, str]] = ...) -> None: ...

class StorageFinishResponse(_message.Message):
    __slots__ = ["Code"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    Code: StorageStatusCodes
    def __init__(self, Code: _Optional[_Union[StorageStatusCodes, str]] = ...) -> None: ...

class DownloadRequest(_message.Message):
    __slots__ = ["pubKey", "uuid", "Slots", "StorageCode", "WalletID", "UserID", "opCode", "JWT", "RoomID", "Owner", "PolicyID"]
    PUBKEY_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    SLOTS_FIELD_NUMBER: _ClassVar[int]
    STORAGECODE_FIELD_NUMBER: _ClassVar[int]
    WALLETID_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    OPCODE_FIELD_NUMBER: _ClassVar[int]
    JWT_FIELD_NUMBER: _ClassVar[int]
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    POLICYID_FIELD_NUMBER: _ClassVar[int]
    pubKey: str
    uuid: str
    Slots: _containers.RepeatedCompositeFieldContainer[UploadSlot]
    StorageCode: str
    WalletID: int
    UserID: int
    opCode: UploadOpCode
    JWT: str
    RoomID: str
    Owner: str
    PolicyID: str
    def __init__(self, pubKey: _Optional[str] = ..., uuid: _Optional[str] = ..., Slots: _Optional[_Iterable[_Union[UploadSlot, _Mapping]]] = ..., StorageCode: _Optional[str] = ..., WalletID: _Optional[int] = ..., UserID: _Optional[int] = ..., opCode: _Optional[_Union[UploadOpCode, str]] = ..., JWT: _Optional[str] = ..., RoomID: _Optional[str] = ..., Owner: _Optional[str] = ..., PolicyID: _Optional[str] = ...) -> None: ...

class DownloadV2Request(_message.Message):
    __slots__ = ["pubKey", "uuid", "Slot", "StorageCode", "WalletID", "UserID", "opCode", "Non", "Last", "JWT", "RoomID", "Owner", "PolicyID"]
    PUBKEY_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    SLOT_FIELD_NUMBER: _ClassVar[int]
    STORAGECODE_FIELD_NUMBER: _ClassVar[int]
    WALLETID_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    OPCODE_FIELD_NUMBER: _ClassVar[int]
    NON_FIELD_NUMBER: _ClassVar[int]
    LAST_FIELD_NUMBER: _ClassVar[int]
    JWT_FIELD_NUMBER: _ClassVar[int]
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    POLICYID_FIELD_NUMBER: _ClassVar[int]
    pubKey: str
    uuid: str
    Slot: UploadSlot
    StorageCode: str
    WalletID: int
    UserID: int
    opCode: UploadOpCode
    Non: bool
    Last: bool
    JWT: str
    RoomID: str
    Owner: str
    PolicyID: str
    def __init__(self, pubKey: _Optional[str] = ..., uuid: _Optional[str] = ..., Slot: _Optional[_Union[UploadSlot, _Mapping]] = ..., StorageCode: _Optional[str] = ..., WalletID: _Optional[int] = ..., UserID: _Optional[int] = ..., opCode: _Optional[_Union[UploadOpCode, str]] = ..., Non: bool = ..., Last: bool = ..., JWT: _Optional[str] = ..., RoomID: _Optional[str] = ..., Owner: _Optional[str] = ..., PolicyID: _Optional[str] = ...) -> None: ...

class DownloadV4Request(_message.Message):
    __slots__ = ["Slot", "StorageCode", "WalletID", "UserID", "OpCode", "Non", "Last", "Seek", "ChunkSize", "JWT", "RoomID", "Owner", "PolicyID"]
    SLOT_FIELD_NUMBER: _ClassVar[int]
    STORAGECODE_FIELD_NUMBER: _ClassVar[int]
    WALLETID_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    OPCODE_FIELD_NUMBER: _ClassVar[int]
    NON_FIELD_NUMBER: _ClassVar[int]
    LAST_FIELD_NUMBER: _ClassVar[int]
    SEEK_FIELD_NUMBER: _ClassVar[int]
    CHUNKSIZE_FIELD_NUMBER: _ClassVar[int]
    JWT_FIELD_NUMBER: _ClassVar[int]
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    POLICYID_FIELD_NUMBER: _ClassVar[int]
    Slot: UploadSlot
    StorageCode: str
    WalletID: int
    UserID: int
    OpCode: UploadOpCode
    Non: bool
    Last: bool
    Seek: int
    ChunkSize: int
    JWT: str
    RoomID: str
    Owner: str
    PolicyID: str
    def __init__(self, Slot: _Optional[_Union[UploadSlot, _Mapping]] = ..., StorageCode: _Optional[str] = ..., WalletID: _Optional[int] = ..., UserID: _Optional[int] = ..., OpCode: _Optional[_Union[UploadOpCode, str]] = ..., Non: bool = ..., Last: bool = ..., Seek: _Optional[int] = ..., ChunkSize: _Optional[int] = ..., JWT: _Optional[str] = ..., RoomID: _Optional[str] = ..., Owner: _Optional[str] = ..., PolicyID: _Optional[str] = ...) -> None: ...

class DownloadResponse(_message.Message):
    __slots__ = ["chunk"]
    CHUNK_FIELD_NUMBER: _ClassVar[int]
    chunk: bytes
    def __init__(self, chunk: _Optional[bytes] = ...) -> None: ...

class DownloadV4Response(_message.Message):
    __slots__ = ["chunk", "ContentLength"]
    CHUNK_FIELD_NUMBER: _ClassVar[int]
    CONTENTLENGTH_FIELD_NUMBER: _ClassVar[int]
    chunk: bytes
    ContentLength: int
    def __init__(self, chunk: _Optional[bytes] = ..., ContentLength: _Optional[int] = ...) -> None: ...

class DownloadInfoRequest(_message.Message):
    __slots__ = ["BaseUUID", "JWT", "RoomID", "Owner", "PolicyID"]
    BASEUUID_FIELD_NUMBER: _ClassVar[int]
    JWT_FIELD_NUMBER: _ClassVar[int]
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    POLICYID_FIELD_NUMBER: _ClassVar[int]
    BaseUUID: str
    JWT: str
    RoomID: str
    Owner: str
    PolicyID: str
    def __init__(self, BaseUUID: _Optional[str] = ..., JWT: _Optional[str] = ..., RoomID: _Optional[str] = ..., Owner: _Optional[str] = ..., PolicyID: _Optional[str] = ...) -> None: ...

class DownloadInfoResponse(_message.Message):
    __slots__ = ["DownloadLimit", "RemainingDownloadLimit"]
    DOWNLOADLIMIT_FIELD_NUMBER: _ClassVar[int]
    REMAININGDOWNLOADLIMIT_FIELD_NUMBER: _ClassVar[int]
    DownloadLimit: int
    RemainingDownloadLimit: int
    def __init__(self, DownloadLimit: _Optional[int] = ..., RemainingDownloadLimit: _Optional[int] = ...) -> None: ...

class DeleteRequest(_message.Message):
    __slots__ = ["uuid", "StorageCode", "WalletID", "slot", "opCode", "UserID", "Cancel", "JWT", "RoomID", "Owner", "PolicyID"]
    UUID_FIELD_NUMBER: _ClassVar[int]
    STORAGECODE_FIELD_NUMBER: _ClassVar[int]
    WALLETID_FIELD_NUMBER: _ClassVar[int]
    SLOT_FIELD_NUMBER: _ClassVar[int]
    OPCODE_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    CANCEL_FIELD_NUMBER: _ClassVar[int]
    JWT_FIELD_NUMBER: _ClassVar[int]
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    POLICYID_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    StorageCode: str
    WalletID: int
    slot: UploadSlot
    opCode: UploadOpCode
    UserID: int
    Cancel: bool
    JWT: str
    RoomID: str
    Owner: str
    PolicyID: str
    def __init__(self, uuid: _Optional[str] = ..., StorageCode: _Optional[str] = ..., WalletID: _Optional[int] = ..., slot: _Optional[_Union[UploadSlot, _Mapping]] = ..., opCode: _Optional[_Union[UploadOpCode, str]] = ..., UserID: _Optional[int] = ..., Cancel: bool = ..., JWT: _Optional[str] = ..., RoomID: _Optional[str] = ..., Owner: _Optional[str] = ..., PolicyID: _Optional[str] = ...) -> None: ...

class DeleteV3Request(_message.Message):
    __slots__ = ["UserID", "WalletID", "Slots", "OpCode", "JWT", "RoomID", "Owner", "PolicyID"]
    USERID_FIELD_NUMBER: _ClassVar[int]
    WALLETID_FIELD_NUMBER: _ClassVar[int]
    SLOTS_FIELD_NUMBER: _ClassVar[int]
    OPCODE_FIELD_NUMBER: _ClassVar[int]
    JWT_FIELD_NUMBER: _ClassVar[int]
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    POLICYID_FIELD_NUMBER: _ClassVar[int]
    UserID: int
    WalletID: int
    Slots: _containers.RepeatedCompositeFieldContainer[UploadSlot]
    OpCode: UploadOpCode
    JWT: str
    RoomID: str
    Owner: str
    PolicyID: str
    def __init__(self, UserID: _Optional[int] = ..., WalletID: _Optional[int] = ..., Slots: _Optional[_Iterable[_Union[UploadSlot, _Mapping]]] = ..., OpCode: _Optional[_Union[UploadOpCode, str]] = ..., JWT: _Optional[str] = ..., RoomID: _Optional[str] = ..., Owner: _Optional[str] = ..., PolicyID: _Optional[str] = ...) -> None: ...

class DeleteResponse(_message.Message):
    __slots__ = ["statusCode"]
    STATUSCODE_FIELD_NUMBER: _ClassVar[int]
    statusCode: DeleteStatusCode
    def __init__(self, statusCode: _Optional[_Union[DeleteStatusCode, str]] = ...) -> None: ...

class DropAccountRequest(_message.Message):
    __slots__ = ["Token", "UserID", "JWT"]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    JWT_FIELD_NUMBER: _ClassVar[int]
    Token: str
    UserID: int
    JWT: str
    def __init__(self, Token: _Optional[str] = ..., UserID: _Optional[int] = ..., JWT: _Optional[str] = ...) -> None: ...

class DropAccountResponse(_message.Message):
    __slots__ = ["Success", "ErrorCode", "ErrorMessage"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERRORCODE_FIELD_NUMBER: _ClassVar[int]
    ERRORMESSAGE_FIELD_NUMBER: _ClassVar[int]
    Success: bool
    ErrorCode: int
    ErrorMessage: str
    def __init__(self, Success: bool = ..., ErrorCode: _Optional[int] = ..., ErrorMessage: _Optional[str] = ...) -> None: ...

class DataRoomPolicy(_message.Message):
    __slots__ = ["ID", "RoomID", "SourceIdentifier", "TargetIdentifier", "Policy", "CreatedAt"]
    ID_FIELD_NUMBER: _ClassVar[int]
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    SOURCEIDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    TARGETIDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    POLICY_FIELD_NUMBER: _ClassVar[int]
    CREATEDAT_FIELD_NUMBER: _ClassVar[int]
    ID: str
    RoomID: str
    SourceIdentifier: str
    TargetIdentifier: str
    Policy: Policy
    CreatedAt: _timestamp_pb2.Timestamp
    def __init__(self, ID: _Optional[str] = ..., RoomID: _Optional[str] = ..., SourceIdentifier: _Optional[str] = ..., TargetIdentifier: _Optional[str] = ..., Policy: _Optional[_Union[Policy, str]] = ..., CreatedAt: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class DataRoom(_message.Message):
    __slots__ = ["ID", "CompanyID", "UserID", "Identifier", "Owner", "CreatedAt", "Policies"]
    ID_FIELD_NUMBER: _ClassVar[int]
    COMPANYID_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    CREATEDAT_FIELD_NUMBER: _ClassVar[int]
    POLICIES_FIELD_NUMBER: _ClassVar[int]
    ID: str
    CompanyID: int
    UserID: int
    Identifier: str
    Owner: str
    CreatedAt: _timestamp_pb2.Timestamp
    Policies: _containers.RepeatedCompositeFieldContainer[DataRoomPolicy]
    def __init__(self, ID: _Optional[str] = ..., CompanyID: _Optional[int] = ..., UserID: _Optional[int] = ..., Identifier: _Optional[str] = ..., Owner: _Optional[str] = ..., CreatedAt: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., Policies: _Optional[_Iterable[_Union[DataRoomPolicy, _Mapping]]] = ...) -> None: ...

class DataRoomCreateRequest(_message.Message):
    __slots__ = ["DataRoom", "Policies", "JWT"]
    DATAROOM_FIELD_NUMBER: _ClassVar[int]
    POLICIES_FIELD_NUMBER: _ClassVar[int]
    JWT_FIELD_NUMBER: _ClassVar[int]
    DataRoom: DataRoom
    Policies: _containers.RepeatedCompositeFieldContainer[DataRoomPolicy]
    JWT: str
    def __init__(self, DataRoom: _Optional[_Union[DataRoom, _Mapping]] = ..., Policies: _Optional[_Iterable[_Union[DataRoomPolicy, _Mapping]]] = ..., JWT: _Optional[str] = ...) -> None: ...

class DataRoomCreateResponse(_message.Message):
    __slots__ = ["DataRoom", "Policies", "Success", "ErrorCode", "ErrorMessage"]
    DATAROOM_FIELD_NUMBER: _ClassVar[int]
    POLICIES_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERRORCODE_FIELD_NUMBER: _ClassVar[int]
    ERRORMESSAGE_FIELD_NUMBER: _ClassVar[int]
    DataRoom: DataRoom
    Policies: _containers.RepeatedCompositeFieldContainer[DataRoomPolicy]
    Success: bool
    ErrorCode: int
    ErrorMessage: str
    def __init__(self, DataRoom: _Optional[_Union[DataRoom, _Mapping]] = ..., Policies: _Optional[_Iterable[_Union[DataRoomPolicy, _Mapping]]] = ..., Success: bool = ..., ErrorCode: _Optional[int] = ..., ErrorMessage: _Optional[str] = ...) -> None: ...

class DataRoomDeleteRequest(_message.Message):
    __slots__ = ["DataRoom", "Policy", "JWT"]
    DATAROOM_FIELD_NUMBER: _ClassVar[int]
    POLICY_FIELD_NUMBER: _ClassVar[int]
    JWT_FIELD_NUMBER: _ClassVar[int]
    DataRoom: DataRoom
    Policy: DataRoomPolicy
    JWT: str
    def __init__(self, DataRoom: _Optional[_Union[DataRoom, _Mapping]] = ..., Policy: _Optional[_Union[DataRoomPolicy, _Mapping]] = ..., JWT: _Optional[str] = ...) -> None: ...

class DataRoomDeleteResponse(_message.Message):
    __slots__ = ["Success", "ErrorCode", "ErrorMessage"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERRORCODE_FIELD_NUMBER: _ClassVar[int]
    ERRORMESSAGE_FIELD_NUMBER: _ClassVar[int]
    Success: bool
    ErrorCode: int
    ErrorMessage: str
    def __init__(self, Success: bool = ..., ErrorCode: _Optional[int] = ..., ErrorMessage: _Optional[str] = ...) -> None: ...

class DataRoomLeaveRequest(_message.Message):
    __slots__ = ["RoomID", "SourceIdentifier"]
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    SOURCEIDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    RoomID: str
    SourceIdentifier: str
    def __init__(self, RoomID: _Optional[str] = ..., SourceIdentifier: _Optional[str] = ...) -> None: ...

class DataRoomLeaveResponse(_message.Message):
    __slots__ = ["Success", "ErrorCode", "ErrorMessage"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERRORCODE_FIELD_NUMBER: _ClassVar[int]
    ERRORMESSAGE_FIELD_NUMBER: _ClassVar[int]
    Success: bool
    ErrorCode: int
    ErrorMessage: str
    def __init__(self, Success: bool = ..., ErrorCode: _Optional[int] = ..., ErrorMessage: _Optional[str] = ...) -> None: ...

class DataPolicy(_message.Message):
    __slots__ = ["ID", "Identifier", "SourceIdentifier", "TargetIdentifier", "SlotsIdentifiers", "RoomID", "OpCode", "Policy", "CreatedAt"]
    ID_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    SOURCEIDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    TARGETIDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    SLOTSIDENTIFIERS_FIELD_NUMBER: _ClassVar[int]
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    OPCODE_FIELD_NUMBER: _ClassVar[int]
    POLICY_FIELD_NUMBER: _ClassVar[int]
    CREATEDAT_FIELD_NUMBER: _ClassVar[int]
    ID: str
    Identifier: str
    SourceIdentifier: str
    TargetIdentifier: str
    SlotsIdentifiers: _containers.RepeatedScalarFieldContainer[str]
    RoomID: str
    OpCode: UploadOpCode
    Policy: Policy
    CreatedAt: _timestamp_pb2.Timestamp
    def __init__(self, ID: _Optional[str] = ..., Identifier: _Optional[str] = ..., SourceIdentifier: _Optional[str] = ..., TargetIdentifier: _Optional[str] = ..., SlotsIdentifiers: _Optional[_Iterable[str]] = ..., RoomID: _Optional[str] = ..., OpCode: _Optional[_Union[UploadOpCode, str]] = ..., Policy: _Optional[_Union[Policy, str]] = ..., CreatedAt: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class DataPolicyCreateRequest(_message.Message):
    __slots__ = ["Policy", "Policies", "JWT"]
    POLICY_FIELD_NUMBER: _ClassVar[int]
    POLICIES_FIELD_NUMBER: _ClassVar[int]
    JWT_FIELD_NUMBER: _ClassVar[int]
    Policy: DataPolicy
    Policies: _containers.RepeatedCompositeFieldContainer[DataPolicy]
    JWT: str
    def __init__(self, Policy: _Optional[_Union[DataPolicy, _Mapping]] = ..., Policies: _Optional[_Iterable[_Union[DataPolicy, _Mapping]]] = ..., JWT: _Optional[str] = ...) -> None: ...

class DataPolicyCreateResponse(_message.Message):
    __slots__ = ["Policies", "Success", "ErrorCode", "ErrorMessage"]
    POLICIES_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERRORCODE_FIELD_NUMBER: _ClassVar[int]
    ERRORMESSAGE_FIELD_NUMBER: _ClassVar[int]
    Policies: _containers.RepeatedCompositeFieldContainer[DataPolicy]
    Success: bool
    ErrorCode: int
    ErrorMessage: str
    def __init__(self, Policies: _Optional[_Iterable[_Union[DataPolicy, _Mapping]]] = ..., Success: bool = ..., ErrorCode: _Optional[int] = ..., ErrorMessage: _Optional[str] = ...) -> None: ...

class DataPolicyDeleteRequest(_message.Message):
    __slots__ = ["Policy", "Policies", "JWT"]
    POLICY_FIELD_NUMBER: _ClassVar[int]
    POLICIES_FIELD_NUMBER: _ClassVar[int]
    JWT_FIELD_NUMBER: _ClassVar[int]
    Policy: DataPolicy
    Policies: _containers.RepeatedCompositeFieldContainer[DataPolicy]
    JWT: str
    def __init__(self, Policy: _Optional[_Union[DataPolicy, _Mapping]] = ..., Policies: _Optional[_Iterable[_Union[DataPolicy, _Mapping]]] = ..., JWT: _Optional[str] = ...) -> None: ...

class DataPolicyDeleteResponse(_message.Message):
    __slots__ = ["Success", "ErrorCode", "ErrorMessage"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERRORCODE_FIELD_NUMBER: _ClassVar[int]
    ERRORMESSAGE_FIELD_NUMBER: _ClassVar[int]
    Success: bool
    ErrorCode: int
    ErrorMessage: str
    def __init__(self, Success: bool = ..., ErrorCode: _Optional[int] = ..., ErrorMessage: _Optional[str] = ...) -> None: ...

class DataRoomPolicyCreateRequest(_message.Message):
    __slots__ = ["Policy", "Policies", "JWT"]
    POLICY_FIELD_NUMBER: _ClassVar[int]
    POLICIES_FIELD_NUMBER: _ClassVar[int]
    JWT_FIELD_NUMBER: _ClassVar[int]
    Policy: DataRoomPolicy
    Policies: _containers.RepeatedCompositeFieldContainer[DataRoomPolicy]
    JWT: str
    def __init__(self, Policy: _Optional[_Union[DataRoomPolicy, _Mapping]] = ..., Policies: _Optional[_Iterable[_Union[DataRoomPolicy, _Mapping]]] = ..., JWT: _Optional[str] = ...) -> None: ...

class DataRoomPolicyCreateResponse(_message.Message):
    __slots__ = ["Success", "ErrorCode", "ErrorMessage", "Policies"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERRORCODE_FIELD_NUMBER: _ClassVar[int]
    ERRORMESSAGE_FIELD_NUMBER: _ClassVar[int]
    POLICIES_FIELD_NUMBER: _ClassVar[int]
    Success: bool
    ErrorCode: int
    ErrorMessage: str
    Policies: _containers.RepeatedCompositeFieldContainer[DataRoomPolicy]
    def __init__(self, Success: bool = ..., ErrorCode: _Optional[int] = ..., ErrorMessage: _Optional[str] = ..., Policies: _Optional[_Iterable[_Union[DataRoomPolicy, _Mapping]]] = ...) -> None: ...

class DataRoomPolicyDeleteRequest(_message.Message):
    __slots__ = ["Policy", "Policies", "JWT"]
    POLICY_FIELD_NUMBER: _ClassVar[int]
    POLICIES_FIELD_NUMBER: _ClassVar[int]
    JWT_FIELD_NUMBER: _ClassVar[int]
    Policy: DataRoomPolicy
    Policies: _containers.RepeatedCompositeFieldContainer[DataRoomPolicy]
    JWT: str
    def __init__(self, Policy: _Optional[_Union[DataRoomPolicy, _Mapping]] = ..., Policies: _Optional[_Iterable[_Union[DataRoomPolicy, _Mapping]]] = ..., JWT: _Optional[str] = ...) -> None: ...

class DataRoomPolicyDeleteResponse(_message.Message):
    __slots__ = ["Success", "ErrorCode", "ErrorMessage"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERRORCODE_FIELD_NUMBER: _ClassVar[int]
    ERRORMESSAGE_FIELD_NUMBER: _ClassVar[int]
    Success: bool
    ErrorCode: int
    ErrorMessage: str
    def __init__(self, Success: bool = ..., ErrorCode: _Optional[int] = ..., ErrorMessage: _Optional[str] = ...) -> None: ...

class DataLog(_message.Message):
    __slots__ = ["ID", "DataIdentifier", "PerformedIdentifier", "Type", "RoomID", "CreatedAt"]
    ID_FIELD_NUMBER: _ClassVar[int]
    DATAIDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    PERFORMEDIDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    CREATEDAT_FIELD_NUMBER: _ClassVar[int]
    ID: str
    DataIdentifier: str
    PerformedIdentifier: str
    Type: Policy
    RoomID: str
    CreatedAt: _timestamp_pb2.Timestamp
    def __init__(self, ID: _Optional[str] = ..., DataIdentifier: _Optional[str] = ..., PerformedIdentifier: _Optional[str] = ..., Type: _Optional[_Union[Policy, str]] = ..., RoomID: _Optional[str] = ..., CreatedAt: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class DataLogListRequest(_message.Message):
    __slots__ = ["OwnerIdentifier", "CompanyID", "RoomID", "DataIdentifier", "Offset", "Limit", "JWT"]
    OWNERIDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    COMPANYID_FIELD_NUMBER: _ClassVar[int]
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    DATAIDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    JWT_FIELD_NUMBER: _ClassVar[int]
    OwnerIdentifier: str
    CompanyID: int
    RoomID: str
    DataIdentifier: str
    Offset: int
    Limit: int
    JWT: str
    def __init__(self, OwnerIdentifier: _Optional[str] = ..., CompanyID: _Optional[int] = ..., RoomID: _Optional[str] = ..., DataIdentifier: _Optional[str] = ..., Offset: _Optional[int] = ..., Limit: _Optional[int] = ..., JWT: _Optional[str] = ...) -> None: ...

class DataLogListResponse(_message.Message):
    __slots__ = ["Logs", "TotalCount"]
    LOGS_FIELD_NUMBER: _ClassVar[int]
    TOTALCOUNT_FIELD_NUMBER: _ClassVar[int]
    Logs: _containers.RepeatedCompositeFieldContainer[DataLog]
    TotalCount: int
    def __init__(self, Logs: _Optional[_Iterable[_Union[DataLog, _Mapping]]] = ..., TotalCount: _Optional[int] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
