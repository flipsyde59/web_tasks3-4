class User:
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password


class Todo:
    def __init__(self, id, title, user_id, done):
        self.id = id
        self.title = title
        self.user_id = user_id
        self.done = done

    def serialize(self):
        return {
            'id': self.id,
            'name': self.title,
            'user_id': self.user_id,
            'done': self.done
        }