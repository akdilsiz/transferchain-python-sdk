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
    """
    Encrypt data asymmetrically using sender's key and recipient's public key.
    This function encrypts the provided data asymmetrically using the
    sender's private key seed and the recipient's public key. It returns the encrypted data.

    Parameters:
        sender_key_seed: Sender's key seed (str): 
            The sender's private key seed for encryption.

        recipient_key: Recipient's public key (str):
            The recipient's public key for encryption.

        data: Data (bytes):
            The data to be encrypted.

    Returns:
        Encrypted data (bytes): The encrypted data.

    Example:
        -
    ```
        from transferchain.crypt import bip39
        from transferchain.crypt import keys
        from transferchain.crypt import crypt
        message = b'alles gut'
        sender_mnemonics = bip39.create_mnomonics()
        sender = keys.create_keys_with_mnemonic(sender_mnemonics, 'p1')

        recipient_mnemonics = bip39.create_mnomonics()
        recipient = keys.create_keys_with_mnemonic(recipient_mnemonics, 'p2')

        encrypted_data = crypt.encrypt_asymmetric(
            sender['Seed'], recipient['Address'], message)
    ```
    """
    recipient_pub_key = address.public_key_encrypt_from_address(recipient_key)
    sk = PrivateKey(private_key=bytes.fromhex(sender_key_seed))
    pk = PublicKey(public_key=bytes.fromhex(recipient_pub_key))
    nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
    box = Box(sk, pk)
    encrypted = box.encrypt(data, nonce)
    return encrypted


def decrypt_asymmetric(sender_address, recipient_seed, encrypted_data):
    """
    Decrypt asymmetrically encrypted data using sender's address and
    recipient's private key seed.This function decrypts asymmetrically
    encrypted data using the sender's address and the recipient's private
    key seed. It returns the decrypted data.

    Exception:
        If the length of the given address is not 64 characters or is empty,
        an Exception is raised, indicating the use of an invalid address.

    Parameters:
        sender_address: Sender's address (str):
            The sender's address.

        recipient_seed: Recipient's private key seed (str):
            The recipient's private key seed for decryption.

        encrypted_data: Encrypted data (bytes):
            The data to be decrypted.

    Returns:
        Decrypted data (bytes): The decrypted data.

    Example:
        -
    ```
        from transferchain.crypt import bip39
        from transferchain.crypt import keys
        from transferchain.crypt import crypt
        message = b'alles gut'
        sender_mnemonics = bip39.create_mnomonics()
        sender = keys.create_keys_with_mnemonic(sender_mnemonics, 'p1')

        recipient_mnemonics = bip39.create_mnomonics()
        recipient = keys.create_keys_with_mnemonic(recipient_mnemonics, 'p2')

        encrypted_data = crypt.encrypt_asymmetric(
            sender['Seed'], recipient['Address'], message)
        decrypted_data = crypt.decrypt_asymmetric(
            sender['Address'], recipient['Seed'], encrypted_data)
    ```
    """
    sender_pub_key = address.public_key_encrypt_from_address(
        sender_address)
    sk = PrivateKey(private_key=bytes.fromhex(recipient_seed))
    pk = PublicKey(public_key=bytes.fromhex(sender_pub_key))
    box = Box(sk, pk)
    return box.decrypt(encrypted_data[24:], encrypted_data[:24])


def sign(private_key_sign, data):
    """
    Sign data using a private signing key.
    This function signs the provided data using the given
    private signing key and returns the digital signature.

    Parameters:
        private_key_sign: Private signing key (str):
            The private key used for signing.

        data: Data (bytes):
            The data to be signed.

    Returns:
        Signature (bytes): The digital signature of the data.

    Example:
        -
    ```
        from transferchain.crypt import bip39
        from transferchain.crypt import keys
        from transferchain.crypt import crypt
        pks = 'a0c4e141c6273b9cfd0ffd4ac64110b31189b7051066e92e45ba4534a8a12008baa5f1b8e00a76e8342bb31b105c396d423d9e897df7a290e55fca4ba8249c79' # noqa
        result = crypt.sign(pks, b'alles gut')
    ```
    """
    signing_key = ed25519.SigningKey(bytes.fromhex(private_key_sign))
    return signing_key.sign(data)


