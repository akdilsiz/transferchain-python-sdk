'''Constants in the module are written here.'''

UPLOAD_CHUNK_SIZE = 1 * 1024 * 1024

SORT_TYPE_ASC = "ASC"
SORT_TYPE_DESC = "DESC"

TRANSFER_TYPE_SENT = "sent"
TRANSFER_TYPE_RECEIVED = "received"

TX_TYPE_SUB_MASTER = 'initial_sub_storage'
TX_TYPE_SUB_ADDRESSES = 'interim_sub_storages'

TX_TYPE_MASTER = "initial_storage"
TX_TYPE_ADDRESS = "interim_storage"
TX_TYPE_ADDRESSES = "interim_storages"
TX_TYPE_TRANSFER = "transfer"
TX_TYPE_TRANSFER_CANCEL = "transfer_Cancel"
TX_TYPE_TRANSFER_SENT = "transfer_sent"
TX_TYPE_TRANSFER_RECIEVE_DELETE = "transfer_receive_delete"
TX_TYPE_STORAGE = "storage"
TX_TYPE_STORAGE_DELETE = "storage_delete"


TransferSent = "sent"
TransferNormal = "normal"
TransferNON = "non"

STORAGE_MAX_FILE_COUNT = 20
