"""This module handles generating and fetching constants and credentials from the database"""

import logging
from datetime import datetime

from mbu_rpa_core.utils.fernet_encryptor import Encryptor

logger = logging.getLogger(__name__)


class Constants:
    """Base class for adding and collection constants and credentials"""

    def add_constant(
        self, constant_name: str, value: str, changed_at: datetime = datetime.now()
    ):
        query = """
            INSERT INTO [RPA].[rpa].[Constants] ([name], [value], [changed_at])
            VALUES (?, ?, ?)
        """
        self.execute_query(query, [constant_name, value, changed_at])

    def get_constant(self, constant_name: str) -> dict:
        query = """
            SELECT name, value FROM [RPA].[rpa].[Constants] WHERE name = ?
        """
        res = self.execute_query(query, [constant_name])
        if res:
            name, value = res[0]
            return {"constant_name": name, "value": value}
        logger.error("No constant found with name: %s", constant_name)
        raise ValueError(f"No constant found with name: {constant_name}")

    def update_constant(
        self, constant_name: str, new_value: str, changed_at: datetime | None = None
    ):
        if not new_value:
            logger.error("new_value must be provided")
            raise ValueError("new_value must be provided")

        if changed_at is None:
            changed_at = datetime.now()

        query = """
            UPDATE [RPA].[rpa].[Constants]
            SET
                value = ?,
                changed_at = ?
            WHERE
                name = ?
        """

        self.execute_query(query, [new_value, changed_at, constant_name])

        if not self.get_constant(constant_name):
            logger.error("No constant found with name: %s", constant_name)
            raise ValueError(f"No constant found with name: {constant_name}")

    def add_credential(
        self,
        credential_name: str,
        username: str,
        password: str,
        changed_at: datetime = datetime.now(),
    ):
        encryptor = Encryptor()
        encrypted_password = encryptor.encrypt(password)
        query = """
            INSERT INTO [RPA].[rpa].[Credentials] ([name], [username], [password], [changed_at])
            VALUES (?, ?, ?, ?)
        """
        self.execute_query(
            query, [credential_name, username, encrypted_password, changed_at]
        )

    def get_credential(self, credential_name: str) -> dict:
        encryptor = Encryptor()
        query = """
            SELECT username, CAST(password AS varbinary(max))
            FROM [RPA].[rpa].[Credentials]
            WHERE name = ?
        """
        res = self.execute_query(query, [credential_name])
        if res:
            username, encrypted_password = res[0]
            decrypted_password = encryptor.decrypt(encrypted_password)
            return {
                "username": username,
                "decrypted_password": decrypted_password,
                "encrypted_password": encrypted_password,
            }
        logger.error("No credential found with name %s", credential_name)
        raise ValueError(f"No credential found with name {credential_name}")

    def update_credential(
        self,
        credential_name: str,
        new_username: str | None = None,
        new_password: str | None = None,
        changed_at: datetime | None = None,
    ):
        if not new_username and not new_password:
            logger.error(
                "At least one of new_username or new_password must be provided"
            )
            raise ValueError(
                "At least one of new_username or new_password must be provided"
            )

        if changed_at is None:
            changed_at = datetime.now()

        fields = []
        values = []

        if new_username:
            fields.append("username = ?")
            values.append(new_username)

        if new_password:
            encryptor = Encryptor()
            encrypted_password = encryptor.encrypt(new_password)
            fields.append("password = ?")
            values.append(encrypted_password)

        fields.append("changed_at = ?")
        values.append(changed_at)

        query = f"""
            UPDATE [RPA].[rpa].[Credentials]
            SET {", ".join(fields)}
            WHERE name = ?
        """

        values.append(credential_name)

        self.execute_query(query, values)

        if not self.get_credential(credential_name):
            logger.error("No constant found with name: %s", credential_name)
            raise ValueError(f"No constant found with name: {credential_name}")
