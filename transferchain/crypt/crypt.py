import os
import hmac
import hashlib
import ed25519
import secrets
import nacl.secret
import nacl.utils
from nacl.public import PrivateKey, Box, PublicKey
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from transferchain.crypt import address


V1 = 0x01
IV_SIZE = 16


def encrypt_asymmetric(sender_key_seed, recipient_key, data):
    recipient_pub_key = address.public_key_encrypt_from_address(recipient_key)
    sk = PrivateKey(private_key=bytes.fromhex(sender_key_seed))
    pk = PublicKey(public_key=bytes.fromhex(recipient_pub_key))
    nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
    box = Box(sk, pk)
    encrypted = box.encrypt(data, nonce)
    return encrypted


def decrypt_asymmetric(sender_address, recipient_seed, encrypted_data):
    sender_pub_key = address.public_key_encrypt_from_address(
        sender_address)
    sk = PrivateKey(private_key=bytes.fromhex(recipient_seed))
    pk = PublicKey(public_key=bytes.fromhex(sender_pub_key))
    box = Box(sk, pk)
    return box.decrypt(encrypted_data[24:], encrypted_data[:24])


def sign(private_key_sign, data):
    signing_key = ed25519.SigningKey(bytes.fromhex(private_key_sign))
    return signing_key.sign(data)


def verify_sign(key_address, data, sign):
    try:
        pub_key = address.public_key_sign_from_address(key_address)
        verification_key = ed25519.VerifyingKey(bytes.fromhex(pub_key))
        verification_key.verify(sign, data)
        return True
    except Exception:
        return False


def generate_encrypt_key(size):
    return bytearray(secrets.randbits(8) for _ in range(size)).hex()[:size]


def hash_to_32_bytes(input_str):
    input_bytes = input_str.encode('utf-8')
    sha256 = hashes.Hash(hashes.SHA256(), backend=default_backend())
    sha256.update(input_bytes)
    hash_result = sha256.finalize()
    return hash_result


def encrypt_byte(plaintext, key):
    new_key = hash_to_32_bytes(key)
    iv = os.urandom(IV_SIZE)
    cipher = Cipher(algorithms.AES(new_key), modes.GCM(iv),
                    backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return iv + ciphertext + encryptor.tag


def decrypt_aesctr_with_hmac(infile, outfile, aes_key, hmac_key):
    # TODO:TEST
    BUFFER_SIZE = 16 * 1024
    offset = 0

    version = infile.read(1)
    offset += 1
    if int(version) != V1:
        raise Exception('invalid version')

    iv = infile.read(IV_SIZE)
    offset += IV_SIZE

    cipher = Cipher(algorithms.AES(aes_key), modes.CTR(iv))
    decryptor = cipher.decryptor()

    hmc = hmac.new(hmac_key, None, hashlib.sha512)
    hmc.update(iv)
    hmac_size = 64

    file_stat = os.stat(infile.name)
    reader_size = file_stat.st_size

    infile_hmac = None
    while True:
        data = infile.read(BUFFER_SIZE)
        if not data:
            break
        limit = len(data)

        if (reader_size < BUFFER_SIZE) \
           or (offset + BUFFER_SIZE >= reader_size):
            limit = len(data) - hmac_size

        d = data[0:limit]
        hmc.update(d)
        result = decryptor.update(d)
        outfile.write(result)
        offset += len(data)

        if offset == reader_size:
            if len(data) < hmac_size:
                raise Exception('hmac size error')
            mac = data[-hmac_size:]
            if len(data[len(data) - hmac_size:]) == hmac_size:
                infile_hmac = mac
                break

    if infile_hmac is None:
        raise Exception('hmac not found')

    if hmac.compare_digest(hmc.digest(), infile_hmac) is False:
        raise Exception('invalid hmac')


def encrypt_aesctr_with_hmac(infile, outfile, aes_key, hmac_key):
    # TODO:TEST
    # we need the test
    # infile/outfile are file objects
    BUFFER_SIZE = 16 * 1024
    iv = os.urandom(IV_SIZE)

    hmc = hmac.new(hmac_key, None, hashlib.sha512)
    cipher = Cipher(algorithms.AES(aes_key), modes.CTR(iv))
    encryptor = cipher.encryptor()

    hmc.update(iv)
    outfile.write("{}".format(V1).encode())
    outfile.write(iv)
    total_count = 0
    while True:
        data = infile.read(BUFFER_SIZE)
        if not data:
            break
        ciphertext = encryptor.update(data)

        hmc.update(ciphertext)
        total_count += outfile.write(ciphertext)
    outfile.write(hmc.digest())
    return total_count


def decrypt_byte(encrypted_data, key):
    new_key = hash_to_32_bytes(key)
    cipher = Cipher(algorithms.AES(new_key),
                    modes.GCM(encrypted_data[:IV_SIZE],
                              encrypted_data[-IV_SIZE:]),
                    backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(encrypted_data[IV_SIZE:-IV_SIZE]) \
        + decryptor.finalize()
