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
    """
    This function is called to fetch the master address of
    the user of the specified type.

    Parameters:
        mnemonics (str):
            mnemonics of account

        password (str):
            password

        tx_type (str):
            master txn types; constants.TX_TYPE_MASTER,
                              constants.TX_TYPE_SUB_MASTER

        limit (int):
            data limit

        offset (int):
            offset

    Returns:
        Return dict. user keys and read client response.

    Example:
        -
    ```
        from transferchain import restore
        from transferchain import constants
        from transferchain.addresses import get_user_password
        from transferchain.config import create_config
        from transferchain.client import TransferChain

        config = create_config()
        tc = TransferChain(config)
        result = tc.add_master_user()
        # if result is oke, continue;
        user_password = get_user_password(tc.config.user_id)
        result = restore.restore_master(
            tc.config.mnemonics, user_password, constants.TX_TYPE_MASTER)

    ```
    """
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
    """
    This function is called to fetch the master address of
    the master user.

    Parameters:
        mnemonics (str):
            mnemonics of account

        password (str):
            password

    Returns:
        Return dict. user keys and read client response.

    Example:
        -
    ```
        from transferchain import restore
        from transferchain.addresses import get_user_password
        from transferchain.config import create_config
        from transferchain.client import TransferChain

        config = create_config()
        tc = TransferChain(config)
        result = tc.add_master_user()
        # if result is oke, continue;
        user_password = get_user_password(tc.config.user_id)
        result = restore.restore_master_user(
            tc.config.mnemonics, user_password)

    ```
    """
    return restore_master(mnemonics, password, constants.TX_TYPE_MASTER)


def restore_sub_user(mnemonics, password, page=1, limit=100):
    """
    This function is called to fetch the master address of
    the sub user.

    Parameters:
        mnemonics (str):
            mnemonics of account

        password (str):
            password

        limit (int):
            page limit

        page (int):
            number of page

    Returns:
        Return dict. user keys and read client response.

    Example:
        -
    ```
        from transferchain import restore
        from transferchain.addresses import get_user_password
        from transferchain.config import create_config
        from transferchain.client import TransferChain

        config = create_config()
        tc = TransferChain(config)
        result = tc.add_master_user()
        # if result is oke, continue;
        user_password = get_user_password(tc.config.user_id)
        result = restore.restore_sub_user(
            tc.config.mnemonics, user_password, page=1)

    ```
    """

    offset = ((page - 1) * limit + 1) - 1
    return restore_master(mnemonics, password, constants.TX_TYPE_SUB_MASTER,
                          limit=limit, offset=offset)


def extract_txn(txn, key, with_gzip=False):
    """
    This function is called to fetch the master address of
    the master user.

    Parameters:
        txn:
            blockchain transaction

        key (keys):
            transaction keys

        with_gzip (bool):
            If the transaction is compressed with gzip, use this.

    Returns:
        Return transaction dict.

    Example:
        -
    ```
        from transferchain import restore
        from transferchain.addresses import get_user_password
        from transferchain.config import create_config
        from transferchain.client import TransferChain

        config = create_config()
        tc = TransferChain(config)
        result = tc.add_master_user()
        # if result is oke, continue;
        user_password = get_user_password(tc.config.user_id)
        result = restore.restore_master_user(
            tc.config.mnemonics, user_password)
        txn_result = restore.extract_txn(
            result['response'].result['txs'][0], result['user_keys'])

    ```
    """
    data = txn['data']['Bytes']
    decoded_data = base64.b64decode(data)
    tx = crypt.decrypt_asymmetric(
        txn['sender_addr'], key['Seed'], decoded_data)
    if with_gzip:
        tx = gzip.decompress(tx)
    return json.loads(tx)


def get_addresses(typ, recipient_addrs, limit=1, offset=0):
    """
    Fetch addresses

    Parameters:
        type (str):
            transaction type

        recipient addres (str):
            broadcast address

        limit (int):
            page limit

        offset (int):
            page offset

    Returns:
        Return Result object.Payload is read client http response

    Example:
        -
    ```
        from transferchain import restore
        from transferchain import constants
        from transferchain.addresses import get_user_password
        from transferchain.config import create_config
        from transferchain.client import TransferChain

        config = create_config()
        tc = TransferChain(config)
        result = tc.add_master_user()

        password = get_user_password(tc.config.user_id)
        result = restore_master_user(tc.config.mnemonics, password)
        user_keys = result['user_keys']
        addresses_result = restore.get_addresses(
            constants.TX_TYPE_ADDRESSES, user_keys['Address'],
            limit=1, offset=0)

    ```
    """
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
    """
    The addresses of the master user are fetched with this
    function and the user object is created.

    Parameters:
        mnemonics (str):
            account mnemonics

        password (str):
            password

        user_id (bool):
            account id

    Returns:
        Return datastructures.User

    Example:
        -
    ```
        from transferchain import restore
        from transferchain.addresses import get_user_password
        from transferchain.config import create_config
        from transferchain.client import TransferChain

        config = create_config()
        tc = TransferChain(config)
        result = tc.add_master_user()
        # if result is oke, continue;
        user_password = get_user_password(tc.config.user_id)
        result = restore.restore_master_with_mnemonics(
            tc.config.mnemonics, user_password, tc.config.user_id)

    ```
    """
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
    """
    The addresses of the sub users are fetched with this
    function and the user object is created.

    Parameters:
        mnemonics (str):
            account mnemonics

        password (str):
            password

        user_id (bool):
            account id

    Returns:
        Return list of datastructures.User

    Example:
        -
    ```
        from transferchain import restore
        from transferchain.addresses import get_user_password
        from transferchain.config import create_config
        from transferchain.client import TransferChain

        config = create_config()
        tc = TransferChain(config)
        result = tc.add_master_user()
        # if result is oke, continue;
        user_password = get_user_password(tc.config.user_id)
        result = restore.restore_sub_user_with_mnemonics(
            tc.config.mnemonics, user_password, tc.config.user_id)
    ```
    """
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
