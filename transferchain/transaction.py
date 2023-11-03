import json
import base64
import hashlib
from collections import OrderedDict
from transferchain.crypt import crypt


def sign_transaction(sign_key, transaction):
    """
    Sign transaction.

    Parameters:
        sign_key (str):
            sign key

        transaction:
            transaction dict

    Returns:
        bytes

    Example:
        -

    """
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
    """
    Create blockchain transaction.

    Parameters:
        ty_type (str):
            transaction type

        sender_keys (datastructures.Address.Key):
            sender keys

        recipient_address (str):
            recipient address

        payload:
            broadcast payload

    Returns:
        Transaction dict

    Example:
        -
    ```
        from transferchain.crypt import bip39
        from transferchain.addresses import get_user_password
        from transferchain.crypt import keys
        from transferchain.datastructures import Address
        from transferchain.transaction import create_transaction
        from transferchain import constants

        user_id = 1
        sub_user_id = 'test'
        mnemonics = bip39.create_mnomonics()
        user_pass = get_user_password(user_id, sub_user_id)
        user_keys = keys.create_keys_with_mnemonic(mnemonics, user_pass)

        tx_master_address = Address(
            Master=True, Key=user_keys, UserID=user_id, Mnemonics=mnemonics)

        tx = create_transaction(
            constants.TX_TYPE_MASTER, user_keys, user_keys['Address'],
            tx_master_address)
    ```
    """
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
