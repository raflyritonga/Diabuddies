from flask import render_template, request, session, redirect
from db import mysql
from datetime import date
import pickle
from fpdf import FPDF

scaler = pickle.load(open('models/scaler.pkl', 'rb'))
model = pickle.load(open('models/svm_model.pkl', 'rb'))
 
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
    conn = mysql.connection
    prediction = -1
    
    if request.method == 'POST':
        # Personal Information
        fullName = request.form.get('input_fullname')
        gender = request.form.get('input_gender')
        icNumber = request.form.get('input_icnumber')
        age = request.form.get('input_age')
        email = request.form.get('input_email')
        occupation = request.form.get('input_occupation')
        adress = request.form.get('input_adress')

        # Medical data
        pregnancies = request.form.get('input_pregnancies')
        glucoseLevel = request.form.get('input_glucoselevel')
        bloodPresure = request.form.get('input_bloodpresure')
        skinThickness = request.form.get('input_skinthickness')
        insulin = request.form.get('input_insulin')
        bmi = request.form.get('input_bmi')
        function = request.form.get('input_function')

        # using machine learning model
        input_features = [[pregnancies, glucoseLevel, bloodPresure, skinThickness, insulin, bmi, function, age]]
        prediction = model.predict(scaler.transform(input_features))

        # Saving the records into the database
        print('database connected')
        todayDate = date.today()
        cur = conn.cursor()
        cur.execute("INSERT INTO reports (account, full_name, result, submission_date) VALUES (%s, %s, %s, %s)", (username, fullName, int(prediction), todayDate))
        conn.commit()
        cur.close()

        # calling function to create PDF report
        createPDF(
            fullName, gender, icNumber, age, email, occupation, adress,
            pregnancies, glucoseLevel, bloodPresure, skinThickness, insulin, bmi, function,
            prediction, todayDate
        )   
        print(prediction)
        print("data inputed successful")
        return redirect('/dashboardpatient/report')
    return render_template('patientViews/dashboard/inputData.html')

def patientDashboard_viewReport():
    username = session['username']
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute("SELECT * FROM reports WHERE account = %s", (username,))
    data = cur.fetchall()

    return render_template('patientViews/dashboard/viewReport.html', data = data)

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
    conn = mysql.connection
    cur = conn.cursor()      
    cur.execute("SELECT * FROM reports WHERE status = 0")
    data = cur.fetchall()
    return render_template('doctorViews/dashboard/viewReport.html', data = data)

def doctorDashboard_signout():
    # Get the session
    username = session['username']

    # Clear the session data
    session.clear()
    print ('session for ', username,' killed suceessful ')

    # Redirect to the homepage or any other desired page
    return redirect('/')

def doctorDashboard_viewReportValidate():
    conn = mysql.connection
    cur = conn.cursor()
    
    if request.method == 'POST':
        requestData = request.get_json()
        fullName = requestData.get('name')
        submissionDate = requestData.get('date')
        status = 1
        cur.execute("""UPDATE reports
                    SET status = %s WHERE full_name = %s AND submission_date = %s""", (status, fullName, submissionDate))
        conn.commit()
        print(fullName)
        print(submissionDate)
        print('Status changed')
    else:
        print('ERROR')
    return redirect ('/dashboarddoctor/report')

def createPDF(
        fullName, gender, icNumber, age, email, occupation, adress,
        pregnancies, glucoseLevel, bloodPresure, skinThickness, insulin, bmi, function,
        prediction, todayDate):
    
    if prediction == 0:
        result = 'NEGATIVE'
    else:
        result = 'POSITIVE'

    currDate = date.today()
    class PDF(FPDF):
        def header(self):
        #    set font    
            self.set_font('courier', 'I', 10)
        #    set text
            self.cell(0, 10, 'AUTO GENERATED REPORT', border = True, ln = 1, align = 'C')
            self.cell(0, 10, 'submission date: ' + todayDate.strftime('%Y-%m-%d'), ln = 1, align = 'R')
            self.cell(0, 10, 'generated on:  ' + currDate.strftime('%Y-%m-%d'), ln = 1, align = 'R')
            
    # create the pdf
    pdf = PDF('P', 'mm', 'Letter')

    # set auto page break
    pdf.set_auto_page_break(auto = 1, margin = 5)

    #add page
    pdf.add_page()

    # specify font and text
    pdf.set_font ('courier', 'B', 12)
    pdf.cell(40,10, 'Personal Information:', ln = 1 )

    pdf.set_font ('courier', '', 12)
    pdf.cell(40,10, 'Name: ' + str(fullName) , ln = 1)
    pdf.cell(40,10, 'IC Number: ' + str(icNumber), ln = 1)
    pdf.cell(40,10, 'Gender: ' + str(gender), ln = 1)
    pdf.cell(40,10, 'Age: ' + str(age), ln = 1)
    pdf.cell(40,10, 'Email: ' + str(email), ln = 1)
    pdf.cell(40,10, 'Occupation: ' + str(occupation), ln = 1)
    pdf.cell(40,10, 'Adress: ' + str(adress), ln = 1)

    # specify font and text
    pdf.cell(40,10, '', ln = 1)
    pdf.set_font ('courier', 'B', 12)
    pdf.cell(40,10, 'Medical Information:', ln = 1 )

    pdf.set_font ('courier', '', 12)
    pdf.cell(40,10, 'Pregnancies: ' + str(pregnancies), ln = 1)
    pdf.cell(40,10, 'Glucose Level: ' + str(glucoseLevel), ln = 1)
    pdf.cell(40,10, 'Blood Preasure: ' + str(bloodPresure), ln = 1)
    pdf.cell(40,10, 'Skin Thickness: ' + str(skinThickness), ln = 1)
    pdf.cell(40,10, 'Insulin: ' + str(insulin), ln = 1)
    pdf.cell(40,10, 'Body Mass Index: ' + str(bmi), ln = 1)
    pdf.cell(40,10, 'Diabetes Pedigree Function: ' + str(function), ln = 1)

    pdf.cell(40,10, '', ln = 1)
    pdf.cell(40,10, 'By the input data above, your test result is', ln = 1)

    pdf.set_font ('courier', 'BU', 12)
    pdf.cell(200,10, result, ln = 1)

    pdf.set_font ('courier', '', 12)
    pdf.cell(40,10, '', ln = 1)
    pdf.cell(40,10, 'Regrads', ln = 1)
    pdf.cell(40,10, 'Diabuddies', ln = 1)

    # save the file
    output_folder = 'D:/05_development/Diabuddies/models/reports'
    output_filename = f"{fullName}{currDate.strftime('%Y-%m-%d')}.pdf"
    output_path = f"{output_folder}/{output_filename}"
    pdf.output(output_path)
