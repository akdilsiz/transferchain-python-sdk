import json
from urllib.parse import urljoin
import requests
from transferchain import settings
from transferchain.utils import datetime_formating
from transferchain.datastructures import (
    CreateWalletResult, WalletInfoResult, UserPackage,
    UserCompany, WalletUser)


def create_wallet(conf, user_id, wallet_uuid):
    """
    Create new wallet

    Parameters:
        conf (datastructures.Config):
            config

        user_id (int):
            account user id

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
        result = wallet.create_wallet(conf, user_id, wallet_uuid)
    ```
    """
    headers = {
        'api_token': conf.api_token,
        'api_secret': conf.api_secret,
        'Content-Type': 'application/json'
    }

    uri = settings.CREATE_WALLET_URI.format(user_id=user_id)
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


def get_wallet_info(conf, user_id, wallet_uuid):
    """
    Get wallet info

    Parameters:
        conf (datastructures.Config):
            config

        user_id (int):
            account user id

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
        result = wallet.get_wallet_info(conf, user_id, wallet_uuid)
    ```
    """
    headers = {
        'api_token': conf.api_token,
        'api_secret': conf.api_secret,
        'Content-Type': 'application/json'
    }

    uri = settings.WALLET_INFORMATION_URI.format(
        user_id=user_id, wallet_uuid=wallet_uuid)
    url = urljoin(settings.TCMP_BASE_URL, uri)
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
    company = UserCompany(
        id=user['ficomp_id'],
        code=user['ficomp_code'],
        title=user['ficomp_title'])

    user = WalletUser(
        package=package,
        company=company,
        id=user['id'],
        type=user['typ'],
        uuid=user['uuid'],
        email=user['email'],
        status=user['statu'],
        mobile=user['mobile'],
        username=user['username'],
        old_hash=user['old_hash'],
        full_name=user['full_name'],
        is_active=user['is_active'],
        last_hash=user['last_hash'],
        role_code=user['role_code'],
        role_title=user['role_title'],
        is_suspended=user['is_suspended'],
        confirmation_code=user['confirmation_code'],
        password_reset_code=user['password_reset_code'],
        account_create_code=user['account_create_code'],
        updated_at=datetime_formating(user['zlins_dttm']),
        created_at=datetime_formating(user['zlupd_dttm']))
    return WalletInfoResult(
        user=user,
        id=data['wallet_id'],
        success=True,
        created_at=datetime_formating(data['zlins_dttm']),
        updated_at=datetime_formating(data['zlupd_dttm']),
    )
