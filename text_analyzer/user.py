"""
This module defines the User class, extending the Entity abstract base class,
to represent user entities with functionalities for email validation, password hashing, and API key management.
"""

import hashlib
import re
import secrets

from .base import Entity


class User(Entity):
    """
    User entity with unique ID, email, password, balance, and API key.

    Parameters
    ----------
    user_id : int
        Unique identifier for the user.
    username : str
        User's name.
    email : str
        User's email address. Must be valid.
    password : str
        User's password. Will be hashed for storage.
    balance : int, optional
        User's starting balance, default is 0.
    api_key : str, optional
        User's API key for authentication, default is None.

    Raises
    ------
    ValueError
        If the email format is invalid.
    """

    def __init__(
        self,
        user_id: int,
        username: str,
        email: str,
        password: str,
        balance=0,
        api_key=None,
    ):
        super().__init__(user_id)
        self.username = username
        if not self._validate_email(email):
            raise ValueError("Invalid email format.")
        self.email = email
        self.password = self._hash_password(password)
        self.balance = balance
        self.api_key = (
            api_key
            if api_key and self._check_unique_api_key(api_key)
            else self.generate_api_key()
        )

    def _validate_email(self, email: str) -> bool:
        """
        Validates the email format.

        Parameters
        ----------
        email : str
            Email address to validate.

        Returns
        -------
        bool
            True if valid, False otherwise.
        """
        pattern = r"^[\w.-]+@[\w.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    def _hash_password(self, password: str) -> str:
        """
        Hashes a password with a salt.

        Parameters
        ----------
        password : str
            Password to hash.

        Returns
        -------
        str
            Hashed password with salt appended.
        """
        salt = secrets.token_hex(16)
        return hashlib.sha256((salt + password).encode()).hexdigest() + ":" + salt

    def _check_unique_api_key(self, api_key: str) -> bool:  # pylint: disable=W0613
        """
        Checks API key uniqueness (placeholder).

        Parameters
        ----------
        api_key : str
            API key to check.

        Returns
        -------
        bool
            True if unique, False otherwise.
        """
        # Placeholder for database check
        return False

    def generate_api_key(self) -> str:
        """
        Generates and returns a unique API key.

        Returns
        -------
        str
            Generated API key.
        """
        self.api_key = secrets.token_hex(32)
        return self.api_key

    def view_balance(self) -> int:
        """
        Returns the user's current balance.

        Returns
        -------
        int
            The current balance.
        """
        return self.balance

    def update_balance(self, amount: int):
        """
        Updates the user's balance by a specified amount.

        Parameters
        ----------
        amount : int
            Amount to update the balance by.

        Raises
        ------
        ValueError
            If the update results in a negative balance.
        """
        if self.balance + amount < 0:
            raise ValueError("Insufficient funds for this operation.")
        self.balance += amount
