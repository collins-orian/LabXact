#!/usr/bin/env python3
"""This file contains routes and main functionality
for the app"""


# All reqired imports
import os
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, Column, Integer, String, Date, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from flask_migrate import Migrate
from config import settings
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from forms import LoginForm, UserForm, UserUpdateForm, PatientRegForm, PatientUpdateForm


# This is the main application entry point and the application secret key
app = Flask(__name__)
app.secret_key = settings.SECRET_KEY


# SQLalchemy Configurations and as well database creation
app.config["SQLALCHEMY_DATABASE_URI"] = settings.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Handles the database migration
migrate = Migrate(app, db)


# This handles the login features and session management for the application
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    """This method loads current user based on
    the user id"""
    return Users.query.get(int(user_id))


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
    inspector = inspect(db.engine)
    if not inspector.has_table('Patients'):
        db.create_all()

    pid = None
    all_patients = Patients.query.order_by(Patients.date_registered)

    form = PatientRegForm()

    # generate the PID Number
    total_patients = Patients.query.count()
    num_digits = len(str(total_patients + 1))
    patient_id = f"PID-{str(total_patients + 1).zfill(num_digits)}"

    if form.validate_on_submit():
        try:
            pid = Patients.query.filter_by(id=patient_id).first()
            if pid is None:
                patient = Patients(patient_id=form.patient_id.data, firstname=form.firstname.data,
                                   middlename=form.middlename.data, lastname=form.lastname.data,
                                   date_of_birth=form.dob.data, age=form.age.data, gender=form.gender.data,
                                   mobile=form.mobile.data, email=form.email.data, address=form.address.data)
                db.session.add(patient)
                db.session.commit()
        except:
            flash('PID already exists!')
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
        # Calculate the age based on the date of birth
        return redirect(url_for("add_patient"))
    return render_template('add_patient.html', form=form, pid=patient_id, all_patients=all_patients,
                           current_user=current_user)


# update patient page
@app.route('/modify_patient/<int:id>', methods=['GET', 'POST'])
@login_required
def modify_patient(id):
    """This route takes you to patients update page"""
    form = PatientUpdateForm()
    patient_to_update = Patients.query.get_or_404(id)
    if request.method == "POST":
        patient_to_update.first_name = request.form.get('firstname')
        patient_to_update.middle_name = request.form.get('middlename')
        patient_to_update.last_name = request.form.get('lastname')
        patient_to_update.date_of_birth = request.form.get('dob')
        patient_to_update.age = request.form.get('age')
        patient_to_update.gender = request.form.get('gender')
        patient_to_update.email = request.form.get('email')
        patient_to_update.mobile = request.form.get('mobile')
        patient_to_update.address = request.form.get('address')
        try:
            db.session.commit()
            flash("Patient Details Updated Successfully!")
            return redirect(url_for("add_patient"))
        except:
            flash("Patient Details Update Failed!")
            return render_template("modify_patient.html", form=form, patient_to_update=patient_to_update, id=id)
    else:
        return render_template("modify_patient.html", form=form, patient_to_update=patient_to_update, id=id)


