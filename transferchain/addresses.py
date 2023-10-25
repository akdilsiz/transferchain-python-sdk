from transferchain.crypt import keys
from transferchain import constants
from transferchain import blockchain
from transferchain.logger import get_logger
from transferchain.transaction import create_transaction
from transferchain.datastructures import (
    Address, Addresses, Result, User)


logger = get_logger(__file__)


def get_user_password(user_id, sub_user_id):
    return f"user-{user_id}-{sub_user_id}"


def generate_user_addresses(user_id, mnemonics, sub_user_id):
    addresses = []
    user_pass = get_user_password(user_id, sub_user_id)
    user_keys = keys.create_keys_with_mnemonic(mnemonics, user_pass)

    tx_master_address = Address(
        Master=True, Key=user_keys, UserID=user_id, Mnemonics=mnemonics,
        MasterAddress=None, SubUserID=sub_user_id)
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
        user_pass = "{}-{}".format(
            get_user_password(user_id, sub_user_id), i)
        user_keys = keys.create_keys_with_mnemonic(mnemonics, user_pass)
        address = Address(
            Master=False, Key=user_keys, UserID=user_id, Mnemonics=mnemonics,
            MasterAddress=tx_master_address.Key['Address'],
            SubUserID=sub_user_id)
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
        id=sub_user_id,
        parent_user_id=user_id,
        addresses=addresses,
        master_address=addresses[0]
    )
    return Result(success=True, data=user)
