DEBUG = True

RPC_ADDRESS = "node1.transferchain.io:50051"

READ_NODE_ADDRESS = "https://read-node-01.transferchain.io"

READ_NODE_WS_ADDRESS = "wss://read-node-01.transferchain.io/ws"

if DEBUG:
    TCMP_BASE_URL = "https://api-test-tcmp.transferchain.io"
else:
    TCMP_BASE_URL = "https://api-tcmp.transferchain.io"

WALLET_INFORMATION_URI = "/v1/user/{user_id}/wallet/{wallet_uuid}"

CREATE_WALLET_URI = "/v1/user/{user_id}/wallet"

SORT_TYPE_ASC = "ASC"
SORT_TYPE_DESC = "DESC"

TRANSFER_TYPE_SENT = "sent"
TRANSFER_TYPE_RECEIVED = "received"
