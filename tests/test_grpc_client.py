import unittest
from transferchain import grpc_client as grpc
from transferchain.protobuf import service_pb2 as pb


class TestGrpcClientMethods(unittest.TestCase):

    def test_grpc_client(self):
        result = grpc.get_client()
        hb_result = result.Heartbeat(pb.Empty())
        self.assertEqual(0, hb_result.ByteSize())
