import psycopg2
from config import POSTGRES_URL


def get_connection():
    return psycopg2.connect(POSTGRES_URL)

def init_db():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS conversations
        (id SERIAL PRIMARY KEY,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )"""
    )

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized!")


def log_message(session_id:str,role:str,content:str):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(
        "INSERT INTO conversations(session_id,role,content)VALUES(%s,%s,%s)",(session_id,role,content)

    )
    conn.commit()
    cursor.close()
    conn.close()
    


