import json
from flask import Flask, render_template
from flask_login import FlaskLoginClient, LoginManager

from accounts.data import user_api, user_manager, db_manager
from profiles.data import profile_api, profile_manager

from accounts.routes import accounts
from accounts.user_login import UserLogin
from config import USER_CONFIG, GUIDE_CONFIG
from profiles.routes import profiles
#---------------------------------------

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#------------------ databases -------------------------

db_url = USER_CONFIG.DB_URL
db_db = USER_CONFIG.USER_DB
db_col = USER_CONFIG.USER_COL
profile_db = USER_CONFIG.profile_db
profile_col = USER_CONFIG.profile_col

umngr = user_manager.UserManager(db_url, db_db, db_col)
dbm = db_manager.DBManager(db_url, profile_db, profile_col)
app.um = user_api.UserAPI(umngr)
pmngr = profile_manager.ProfileManager(dbm)
app.pm = profile_api.ProfileAPI(pmngr)


#-------------------blueprints--------------------

app.register_blueprint(accounts, url_prefix="/accounts")
app.register_blueprint(profiles, url_prefix="/profiles")
app.add_url_rule(
    "/users/<username>/profiles",
    endpoint="user_profiles_root",
    view_func=app.view_functions["accounts.user_profiles"],
)

#------------------Login------------------------------

app.test_client_class = FlaskLoginClient 
UserLogin.setup_db(app.um)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "accounts.login"

@login_manager.user_loader
def load_user(user_id):
    print('loading user')
    user = UserLogin.get(user_id)
    print('user loaded:', user_id, user)
    return user

#---------------------------------------------

## routes 
@app.route('/')
def index():
    ''' serve index.html '''
    
    return render_template('index.html')


if __name__=="__main__":
    app.run(debug=True)
