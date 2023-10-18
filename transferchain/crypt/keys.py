import hashlib
import binascii
import x25519
import ed25519
import base58


def create_keys_with_mnemonic(keys, password):
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
    seed_bytes = bytes.fromhex(seed)
    key_pair = ed25519.SigningKey(seed_bytes)
    private_key_hex = key_pair.to_ascii(encoding='hex').decode('utf-8')
    public_key_hex = key_pair.get_verifying_key().to_ascii(
        encoding='hex').decode('utf-8')
    return private_key_hex, public_key_hex


def curve25519_scalar_base_mult(seed):
    private_key = bytes.fromhex(seed)
    public_key = x25519.scalar_base_mult(private_key)
    return public_key.hex()


def base58_encode(e):
    return base58.b58encode(bytes.fromhex(e)).decode('utf-8')


def generate_keys(seed):
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
