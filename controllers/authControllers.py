from flask import render_template, request, session, redirect
from db import mysql
import hashlib

def loginPatient():
    if request.method == 'POST':
        username = request.form.get('patient_username')
        password = request.form.get('patient_password')
        conn = mysql.connection
        conn = mysql.connection
        if conn:
            print('database connected')
            cur = conn.cursor()

            # Cheaking
            cur.execute("SELECT * FROM patients WHERE username = %s", (username,))
            patient = cur.fetchone()
            if patient is not None:
                storedPass = patient['password']
                if hashlib.md5(password.encode()).hexdigest() == storedPass:
                    session['username'] = username
                    print('Login as ', session.get('username'), 'Successful!')
                    return redirect('/dashboardpatient')
                else:
                    print('Incorrect Password')
                    return redirect('/loginpatient')
            else:
                print('Patient not found')
                return redirect('/loginpatient')
        else :
            print('Connection failed')
            return redirect('/loginpatient')    
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

        # Password and repeatPassword cheaking
        if password == repeatPassword :
            conn = mysql.connection
            if conn:
                print('database connected')
                cur = conn.cursor()

                # Username cheaking
                cur.execute("SELECT * FROM patients WHERE username = %s", (username,))
                result = cur.fetchone()
                if result is not None:
                    print('Username already exists')
                    return redirect('/signuppatient')
                
                encryptedPassword = hashlib.md5(password.encode()).hexdigest()
                # Adding new user
                cur.execute("INSERT INTO patients (ic_number, full_name, username, password) VALUES (%s, %s, %s, %s)", (icNumber, fullName, username, encryptedPassword))
                conn.commit()
                cur.close()
                # session[username]
                # redirect here
                print('registered success')
                return redirect('/loginpatient')
            else :
                return redirect('/signuppatient')
        else :
            print('Repeat your passowrd correctly')    
            return redirect('/signuppatient')
 
    return render_template('patientViews/auth/signupPatient.html')

def signupDoctor():
    return render_template('doctorViews/auth/signupDoctor.html')