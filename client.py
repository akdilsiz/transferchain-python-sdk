import os
import exceptions
from crypt import bip39
from logger import get_logger


logger = get_logger(__file__)


def create_config():
    user_id = os.environ.get('TRANSFERCHAIN_USER_ID')
    if not user_id:
        raise exceptions.ValidationError("config error: invalid user id")

    wallet_uuid = os.environ.get('TRANSFERCHAIN_WALLET_UUID')
    if not wallet_uuid:
        # new wallet
        pass

    mnemonics = os.environ.get('TRANSFERCHAIN_MNEMONICS')
    if mnemonics is None:
        raise exceptions.ValidationError('config error: invalid mnemonics')

    mnemonics_list = str(mnemonics).split('')
    if len(mnemonics_list) != 24:
        # create new mnemonics
        # bip39.new_mnemonics()
        pass

    api_token = os.environ.get('TRANSFERCHAIN_API_TOKEN')
    api_secret = os.environ.get('TRANSFERCHAIN_API_SECRET')

    if api_token == "" or api_secret == "":
        raise exceptions.ValidationError(
            "config error: invalid api token or api secret")

    


def new_client(config):
    # check config
    # create sqllite db
    '''
    return namedtuple(storage=storage, config=config)
    -------
    

    client = new_client()
    
    transfer_service = create_transfer_service(client)

    '''
    pass


new_client("")
