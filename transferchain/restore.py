import gzip
import json
import base64
from tcabci_read_client import HttpClient
from transferchain import settings
from transferchain import constants
from transferchain.crypt import keys, crypt
from transferchain.datastructures import (
    Result, User, Address)


def restore_master(mnemonics, password, tx_type, limit=1, offset=0):
    user_keys = keys.create_keys_with_mnemonic(mnemonics, password)
    client = HttpClient(settings.READ_NODE_ADDRESS)
    response = client.tx_search(
        recipient_addrs=[
            user_keys['Address']
        ],
        height=0,
        height_operator=">=",
        hashes=None,
        typ=tx_type,
        limit=limit,
        offset=offset,
        order_by=constants.SORT_TYPE_ASC
    )
    return {'user_keys': user_keys, 'response': response}


def restore_master_user(mnemonics, password):
    return restore_master(mnemonics, password, constants.TX_TYPE_MASTER)


def restore_sub_user(mnemonics, password, page=1, limit=100):
    offset = ((page - 1) * limit + 1) - 1
    return restore_master(mnemonics, password, constants.TX_TYPE_SUB_MASTER,
                          limit=limit, offset=offset)


def extract_txn(txn, key, with_gzip=False):
    data = txn['data']['Bytes']
    decoded_data = base64.b64decode(data)
    tx = crypt.decrypt_asymmetric(
        txn['sender_addr'], key['Seed'], decoded_data)
    if with_gzip:
        tx = gzip.decompress(tx)
    return json.loads(tx)


def get_addresses(typ, recipient_addrs, limit=1, offset=0):
    # TEST
    client = HttpClient(settings.READ_NODE_ADDRESS)
    response = client.tx_search(
        recipient_addrs=[recipient_addrs],
        height=0,
        height_operator=">=",
        hashes=None,
        typ=typ,
        limit=1,
        offset=0,
        order_by=constants.SORT_TYPE_ASC
    )
    if not response.success:
        return Result(success=False, error_message='Addresses txn fetch error')

    result = response.result['txs']
    if len(result) == 0:
        return Result(success=False, error_message='Master txn not found')
    return Result(success=True, data=result[0])


def restore_master_with_mnemonics(mnemonics, password, user_id):
    result = restore_master_user(mnemonics, password)
    user_keys = result['user_keys']
    response = result['response']
    if not response.success:
        return Result(success=False, error_message='Master txn fetch error')

    result = response.result['txs']
    if len(result) == 0:
        return Result(success=False, error_message='Master txn not found')

    master_txn = extract_txn(result[0], user_keys)

    if master_txn['UserID'] != user_id:
        return Result(success=False, error_message='blockchain is not authorized with the information provided')  # noqa

    addresses_result = get_addresses(
        constants.TX_TYPE_ADDRESSES, user_keys['Address'], limit=1, offset=0)
    if addresses_result.success is False:
        return addresses_result

    addresses_txn = extract_txn(
        addresses_result.data, user_keys, with_gzip=True)

    master_address = Address(**master_txn)
    master_key_address = master_txn['Key']['Address']
    addresses = [
        Address(MasterAddress=master_key_address, **master_txn)
    ]
    for address in addresses_txn['Addresses']:
        addresses.append(Address(**address))

    user = User(
        id=master_address.UserID,
        parent_user_id=master_address.SubUserID,
        addresses=addresses,
        master_address=master_address,
        master=True
    )
    return Result(success=True, data=user)


def restore_sub_user_with_mnemonics(mnemonics, password, user_id):
    page = 1
    users = []
    while True:
        result = restore_sub_user(mnemonics, password, page=page)
        user_keys = result['user_keys']
        response = result['response']

        if not response.success:
            return Result(
                success=False, error_message='Master txn fetch error')

        txns = response.result['txs']
        if len(txns) == 0:
            # empty response
            break

        for txn in txns:
            master_txn = extract_txn(txn, user_keys)
            if master_txn['UserID'] != user_id:
                return Result(success=False, error_message='blockchain is not authorized with the information provided')  # noqa

            addresses_result = get_addresses(
                constants.TX_TYPE_SUB_ADDRESSES,
                master_txn['Key']['Address'], limit=1, offset=0)
            if addresses_result.success is False:
                return addresses_result
            addresses_txn = extract_txn(
                addresses_result.data, master_txn['Key'], with_gzip=True)

            master_address = Address(**master_txn)
            master_key_address = master_txn['Key']['Address']
            addresses = [
                Address(MasterAddress=master_key_address, **master_txn)
            ]
            for address in addresses_txn['Addresses']:
                addresses.append(Address(**address))

            user = User(
                id=master_address.SubUserID,
                parent_user_id=master_address.UserID,
                addresses=addresses,
                master_address=master_address,
                master=False
            )
            users.append(user)
        page += 1
        if len(users) == response.result['total_count']:
            break
    return Result(success=True, data=users)
