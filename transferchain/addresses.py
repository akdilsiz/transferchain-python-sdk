from transferchain.crypt import keys
from transferchain import constants
from transferchain import blockchain
from transferchain.logger import get_logger
from transferchain.transaction import create_transaction
from transferchain.datastructures import (
    DataAddress, DataAddresses, Result)


logger = get_logger(__file__)


def get_user_password(user_id, sub_user_id):
    return f"user-{user_id}-{sub_user_id}"


def generate_user_addresses(user_id, mnemonics, sub_user_id):
    addresses = []
    user_pass = get_user_password(user_id, sub_user_id)
    user_keys = keys.create_keys_with_mnemonic(mnemonics, user_pass)

    tx_master_address = DataAddress(
        master=True, key=user_keys, user_id=user_id, mnemonics=mnemonics)
    addresses.append(tx_master_address)
    tx = create_transaction(
        constants.TX_TYPE_MASTER, user_keys, user_keys, tx_master_address)
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
        address = DataAddress(
            master=False, key=user_keys, user_id=user_id, mnemonics=mnemonics)
        addresses.append(address)
        addresses_payload.append(address.to_json(with_pascal_case=True))

    tx = create_transaction(
        constants.TX_TYPE_ADDRESSES,
        user_keys,
        user_keys,
        DataAddresses(user_id=user_id, addresses=addresses_payload)
    )
    result = blockchain.broadcast(tx)
    if result.success is False:
        return Result(
            success=False,
            error_message='The addresses is not published on the blockchain.') # noqa
    return Result(success=True, data=addresses)
