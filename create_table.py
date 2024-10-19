import os
import psycopg2

DATABASE_URL = os.environ.get('DATABASE_URL')

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

cursor.execute('''
               
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
    username VARCHAR(100),
    phone VARCHAR(20),
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ref_count INTEGER DEFAULT 0,
    ref_id BIGINT
);
''')

conn.commit()
cursor.close()
conn.close()

print("Table created successfully.")