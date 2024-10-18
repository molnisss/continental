import os
import psycopg2
from datetime import datetime
from urllib.parse import urlparse


class User:
    def __init__(self, account_id: int = None) -> None:
        # Parse the DATABASE_URL environment variable
        DATABASE_URL = os.environ.get('DATABASE_URL')
        
        if DATABASE_URL:
            result = urlparse(DATABASE_URL)
            self.conn = psycopg2.connect(
                database=result.path[1:], 
                user=result.username, 
                password=result.password, 
                host=result.hostname, 
                port=result.port
            )
        else:
            raise Exception("DATABASE_URL is not set in the environment variables.")
        
        self.cursor = self.conn.cursor()

        if account_id is not None:
            self.cursor.execute(
                'SELECT * FROM users WHERE account_id = %s', (account_id,)
            )
            user = self.cursor.fetchone()

            if user:
                self.account_id = user[0]
                self.username = user[1]
                self.phone = user[2]
                self.registered_at = user[3]
                self.ref_count = user[4]
                self.ref_id = user[5]


    def join_users(self, account_id: int, username: str, ref_id: str = None) -> bool:
        """
        Запис користувача в базу даних
        :param account_id: int
        :param username: str
        :return статус: bool
        """
        status = False
        self.cursor.execute(
            "SELECT * FROM users WHERE account_id = %s", (account_id,)
        )
        row = self.cursor.fetchall()

        if len(row) == 0:
            user_data = (account_id, username, 'NOT', datetime.now(), 0, ref_id)

            self.cursor.execute(
                "INSERT INTO users (account_id, username, phone, registered_at, ref_count, ref_id) VALUES (%s, %s, %s, %s, %s, %s)",
                user_data
            )
            self.conn.commit()

            status = True

        return status

    def update_phone(self, phone: str) -> bool:
        """
        Оновлення номера телефону користувача в базі даних
        :param phone: str
        :return: bool
        """
        self.cursor.execute(
            "UPDATE users SET phone = %s WHERE account_id = %s", (phone, self.account_id)
        )
        self.conn.commit()

        return True

    def add_referral(self) -> bool:
        refs_amount = self.get_refs_amount()
        self.cursor.execute(
            "UPDATE users SET ref_count = %s WHERE account_id = %s", (refs_amount + 1, self.account_id)
        )

        self.conn.commit()

        return True

    def get_referrer_id(self) -> str:
        self.cursor.execute(
            "SELECT ref_id FROM users WHERE account_id = %s", (self.account_id,)
        )
        ref_id = self.cursor.fetchone()
        return ref_id[0] if ref_id else None

    def get_refs_amount(self) -> int:
        self.cursor.execute(
            "SELECT ref_count FROM users WHERE account_id = %s", (self.account_id,)
        )
        ref_count = self.cursor.fetchone()

        return ref_count[0] if ref_count else 0


















