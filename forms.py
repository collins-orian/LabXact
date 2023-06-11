from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, DateField
from wtforms.validators import data_required, equal_to


# create user form class
class UserForm(FlaskForm):
    fullname = StringField("Fullname", validators=[data_required()])
    username = StringField("Username", validators=[data_required()])
    email = StringField("Email", validators=[data_required()])
    role = SelectField(u'Role', choices=[('labstaff', 'Laboratory Staff'), ('labmanager', 'Laboratory Manager'), (
        'super', 'Supervisor'), ('admin', 'Administrator')], validators=[data_required()])
    section = SelectField(u'Assigned Section', choices=[('Reception', 'Reception'),('Chemistry', 'Clinical Chemistry'), ('Haematology', 'Haematology'), (
        'Microbiology', 'Medical Microbiology')], validators=[data_required()])
    password = PasswordField("Password", validators=[data_required(), equal_to(
        'password_confirm', message="Passwords Must match")])
    password_confirm = PasswordField(
        "Confirm Password", validators=[data_required()])
    submit = SubmitField("Add User")


# create user form class
class UpdateUserForm(FlaskForm):
    fullname = StringField("Fullname", validators=[data_required()])
    username = StringField("Username", validators=[data_required()])
    email = StringField("Email", validators=[data_required()])
    role = SelectField(u'Role', choices=[('labstaff', 'Laboratory Staff'), ('labmanager', 'Laboratory Manager'), (
        'super', 'Supervisor'), ('admin', 'Administrator')], validators=[data_required()])
    section = SelectField(u'Assigned Section', choices=[('Reception', 'Reception'),('Chemistry', 'Clinical Chemistry'), ('Haematology', 'Haematology'), (
        'Microbiology', 'Medical Microbiology')], validators=[data_required()])
    password = PasswordField("Password", validators=[data_required(), equal_to(
        'password_confirm', message="Passwords Must match")])
    password_confirm = PasswordField(
        "Confirm Password", validators=[data_required()])
    submit = SubmitField("Update User")


# create login form
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[data_required()])
    password = PasswordField("Password", validators=[data_required()])
    submit = SubmitField("Login")


# patient registration form
class PatientRegForm(FlaskForm):
    patient_id = StringField("Patient ID Number (PID)",
                             validators=[data_required()])
    firstname = StringField("Firstname", validators=[data_required()])
    middlename = StringField("Middlename")
    lastname = StringField("Lastname", validators=[data_required()])
    dob = DateField("Date Of Birth", validators=[
                    data_required()], format='%Y-%m-%d')
    age = StringField("Age", validators=[data_required()])
    gender = SelectField("Gender", validators=[data_required()], choices=[
                         ('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')])
    email = StringField("Email")
    mobile = StringField("Mobile", validators=[data_required()])
    address = StringField("Address", validators=[data_required()])
    submit = SubmitField("Register")
