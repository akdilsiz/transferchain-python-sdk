'''Configs to be used in the module are created here.'''

import os
import uuid
from transferchain import utils
from transferchain import exceptions
from transferchain.datastructures import Config
from transferchain.wallet import create_wallet, get_wallet_info


def create_config():
    """
    This function returns the config object.It takes parameters from env.

    If TRANSFERCHAIN_WALLET_UUID is empty, it is automatic generated.

    If there are no TRANSFERCHAIN_MNEMONICS, call the client.add_master_user.

    If give the TRANSFERCHAIN_MNEMONICS and already have an account you call
    the client.restore_master_user

    Parameters:
        TRANSFERCHAIN_USER_ID (int):
            account user id

        TRANSFERCHAIN_API_TOKEN (str):
            transferchain api token

        TRANSFERCHAIN_API_SECRET (str):
            transferchain api secret

        TRANSFERCHAIN_WALLET_UUID (str):
            optinal value, random uuid generated for subuser

        TRANSFERCHAIN_MNEMONICS (str):
            account mnemonics

    Returns:
        datastructers.Config

    Example:
        -
    ```
        from transferchain.config import create_config
        config = create_config()

    ```
    """
    user_id = int(os.environ.get('TRANSFERCHAIN_USER_ID', 0))

    if not user_id:
        raise exceptions.ValidationError("config error: invalid user id")

    api_token = os.environ.get('TRANSFERCHAIN_API_TOKEN')
    api_secret = os.environ.get('TRANSFERCHAIN_API_SECRET')

    if api_token == "" or api_secret == "":
        raise exceptions.ValidationError(
            "config error: invalid api token or api secret")

    db_path = os.path.join(os.getcwd(), "tc.db")
    conf = Config(api_token=api_token, api_secret=api_secret,
                  db_path=db_path)

    wallet_uuid = os.environ.get('TRANSFERCHAIN_WALLET_UUID')
    if not wallet_uuid:
        wallet_uuid = str(uuid.uuid4())
        result = create_wallet(conf, user_id, wallet_uuid)
        if result.success is False:
            raise exceptions.ValidationError(result.error_message)
        wallet_id = result.wallet_id
    else:
        if not utils.is_valid_uuid(wallet_uuid):
            raise exceptions.ValidationError('invalid wallet uuid')
        wallet_info = get_wallet_info(conf, wallet_uuid)
        wallet_id = wallet_info.id

    mnemonics = os.environ.get('TRANSFERCHAIN_MNEMONICS', '')
    # if not mnemonics or len(mnemonics.split('')) != 24:
    #    mnemonics = bip39.create_mnomonics()
    #    # create user addresses or  restore

    return conf._replace(
        user_id=user_id,
        wallet_uuid=wallet_uuid,
        wallet_id=wallet_id,
        mnemonics=mnemonics)
