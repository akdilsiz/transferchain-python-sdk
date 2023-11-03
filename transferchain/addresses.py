'''
This module enables the creation of addresses
for users and broadcasting them to the blockchain.
'''

from transferchain.crypt import keys
from transferchain import constants
from transferchain import blockchain
from transferchain.logger import get_logger
from transferchain.transaction import create_transaction
from transferchain.datastructures import (
    Address, Addresses, Result, User)


logger = get_logger(__file__)


def get_user_password(user_id, sub_user_id=None):
    """
    Return a user password.The password created here is used when creating keys

    Parameters:
        user_id (int):
            account user id

        sub_user_id (str):
            optinal value, random uuid generated for subuser

    Returns:
        A key password

    Example:
        -
    ```
        from transferchain.addresses import get_user_password
        password = get_user_password(1)  # result is user-1
        sub_user_password = get_user_password(1, 'abc') # result is user-1-abc

    ```
    """
    if sub_user_id:
        return f"user-{user_id}-{sub_user_id}"
    return f"user-{user_id}"


def generate_sub_user_addresses(user_id, master_user_address,
                                mnemonics, sub_user_id):
    """
    Return a datastructures.User object.
    The sub user's master address is broadcast to the master user's
    master address. The sub user's sub addresses are broadcast to
    his master address.

    Parameters:
        user_id (int):
            account user id

        master_user_address (Address):
            Address object of master user.If you need the check,
            check the Master attribute.

        mnemonics (str):
            mnemonics of account

        sub_user_id (str):
            account user id

    Returns:
        Result object. Result.data is datastructures.User


    Example:
        -
    ```
        import uuid
        from transferchain.crypt import bip39
        from transferchain.addresses import (
            generate_user_addresses, generate_sub_user_addresses)

        uuid = str(uuid.uuid4())
        mnemonics = bip39.create_mnomonics()
        result = generate_user_addresses(1, mnemonics)
        master_address = result.data.master_address
        result = generate_sub_user_addresses(
            1, master_address, mnemonics, uuid)
    ```

    """
    addresses = []
    user_pass = get_user_password(user_id, sub_user_id)
    user_keys = keys.create_keys_with_mnemonic(mnemonics, user_pass)

    tx_master_address = Address(
        Master=True, Key=user_keys, UserID=user_id, Mnemonics=mnemonics,
        MasterAddress=None, SubUserID=sub_user_id)
    addresses.append(tx_master_address)
    tx = create_transaction(
        constants.TX_TYPE_SUB_MASTER, user_keys,
        master_user_address.Key['Address'],
        tx_master_address)
    result = blockchain.broadcast(tx)
    if result.success is False:
        return Result(
            success=False,
            error_message='The master address is not published on the blockchain.') # noqa

    addresses_payload = []
    for i in range(0, 250):
        user_pass = "{}-{}".format(
            get_user_password(user_id, sub_user_id), i)
        user_sub_keys = keys.create_keys_with_mnemonic(mnemonics, user_pass)
        address = Address(
            Master=False,
            Key=user_sub_keys,
            UserID=user_id,
            Mnemonics=mnemonics,
            MasterAddress=tx_master_address.Key['Address'],
            SubUserID=sub_user_id)
        addresses.append(address)
        addresses_payload.append(address._asdict())

    tx = create_transaction(
        constants.TX_TYPE_SUB_ADDRESSES,
        user_keys,
        user_keys['Address'],
        Addresses(UserID=user_id, Addresses=addresses_payload)
    )
    result = blockchain.broadcast(tx)
    if result.success is False:
        return Result(
            success=False,
            error_message='The addresses is not published on the blockchain.') # noqa
    user = User(
        id=sub_user_id,
        parent_user_id=user_id,
        addresses=addresses,
        master_address=addresses[0],
        master=False
    )
    return Result(success=True, data=user)


def generate_user_addresses(user_id, mnemonics):
    """
    Return a datastructures.User object.
    It broadcasts the master address to itself.
    It broadcasts its own sub-addresses to its own master.

    Parameters:
        user_id (int):
            account user id

        mnemonics (str):
            mnemonics of account

    Returns:
        Result object. Result.data is datastructures.User


    Example:
        -
    ```
        from transferchain.crypt import bip39
        from transferchain.addresses import generate_user_addresses

        mnemonics = bip39.create_mnomonics()
        result = generate_user_addresses(1, mnemonics)
    ```
    """
    addresses = []
    user_pass = get_user_password(user_id)
    user_keys = keys.create_keys_with_mnemonic(mnemonics, user_pass)
    tx_master_address = Address(
        Master=True, Key=user_keys, UserID=user_id, Mnemonics=mnemonics,
        MasterAddress=None, SubUserID=None)
    addresses.append(tx_master_address)
    tx = create_transaction(
        constants.TX_TYPE_MASTER, user_keys, user_keys['Address'],
        tx_master_address)
    result = blockchain.broadcast(tx)
    if result.success is False:
        return Result(
            success=False,
            error_message='The master address is not published on the blockchain.') # noqa

    addresses_payload = []

    for i in range(0, 250):
        user_pass = "{}-{}".format(get_user_password(user_id), i)
        user_sub_keys = keys.create_keys_with_mnemonic(mnemonics, user_pass)
        address = Address(
            Master=False,
            Key=user_sub_keys,
            UserID=user_id,
            Mnemonics=mnemonics,
            MasterAddress=tx_master_address.Key['Address'],
            SubUserID=None)
        addresses.append(address)
        addresses_payload.append(address._asdict())

    tx = create_transaction(
        constants.TX_TYPE_ADDRESSES,
        user_keys,
        user_keys['Address'],
        Addresses(UserID=user_id, Addresses=addresses_payload)
    )
    result = blockchain.broadcast(tx)
    if result.success is False:
        return Result(
            success=False,
            error_message='The addresses is not published on the blockchain.') # noqa
    user = User(
        id=user_id,
        parent_user_id=user_id,
        addresses=addresses,
        master_address=addresses[0],
        master=True
    )
    return Result(success=True, data=user)
