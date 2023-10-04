import hashlib
import secrets
from transferchain.crypt.words import word_list


def create_mnomonics():
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
    _h = hashlib.sha256(e)
    bits = bytes_to_bits(_h.digest())
    cur = int(len(e) * 8 / 32)
    cs = bits[:cur]
    bits = bytes_to_bits(e)
    bits.extend(cs)
    return bits
