from flask import render_template, request, session, redirect
from db import mysql

def patientDashbboard_profile():
    return render_template('patientViews/dashboard/profile.html')

def patientDashbboard_inputData():
    return render_template('patientViews/dashboard/inputData.html')

def patientDashbboard_viewReport():
    return render_template('patientViews/dashboard/viewReport.html')

def patientDashbboard_signout():
    return render_template('patientViews/auth/loginPatient.html')






def doctorDashbboard_profile():
    return render_template('doctorViews/dashboard/profile.html')


def doctorDashbboard_viewReport():
    return render_template('doctorViews/dashboard/viewReport.html')