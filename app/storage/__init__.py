import sqlite3
from pathlib import Path
from werkzeug.security import check_password_hash, generate_password_hash
from ..entities import User, Todo

# Подключаемся к БД
db = sqlite3.connect(Path(__file__).parent / '..' / '..' / 'db' / 'database.sqlite', check_same_thread=False)


class Storage:

    @staticmethod
    def add_user(user):
        # Вместо пароля сохраняем хэш пароля
        # https://werkzeug.palletsprojects.com/en/0.16.x/utils/#werkzeug.security.generate_password_hash
        db.execute('INSERT INTO users (email, password) VALUES (?, ?)', (user.email, generate_password_hash(user.password)))
        db.commit()

    @staticmethod
    def get_user_by_email_and_password(email, password_hash):
        user_data = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        # Не проверяем явно равенство паролей, а проверяем через его хэш
        # https://werkzeug.palletsprojects.com/en/0.16.x/utils/#werkzeug.security.check_password_hash
        if user_data and check_password_hash(user_data[2], password_hash):
            return User(*user_data)
        else:
            return None

    @staticmethod
    def get_user_by_id(user_id):
        user_data = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        if user_data:
            return User(*user_data)
        else:
            return None

    @staticmethod
    def get_user_todos(user_id):
        todos = db.execute('SELECT id, title, user_id, done FROM todos WHERE user_id = ?', (user_id,)).fetchall()
        return list(map(lambda todo: Todo(*todo), todos))

    @staticmethod
    def add_todo(todo):
        todo_id = db.execute('INSERT INTO todos (title, user_id, done) VALUES (?, ?, ?)', (todo.title, todo.user_id, todo.done)).lastrowid
        db.commit()
        todo = db.execute('SELECT id, title, user_id, done FROM todos WHERE id = ?', (todo_id,)).fetchone()
        return Todo(*todo)

    @staticmethod
    def delete_todo(todo_id):
        db.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
        db.commit()

    @staticmethod
    def update_todo_status(todo_id, action):
        if action == "done":
            db.execute('UPDATE todos SET done = 1 WHERE id = ?', (todo_id,))
            db.commit()
        if action == "undone":
            db.execute('UPDATE todos SET done = 0 WHERE id = ?', (todo_id,))
            db.commit()

    @staticmethod
    def get_todo_status(todo_id):
        todo_status = db.execute('SELECT * FROM todos WHERE id = ?', (todo_id,)).fetchone()
        if todo_status:
            return Todo(todo_status[0], todo_status[1], todo_status[2], todo_status[3])
        else:
            return None

    @staticmethod
    def is_user_registered(email):
        user_data = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        if user_data:
            return True
        else:
            return False