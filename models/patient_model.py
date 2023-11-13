#!usr/bin/env python3

"""Contains the patient model for the app."""


# All the imports
from sqlalchemy import Column, Integer, String, Date, Enum, DateTime
from datetime import datetime
from labxact.extensions import db


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

    def __str__(self):
        """This method returns the patients fullname and other details
        as string"""

        return f'{self.patient_id} - {self.firstname} {self.lastname} - {self.email}'


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
