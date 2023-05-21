#!/usr/bin/env python3

from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Users

admin_blueprt = Blueprint("admin", __name__, static_folder="static",
                          template_folder="templates")


@admin_blueprt.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = Users.query.filter_by(
            uname=username, passwd=password).first()

        # Check if the user exists and is an admin
        if user and user.role == "admin":
            # User is valid and is an admin
            return redirect(url_for('admin.admin_dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')


@admin_blueprt.route("/dashboard")
def admin_dashboard():
    return render_template('index.html')


@admin_blueprt.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        fullname = request.form.get('fullname')
        designation = request.form.get('designation')

        # Create a new table if it doesn't exist
        if not Users.__table__.exists(db.engine):
            db.create_all()

        # Creste a new user
        new_user = Users(uname=username, passwd=password,
                         fname=fullname, role=designation)
        db.session.add(new_user)
        db.session.commit()

        return 'User created successfully'

    return render_template('create_user.html')
