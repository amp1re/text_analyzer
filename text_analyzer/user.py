import hashlib
import re
import secrets

from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    balance = Column(Float, default=0.0)
    api_key = Column(String, unique=True)
    operations = relationship("OperationLog", back_populates="user")

    def __init__(self, username, email, password, balance=0, api_key=None):
        self.username = username
        if not self._validate_email(email):
            raise ValueError("Invalid email format.")
        self.email = email
        self.password = self._hash_password(password)
        self.balance = balance

    def _validate_email(self, email: str) -> bool:
        pattern = r"^[\w.-]+@[\w.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    def _hash_password(self, password: str) -> str:
        salt = secrets.token_hex(16)
        return hashlib.sha256((salt + password).encode()).hexdigest() + ":" + salt

    def check_and_set_api_key(self, api_key, session):
        if self._check_unique_api_key(api_key, session):
            self.api_key = api_key
        else:
            self.api_key = self._generate_api_key(session)

    def view_balance(self, session):
        user = session.query(User).filter_by(id=self.id).one()
        return user.balance

    def update_balance(self, amount, session):
        if self.balance + amount < 0:
            raise ValueError("Insufficient funds for this operation.")
        self.balance += amount
        session.commit()

    def set_api_key(self, session, api_key=None):
        """Установка и проверка уникальности API ключа."""
        if api_key is None:
            api_key = self._generate_api_key(session)
        elif not self._check_unique_api_key(api_key, session):
            raise ValueError("API key is not unique.")

        self.api_key = api_key

    def _check_unique_api_key(self, api_key, session):
        """Проверка уникальности API ключа."""
        exists_api_key = (
            session.query(User).filter_by(api_key=api_key).first() is not None
        )
        return not exists_api_key

    def _generate_api_key(self, session):
        """Генерация уникального API ключа."""
        while True:
            potential_key = secrets.token_hex(32)
            if self._check_unique_api_key(potential_key, session):
                return potential_key
