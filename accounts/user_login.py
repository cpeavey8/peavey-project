# from accounts.data.user_api import UserAPI
# um = UserAPI()

'''
Works statically - UserLogin.setup_db, UserLogin.get
But also used to create instances of users for login purposes (current_user)
'''
from flask import current_app
from flask_login import UserMixin


class UserLogin(UserMixin):

    def __init__(self,user_id,username, admin=None):
        self.id = str(user_id)
        self.username = username
        self.admin = bool(admin)

    @staticmethod
    def setup_db(um):
        UserLogin.um = um

    @staticmethod
    def get(user_id):
        ''' get user by id; construct and return User object
        use current_app.um to access UserAPI / UserManager'''

        u = current_app.um.read_by_id(str(user_id))


        if u:
            uid = u.get('_id') or u.get('id')
            un = u.get('username')
            admin = u.get('admin', None)

            return UserLogin(uid, un, admin)
        return None
