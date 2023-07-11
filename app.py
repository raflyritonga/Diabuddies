from flask import Flask, render_template
import pickle
from controllers import authControllers, dashboardControllers
from db import init_app

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rahasiaBangetNich'

scaler = pickle.load(open('models/scaler.pkl', 'rb'))
model = pickle.load(open('models/svm_model.pkl', 'rb'))

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

@app.route('/dashboarddoctor/signout')
def goToDashsboardDoctor_signout():
    return dashboardControllers.doctorDashboard_signout()


@app.route('/', methods=['GET'])
def input():

    # prediction = -1
    # name = None
    # if request.method == 'POST':
    #     name = request.form.get('name')
    #     pregs = int(request.form.get('pregs'))
    #     gluc = int(request.form.get('gluc'))
    #     bp = int(request.form.get('bp'))
    #     skin = int(request.form.get('skin'))
    #     insulin = float(request.form.get('insulin'))
    #     bmi = float(request.form.get('bmi'))
    #     func = float(request.form.get('func'))
    #     age = int(request.form.get('age'))

    #     input_features = [[pregs, gluc, bp, skin, insulin, bmi, func, age]]
    #     prediction = model.predict(scaler.transform(input_features))
        
        # Render inputs.html with user inputs
        # return render_template('index.html', name=name, preg=pregs, gluc=gluc, bp=bp, skin=skin, insulin=insulin, bmi=bmi, func=func, age=age, prediction=prediction)
    
    # Render index.html with the prediction result
    # return render_template('index.html', prediction=prediction, name=name)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
