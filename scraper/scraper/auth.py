from werkzeug.security import safe_str_cmp


class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


users = [
    User(1, "john", "pass"),
    User(1, "Sally", "pass"),
]

username_table = {u.username: u for u in users}
user_id_table = {u.id: u for u in users}


def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode("utf-8"), password.encode("utf-8")):
        return user


def identity(payload):
    user_id = payload["identity"]
    return user_id_table.get(user_id, None)
