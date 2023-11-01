import json
import base64
import hashlib
from collections import OrderedDict
from transferchain.crypt import crypt


def sign_transaction(sign_key, transaction):
    tx = OrderedDict({
        "id": "",
        "version": 2,
        "type": transaction['tx_type'],
        "sender_addr": transaction['sender_address'],
        "recipient_addr": transaction['recipient_address'],
        "data": transaction['data'],
        "sign": None,
        "fee": 0
    })
    data = json.dumps(tx).replace(' ', '').encode('utf-8')
    sign = crypt.sign(sign_key, data)
    return sign


def create_transaction(tx_type, sender_keys, recipient_address, payload):
    sender_address = sender_keys['Address']
    data = crypt.encrypt_asymmetric(
        sender_keys['Seed'], recipient_address,
        payload.dump())

    tx_id = hashlib.sha512(data).hexdigest()

    transaction = {
        "fee": 0,
        "tx_id": tx_id,
        "version": 2,
        "data": base64.b64encode(data).decode(),
        "sign": None,
        "tx_type": tx_type,
        "sender_address": sender_address,
        "recipient_address": recipient_address
    }
    tx_sign = sign_transaction(sender_keys['PrivateKeySign'], transaction)
    transaction["sign"] = base64.b64encode(tx_sign).decode()
    return transaction
