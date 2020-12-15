# -- Imports --------------------------------------------------------------------------

from typing import (
    Union, Any
)
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from base64 import b64encode, b64decode
from pathlib import Path
from aiofiles import open as aio_open
try:
    from cloudpickle import dumps, loads
except (ImportError, ModuleNotFoundError):
    from pickle import dumps, loads
from gzip import compress as gzip_compress, decompress as gzip_decompress

# -------------------------------------------------------------------------- Imports --

# -- Variables --------------------------------------------------------------------------

BLOCK_SIZE = 16

# -------------------------------------------------------------------------- Variables --

# -- Private Functions --------------------------------------------------------------------------


def __create_aes(password: Union[str, bytes],
                 iv: bytes):
    """
    create aes object
    :param password: password
    :param iv: initialization vector
    :return: aes object
    """
    sha256_hash = SHA256.new()
    sha256_hash.update(password.encode() if isinstance(password, str) else password)
    hashed_key = sha256_hash.digest()
    return AES.new(hashed_key, AES.MODE_CFB, iv)


def __pad(data):
    length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + (chr(length)*length).encode()


def __unpad(data):
    return data[:-data[-1]]

# -------------------------------------------------------------------------- Private Functions --

# -- Public Functions --------------------------------------------------------------------------


def encrypt(data: bytes,
            password: Union[str, bytes],
            compress: bool = False) -> bytes:
    """
    encrypt data
    :param data: plain data
    :param password: password
    :param compress: compress the encrypted data.
    :return: encrypted data
    """
    iv = Random.new().read(AES.block_size)
    data = iv + __create_aes(password, iv).encrypt(data)
    if compress:
        return b'moca' + gzip_compress(data)
    else:
        return data
    

def decrypt(data: bytes,
            password: Union[str, bytes]) -> bytes:
    """
    decrypt data
    :param data: encrypted data
    :param password: password
    :return: plain data
    """
    __data = gzip_decompress(data[4:]) if data.startswith(b'moca') else data
    iv, cipher = __data[:AES.block_size], __data[AES.block_size:]
    return __create_aes(password, iv).decrypt(cipher)


def encrypt_string(text: str,
                   password: Union[str, bytes]) -> str:
    """
    encrypt string data.
    :param text: target string.
    :param password: password.
    :return: encrypted string.
    """
    encrypted_bytes = encrypt(text.encode(), password)
    return b64encode(encrypted_bytes).decode()


def decrypt_string(text: str,
                   password: Union[str, bytes]) -> str:
    """
    decrypt string data.
    :param text: encrypted string.
    :param password: password.
    :return: plain string.
    """
    plain_bytes = decrypt(b64decode(text), password)
    return plain_bytes.decode()


def encrypt_file(filename: Union[str, Path], password: Union[str, bytes],
                 output: Union[str, Path], compress: bool = False) -> None:
    with open(str(filename), mode='rb') as plain:
        with open(str(output), mode='wb') as encrypted:
            encrypted.write(encrypt(plain.read(), password, compress))


def decrypt_file(filename: Union[str, Path], password: Union[str, bytes], output: Union[str, Path]) -> None:
    with open(str(filename), mode='rb') as encrypted:
        with open(str(output), mode='wb') as plain:
            plain.write(decrypt(encrypted.read(), password))


async def encrypt_file_aio(filename: Union[str, Path], password: Union[str, bytes],
                           output: Union[str, Path], compress: bool = False) -> None:
    async with aio_open(str(filename), mode='rb') as plain:
        async with aio_open(str(output), mode='wb') as encrypted:
            await encrypted.write(encrypt(await plain.read(), password, compress))


async def decrypt_file_aio(filename: Union[str, Path], password: Union[str, bytes], output: Union[str, Path]) -> None:
    async with aio_open(str(filename), mode='rb') as encrypted:
        async with aio_open(str(output), mode='wb') as plain:
            await plain.write(decrypt(await encrypted.read(), password))


def dumps_with_encryption(data: Any, password: Union[str, bytes], compress: bool = False) -> bytes:
    pickled_data = dumps(data)
    return encrypt(pickled_data, password, compress)


def loads_with_encryption(data: bytes, password: Union[str, bytes]) -> Any:
    pickled_data = decrypt(data, password)
    return loads(pickled_data)


def dump_with_encryption(data: Any, filename: Union[str, Path],
                         password: Union[str, bytes], compress: bool = False) -> None:
    with open(str(filename), 'wb') as file:
        file.write(dumps_with_encryption(data, password, compress))
        
        
def load_with_encryption(filename: Union[str, Path], password: Union[str, bytes]) -> Any:
    with open(str(filename), mode='rb') as file:
        return loads_with_encryption(file.read(), password)


async def dump_with_encryption_aio(data: Any, filename: Union[str, Path],
                                   password: Union[str, bytes], compress: bool = False) -> None:
    async with aio_open(str(filename), 'wb') as file:
        await file.write(dumps_with_encryption(data, password, compress))


async def load_with_encryption_aio(filename: Union[str, Path], password: Union[str, bytes]) -> Any:
    async with aio_open(str(filename), mode='rb') as file:
        return loads_with_encryption(await file.read(), password)


def pyjs_encrypt(msg: bytes, key: bytes) -> bytes:
    """
    This function is compatible with sa_code.aes.pyJsDecrypt
    The length of the key must be 16 characters.
    """
    iv = Random.new().read(BLOCK_SIZE)
    aes = AES.new(key, AES.MODE_CBC, iv)
    return b64encode(iv + aes.encrypt(__pad(msg)))


def pyjs_decrypt(msg: bytes, key: bytes) -> bytes:
    """T
    This function is compatible with sa_code.aes.pyJsEncrypt
    The length of the key must be 16 characters.
    """
    encrypted = b64decode(msg)
    iv = encrypted[:BLOCK_SIZE]
    aes = AES.new(key, AES.MODE_CBC, iv)
    return __unpad(aes.decrypt(encrypted[BLOCK_SIZE:]))


# -------------------------------------------------------------------------- Public Functions --
