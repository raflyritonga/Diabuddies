from flask import render_template, request, session, redirect
from db import mysql

def patientDashboard_profile():
    if request.method == 'POST':
        return 0





    # get the session
    username = session['username']
    # database connection
    conn = mysql.connection
    print('database connected')
    cur = conn.cursor()
    # retrieve data from database based on user's session
    cur.execute("SELECT * FROM patients WHERE username = %s", (username,))
    patientInformation = cur.fetchone()
    icNumber = patientInformation[1]
    fullName = patientInformation[2]    
    return render_template(
        'patientViews/dashboard/profile.html',
        icNumberInHTML = icNumber,
        fullNameInHTML = fullName
        )

def patientDashboard_inputData():
    return render_template('patientViews/dashboard/inputData.html')

def patientDashboard_viewReport():
    return render_template('patientViews/dashboard/viewReport.html')

def patientDashboard_signout():
    return render_template('patientViews/auth/loginPatient.html')






def doctorDashbboard_profile():
    return render_template('doctorViews/dashboard/profile.html')


def doctorDashbboard_viewReport():
    return render_template('doctorViews/dashboard/viewReport.html')