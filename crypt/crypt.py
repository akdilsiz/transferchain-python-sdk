import os
import ed25519
import nacl.secret
import nacl.utils
from nacl.public import PrivateKey, Box, PublicKey
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import secrets
import address


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
    nonce = os.urandom(16)
    cipher = Cipher(algorithms.AES(new_key), modes.GCM(nonce),
                    backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return nonce + ciphertext + encryptor.tag


def decrypt_byte(encrypted_data, key):
    new_key = hash_to_32_bytes(key)
    cipher = Cipher(algorithms.AES(new_key),
                    modes.GCM(encrypted_data[:16], encrypted_data[-16:]),
                    backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(encrypted_data[16:-16]) + decryptor.finalize()
