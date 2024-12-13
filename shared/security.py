from base64 import b64decode, b64encode
from hashlib import md5

from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes

from setup import config

# AESCipher obtenido de https://gist.github.com/forkd/168c9d74b988391e702aac5f4aa69e41
# Padding for the input string --not
# related to encryption itself.
_BLOCK_SIZE = 16  # Bytes
_pad = lambda s: s + (_BLOCK_SIZE - len(s) % _BLOCK_SIZE) * chr(
    _BLOCK_SIZE - len(s) % _BLOCK_SIZE
)
# Para python 3. El parametro 's' debe ser bytes no str
_pad3 = lambda s: s + (_BLOCK_SIZE - len(s) % _BLOCK_SIZE) * bytes(
    [_BLOCK_SIZE - len(s) % _BLOCK_SIZE]
)
_unpad = lambda s: s[: -ord(s[len(s) - 1 :])]

DEFAULT_MODE_CRYPT = "MODE_GCM"


class AESCipher:
    """
    Usage:
        c = AESCipher('cipher_key').encrypt('string', mode)
        m = AESCipher('cipher_key').decrypt('string', mode)
    """

    def __init__(self, key):
        self.key = md5(key.encode("utf8")).hexdigest().encode("utf8")

    def encrypt(self, raw, mode=DEFAULT_MODE_CRYPT):
        raw = _pad3(raw.encode("utf-8"))
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(self.key, getattr(AES, mode), iv)

        return b64encode(iv + cipher.encrypt(raw)).decode("utf-8")

    def decrypt(self, enc, mode=DEFAULT_MODE_CRYPT):
        enc = b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, getattr(AES, mode), iv)
        return _unpad(cipher.decrypt(enc[16:])).decode("utf-8")


def decrypt_pass(pass_mambu, cipher_mode=DEFAULT_MODE_CRYPT):
    return AESCipher(config.CIPHERKEY).decrypt(pass_mambu, mode=cipher_mode)


def encrypt_pass(pass_mambu, cipher_mode=DEFAULT_MODE_CRYPT):
    return AESCipher(config.CIPHERKEY).encrypt(pass_mambu, mode=cipher_mode)
