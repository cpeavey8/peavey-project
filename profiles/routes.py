from datetime import datetime
from functools import wraps
from flask import Blueprint, current_app, flash, redirect, render_template, abort, request, url_for
from flask_login import current_user, login_required

from accounts.data.user_api import UserAPI #Check
from profiles.data.profile_api import ProfileAPI

profiles = Blueprint('profiles', __name__,
                        template_folder='templates')

from typing import cast

def get_um() -> UserAPI:
    """A type-hinted getter for the ProfileManager."""
    return cast(UserAPI, current_app.um)

def get_pm() -> ProfileAPI:
    """A type-hinted getter for the ProfileManager."""
    return cast(ProfileAPI, current_app.pm)

@profiles.post('/delete/all')
def delete_all():
    ''' for testing '''
    
    n = get_pm().delete_all()
    return f"deleted {n} profiles"

@profiles.get('/')
def list_profiles():

    profs = get_pm().read_all() 

    # TODO: implement profiles.html
    return render_template('list_profiles.html',profs=profs)

#======================= TODO: IMPLEMENT THESE ===========

@profiles.route('/create', methods=['GET','POST'])
def create_profile():
    '''
    on GET, serve profile create form
    on POST, get username and profile_name from form

    if username is not valid, flash a message and redirect here
    else create the profile and redirect to the new profile page
    '''
    if request.method == 'GET':
        return render_template('create_profile.html')
    else:
        un = request.form.get('username')
        pn = request.form.get('profile_name')
        
        user_list = get_um().read({'username':un}) 
    
        if not user_list or user_list.get('users') == []:
            flash(f"user {un} not found")
            return render_template('redirect.html', ref=url_for('profiles.create_profile'))
        
        profile = get_pm().read_by_profile_name(pn)

        if profile:
            flash("profile name taken")
            return render_template('create_profile.html')
        else:
            prof = get_pm().create({'username':un, 'profile_name':pn})
            return render_template('redirect.html', ref=url_for('profiles.profile', profile_name=pn))
            


    

@profiles.get('/<profile_name>')
def profile(profile_name):
    '''get profile by profile name
    render profile_view with profile data
    profile view should:
        give profile name and username in a table
        show a list of skills
        have a form that allows you to add skills
        the form should have a hidden input with value equal to the profile id}
    '''  
    prof = get_pm().read_by_profile_name(profile_name)


    if not prof:
        flash("no such profile")
        return redirect(url_for('profiles.list_profiles'))
    else:
        return render_template('profile.html', prof=prof)



"""
@accounts.get('/users/{username}/profiles/)
def get_user_profiles(username):
   ''' get profiles by username 
   show a listing in a table
   THIS ENDPOINT GOES IN accounts.routes'''
"""
@profiles.post('/<profile_name>/add-skill')
def add_skill(profile_name):
    ''' add skill from form
    form should have profile_id and skill
    add skill to profile skills and redirect back to the profile'''
    
    skill = request.form.get('skill')
    profile_id = request.form.get('profile_id') 
    
    if not profile_id:
        flash("Error: Missing Profile ID.")
        return redirect(url_for('profiles.profile', profile_name=profile_name))

    n_modified = get_pm().add_skill(profile_id, [skill]) 
    
    if n_modified > 0:
        flash(f"Skill '{skill}' added to {profile_name}.")
    else:
        flash(f"Skill '{skill}' already exists or failed to update.")
        
    return redirect(url_for('profiles.profile', profile_name=profile_name))

    

