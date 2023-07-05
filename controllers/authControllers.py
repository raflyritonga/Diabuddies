from flask import render_template, request, session, redirect
from db import mysql


def loginPatient():
    return render_template('patientViews/auth/loginPatient.html')

def loginDoctor():
    return render_template('doctorViews/auth/loginDoctor.html')

def signupPatient():
    if request.method == 'POST':
        fullName = request.form.get('patient_fullName')
        username = request.form.get('patient_username')
        icNumber = request.form.get('patient_icNumber')
        password = request.form.get('patient_password')
        repeatPassword = request.form.get('patient_repeatPassword')

        if password == repeatPassword :
            conn = mysql.connection
            if conn:
                print('database connected')
                cur = conn.cursor()
                cur.execute("INSERT INTO patients (ic_number, full_name, username, password) VALUES (%s, %s, %s, %s)", (icNumber, fullName, username, password))
                conn.commit()
                cur.close()
                # session[username]
                # redirect here
                print('registered success')
                return render_template('patientViews/auth/loginPatient.html')
            else :
                return render_template('patientViews/auth/signupPatient.html')
        else :
            return print('Repeeat your passowrd correctly')    
 
    return render_template('patientViews/auth/signupPatient.html')

def signupDoctor():
    return render_template('doctorViews/auth/signupDoctor.html')