from flask import render_template, request, session, redirect
from db import mysql

# ------------ PATIENT'S DASHBOARD LOGICS
def patientDashboard_profile():
    # get the session
    username = session['username']
    # database connection
    conn = mysql.connection
    if request.method == 'POST':
        fullName = request.form.get('patient_fullname')
        gender = request.form.get('patient_gender')
        icNumber = request.form.get('patient_icnumber')
        dateOfBirth = request.form.get('patient_dateofbirth')
        email = request.form.get('patient_email')
        occupation = request.form.get('patient_occupation')
        adress = request.form.get('patient_adress')

        if conn:
            print('database connected')
            cur = conn.cursor()
            query = """UPDATE patients 
                        SET ic_number = %s, full_name = %s, gender = %s, date_of_birth = %s, email = %s, occupation = %s, adress = %s 
                        WHERE username = %s"""
            cur.execute(query, (icNumber, fullName, gender, dateOfBirth, email, occupation, adress, username))
            conn.commit()
            print("data updated successful")
            redirect('/dashboardpatient/profile')
        else :
            print("failed to connect to the database")
            redirect('/dashboardpatient/profile')

    print('database connected')
    cur = conn.cursor()

    # retrieve data from database based on user's session
    cur.execute("SELECT * FROM patients WHERE username = %s", (username,))
    patientInformation = cur.fetchone()
    icNumber =  patientInformation[1] if patientInformation[1] is not None else "" 
    fullName = patientInformation[2] if patientInformation[2] is not None else ""   
    gender = patientInformation[5] if patientInformation[5] is not None else ""
    dateOfBirth = patientInformation[6] if patientInformation[6] is not None else ""
    email = patientInformation[7] if patientInformation[7] is not None else ""
    occupation = patientInformation[8] if patientInformation[8] is not None else ""
    adress = patientInformation[9] if patientInformation[9] is not None else ""

    return render_template(
        'patientViews/dashboard/profile.html',
        icNumberInHTML = icNumber,
        fullNameInHTML = fullName,
        genderInHTML = gender,
        dateOfBirthInHTML = dateOfBirth,
        emailInHTML = email,
        occupationInHTML = occupation,
        adressInHTML = adress
        )

def patientDashboard_inputData():
    username = session['username']
    return render_template('patientViews/dashboard/inputData.html')

def patientDashboard_viewReport():
    username = session['username']
    return render_template('patientViews/dashboard/viewReport.html')

def patientDashboard_signout():
    # Get the session
    username = session['username']

    # Clear the session data
    session.clear()
    print ('session for ', username,' killed suceessful ')

    # Redirect to the homepage or any other desired page
    return redirect('/')


# ------------ DOCTOR'S DASHBOARD LOGICS
def doctorDashboard_profile():
    # get the session
    username = session['username']
    # database connection
    conn = mysql.connection
    if request.method == 'POST':
        fullName = request.form.get('doctor_fullname')
        gender = request.form.get('doctor_gender')
        icNumber = request.form.get('doctor_icnumber')
        doctorId = request.form.get('doctor_doctorid')
        dateOfBirth = request.form.get('doctor_dateofbirth')
        email = request.form.get('doctor_email')
        hospital = request.form.get('doctor_hospital')

        if conn:
            print('database connected')
            cur = conn.cursor()
            query = """UPDATE doctors 
                        SET full_name = %s, ic_number = %s, doctor_id = %s, gender = %s, date_of_birth = %s, email = %s, hospital_placement = %s
                        WHERE username = %s"""
            cur.execute(query, (fullName, icNumber, doctorId, gender, dateOfBirth, email, hospital, username))
            conn.commit()
            print("data updated successful")
            redirect('/dashboarddoctor/profile')
        else :
            print("failed to connect to the database")
            redirect('/dashboarddoctor/profile')

    print('database connected')
    cur = conn.cursor()

    # retrieve data from database based on user's session
    cur.execute("SELECT * FROM doctors WHERE username = %s", (username,))
    doctorInformation = cur.fetchone()
    fullName = doctorInformation[1] if doctorInformation[1] is not None else ""   
    icNumber =  doctorInformation[2] if doctorInformation[2] is not None else "" 
    doctorId =  doctorInformation[4] if doctorInformation[4] is not None else "" 
    gender = doctorInformation[6] if doctorInformation[6] is not None else ""
    dateOfBirth = doctorInformation[7] if doctorInformation[7] is not None else ""
    email = doctorInformation[8] if doctorInformation[8] is not None else ""
    hospital = doctorInformation[9] if doctorInformation[9] is not None else ""

    return render_template(
        'doctorViews/dashboard/profile.html',
        fullNameInHTML = fullName,
        icNumberInHTML = icNumber,
        doctorIdInHTML = doctorId,
        genderInHTML = gender,
        dateOfBirthInHTML = dateOfBirth,
        emailInHTML = email,
        hospitalInHTML = hospital
    )

def doctorDashboard_viewReport():
    username = session['username']
    return render_template('doctorViews/dashboard/viewReport.html')

def doctorDashboard_signout():
    # Get the session
    username = session['username']

    # Clear the session data
    session.clear()
    print ('session for ', username,' killed suceessful ')

    # Redirect to the homepage or any other desired page
    return redirect('/')