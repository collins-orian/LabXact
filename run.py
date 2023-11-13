#!/usr/bin/env python3
"""This file runs the application"""

from labxact import create_app
from flask import render_template

app = create_app()

# home page


@app.route('/')
@app.route('/home')
def home():
    """This route takes you to the home page"""
    return render_template('index.html')


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



if __name__ == "__main__":
    app.run(debug=True)
