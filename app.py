#!/usr/bin/env python3

from flask import Flask
from admin.admin import admin_blueprt
from models import db

app = Flask(__name__)

# registered blueprints...
app.register_blueprint(admin_blueprt, url_prefix="/admin")

# SQLalchemy Configurations...
app.secret_key = "iuiu21986*^GUIY&IV*88gg88oqwd"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:devops/ITS2022@localhost:3306/labxact"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
