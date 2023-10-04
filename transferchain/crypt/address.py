import base58


def public_key_sign_from_address(address):
    result = base58.b58decode(address).hex()[:64]
    length = len(result)
    if length == 0 or length != 64:
        raise Exception('invalid address')
    return result


def public_key_encrypt_from_address(address):
    result = base58.b58decode(address).hex()[64:]
    length = len(result)
    if length == 0 or length != 64:
        raise Exception('invalid address')
    return result
