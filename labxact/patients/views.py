#!/usr/bin/env python3
"""This file routes views for patient section of the app"""


from . import patient
from flask import request, render_template, redirect, url_for, flash
from ..logger import logger
from flask_login import login_required, current_user
from forms import PatientRegForm, PatientSearchForm, PatientUpdateForm
from utils import PatientService
from ...models.patient_model import Patients


# patient registration page
@patient.route('/register', methods=['GET', 'POST'])
@login_required
def add_patient():
    """This route takes you to the patient
    registration page"""

    pid = None
    all_patients = PatientService.all_patients()

    form = PatientRegForm()

    # generate the PID Number
    total_patients = PatientService.patient_count()
    num_digits = len(str(total_patients + 1))
    patient_id = f"PID-{str(total_patients + 1).zfill(num_digits)}"

    if form.validate_on_submit():
        try:
            pid = PatientService.get_patient_by_pid(patient_id)
            if pid is None:
                # Calculate the age of the patient based on the date of birth field in the form.
                # age = patients.calculate_age(form.dob.data)

                # Set the value of the age field in the form to the age that we calculated.
                # form.age.data = age

                PatientService.create_patient(form.patient_id.data,
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
            return redirect(url_for('patients.add_patient'))

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
            f'Patient ---> {form.patient_id.data} <---> registered by ---> {current_user}')
        # Calculate the age based on the date of birth
        return redirect(url_for("patients.add_patient"))
    return render_template('add_patient.html', form=form,
                           pid=patient_id, all_patients=all_patients,
                           current_user=current_user)


# pass data to the navbar
@patient.context_processor
def base():
    """This function passes data to the navbar"""
    form = PatientSearchForm()
    return dict(form=form)


# create search function
@patient.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = PatientSearchForm()
    results = Patients.query
    if form.validate_on_submit():
        # Get the search term from the form
        search = form.searched.data
        # Query the database for the search term neglecting case sensitivity

        results = results.filter(Patients.patient_id.ilike(
            '%' + search + '%') | Patients.firstname.ilike('%' + search + '%') |
            Patients.lastname.ilike('%' + search + '%'))
        results = results.order_by(Patients.patient_id)
        return render_template('search.html', form=form, searched=search, results=results)


# update patient page
@patient.route('/modify_patient/<int:id>', methods=['GET', 'POST'])
@login_required
def modify_patient(id):
    """This route takes you to patients update page"""
    form = PatientUpdateForm()
    patient_to_update = PatientService.get_patient(id)
    if request.method == "POST":
        try:
            PatientService.update_patient(patient_to_update,
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
                f'Patient ---> {patient_to_update} <---> details updated by ---> {current_user}')
            return redirect(url_for("patients.add_patient"))
        except:
            flash("Patient Details Update Failed!")
            return render_template("modify_patient.html", form=form,
                                   patient_to_update=patient_to_update, id=id)
    else:
        return render_template("modify_patient.html", form=form,
                               patient_to_update=patient_to_update, id=id)


# delete patient page
@patient.route('/delete_patient/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_patient(id):
    """This route deletes patient record"""
    form = PatientRegForm()
    all_patients = PatientService.all_patients()
    patient_to_delete = PatientService.get_patient(id)
    try:
        PatientService.delete_patient(patient_to_delete.id)
        flash("Patient Deleted Successfully")
        logger.info(
            f'Patient ---> {patient_to_delete} <---> deleted by ---> {current_user}')
        return render_template('add_patient.html', form=form,
                               all_patients=all_patients)

    except:
        flash("Patient Delete Failed!")
        return redirect(url_for('patients.add_patient'))
