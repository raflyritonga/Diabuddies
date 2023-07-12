from flask import Flask, render_template
import pickle
from controllers import authControllers, dashboardControllers
from db import init_app

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rahasiaBangetNich'

init_app(app)

# --------------- ROUTES FOR PATIENT AUTHENTICATION
@app.route('/signuppatient', methods = ['GET', 'POST'])
def goToSignupPatient():
    return authControllers.signupPatient()
@app.route('/loginpatient', methods = ['GET', 'POST'])
def goToLoginPatient():
    return authControllers.loginPatient()



# --------------- ROUTES FOR DOCTOR AUTHENTICATION
@app.route('/signupdoctor', methods = ['GET', 'POST'])
def goToSignupDoctor():
    return authControllers.signupDoctor()
@app.route('/logindoctor', methods = ['GET', 'POST'])
def goToLoginDoctor():
    return authControllers.loginDoctor()



# -------------- ROUTES FOR PATIENT DASHBOARD
@app.route('/dashboardpatient/profile', methods = ['GET', 'POST'])
def goToDashboardPatient_profile():
    return dashboardControllers.patientDashboard_profile()

@app.route('/dashboardpatient/input', methods = ['GET', 'POST'])
def goToDashsboardPatient_inputData():
    return dashboardControllers.patientDashboard_inputData()

@app.route('/dashboardpatient/report', methods = ['GET', 'POST'])
def goToDashsboardPatient_viewReport():
    return dashboardControllers.patientDashboard_viewReport()

@app.route('/dashboardpatient/signout')
def goToDashsboardPatient_signout():
    return dashboardControllers.patientDashboard_signout()


# -------------- ROUTES FOR DOCTOR DASHBOARD
@app.route('/dashboarddoctor/profile', methods = ['GET', 'POST'])
def goToDashboardDoctor_profile():
    return dashboardControllers.doctorDashboard_profile()

@app.route('/dashboarddoctor/report', methods = ['GET', 'POST'])
def goToDashsboardDoctor_viewReport():
    return dashboardControllers.doctorDashboard_viewReport()

@app.route('/dashboarddoctor/report/validate', methods = ['GET', 'POST'])
def goToDashsboardDoctor_viewReportValidate():
    return dashboardControllers.doctorDashboard_viewReportValidate()

@app.route('/dashboarddoctor/signout')
def goToDashsboardDoctor_signout():
    return dashboardControllers.doctorDashboard_signout()


@app.route('/', methods=['GET'])
def input():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
