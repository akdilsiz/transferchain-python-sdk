import hashlib
import binascii
import x25519
import ed25519
import base58


def create_keys_with_mnemonic(keys, password):
    """
    Create cryptographic keys from a mnemonic phrase and a password.
    This function takes a 24-word mnemonic phrase and a password,
    and using them, it generates cryptographic keys. It follows these steps:

    1. A salt is created by combining the word 'mnemonic' with the
    provided password.

    2. The PBKDF2-HMAC-SHA256 key derivation function is applied to the
    mnemonic phrase using the salt and other parameters.

    3. The resulting binary data is converted to a hexadecimal seed.

    4. The seed is used to generate cryptographic keys using a separate
    function called 'generate_keys'.

    5. The generated cryptographic keys, including public and private keys,
    are returned as a dictionary.

    Exception:
        If the 'keys' parameter is empty or invalid, an Exception is raised,
        indicating an issue with the provided mnemonic phrase

    Parameters:
        keys (Mnemonic phrase (str)):
            24-word mnemonic phrase for cryptographic purposes.

        password (str):
            A password used to generate the cryptographic keys.

    Returns:
        Cryptographic keys (dict): A dictionary containing public and
        private cryptographic keys.

    Example:
        -
    ```
        from transferchain.crypt import keys
        _keys = keys.create_keys_with_mnemonic('test mnemonics', 'password')
    ```
    """
    if not keys:
        raise Exception('invalid keys')

    salt = 'mnemonic{}'.format(password)
    dk = hashlib.pbkdf2_hmac(
        'sha256',
        keys.encode('utf-8'),
        salt.encode('utf-8'),
        2048,
        32)
    seed = binascii.hexlify(dk).decode('utf-8')
    keys = generate_keys(seed)
    return keys


def generate_ed25519_keypair_from_seed(seed):
    """
    Generate an Ed25519 key pair from a given seed.
    This function takes a hexadecimal seed and generates an Ed25519
    key pair using the seed as a starting point. The key pair consists
    of a private key and a corresponding public key. The keys are
    returned as a tuple, with the private key first and the public key second.

    Note: Ed25519 is a popular public-key signature system used for secure
    digital signatures and encryption.


    Exception:
        If the provided seed is invalid or empty, an Exception is raised,
        indicating an issue with the seed.

    Parameters:
        seed (str):
             A hexadecimal seed used to generate the key pair.

    Returns:
        Ed25519 key pair (tuple): A tuple containing the private and
        public keys in hexadecimal form.

    Example:
        -
    ```
        from transferchain.crypt import keys
        seen = 'd02552defcf487c2e8c623925479d079f203bf8ab945ceb97f4cc30c42bf75e3'
        result = keys.generate_ed25519_keypair_from_seed(seed)
    ```
    """
    seed_bytes = bytes.fromhex(seed)
    key_pair = ed25519.SigningKey(seed_bytes)
    private_key_hex = key_pair.to_ascii(encoding='hex').decode('utf-8')
    public_key_hex = key_pair.get_verifying_key().to_ascii(
        encoding='hex').decode('utf-8')
    return private_key_hex, public_key_hex


def curve25519_scalar_base_mult(seed):
    """
    Perform scalar multiplication on the base point of the Curve25519
    elliptic curve using a given seed.
    This function performs scalar multiplication on the base point
    of the Curve25519 elliptic curve using the provided seed.
    It results in a public key, which is returned in hexadecimal format.

    Note: Curve25519 is an elliptic curve cryptography system known for
    its security and performance in various cryptographic applications.

    Exception:
        If the provided seed is invalid or empty, an Exception is raised,
        indicating an issue with the seed.

    Parameters:

        seed (str):
             A hexadecimal seed used to generate the key pair.

    Returns:
        Ed25519 key pair (tuple): A tuple containing the private and
        public keys in hexadecimal form.

    Example:
        -
    ```
        from transferchain.crypt import keys
        seen = 'd02552defcf487c2e8c623925479d079f203bf8ab945ceb97f4cc30c42bf75e3'
        result = keys.keys.curve25519_scalar_base_mult(seed)
    ```
    """
    private_key = bytes.fromhex(seed)
    public_key = x25519.scalar_base_mult(private_key)
    return public_key.hex()


def base58_encode(e):
    """
    Encode a hexadecimal value using the Base58 encoding.
    This function takes a hexadecimal value as input and encodes
    it using the Base58 encoding scheme. Base58 encoding is commonly
    used in various cryptographic and blockchain applications to
    represent data in a more compact and human-readable format.

    Exception:
        If the provided hexadecimal value is invalid or empty,
        an Exception is raised, indicating an issue with the input.

    Parameters:
        e (Hexadecimal value (str)):
            The hexadecimal value to be encoded.

    Returns:
        Base58-encoded value (str): The Base58-encoded representation
        of the input hexadecimal value.

    Example:
        -
    ```
        from transferchain.crypt import keys
        seen = 'd02552defcf487c2e8c623925479d079f203bf8ab945ceb97f4cc30c42bf75e3'
        result = keys.generate_keys(seed)
    ```
    """
    return base58.b58encode(bytes.fromhex(e)).decode('utf-8')


def generate_keys(seed):
    """
    Generate a set of cryptographic keys and related values from a
    given seed.This function generates a set of cryptographic keys
    and related values from the provided seed. It performs the
    following operations:

    1. Calculates a public key for encryption using the Curve25519
       elliptic curve.

    2. Generates an Ed25519 key pair for digital signatures.

    3. Combines the private and public keys into a single private key.

    4. Encodes the seed, public keys, and various values in Base58 format.

    5. Constructs an address using the public keys.

    The result is returned as a dictionary containing the seed,
    Base58-encoded values, private and public keys, and the address.

    Exception:
        If the provided seed is invalid or empty, an Exception is raised,
        indicating an issue with the seed.

    Parameters:

        seed (str):
             A hexadecimal seed used as the basis for key generation.

    Returns:
        Key-related values (dict): A dictionary containing
        various key-related values.

    Example:
        -
    ```
        from transferchain.crypt import keys
        seen = 'd02552defcf487c2e8c623925479d079f203bf8ab945ceb97f4cc30c42bf75e3'
        result = keys.generate_keys(seed)
    ```
    """
    if not seed:
        raise Exception('invalid seed')

    public_key_encrypt = curve25519_scalar_base_mult(seed)

    private_key_ed, public_key = generate_ed25519_keypair_from_seed(seed)
    private_key = "{}{}".format(private_key_ed, public_key)
    seed58 = base58_encode(seed)
    public_key_sign58 = base58_encode(public_key)
    public_key_encrypt58 = base58_encode(public_key_encrypt)
    address = base58_encode(public_key + public_key_encrypt)

    result = {
        'Seed': seed,
        'Seed58': seed58,
        'PrivateKeySign': private_key,
        'PublicKeySign': public_key,
        'PublicKeySign58': public_key_sign58,
        'PublicKeyEncrypt': public_key_encrypt,
        'PublicKeyEncrypt58': public_key_encrypt58,
        'Address': address
    }
    return result
