import re
from flask_app import app,render_template, redirect, request, bcrypt, session, flash 
from flask_app.models.patient import Patient
from flask_app.models.doctor import Doctor




@app.route("/pat/reg")
def patreg():
    return render_template("login_regpat.html")

@app.route('/register/patient', methods = ['POST'])
def register_patient():
    patient = Patient.get_by_email(request.form)
    if patient:
        flash("already patient")
        return redirect('/home')
    print(request.form)
    if not Patient.validate_patient(request.form):
        return redirect('/home')     
    pw_hashed = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hashed)
    patient_data = {
        'name': request.form['name'],
        'email': request.form['email'],
        'pet_name': request.form['pet_name'],
        'password': pw_hashed,

    }
    patient_id = Patient.save(patient_data)
    session['patient_id'] = patient_id
    session['name'] = request.form['name']
    return redirect('/pat/reg')

@app.route("/login/pat", methods=['POST'])
def loginpat():
    print(request.form)
    patient = Patient.get_by_email(request.form)
    if not patient:
        flash("invalid credentials")
        return redirect('/home')
    password_valid = bcrypt.check_password_hash(patient.password, request.form['password'])
    if not password_valid:
        flash("invalid credentials")
        return redirect('/home')
    session['patient_id'] = patient.id
    session['name'] = patient.name
    return redirect('/home')

@app.route("/waitlist")
def waitlist():
    return render_template("waitlist.html")

@app.route("/addto/waitlist")
def add_waitlist():
    if 'wait_list' not in session:
        session['wait_list'] = []
        patient = Patient.get_one({'id': session['patient_id']})
        session['wait_list'].append(patient)
    else:
        patient = Patient.get_one({'id': session['patient_id']})
        session['wait_list'].append(patient)

    return redirect('/waitlist')

@app.route('/new_patients', methods=['POST'])
def new_patients():
    print(request.form)
    Patient.save(request.form)
    if not Patient.validate_patients(request.form):
        return redirect('/bob')     
    return redirect('/newpat_form')

@app.route('/newpat_form')
def newpat_form():
    return render_template('new_patient.html')

@app.route('/patients/<int:id>')
def show(id):
    data = {'id': id}
    patients = Patient.get_one(data)
    return render_template('show.html', patients= patients)

@app.route('/patients')
def patient():
    if 'doctor_id' not in session:
        return redirect('/logout')
    return render_template('index.html')

@app.route('/edit/<int:id>')
def edit_patients(id):
    data = {'id': id}
    return render_template('edit_patients.html', patients = Patient.get_one(data))

@app.route('/update/patients', methods = ['POST'])
def update_patients():
    print(request.form)
    if not Patient.validate_patients(request.form):
        return redirect(f"/edit/{request.form['id']}")     
    Patient.update(request.form)
    return redirect('/patientss')

@app.route('/delete/<int:id>')
def delete_patients(id):
    data = {'id': id}
    Patient.destroy(data)
    return redirect('/patientss')
