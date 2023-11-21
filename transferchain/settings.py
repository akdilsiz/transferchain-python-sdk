'''
Constants that will change depending on the situation
in the module are written here.'''
DEBUG = True

# production urls
RPC_ADDRESS = "node1.transferchain.io:50051"
READ_NODE_ADDRESS = "https://read-node-01.transferchain.io"
READ_NODE_WS_ADDRESS = "wss://read-node-01.transferchain.io/ws"
TCMP_BASE_URL = "https://api-tcmp.transferchain.io"

# uri
WALLET_INFORMATION_URI = "/v1/wallet/{wallet_uuid}?type=uuid"
CREATE_WALLET_URI = "/v1/wallet"

if DEBUG:
    # testurls
    RPC_ADDRESS = "test-file-operation.transferchain.io:50051"
    TCMP_BASE_URL = "https://api-test-tcmp.transferchain.io"
    READ_NODE_ADDRESS = "https://test-read-node-01.transferchain.io"
    READ_NODE_WS_ADDRESS = "wss://test-read-node-01.transferchain.io/ws"
