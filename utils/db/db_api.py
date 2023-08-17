import sqlite3

class DatabaseAPI():

    def __init__(self, db_name: str):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
    
    def check_table(self):
        with self.connection:  
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS users_sessions (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER,
                                parent_message_id INTEGER,
                                child_messages_id NULL
            )''')

    def select_parent_id(self, user_id: int):
        with self.connection: 
            return self.cursor.execute('SELECT parent_message_id FROM users_sessions WHERE user_id = ?', (user_id,)).fetchone()[0]

    def cancel_ids(self, user_id: int):
        with self.connection: 
            self.cursor.execute('UPDATE users_sessions SET parent_message_id = ?, child_messages_id = ? WHERE user_id = ?', (None, None, user_id))

    def isinstancedb(self, user_id: int):
        with self.connection: 
            return self.cursor.execute('SELECT * FROM users_sessions WHERE user_id = ?', (user_id,)).fetchone()

    def add_new_user(self, user_id: int, parent_msg_id: int):
        with self.connection: 
            self.cursor.execute('INSERT INTO users_sessions (user_id, parent_message_id) VALUES (?, ?)', (user_id, parent_msg_id))

    def update_parent_msg_id(self, user_id: int, parent_msg_id: int):
        with self.connection: 
            self.cursor.execute('UPDATE users_sessions SET parent_message_id = ? WHERE user_id = ?', (parent_msg_id, user_id))

    def check_ids(self, user_id: int):
        with self.connection: 
            return self.cursor.execute('SELECT `parent_message_id`, `child_messages_id` FROM users_sessions WHERE `user_id` = ?', (user_id,)).fetchone()

    def update_child_ids(self, child_messages_ids: list, user_id: int):
        with self.connection: 
            self.cursor.execute('UPDATE users_sessions SET child_messages_id = ? WHERE user_id = ?', (child_messages_ids, user_id))

    def find_user_id(self, parent_msg_id: int):
        with self.connection: 
            return self.cursor.execute('SELECT user_id FROM users_sessions WHERE parent_message_id = ?', (parent_msg_id,)).fetchone()[0]


db_API = DatabaseAPI('tutorial.db')