def verify_sign(key_address, data, sign):
    """
    Verify a digital signature using the public key.
    This function verifies a digital signature using the public key
    associated with the provided address. It returns True if the
    signature is valid, and False otherwise.

    Parameters:
        key_address: Key address (str):
            The address associated with the public key.

        data: Data (bytes):
            The data to be verified.

        sign: Digital signature (bytes):
            The signature to be verified.
    
    Returns:
        Verification result (bool): True if the signature is valid, False otherwise.

    Example:
        -
    ```
        from transferchain.crypt import bip39
        from transferchain.crypt import keys
        from transferchain.crypt import crypt

        mnemonics = bip39.create_mnomonics()
        keys_ = keys.create_keys_with_mnemonic(mnemonics, 'p2')
        data = b'alles gut'
        sign_key = crypt.sign(keys_['PrivateKeySign'], data)
        result = crypt.verify_sign(keys_['Address'], data, sign_key)
    ```
    """
    try:
        pub_key = address.public_key_sign_from_address(key_address)
        verification_key = ed25519.VerifyingKey(bytes.fromhex(pub_key))
        verification_key.verify(sign, data)
        return True
    except Exception:
        return False


def generate_encrypt_key(size):
    """
    Generate a random encryption key of the specified size.
    This function generates a random encryption key of the
    specified size and returns it as a hexadecimal string.

    Parameters:
        size: Key size (int):
            The size of the encryption key.

    Returns:
        Encryption key (str): A randomly generated encryption key of the specified size.

    Example:
        -
    ```
        from transferchain.crypt import crypt

        result = crypt.generate_encrypt_key(10)
    ```
    """
    return bytearray(secrets.randbits(8) for _ in range(size)).hex()[:size]


def hash_to_32_bytes(input_str):
    """
    Calculate the SHA-256 hash of a string and return the
    result as 32 bytes.This function calculates the SHA-256
    hash of the provided string and returns the result as 32 bytes.

    Parameters:
        input_str: Input string (str):
            The string to be hashed.

    Returns:
        Hash result (bytes): The SHA-256 hash result as 32 bytes.

    Example:
        -
    ```
        from transferchain.crypt import crypt

        crypt.hash_to_32_bytes('test)
    ```
    """
    input_bytes = input_str.encode('utf-8')
    sha256 = hashes.Hash(hashes.SHA256(), backend=default_backend())
    sha256.update(input_bytes)
    hash_result = sha256.finalize()
    return hash_result


