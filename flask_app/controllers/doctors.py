import re
from flask_app import app,render_template, redirect, request, bcrypt, session, flash 
from flask_app.models.doctor import Doctor




@app.route("/")
def index():
    return render_template('intro.html')

@app.route("/home")
def home():
    return render_template('index.html')

@app.route('/register', methods = ['POST'])
def register():
    doctor = Doctor.get_by_email(request.form)
    if doctor:
        flash("already doctor")
        return redirect('/home')
    print(request.form)
    if not Doctor.validate_doctor(request.form):
        return redirect('/home')     
    pw_hashed = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hashed)
    doctor_data = {
        'name': request.form['name'],
        'email': request.form['email'],
        'password': pw_hashed
    }
    doctor_id = Doctor.save(doctor_data)
    session['doctor_id'] = doctor_id
    session['name'] = request.form['name']
    return redirect('/doc_patients')

@app.route('/doc_patients')
def docpatients():
    return render_template('patients.html')

@app.route("/login_reg")
def login_reg():
    return render_template('login_reg.html')

@app.route("/login", methods=['POST'])
def login():
    print(request.form)
    doctor = Doctor.get_by_email(request.form)
    if not doctor:
        flash("invalid credentials")
        return redirect('/home')
    password_valid = bcrypt.check_password_hash(doctor.password, request.form['password'])
    if not password_valid:
        flash("invalid credentials")
        return redirect('/home')
    session['doctor_id'] = doctor.id
    session['name'] = doctor.name
    return redirect('/doc_patients')

@app.route('/show/doctor')
def show_doctor():
    data = {'id': session['doctor_id']}
    return render_template('show_doctor.html', doctor = Doctor.get_one_with_recipes(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/home')