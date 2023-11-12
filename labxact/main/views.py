#!/usr/bin/env python3
"""This file routes views for admin section of the app"""

from flask import render_template
from . import main


# home page
@main.route('/')
@main.route('/home')
def home():
    """This route takes you to the home page"""
    return render_template('index.html')


# Invalid URL
@main.errorhandler(404)
def page_not_found(e):
    """This route returns an error page if page
    is not found"""
    return render_template('404.html'), 404


# Internal server error
@main.errorhandler(500)
def internal_server_error(e):
    """This route returns an error page when the
    server is down or has issues"""
    return render_template('500.html'), 500