# delete patient page
@app.route('/delete_patient/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_patient(id):
    """This route deletes patient record"""
    form = PatientRegForm()
    all_patients = Patients.query.order_by(Patients.date_registered)
    patient_to_delete = Patients.query.get_or_404(id)
    try:
        db.session.delete(patient_to_delete)
        db.session.commit()
        flash("Patient Deleted Successfully")
        return render_template('add_patient.html', form=form, all_patients=all_patients)

    except:
        flash("Patient Delete Failed!")
        return redirect(url_for('add_patient'))


# delete user from database
@app.route('/delete_user/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    """This route deletes user record"""
    form = UserForm()
    user_to_delete = Users.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully")
        all_users = Users.query.order_by(Users.date_added)
        return render_template('add_user.html', form=form, our_users=all_users)
    except:
        flash("User Delete Failed!")
        return redirect(url_for('add_user'))


# add user to database
@app.route('/user/add', methods=['GET', 'POST'])
@login_required
def add_user():
    """This route takes you to the add user page"""
    inspector = inspect(db.engine)
    if not inspector.has_table('Users'):
        db.create_all()

    all_users = Users.query.order_by(Users.date_added)
    form = UserForm()
    if form.validate_on_submit():
        user_email = Users.query.filter_by(email=form.email.data).first()
        user_username = Users.query.filter_by(email=form.email.data).first()
        if user_email is None and user_username is None:
            hashed_pwd = generate_password_hash(form.password.data, "sha256")
            user = Users(fullname=form.fullname.data, username=form.username.data,
                         email=form.email.data, role=form.role.data, section=form.section.data,
                         password_hash=hashed_pwd)
            db.session.add(user)
            db.session.commit()
        form.username.data = ''
        form.fullname.data = ''
        form.email.data = ''
        form.role.data = ''
        form.section.data = ''
        form.password.data = ''
        form.password_confirm.data = ''
        flash("User Added Successfully")
        return redirect(url_for("add_user"))
    return render_template('add_user.html', form=form, our_users=all_users)


# update user information
@app.route('/modify_user/<int:id>', methods=['GET', 'POST'])
@login_required
def modify_user(id):
    """This route modifies users information"""
    form = UserUpdateForm()
    user_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        user_to_update.fullname = request.form.get('fullname')
        user_to_update.username = request.form.get('username')
        user_to_update.email = request.form.get('email')
        user_to_update.role = request.form.get('role')
        user_to_update.section = request.form.get('section')
        user_to_update.password = request.form.get('password')
        try:
            db.session.commit()
            flash("User Details Updated Successfully!")
            return redirect(url_for("add_user"))
        except:
            flash("User Details Update Failed!")
            return render_template("modify_user.html", form=form, user_to_update=user_to_update, id=id)
    else:
        return render_template("modify_user.html", form=form, user_to_update=user_to_update, id=id)


# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    """This route takes you to the login page"""
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            # check hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash(f"Welcome {current_user.fullname.upper()}!")
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
    logout_user()
    flash("Logout Successful!")
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


# The models below create database tables for the application and 
# ensures that the database tables are created in the correct order


# User Model
class Users(db.Model, UserMixin):
    """This is the user class that defines the user model"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String(100), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    role = Column(String(50), nullable=False)
    section = Column(String(50), nullable=False)
    date_added = Column(DateTime, default=datetime.utcnow())

    # Relationship to the Sections table
    # section = relationship('Sections', back_populates='users')

    @property
    def password(self):
        """This method raises error if password doesn't
        match the requirement"""
        raise AttributeError("Password is not a readable attribute!")

    @password.setter
    def password(self, password):
        """This method generates a hash password"""
        self.password_hash = generate_password_hash(password)

    def veryfy_password(self, password):
        """This method matches the hash password on the database
        to that of the password entered by the user for login"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """This method returns the users fullname
        as string"""
        return '<Name %r>' % self.fullname


# Patient model
class Patients(db.Model):
    """This is the patient class that defines the
    patient model"""
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(String(100), unique=True, nullable=False)
    firstname = Column(String(50), nullable=False)
    middlename = Column(String(50))
    lastname = Column(String(50), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(Enum('Male', 'Female', 'other'), nullable=False)
    mobile = Column(String(20), nullable=False)
    email = Column(String(60))
    address = Column(String(150), nullable=False)
    date_registered = Column(
        DateTime, default=datetime.now(), nullable=False)

    # sample = relationship('Samples', back_populates="patients")


"""
    
    

# Test model
class Tests(db.Model):
    __tablename__ = 'tests'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    section = Column(Integer, ForeignKey("sections.id"))

    # Relationship to the Section table
    section = relationship('Sections', back_populates='tests')

    # Relationship to the Sample table
    samples = relationship("Samples", back_populates="test")


# Samples Model
class Samples(db.Model):
    id = Column(Integer, primary_key=True)
    sample_id = Column(Integer, primary_key=True)
    type = Column(String(50), nullable=False)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    test_id = Column(Integer, ForeignKey('tests.id'))
    date_registered = Column(
        DateTime, default=datetime.now(), nullable=False)
    status = Column(String(25), nullable=False)

    # Relationship to the Test table
    test = relationship('Test', back_populates='samples')
    

# Sections model
class Sections(db.Model):
    __tablename__ = 'sections'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    
    # Relationship to the Users table
    users = relationship('Users', back_populates='sections')

    # Relationship to the Tests table
    tests = relationship('Tests', back_populates='section')


# Inventory model
class Inventory(db.Model):
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    quantity = Column(Integer, primary_key=True)


# Report model
class Reports(db.Model):
    __tablename__ = 'reports'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sample_id = Column(Integer, ForeignKey("samples.id"))
    test_id = Column(Integer, ForeignKey("tests.id"))
    result = Column(String(255))

    # Relationship to the Sample table
    sample = relationship('Samples', back_populates='test_results')

    # Relationship to the Test table
    test = relationship('Tests', back_populates='test_results')


"""


if __name__ == '__main__':
    app.run(port=5000)
