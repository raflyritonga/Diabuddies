from flask import render_template, request, session, redirect
from db import mysql
import hashlib

# ------ SIGNUP PATIENT ------------
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

                print('registered success')
                return redirect('/loginpatient')
            else :
                return redirect('/signuppatient')
        else :
            print('Repeat your passowrd correctly')    
            return redirect('/signuppatient')
 
    return render_template('patientViews/auth/signupPatient.html')

# ------ LOGIN PATIENT ------------
def loginPatient():
    if request.method == 'POST':
        username = request.form.get('patient_username')
        password = request.form.get('patient_password')
        conn = mysql.connection
        if conn:
            print('database connected')
            cur = conn.cursor()

            # Cheaking
            cur.execute("SELECT * FROM patients WHERE username = %s", (username,))
            patient = cur.fetchone()
            if patient is not None:
                storedPass = patient[4]
                if hashlib.md5(password.encode()).hexdigest() == storedPass:
                    # session
                    session['username'] = username
                    print('Login as', session['username'], 'Successful!')
                    if 'username' in session :
                        user = session['username']
                        print('This session belongs to ', user)
                        return redirect('/dashboardpatient/profile') 
                    else:
                        return redirect('/loginpatient')              
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



# ------ SIGNUP DOCTOR ------------
def signupDoctor():
    if request.method == 'POST':
        fullName = request.form.get('doctor_fullName')
        username = request.form.get('doctor_username')
        doctorId = request.form.get('doctor_doctorId')
        icNumber = request.form.get('doctor_icNumber')
        password = request.form.get('doctor_password')
        repeatPassword = request.form.get('doctor_repeatPassword')

        # Password and repeatPassword cheaking
        if password == repeatPassword :
            conn = mysql.connection
            if conn:
                print('database connected')
                cur = conn.cursor()

                # Username cheaking
                cur.execute("SELECT * FROM doctors WHERE username = %s", (username,))
                result = cur.fetchone()
                if result is not None:
                    print('Username already exists')
                    return redirect('/signupdoctor')
                
                encryptedPassword = hashlib.md5(password.encode()).hexdigest()
                # Adding new user
                cur.execute("INSERT INTO doctors (full_name, ic_number, username, doctor_id, password) VALUES (%s, %s, %s, %s, %s)", (fullName, icNumber, username, doctorId, encryptedPassword))
                conn.commit()
                cur.close()

                print('registered success')
                return redirect('/logindoctor')
            else :
                return redirect('/signupdoctor')
        else :
            print('Repeat your passowrd correctly')    
            return redirect('/signupdoctor')
        
    return render_template('doctorViews/auth/signupDoctor.html')


# ------ LOGIN DOCTOR ------------
def loginDoctor():
    if request.method == 'POST':
        username = request.form.get('doctor_username')
        doctorId = request.form.get('doctor_doctorId')
        password = request.form.get('doctor_password')
        conn = mysql.connection
        if conn:
            print('database connected')
            cur = conn.cursor()

            # Cheaking
            cur.execute("SELECT * FROM doctors WHERE username = %s", (username,))
            doctor = cur.fetchone()
            if doctor is not None:
                storedPass = doctor[5]
                storedDoctorId = doctor[4]
                if hashlib.md5(password.encode()).hexdigest() == storedPass:
                    if doctorId == storedDoctorId:
                        # session
                        session['username'] = username
                        print('Login as', session['username'], 'Successful!')
                        if 'username' in session :
                            user = session['username']
                            print('This session belongs to ', user)
                            return redirect('/dashboarddoctor/profile') 
                        else:
                            return redirect('/logindoctor')  
                    else:
                        print('Doctor Id is wrong')
                        return redirect('/logindoctor')  
                else:
                    print('Incorrect Password')
                    return redirect('/logindoctor')
            else:
                print('Patient not found')
                return redirect('/logindoctor')
        else :
            print('Connection failed')
            return redirect('/logindoctor')  

    return render_template('doctorViews/auth/loginDoctor.html')