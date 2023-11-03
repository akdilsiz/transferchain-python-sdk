import base58


def public_key_sign_from_address(address):
    """
    Generate a signed public key from a given cryptocurrency address.
    This function decodes the given cryptocurrency address using base58
    and extracts the first 64 characters in hexadecimal form, which
    represents the signed public key.

    Exception:
        If the length of the given address is not 64 characters or is empty,
        an Exception is raised, indicating the use of an invalid address.

    Parameters:
        address (Cryptocurrency address (str)):
            The address from which the signed public key will be generated.

    Returns:
        Signed public key (str)
        The signed public key derived from the given address.

    Example:
        -
    ```
        from transferchain.crypt import address
        from transferchain.crypt import keys
        _keys = keys.create_keys_with_mnemonic('test mnemonics', 'password')
        result = address.public_key_sign_from_address(_keys['Address'])
    ```
    """
    result = base58.b58decode(address).hex()[:64]
    length = len(result)
    if length == 0 or length != 64:
        raise Exception('invalid address')
    return result


def public_key_encrypt_from_address(address):
    """
    Generate an encrypted public key from a given cryptocurrency address.
    This function decodes the given cryptocurrency address using base58
    and extracts the last 64 characters in hexadecimal form, which
    represents the encrypted public key.

    Exception:
        If the length of the given address is not 64 characters or is empty,
        an Exception is raised, indicating the use of an invalid address.

    Parameters:
        address (Cryptocurrency address (str)):
            The address from which the signed public key will be generated.

    Returns:
        Encrypted public key (str): The encrypted public key derived from
        the given address.

    Example:
        -
    ```
        from transferchain.crypt import address
        from transferchain.crypt import keys
        _keys = keys.create_keys_with_mnemonic('test mnemonics', 'password')
        result = address.public_key_encrypt_from_address(_keys['Address'])
    ```
    """
    result = base58.b58decode(address).hex()[64:]
    length = len(result)
    if length == 0 or length != 64:
        raise Exception('invalid address')
    return result
