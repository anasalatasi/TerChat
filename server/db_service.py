import sqlite3


class DatabaseService:
    @staticmethod
    def init_db():
        with sqlite3.connect('messages.db') as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS messages
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          text TEXT NOT NULL,
                          timestamp TEXT NOT NULL,
                          sender TEXT NOT NULL)''')
            conn.commit()

    @staticmethod
    def insert_message(text, timestamp, sender):
        with sqlite3.connect('messages.db') as conn:
            c = conn.cursor()
            c.execute("INSERT INTO messages (text, timestamp, sender) VALUES (?, ?, ?)",
                      (text, timestamp, sender))
            conn.commit()

    @staticmethod
    def get_all_messages():
        with sqlite3.connect('messages.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM messages")
            return [{'id': row[0], 'text': row[1], 'timestamp': row[2], 'sender': row[3]} for row in c.fetchall()]

    @staticmethod
    def get_message_count():
        with sqlite3.connect('messages.db') as conn:
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM messages")
            return c.fetchone()[0]