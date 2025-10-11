from flask import Blueprint, flash, redirect, render_template, request, url_for, current_app
from flask_login import login_required, login_user, logout_user, current_user
from profiles.data.profile_api import ProfileAPI
from typing import cast
from accounts.user_login import UserLogin

accounts = Blueprint('accounts', __name__,
                        template_folder='templates')

def get_pm() -> ProfileAPI:
    """A type-hinted getter for the ProfileManager."""
    return cast(ProfileAPI, current_app.pm)

@accounts.route('/users/create', methods=['POST', 'GET'])
def create():
    ''' on GET, serve user create form
    on POST, get form data and update'''


    if request.method == 'GET':
        return render_template('create.html')
    
    else:
        # Convert admin checkbox to boolean
        form_data = request.form.to_dict()
        form_data['admin'] = True if form_data.get('admin') == 'on' else False

        try:
            result = current_app.um.create(form_data)
        except Exception as e:
            print(e)
            flash(str(e))
            return redirect(url_for('accounts.create'))
        else:
            un = form_data.get('username')
            flash(f"Created user {un}")
            return redirect(url_for('accounts.users'))
    

@accounts.get('/users/')
@login_required
def users():

    us = current_app.um.read_all()
    us = us.get('users')


    if not current_user.admin:
        return "not authorized", 403

    return render_template('users.html', users=us)

@accounts.route('/users/<username>', methods=['POST', 'GET'])
@login_required
def view(username):
    ''' on GET, serve populated user update form
    on POST, get form data and update user'''

    us = current_app.um.read({'username': username})

    if not us:
        return "not found", 404

    if not (current_user.admin or current_user.username==username):
        return "not authorized", 403
    
    user = us

    if not us:
        flash("User not found")
        return redirect(url_for('accounts.users'))
    
    user = us[0]

    if request.method == 'GET':
        return render_template('view.html', user=user)
    else:

        uid = user.get('id')
        result = current_app.um.update(uid, request.form)

        if result:
        
            flash("Updated user")
            return redirect(url_for('accounts.view', username=username))
        else:
            flash("Failed to update user")
            return redirect(url_for('accounts.view', username=username))

@accounts.post('/users/delete/all')
@login_required
def delete_all():

    if not current_user.admin:
        return "not authorized", 403
        
    n = current_app.um.delete_all()
    return f"deleted {n} users"

@accounts.post('/users/delete/<username>')
@login_required
def delete(username):
    if not (current_user.admin or current_user.username==username):
        return "not authorized", 403
    
    data = current_app.um.read({'username': username})
    user = data.get('users', [])
    result = current_app.um.delete_by_id(user[0]['id'])

    if result:
        flash(f"Deleted user {username}")
    else:
        flash(f"Failed to delete user {username}")
    
    return redirect(url_for('accounts.users'))

@accounts.route('/login', methods=['GET','POST'])
def login():
    '''on GET, serve login page.  on POST, authenticate and login
    use current_app.um to access UserAPI / UserManager
    '''

    if request.method=='GET':
        return render_template('login.html')
    
    username = request.form.get('username')
    password = request.form.get('password')

    users = current_app.um.read({'username': username, 'password': password})
    users = users.get('users', [])

    if users:
        u = users[0]

        uid = str(u.get('id'))
        un = u.get('username')
        admin = u.get('admin')

        ul = UserLogin(uid,un,admin)

        print("User data:", u)
        print('Logging in user with _id:', uid)
        login_user(ul)
        print('Logged in:', ul, 'is_authenticated:', ul.is_authenticated)
        flash('logged in')
        return redirect(url_for('index'))
    else:
        flash('login unsuccessful')
        return redirect(url_for('accounts.login'))

@accounts.route("/logout")
@login_required
def logout():
    logout_user()
    flash('logged out')
    return redirect(url_for('index'))


@accounts.get('/users/<username>/profiles')
def user_profiles(username):
    ''' get all profiles for a user by username'''
   
    profs = get_pm().read_by_username(username) 
    return render_template('user_profiles.html', profs=profs or [], username=username)

