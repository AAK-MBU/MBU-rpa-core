"""
This module provides a class for encrypting and decrypting data using the
Fernet symmetric encryption algorithm.
"""

import base64
import hashlib
import logging
import os

from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)


class Encryptor:
    """
    A class for encrypting and decrypting data using the Fernet symmetric encryption algorithm.
    """

    def __init__(self):
        self.key = os.getenv("OPENORCHESTRATORKEY")
        if not self.key:
            logger.error(
                "Environment variable 'OPENORCHESTRATORKEY' is not set or is empty."
            )
            raise ValueError(
                "Environment variable 'OPENORCHESTRATORKEY' is not set or is empty."
            )
        self.cipher_suite = self.generate_cipher_suite()

    def generate_cipher_suite(self) -> Fernet:
        """
        Generates a Fernet cipher suite using a SHA-256 hash of the provided key.

        Returns:
            Fernet: An instance of the Fernet cipher suite.
        """
        hashed_key = hashlib.sha256(self.key.encode()).digest()
        base64_key = base64.urlsafe_b64encode(hashed_key[:32])
        return Fernet(base64_key)

    def encrypt(self, data: str) -> bytes:
        """
        Encrypts a string.

        Args:
            data (str): The string to be encrypted.

        Returns:
            bytes: The encrypted data.
        """
        if not isinstance(data, str):
            logger.error("Data must be a string.")
            raise TypeError("Data must be a string.")
        encrypted_data = self.cipher_suite.encrypt(data.encode())
        return encrypted_data

    def decrypt(self, cipherdata: bytes) -> str:
        """
        Decrypts data that was encrypted.

        Args:
            cipherdata (bytes): The data to be decrypted.

        Returns:
            str: The decrypted plaintext string.
        """
        if not isinstance(cipherdata, bytes):
            logger.error("Data must be a string.")
            raise TypeError("Cipherdata must be bytes.")
        try:
            decrypted_data = self.cipher_suite.decrypt(cipherdata).decode()
            return decrypted_data
        except Exception as e:
            logger.error("Decryption failed. Ensure the cipherdata is valid.")
            raise ValueError(
                "Decryption failed. Ensure the cipherdata is valid."
            ) from e
