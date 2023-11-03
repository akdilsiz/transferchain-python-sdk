import grpc
from transferchain.cert import RPC_CERT
from transferchain.settings import RPC_ADDRESS
from transferchain.protobuf import service_pb2_grpc


GRPC_CLIENT = None


def get_client():
    '''
    Grpc connection function.
    Once called, grpc connects to the server and stores
    this connection in a global variable.
    '''
    global GRPC_CLIENT
    if GRPC_CLIENT is not None:
        return GRPC_CLIENT
    creds = grpc.ssl_channel_credentials(root_certificates=RPC_CERT)
    channel = grpc.secure_channel(RPC_ADDRESS, creds)
    GRPC_CLIENT = service_pb2_grpc.tcRpcStub(channel)
    return GRPC_CLIENT
