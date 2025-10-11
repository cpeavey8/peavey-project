try:
    from .db_manager import DBManager
except:
    from accounts.data.db_manager import DBManager

from pymongo.errors import DuplicateKeyError

class UserManager(DBManager):

    def __init__(self, conn_str:str,db:str, col:str):
        '''connect to db server and set self.col'''
        
        super().__init__(conn_str,db,col)
        self.col.create_index("username", unique=True)  

    def authenticate(self, username:str, password:str):
        ''' simple static method to authenticate username/password'''
        return super().read({'username': username, 'password': password})
    
    def create(self, u):

        try:
            uid = super().create(u)
        except DuplicateKeyError as e:
            raise Exception("username must be unique")
        else:
            return uid


