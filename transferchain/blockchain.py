from tcabci_read_client import HttpClient
from transferchain import settings


def broadcast(transaction):
    client = HttpClient(settings.READ_NODE_ADDRESS)
    response = client.broadcast(**transaction)
    return response
