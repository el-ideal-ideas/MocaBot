# -- Imports --------------------------------------------------------------------------

from typing import (
    Union
)
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from base64 import b64encode, b64decode

# -------------------------------------------------------------------------- Imports --

# -- Variables --------------------------------------------------------------------------

MODE_ECB = 1
MODE_CBC = 2
MODE_CFB = 3
MODE_OFB = 5
MODE_CTR = 6
MODE_OPENPGP = 7
MODE_CCM = 8
MODE_EAX = 9
MODE_SIV = 10
MODE_GCM = 11
MODE_OCB = 12

# -------------------------------------------------------------------------- Variables --

# -- MocaAES --------------------------------------------------------------------------


class MocaAES:
    """
    AES encryption.

    Attributes
    ----------
    self._pass: bytes
        the password.
    """

    MODE_ECB = 1
    MODE_CBC = 2
    MODE_CFB = 3
    MODE_OFB = 5
    MODE_CTR = 6
    MODE_OPENPGP = 7
    MODE_CCM = 8
    MODE_EAX = 9
    MODE_SIV = 10
    MODE_GCM = 11
    MODE_OCB = 12

    def __init__(self, password: Union[str, bytes]):
        sha256_hash = SHA256.new()
        sha256_hash.update(password if isinstance(password, bytes) else password.encode())
        hashed_key = sha256_hash.digest()
        self._pass: bytes = hashed_key

    def encrypt(self, data: bytes, mode: int = 9) -> bytes:
        """
        MODE_ECB = 1
        MODE_CBC = 2
        MODE_CFB = 3
        MODE_OFB = 5
        MODE_CTR = 6
        MODE_OPENPGP = 7
        MODE_CCM = 8
        MODE_EAX = 9
        MODE_SIV = 10
        MODE_GCM = 11
        MODE_OCB = 12
        """
        cipher = AES.new(self._pass, mode, Random.new().read(AES.block_size))
        ciphertext, tag = cipher.encrypt_and_digest(data)
        data = cipher.nonce + tag + ciphertext
        return data

    def decrypt(self, data: bytes, mode: int = 9) -> bytes:
        """
        MODE_ECB = 1
        MODE_CBC = 2
        MODE_CFB = 3
        MODE_OFB = 5
        MODE_CTR = 6
        MODE_OPENPGP = 7
        MODE_CCM = 8
        MODE_EAX = 9
        MODE_SIV = 10
        MODE_GCM = 11
        MODE_OCB = 12
        """
        nonce, tag, ciphertext = data[:16], data[16:32], data[32:]
        cipher = AES.new(self._pass, mode, nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)
        return data

    def encrypt_string(self, text: str, mode: int = 9) -> str:
        """
        MODE_ECB = 1
        MODE_CBC = 2
        MODE_CFB = 3
        MODE_OFB = 5
        MODE_CTR = 6
        MODE_OPENPGP = 7
        MODE_CCM = 8
        MODE_EAX = 9
        MODE_SIV = 10
        MODE_GCM = 11
        MODE_OCB = 12
        """
        return b64encode(self.encrypt(text.encode(), mode)).decode()

    def decrypt_string(self, text: str, mode: int = 9) -> str:
        """
        MODE_ECB = 1
        MODE_CBC = 2
        MODE_CFB = 3
        MODE_OFB = 5
        MODE_CTR = 6
        MODE_OPENPGP = 7
        MODE_CCM = 8
        MODE_EAX = 9
        MODE_SIV = 10
        MODE_GCM = 11
        MODE_OCB = 12
        """
        return self.decrypt(b64decode(text), mode).decode()

# -------------------------------------------------------------------------- MocaAES --
