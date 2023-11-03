import hashlib
import secrets
from transferchain.crypt.words import word_list


def create_mnomonics():
    """
    Generate a 24-word mnemonic phrase for cryptographic purposes.

    Returns:
        Mnemonic phrase (str): A 24-word phrase for cryptographic use.

    Example:
        -
    ```
        from transferchain.crypt import bip39
        result = bip39.create_mnomonics()
    ```
    """
    chunk_size = 11
    entropy = bytearray(secrets.randbits(8) for _ in range(int(256 / 8)))
    final_entropy = checksum(entropy)
    entropy_length = len(final_entropy)
    words = [''] * 24

    for i in range(0, entropy_length, chunk_size):
        val = final_entropy[i: chunk_size + i]
        int_val = int(''.join(val), 2)
        word = word_list[int_val]
        words[int((chunk_size + i) / 11 - 1)] = word
    return ' '.join(words)


def bytes_to_bits(byte_array):
    """
    Convert a byte array to a list of bits.
    This function takes a byte array and converts it into a list of bits,
    which can be used in various cryptographic operations.

    Parameters:
        byte_array (Byte array (bytearray)):
            The byte array to convert to bits.
    Returns:
        List of bits (list): A list of bits representing the byte array.

    Example:
        -
    ```
        from transferchain.crypt import bip39
        result = bip39.bytes_to_bits(b'test')
    ```
    """
    length = len(byte_array)
    bits = [0] * (length * 8)

    for i in range(length):
        b = byte_array[i]
        for j in range(8):
            mask = 1 << j
            bit = b & mask
            if bit == 0:
                bits[(i * 8) + 8 - (j + 1)] = '0'
            else:
                bits[(i * 8) + 8 - (j + 1)] = '1'
    return bits


def checksum(e):
    """
    Calculate a checksum for a given byte array.
    This function computes a checksum for a given byte array and
    returns the checksum bits, which are often used in cryptographic
    processes to ensure data integrity.

    Parameters:
        e (Byte array (bytearray)):
            The byte array for which the checksum will be calculated.

    Returns:
        Checksum bits (list): The calculated checksum bits.

    Example:
        -
    ```
        from transferchain.crypt import bip39
        result = bip39.checksum(b'test')
    ```
    """
    _h = hashlib.sha256(e)
    bits = bytes_to_bits(_h.digest())
    cur = int(len(e) * 8 / 32)
    cs = bits[:cur]
    bits = bytes_to_bits(e)
    bits.extend(cs)
    return bits
