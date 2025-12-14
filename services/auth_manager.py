from typing import Optional
import bcrypt

from models.user import User
from services.database_manager import DatabaseManager


class AuthManager:
    """Handles user registration and login using bcrypt."""

    def __init__(self, db: DatabaseManager):
        self._db = db

    def register_user(self, username: str, password: str, role: str = "user") -> None:
        # bcrypt hashing
        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )

        self._db.execute_query(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, password_hash, role),
        )

    def login_user(self, username: str, password: str) -> Optional[User]:
        row = self._db.fetch_one(
            "SELECT username, password_hash, role FROM users WHERE username = ?",
            (username,),
        )

        if row is None:
            return None

        username_db, password_hash_db, role_db = row

        # bcrypt password check
        if bcrypt.checkpw(
            password.encode("utf-8"),
            password_hash_db
        ):
            return User(username_db, password_hash_db, role_db)

        return None



