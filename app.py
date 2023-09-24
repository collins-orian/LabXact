#!/usr/bin/env python3
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Float, String, Date, Enum, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from flask_migrate import Migrate
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from forms import LoginForm, UserForm, UpdateUserForm, PatientRegForm

app = Flask(__name__)


# Secret key
app.secret_key = "devops/ITS2022@."


# SQLalchemy Configurations...
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:devops/ITS2022@localhost:3306/labxact"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# Handles database migration
migrate = Migrate(app, db)


# Handling flask_login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
# home page


@app.route('/')
def home():
    return render_template('index.html')


# dashboard page
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/patient/register', methods=['GET', 'POST'])
@login_required
def add_patient():
    # Create a new table if it doesn't exist
    if not Patients.__table__.exists(db.engine):
        db.create_all()
    pid = None
    all_patients = Patients.query.order_by(Patients.date_registered)
    form = PatientRegForm()

    # Retrieve the total number of patients from the database
    total_patients = Patients.query.count()

    # Determine the number of digits required
    num_digits = len(str(total_patients + 1))

    # Format the patient ID with leading zeros
    patient_id = f"PID-{str(total_patients + 1).zfill(num_digits)}"

    if form.validate_on_submit():

        try:
            pid = Patients.query.filter_by(id=patient_id).first()
            if pid is None:

                patient = Patients(patient_id=form.patient_id.data, firstname=form.firstname.data, middlename=form.middlename.data, lastname=form.lastname.data,
                                   date_of_birth=form.dob.data, age=form.age.data, gender=form.gender.data, mobile=form.mobile.data, email=form.email.data, address=form.address.data)
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
    return render_template('add_patient.html', form=form, pid=patient_id, all_patients=all_patients)


# update patient information
@app.route('/modify_patient/<int:id>', methods=['GET', 'POST'])
@login_required
def modify_patient(id):
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


# delete patient from database
@app.route('/delete_patient/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_patient(id):
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
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    username = None
    form = UserForm()
    delete_user = Users.query.get_or_404(id)
    try:
        db.session.delete(delete_user)
        db.session.commit()
        flash("User Deleted Successfully")
        all_users = Users.query.order_by(Users.date_added)
        return render_template('add_user.html', form=form, our_users=all_users)
    except:
        flash("User Delete Failed!")



# add user to database
@app.route('/user/add', methods=['GET', 'POST'])
@login_required
def add_user():
    # Create a new table if it doesn't exist
    if not Users.__table__.exists(db.engine):
        db.create_all()
    username = None
    all_users = Users.query.order_by(Users.date_added)
    form = UserForm()
    if form.validate_on_submit():
        user_email = Users.query.filter_by(email=form.email.data).first()
        user_username = Users.query.filter_by(email=form.email.data).first()
        if user_email is None and user_username is None:
            hashed_pwd = generate_password_hash(form.password.data, "sha256")
            user = Users(fullname=form.fullname.data, username=form.username.data,
                         email=form.email.data, role=form.role.data, 
                         section=form.section.data, password_hash=hashed_pwd)
            db.session.add(user)
            db.session.commit()
        username = form.username.data
        form.username.data = ''
        form.fullname.data = ''
        form.email.data = ''
        form.role.data = ''
        form.section.data = ''
        form.password.data = ''
        form.password_confirm.data = ''
        flash("User Added Successfully")
        return redirect(url_for("add_user"))
    return render_template('add_user.html', form=form, name=username, our_users=all_users)


# update user information
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    form = UpdateUserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.fullname = request.form.get('fullname')
        name_to_update.username = request.form.get('username')
        name_to_update.email = request.form.get('email')
        name_to_update.role = request.form.get('role')
        name_to_update.section = request.form.get('section')
        name_to_update.password = request.form.get('password')
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
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            # check hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login Successful!")
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
    logout_user()
    flash("Logout Successful!")
    return redirect(url_for('login'))

# Invalid URL


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Internal server error
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# Define the Patient model
class Patients(db.Model):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(String(100), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    middle_name = Column(String(50))
    last_name = Column(String(50), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(Enum('Male', 'Female', 'other'), nullable=False)
    mobile = Column(String(20), nullable=False)
    email = Column(String(60))
    address = Column(String(150), nullable=False)
    date_registered = Column(
        DateTime, default=datetime.now(), nullable=False)

    # laboratory_id = Column(Integer, ForeignKey('laboratory.id'))

    # laboratory = relationship("Laboratory")


# # Create the Laboratory model
# class Laboratory(db.Model):
#     __tablename__ = 'laboratory'

#     id = Column(Integer, primary_key=True)
#     name = Column(String(50), nullable=False)

# Create User Model
class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String(100), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    role = Column(String(50), nullable=False)
    section = Column(String(50), nullable=False)
    date_added = Column(DateTime, default=datetime.utcnow())

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute!")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def veryfy_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Name %r>' % self.fullname


if __name__ == '__main__':
    app.run(debug=True, port=5000)
