#!/usr/bin/env python3
"""This file routes views for user section of the app"""

from . import user
from flask import request, render_template, redirect, url_for, flash
from ..logger import logger
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from forms import UserForm, UserUpdateForm, UserSearchForm, LoginForm
from utils import UserService
from ...models.user_model import Users


@user.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


# delete user from database
@user.route('/delete_user/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    """This route deletes user record"""
    form = UserForm()
    user_to_delete = UserService.get_user(id)
    all_users = UserService.all_users()
    try:
        UserService.delete_user(user_to_delete.id)
        flash("User Deleted Successfully")
        logger.info(
            f'User ---> {user_to_delete} <---> deleted by ---> {current_user}')
        return render_template('add_user.html', form=form, our_users=all_users)
    except:
        flash("User Delete Failed!")
        return redirect(url_for('users.add_user'))


# add user to database
@user.route('/user/add', methods=['GET', 'POST'])
@login_required
def add_user():
    """This route takes you to the add user page"""
    all_users = UserService.all_users()
    form = UserForm()
    if form.validate_on_submit():
        user_email = UserService.get_user_by_email(form.email.data)
        user_username = UserService.get_user_by_username(form.username.data)
        if user_email is None and user_username is None:
            try:
                hashed_pwd = generate_password_hash(
                    form.password.data, "scrypt", salt_length=64)
                UserService.create_user(form.firstname.data,
                                  form.lastname.data,
                                  form.username.data,
                                  form.email.data,
                                  hashed_pwd,
                                  form.role.data,
                                  form.section.data)
                flash("User Added Successfully")
                logger.info(
                    f'User ---> {form.username.data} <---> added by ---> {current_user}')
                return redirect(url_for("users.add_user"))
            except:
                flash("User Add Failed!")
                return redirect(url_for("users.add_user"))
        form.username.data = ''
        form.firstname.data = ''
        form.lastname.data = ''
        form.email.data = ''
        form.role.data = ''
        form.section.data = ''
        form.password.data = ''
        form.password_confirm.data = ''

    return render_template('add_user.html',
                           form=form, our_users=all_users)


# update user information
@user.route('/modify_user/<int:id>', methods=['GET', 'POST'])
@login_required
def modify_user(id):
    """This route modifies users information"""
    form = UserUpdateForm()
    user_to_update = UserService.get_user(id)
    if request.method == "POST":
        try:
            UserService.update_user(user_to_update,
                              request.form.get('firstname'),
                              request.form.get('lastname'),
                              request.form.get('username'),
                              request.form.get('email'),
                              request.form.get('password'),
                              request.form.get('role'),
                              request.form.get('section'))
            flash("User Details Updated Successfully!")
            logger.info(
                f'User {user_to_update.username} updated by ---> {current_user}')
            return redirect(url_for("users.add_user"))
        except:
            flash("User Details Update Failed!")
            return render_template("modify_user.html", form=form,
                                   user_to_update=user_to_update, id=id)
    else:
        return render_template("modify_user.html", form=form,
                               user_to_update=user_to_update, id=id)


# Login page
@user.route('/login', methods=['GET', 'POST'])
def login():
    """This route takes you to the login page"""
    form = LoginForm()
    if form.validate_on_submit():
        user = UserService.get_user_by_username(form.username.data)
        if user:
            # check hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash(
                    f'Welcome {user.firstname} {user.lastname}!')
                logger.info(
                    f'User logged in: {current_user}')
                return redirect(url_for('users.dashboard'))
            else:
                flash("Wrong Password! - Please Try again.")
        else:
            flash("User does not exist! - Please Try again.")
    return render_template('login.html', form=form)


# logout page
@user.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """This route logs you out of your account"""
    try:
        logger.info(
            f'User logging out ---> {current_user} <---> Logout Successful! ')
        logout_user()
        flash("Logout Successful!")
    except Exception as e:
        logger.error(e)
        raise e
    return redirect(url_for('users.login'))


# pass data to the navbar
@user.context_processor
def base():
    """This function passes data to the navbar"""
    form = UserSearchForm()
    return dict(form=form)


# create search function
@user.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = UserSearchForm()
    results = Users.query
    if form.validate_on_submit():
        # Get the search term from the form
        search = form.searched.data
        # Query the database for the search term neglecting case sensitivity

        results = results.filter(Users.firstname.ilike(
            '%' + search + '%') | Users.lastname.ilike('%' + search + '%') |
            Users.username.ilike('%' + search + '%'))
        results = results.order_by(Users.firstname)
        return render_template('search.html', form=form, searched=search, results=results)
