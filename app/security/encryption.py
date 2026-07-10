import base64
import hashlib

from app.config.settings import settings


class EncryptionHelper:
    @staticmethod
    def _key_stream(length):
        key = settings.ENCRYPTION_KEY or settings.JWT_SECRET_KEY or "fraudshield-local-key"
        digest = hashlib.sha256(key.encode("utf-8")).digest()
        return (digest * ((length // len(digest)) + 1))[:length]

    @classmethod
    def encrypt(cls, value):
        raw = value.encode("utf-8")
        key_stream = cls._key_stream(len(raw))
        encrypted = bytes(byte ^ key_stream[index] for index, byte in enumerate(raw))
        return base64.urlsafe_b64encode(encrypted).decode("utf-8")

    @classmethod
    def decrypt(cls, token):
        encrypted = base64.urlsafe_b64decode(token.encode("utf-8"))
        key_stream = cls._key_stream(len(encrypted))
        raw = bytes(byte ^ key_stream[index] for index, byte in enumerate(encrypted))
        return raw.decode("utf-8")
