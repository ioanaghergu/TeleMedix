from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, userid, email, password, username,birth_date,roleid):
        self.userid = userid
        self.email = email
        self.password = password
        self.username = username
        self.birth_date = birth_date
        self.roleid = roleid

    def get_id(self):
        return self.userid
