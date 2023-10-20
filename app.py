#!/usr/bin/env python3
"""This file contains routes and main functionality
for the app"""


# All reqired imports
from flask import Flask, request, render_template, redirect, url_for, flash
from models import init_db
from config import settings
from services import logger
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from forms import LoginForm, UserForm, UserUpdateForm, PatientRegForm, PatientUpdateForm
from services.user_services import UserService
from services.patient_services import PatientService


# This is the main application entry point and the application secret key
app = Flask(__name__)
app.secret_key = settings.SECRET_KEY


# App SQLalchemy Configurations
app.config["SQLALCHEMY_DATABASE_URI"] = settings.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Initialises the database
db = init_db(app)


# Create the services for the models
users = UserService()
patients = PatientService()


# This handles the login features and session management for the application
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    """This method loads current user based on
    the user id"""
    return users.get_user(int(user_id))


# These are the routes that are present in the application
# They are all defined below


# home page
@app.route('/')
def home():
    """This route takes you to the home page"""
    return render_template('index.html')


# dashboard page
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    """This route takes you to the dashboard page"""
    return render_template('dashboard.html')


# patient registration page
@app.route('/patient/register', methods=['GET', 'POST'])
@login_required
def add_patient():
    """This route takes you to the patient
    registration page"""

    pid = None
    all_patients = patients.all_patients()

    form = PatientRegForm()

    # generate the PID Number
    total_patients = patients.patient_count()
    num_digits = len(str(total_patients + 1))
    patient_id = f"PID-{str(total_patients + 1).zfill(num_digits)}"

    if form.validate_on_submit():
        try:
            pid = patients.get_patient_by_pid(patient_id)
            if pid is None:
                # Calculate the age of the patient based on the date of birth field in the form.
                # age = patients.calculate_age(form.dob.data)

                # Set the value of the age field in the form to the age that we calculated.
                # form.age.data = age

                patients.create_patient(form.patient_id.data,
                                        form.firstname.data,
                                        form.middlename.data,
                                        form.lastname.data,
                                        form.dob.data,
                                        form.age.data,
                                        form.gender.data,
                                        form.mobile.data,
                                        form.email.data,
                                        form.address.data)
        except:
            flash('Patient with PID Number already exists!!!')
            return redirect(url_for('add_patient'))

        form.patient_id.data = ''
        form.firstname.data = ''
        form.middlename.data = ''
        form.lastname.data = ''
        form.dob.data = ''
        form.age.data = ''
        form.gender.data = ''
        form.email.data = ''
        form.mobile.data = ''
        form.address.data = ''
        flash("Patient Registered Successfully")
        logger.info(
            f'Patient {form.patient_id.data} - {form.firstname.data} {form.lastname.data} registered by {current_user}')
        # Calculate the age based on the date of birth
        return redirect(url_for("add_patient"))
    return render_template('add_patient.html', form=form,
                           pid=patient_id, all_patients=all_patients,
                           current_user=current_user)


# update patient page
@app.route('/modify_patient/<int:id>', methods=['GET', 'POST'])
@login_required
def modify_patient(id):
    """This route takes you to patients update page"""
    form = PatientUpdateForm()
    patient_to_update = patients.get_patient(id)
    if request.method == "POST":
        try:
            patients.update_patient(patient_to_update,
                                    request.form.get('firstname'),
                                    request.form.get('middlename'),
                                    request.form.get('lastname'),
                                    request.form.get('dob'),
                                    request.form.get('age'),
                                    request.form.get('gender'),
                                    request.form.get('mobile'),
                                    request.form.get('email'),
                                    request.form.get('address'))
            flash("Patient Details Updated Successfully!")
            logger.info(
                f'Patient {patient_to_update} details updated by {current_user}')
            return redirect(url_for("add_patient"))
        except:
            flash("Patient Details Update Failed!")
            return render_template("modify_patient.html", form=form,
                                   patient_to_update=patient_to_update, id=id)
    else:
        return render_template("modify_patient.html", form=form,
                               patient_to_update=patient_to_update, id=id)


