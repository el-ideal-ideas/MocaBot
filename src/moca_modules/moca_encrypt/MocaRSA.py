# -- Imports --------------------------------------------------------------------------

from typing import (
    Union, Optional, Tuple
)
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from Crypto import Random
from base64 import b64encode, b64decode
from pathlib import Path

# -------------------------------------------------------------------------- Imports --

# -- Moca RSA --------------------------------------------------------------------------


class MocaRSA:
    """
    RSA encryption.

    Attributes
    ----------
    self._passphrase: Optional[str]
        the passphrase.
    self._private_key: Optional[bytes]
        the private key.
    self._public_key: Optional[bytes]
        the public key.
    self._key: Optional[RsaKey]
        the RsaKey object.
    """

    def __init__(self, passphrase: Optional[str] = None):
        self._passphrase: Optional[str] = passphrase
        self._private_key: Optional[bytes] = None
        self._public_key: Optional[bytes] = None
        self._key: Optional[RsaKey] = None

    def generate_new_key(self) -> Tuple[bytes, bytes]:
        key = RSA.generate(2048)
        private_key = key.export_key(passphrase=self._passphrase, pkcs=8,
                                     protection="scryptAndAES128-CBC")
        public_key = key.publickey().export_key()
        self._private_key = private_key
        self._public_key = public_key
        self._key = key
        return private_key, public_key

    @staticmethod
    def generate_key(passphrase: Optional[str] = None) -> Tuple[bytes, bytes]:
        key = RSA.generate(2048)
        if passphrase is None:
            private_key = key.export_key(pkcs=8, protection="scryptAndAES128-CBC")
        else:
            private_key = key.export_key(passphrase=passphrase, pkcs=8, protection="scryptAndAES128-CBC")
        public_key = key.publickey().export_key()
        return private_key, public_key

    def get_key_object(self) -> RsaKey:
        if self._key is None:
            self.generate_new_key()
        return self._key

    def get_public_key(self) -> bytes:
        if self._public_key is None:
            return self.generate_new_key()[1]
        else:
            return self._public_key

    def get_private_key(self) -> bytes:
        if self._private_key is None:
            return self.generate_new_key()[0]
        else:
            return self._private_key

    def get_keys(self) -> Tuple[bytes, bytes]:
        if self._private_key is None:
            return self.generate_new_key()
        else:
            return self._private_key, self._public_key

    def save_private_key(self, filename: Union[Path, str]) -> None:
        with open(str(filename), mode='wb') as f:
            f.write(self.get_private_key())

    def save_public_key(self, filename: Union[Path, str]) -> None:
        with open(str(filename), mode='wb') as f:
            f.write(self.get_public_key())

    def load_key(self, filename: Union[Path, str]) -> Tuple[bytes, bytes]:
        with open(str(filename), mode='rb') as f:
            key = RSA.importKey(f.read(), passphrase=self._passphrase)
            private_key = key.export_key(passphrase=self._passphrase, pkcs=8,
                                         protection="scryptAndAES128-CBC")
            public_key = key.publickey().export_key()
            self._private_key = private_key
            self._public_key = public_key
            self._key = key
            return private_key, public_key

    def encrypt(self, data: bytes) -> bytes:
        # Encrypt the session key with the public RSA key
        session_key = Random.get_random_bytes(16)
        cipher_rsa = PKCS1_OAEP.new(self.get_key_object())
        enc_session_key = cipher_rsa.encrypt(session_key)
        # Encrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(data)
        return enc_session_key + cipher_aes.nonce + tag + ciphertext

    def decrypt(self, data: bytes) -> bytes:
        size = self.get_key_object().size_in_bytes()
        enc_session_key, nonce, tag, ciphertext = \
            data[:size], data[size:size + 16], data[size + 16:size + 32], data[size + 32:]
        # Decrypt the session key with the private RSA key
        cipher_rsa = PKCS1_OAEP.new(self.get_key_object())
        session_key = cipher_rsa.decrypt(enc_session_key)
        # Decrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
        return data

    def encrypt_string(self, text: str) -> str:
        return b64encode(self.encrypt(text.encode())).decode()

    def decrypt_string(self, text: str) -> str:
        return self.decrypt(b64decode(text)).decode()

    def signature(self, data: bytes) -> bytes:
        hash_data = SHA256.new(data)
        signature = pkcs1_15.new(self.get_key_object()).sign(hash_data)
        return signature

    def verify(self, data: bytes, signature: bytes) -> bool:
        hash_data = SHA256.new(data)
        try:
            pkcs1_15.new(self.get_key_object()).verify(hash_data, signature)
            verified = True
        except ValueError:
            verified = False
        return verified

# -------------------------------------------------------------------------- Moca RSA --
