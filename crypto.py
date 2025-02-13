from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.hmac import HMAC
from cryptography.hazmat.primitives.hashes import SHA256
import os, secrets

def generate_key(length: int) -> bytes:
    '''
    Generates a secure cryptographic key.

    Args:
        length (int): Length (in bytes) of the generated cryptographic key.

    Returns:
        bytes: The generated random key.
    '''

    return secrets.token_bytes(length)

def generate_keys(vault_size: int, key_size: int) -> list:
    '''
    Generates a set of keys.

    Args:
        vault_size (int): The size of the set of keys.
        key_size (int): The size of the keys.

    Returns:
        list: The set of keys generated.
    '''

    vault = list()

    for _ in range(vault_size):

        vault.append(generate_key(key_size))

    return vault

def encrypt(data: bytes, key: bytes) -> bytes:
    '''
    Encrypts data given a secure cryptographic key.

    Args:
        data (bytes): The information desired for encryption.
        key (bytes): The key that will be used for encryption.

    Returns:
        bytes: The encrypted data with the given key.
    '''

    # Generate the random nonce

    nonce = os.urandom(12)

    # Encrypt the given data

    algorithm = AESGCM(key)

    return (nonce + algorithm.encrypt(nonce, data, None))

def decrypt(data: bytes, key: bytes, nonce: bytes) -> bytes:
    '''
    Decrypts data given a secure cryptographic key.

    Args:
        data (bytes): The information desired for decryption.
        key (bytes): The key that will be used for decryption.
        nonce (bytes): The nonce used for encryption.

    Returns:
        bytes: The decrypted data with the given key.
    '''

    # Decrypt the given data

    algorithm = AESGCM(key)

    return algorithm.decrypt(nonce, data, None)

def hmac(data: bytes, key: bytes) -> bytes:
    '''
    Creates a tag for a given binary information.

    Args:
        data (bytes): The information desired for tag creation.
        key (bytes): The key that will be used for the tag creation.

    Returns:
        bytes: The created tag with the given details.
    '''

    # Create the tag with the SHA256 HMAC algorithm

    algorithm = HMAC(key, SHA256())

    algorithm.update(data)

    return algorithm.finalize()