# delete patient page
@app.route('/delete_patient/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_patient(id):
    """This route deletes patient record"""
    form = PatientRegForm()
    all_patients = patients.all_patients()
    patient_to_delete = patients.get_patient(id)
    try:
        patients.delete_patient(patient_to_delete.id)
        flash("Patient Deleted Successfully")
        logger.info(
            f'Patient {patient_to_delete} deleted by {current_user}')
        return render_template('add_patient.html', form=form,
                               all_patients=all_patients)

    except:
        flash("Patient Delete Failed!")
        return redirect(url_for('add_patient'))


# delete user from database
@app.route('/delete_user/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    """This route deletes user record"""
    form = UserForm()
    user_to_delete = users.get_user(id)
    all_users = users.all_users()
    try:
        users.delete_user(user_to_delete.id)
        flash("User Deleted Successfully")
        logger.info(
            f'User {user_to_delete} deleted by {current_user}')
        return render_template('add_user.html', form=form, our_users=all_users)
    except:
        flash("User Delete Failed!")
        return redirect(url_for('add_user'))


# add user to database
@app.route('/user/add', methods=['GET', 'POST'])
@login_required
def add_user():
    """This route takes you to the add user page"""
    all_users = users.all_users()
    form = UserForm()
    if form.validate_on_submit():
        user_email = users.get_user_by_email(form.email.data)
        user_username = users.get_user_by_username(form.username.data)
        if user_email is None and user_username is None:
            try:
                hashed_pwd = generate_password_hash(
                    form.password.data, "scrypt")
                users.create_user(form.firstname.data,
                                  form.lastname.data,
                                  form.username.data,
                                  form.email.data,
                                  hashed_pwd,
                                  form.role.data,
                                  form.section.data)
                flash("User Added Successfully")
                logger.info(
                    f'User {form.username.data} - {form.firstname.data} {form.lastname.data} added by {current_user}')
                return redirect(url_for("add_user"))
            except:
                flash("User Add Failed!")
                return redirect(url_for("add_user"))
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
@app.route('/modify_user/<int:id>', methods=['GET', 'POST'])
@login_required
def modify_user(id):
    """This route modifies users information"""
    form = UserUpdateForm()
    user_to_update = users.get_user(id)
    if request.method == "POST":
        try:
            users.update_user(user_to_update,
                              request.form.get('firstname'),
                              request.form.get('lastname'),
                              request.form.get('username'),
                              request.form.get('email'),
                              request.form.get('password'),
                              request.form.get('role'),
                              request.form.get('section'))
            flash("User Details Updated Successfully!")
            logger.info(
                f'User {user_to_update} details updated by {current_user}')
            return redirect(url_for("add_user"))
        except:
            flash("User Details Update Failed!")
            return render_template("modify_user.html", form=form,
                                   user_to_update=user_to_update, id=id)
    else:
        return render_template("modify_user.html", form=form,
                               user_to_update=user_to_update, id=id)


# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    """This route takes you to the login page"""
    form = LoginForm()
    if form.validate_on_submit():
        user = users.get_user_by_username(form.username.data)
        if user:
            # check hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash(
                    f'Welcome {user.firstname} {user.lastname}!')
                logger.info(
                    f'User logged in: {current_user}')
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong Password! - Please Try again.")
        else:
            flash("User does not exist! - Please Try again.")
    return render_template('login.html', form=form)


# logout page
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """This route logs you out of your account"""
    try:
        logger.info(
            f'User logging out ---> {current_user} ---> Logout Successful!!!')
        logout_user()
        flash("Logout Successful!")
    except Exception as e:
        logger.error(e)
        raise e
    return redirect(url_for('login'))


# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    """This route returns an error page if page
    is not found"""
    return render_template('404.html'), 404


# Internal server error
@app.errorhandler(500)
def internal_server_error(e):
    """This route returns an error page when the
    server is down or has issues"""
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
