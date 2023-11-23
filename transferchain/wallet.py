import json
from urllib.parse import urljoin
import requests
from transferchain import settings
from transferchain.utils import datetime_formating
from transferchain.datastructures import (
    CreateWalletResult, WalletInfoResult, UserPackage,
    UserCompany, WalletUser)


def create_wallet(conf, wallet_uuid):
    """
    Create new wallet

    Parameters:
        conf (datastructures.Config):
            config

        wallet_uuid (str):
            wallet uuid

    Returns:
        CreateWalletResult

    Example:
        -
    ```
        import os
        import uuid
        from transferchain.datastructures import Config
        from transferchain import wallet

        user_id = os.environ.get('TRANSFERCHAIN_USER_ID')
        api_token = os.environ.get('TRANSFERCHAIN_API_TOKEN')
        api_secret = os.environ.get('TRANSFERCHAIN_API_SECRET')
        conf = Config(api_token=api_token, api_secret=api_secret)
        wallet_uuid = str(uuid.uuid4())
        os.environ['TRANSFERCHAIN_TEST_WALLET_UUID'] = wallet_uuid
        result = wallet.create_wallet(conf, wallet_uuid)
    ```
    """
    headers = {
        'api_token': conf.api_token,
        'api_secret': conf.api_secret,
        'Content-Type': 'application/json'
    }

    uri = settings.CREATE_WALLET_URI
    url = urljoin(settings.TCMP_BASE_URL, uri)
    payload = json.dumps({'uuid': wallet_uuid})
    req = requests.post(url, data=payload, headers=headers)
    try:
        response = req.json()
    except requests.exceptions.JSONDecodeError as e:
        return CreateWalletResult(success=False, error_message=str(e))
    data = response.get('data') or {}
    return CreateWalletResult(
        success=req.ok,
        wallet_id=data.get('wallet_id'),
        error_message=response.get('message', ''))


def get_wallet_info(conf, wallet_uuid):
    """
    Get wallet info

    Parameters:
        conf (datastructures.Config):
            config

        wallet_uuid (str):
            wallet uuid

    Returns:
        WalletInfoResult

    Example:
        -
    ```
        import os
        import uuid
        from transferchain.datastructures import Config
        from transferchain import wallet

        user_id = os.environ.get('TRANSFERCHAIN_USER_ID')
        api_token = os.environ.get('TRANSFERCHAIN_API_TOKEN')
        api_secret = os.environ.get('TRANSFERCHAIN_API_SECRET')
        conf = Config(api_token=api_token, api_secret=api_secret)
        wallet_uuid = os.environ['TRANSFERCHAIN_TEST_WALLET_UUID']
        result = wallet.get_wallet_info(conf, wallet_uuid)
    ```
    """
    headers = {
        'api_token': conf.api_token,
        'api_secret': conf.api_secret,
        'Content-Type': 'application/json'
    }

    uri = settings.WALLET_INFORMATION_URI.format(
        wallet_uuid=wallet_uuid)
    query = settings.WALLET_INFORMATION_QUERY
    url = urljoin(settings.TCMP_BASE_URL, (uri + query))
    req = requests.get(url, headers=headers)
    try:
        response = req.json()
    except requests.exceptions.JSONDecodeError as e:
        return CreateWalletResult(success=False, error_message=str(e))
    data = response.get('data') or {}
    if not req.ok:
        return WalletInfoResult(
            success=False,
            error_message=response.get('message', ''))

    user = data['user']
    package = UserPackage(
        id=user['mmitem_id'],
        code=user['mmitem_code'],
        title=user['mmitem_title'])

    return WalletInfoResult(
        id=data['id'],
        package=package,
        success=True,
        created_at=datetime_formating(data['zlins_dttm']),
        updated_at=datetime_formating(data['zlupd_dttm']),
    )
