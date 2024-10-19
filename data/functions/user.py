import sqlite3
from datetime import datetime


class User:
    user_id: int

    def __init__(self, user_id: int = None) -> None:
        self._sql_path = './data/database.db'

        self.conn = sqlite3.connect(database=self._sql_path)
        self.cursor = self.conn.cursor()

        if user_id is not None:
            self.cursor.execute(
                'SELECT * FROM users WHERE user_id = ?', [user_id]
            )
            user = self.cursor.fetchone()

            self.user_id = user[0]
            self.username = user[1]
            self.phone = user[2]
            self.date = user[3]
            self.ref_count = user[4]
            self.ref_id = user[5]

    def join_users(self, user_id: int, username: str, ref_id: str = None) -> bool:
        """
        Запись пользователя в базу данных
        :param user_id: int
        :param username: str
        :return status: bool
        """
        status = False
        self.cursor.execute(
            "SELECT * FROM users WHERE user_id = ?", [user_id]
        )
        row = self.cursor.fetchall()

        if len(row) == 0:
            user_data = [user_id, f"{username}", 'NOT', datetime.now(), 0, ref_id,]

            self.cursor.execute(
                    "INSERT INTO users VALUES (?,?,?,?,?,?)", user_data
            )
            self.conn.commit()

            status = True

        return status

    def update_phone(self, phone: str) -> bool:
        """
        Запись пользователя в базу данных
        :param phone: int
        :return: bool
        """
        self.cursor.execute(
            "UPDATE users SET phone = ? WHERE user_id = ?", [phone, self.user_id]
        )
        self.conn.commit()

        return True

    def add_referral(self) -> bool:
        refs_amount = self.get_refs_amount()
        self.cursor.execute(
            "UPDATE users SET ref_count = ? WHERE user_id = ?", [refs_amount + 1, self.user_id]
        )

        self.conn.commit()

        return True
    
    def get_referrer_id(self) -> str:
        self.cursor.execute(
            "SELECT ref_id FROM users WHERE user_id = ?", [self.user_id]
        )
        ref_id = self.cursor.fetchone()
        return ref_id[0]

    def get_refs_amount(self) -> int:
        self.cursor.execute(
            "SELECT ref_count FROM users WHERE user_id = ?", [self.user_id]
        )
        ref_count = self.cursor.fetchone()

        return ref_count[0]


