def encrypt_byte(plaintext, key):
    """
    Encrypt a plaintext using AES-GCM with a given key.
    This function encrypts the provided plaintext using the AES-GCM
    encryption algorithm with the specified key and returns the
    encrypted data.

    Parameters:
        plaintext: Plaintext (bytes):
            The data to be encrypted.

        key: Encryption key (str):
            The encryption key used for encryption.

    Returns:
        Encrypted data (bytes): The encrypted data.

    Example:
        -
    ```
        from transferchain.crypt import crypt

        message = b'alles gut'
        key = 'secret_key'
        enc_result = crypt.encrypt_byte(message, key)
    ```
    """
    new_key = hash_to_32_bytes(key)
    iv = os.urandom(IV_SIZE)
    cipher = Cipher(algorithms.AES(new_key), modes.GCM(iv),
                    backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return iv + ciphertext + encryptor.tag


def decrypt_aesctr_with_hmac(infile, outfile, aes_key, hmac_key):
    """
    Decrypt a file encrypted using AES-CTR mode with HMAC-based
    integrity checks.This function decrypts a file that was
    previously encrypted using AES-CTR mode with HMAC-based
    integrity checks. It reads the encrypted input file, verifies
    the HMAC-based integrity, and writes the decrypted data to
    the output file.

    Exception:
        If the provided input file is invalid, has an invalid version,
        or the HMAC verification fails, an Exception is raised,
        indicating an issue with the input or the file's integrity.

    Parameters:
        infile: Encrypted input file (file object):
            The file to be decrypted.

        outfile: Decrypted output file (file object):
            The file to store the decrypted data.

        aes_key: AES encryption key (str):
            The key used for AES decryption.

        hmac_key: HMAC key (str):
            The key used for HMAC-based integrity checks.

    Example:
        -
    ```
    from transferchain.crypt import crypt

    input_file_path = 'encrypted_file.bin'
    output_file_path = 'decrypted_file.txt'

    aes_key = 'your_aes_key_here'
    hmac_key = 'your_hmac_key_here'

    try:
        with open(input_file_path, 'rb') as encrypted_file, open(output_file_path, 'wb') as decrypted_file:
            crypt.decrypt_aesctr_with_hmac(encrypted_file, decrypted_file, aes_key, hmac_key)
        print(f'Decryption successful. Decrypted file saved to {output_file_path}')
    except Exception as e:
        print(f'Error: {e}')
    ```
    """
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
    """
    Encrypt a file using AES-CTR mode with HMAC-based integrity checks.
    This function encrypts the provided input file using AES-CTR mode
    with HMAC-based integrity checks. It writes the encrypted data to
    the output file and returns the total number of bytes written.
    Note: The function uses a random initialization vector (IV)
    and calculates an HMAC-based digest for data integrity.

    Exception:
        If the provided input file or keys are invalid,
        an Exception is raised, indicating an issue with the inputs.

    Parameters:
        infile: Input file (file object):
            The file to be encrypted.

        outfile: Output file (file object):
            The file to store the encrypted data.

        aes_key: AES encryption key (str):
            The key used for AES encryption.

        hmac_key: HMAC key (str):
            The key used for HMAC-based integrity checks.

    Returns:
        Total bytes written (int): The total number of
        bytes written to the output file.

    Example:
        -
    ```
    from transferchain.crypt import crypt

    input_file_path = 'unencrypted_file.txt'
    output_file_path = 'encrypted_file.bin'

    aes_key = 'your_aes_key_here'
    hmac_key = 'your_hmac_key_here'

    try:
        with open(input_file_path, 'rb') as unencrypted_file, open(output_file_path, 'wb') as encrypted_file:
            total_bytes_written = crypt.encrypt_aesctr_with_hmac(unencrypted_file, encrypted_file, aes_key, hmac_key)
        print(f'Encryption successful. Encrypted file saved to {output_file_path}.')
        print(f'Total bytes written: {total_bytes_written}')
    except Exception as e:
        print(f'Error: {e}')
    ```
    """
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
    """
    Decrypt encrypted data using AES-GCM with a given key.
    This function decrypts the provided encrypted data using
    the AES-GCM decryption algorithm with the specified key
    and returns the decrypted data.

    Parameters:
        encrypted_data: Encrypted data (bytes):
            The data to be decrypted.

        key: Decryption key (str):
            The decryption key used for decryption.

    Returns:
        Decrypted data (bytes): The decrypted data.

    Example:
        -
    ```
        from transferchain.crypt import crypt

        message = b'alles gut'
        key = 'secret_key'
        enc_result = crypt.encrypt_byte(message, key)
        dec_result = crypt.decrypt_byte(enc_result, key)
    ```
    """
    new_key = hash_to_32_bytes(key)
    cipher = Cipher(algorithms.AES(new_key),
                    modes.GCM(encrypted_data[:IV_SIZE],
                              encrypted_data[-IV_SIZE:]),
                    backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(encrypted_data[IV_SIZE:-IV_SIZE]) \
        + decryptor.finalize()
