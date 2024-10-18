import os
import psycopg2
from datetime import datetime
from urllib.parse import urlparse


class User:
    def __init__(self, user_id: int = None) -> None:
        # Parse the DATABASE_URL environment variable
        DATABASE_URL = os.environ.get('postgres://ucq4qv2htrt2pv:p53ab00f49ae8715210bbe53160ca125ccc7b333aae748ff430e58214026c7107@ccaml3dimis7eh.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com:5432/d44tn3vgqmiju6')
        
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

        if user_id is not None:
            self.cursor.execute(
                'SELECT * FROM users WHERE user_id = %s', (user_id,)
            )
            user = self.cursor.fetchone()

            if user:
                self.user_id = user[0]
                self.username = user[1]
                self.phone = user[2]
                self.date = user[3]
                self.ref_count = user[4]
                self.ref_id = user[5]


    def join_users(self, user_id: int, username: str, ref_id: str = None) -> bool:
        """
        Запис користувача в базу даних
        :param user_id: int
        :param username: str
        :return статус: bool
        """
        status = False
        self.cursor.execute(
            "SELECT * FROM users WHERE user_id = %s", (user_id,)
        )
        row = self.cursor.fetchall()

        if len(row) == 0:
            user_data = (user_id, username, 'NOT', datetime.now(), 0, ref_id)

            self.cursor.execute(
                "INSERT INTO users (user_id, username, phone, date, ref_count, ref_id) VALUES (%s, %s, %s, %s, %s, %s)",
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
            "UPDATE users SET phone = %s WHERE user_id = %s", (phone, self.user_id)
        )
        self.conn.commit()

        return True

    def add_referral(self) -> bool:
        refs_amount = self.get_refs_amount()
        self.cursor.execute(
            "UPDATE users SET ref_count = %s WHERE user_id = %s", (refs_amount + 1, self.user_id)
        )

        self.conn.commit()

        return True

    def get_referrer_id(self) -> str:
        self.cursor.execute(
            "SELECT ref_id FROM users WHERE user_id = %s", (self.user_id,)
        )
        ref_id = self.cursor.fetchone()
        return ref_id[0] if ref_id else None

    def get_refs_amount(self) -> int:
        self.cursor.execute(
            "SELECT ref_count FROM users WHERE user_id = %s", (self.user_id,)
        )
        ref_count = self.cursor.fetchone()

        return ref_count[0] if ref_count else 0


















