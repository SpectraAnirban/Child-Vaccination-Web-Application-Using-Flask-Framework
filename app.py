from flask_migrate import Migrate
import io
from datetime import datetime

from flask import Flask, render_template, request, redirect, flash, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test1.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    # ... add other columns as needed

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    # ... add other columns as needed

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    # ... add other columns as needed

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    child_name = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    # ... other fields as needed


class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    child_name = db.Column(db.String(100), nullable=False)
    parents_name = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    blood_group = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    postcode = db.Column(db.String(20), nullable=False)


class BookAppointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)  # New foreign key for hospital
    child_name = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default="pending")  # New status field with default value

    hospital = db.relationship('Hospital', backref=db.backref('appointments', lazy=True))


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    report_pdf = db.Column(db.LargeBinary, nullable=False)  # Store the PDF binary data

    user = db.relationship('User', backref=db.backref('reports', lazy=True))
    hospital = db.relationship('Hospital', backref=db.backref('reports', lazy=True))






@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if user exists in User table
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect('/user-home')

        # Check if user exists in Admin table
        admin = Admin.query.filter_by(username=username, password=password).first()
        if admin:
            session['admin_id'] = admin.id
            return redirect('/admindash')

        hospitals = Hospital.query.filter_by(username=username, password=password).first()
        if hospitals:
            session['hospital_id'] = hospitals.id
            return redirect('/hospital')

        return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')

    return render_template('register.html')


@app.route('/update_password', methods=['GET', 'POST'])
def update_password():
    if request.method == 'POST':
        user_email = request.form['user_email']

        if 'user_id' in session:
            user_id = session['user_id']
            user = User.query.filter_by(email=user_email, id=user_id).first()

            if not user:
                flash('No user found with this email and user ID.', 'error')
            else:
                new_password = request.form['new_password']
                confirm_new_password = request.form['confirm_new_password']

                if new_password != confirm_new_password:
                    flash('New passwords do not match.', 'error')
                else:
                    user.password = new_password
                    db.session.commit()
                    flash('Password updated successfully!', 'success')
                    return redirect(url_for('login'))
        else:
            flash('Session not found or expired. Please log in again.', 'error')

    return render_template('forgotpassword.html')


@app.route('/user-home', methods=['GET', 'POST'])
def user_home():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)

        user_profiles = UserProfile.query.filter_by(user_id=user_id).all()

        return render_template('userhome.html', user=user, user_profiles=user_profiles)
    else:
        return "User not logged in"


@app.route('/add_child', methods=['GET', 'POST'])
def add_child():
    if request.method == 'POST':
        child_name = request.form['child_name']
        parents_name = request.form['parents_name']
        contact_number = request.form['contact_number']
        birthdate_str = request.form['birthdate']  # Get the birthdate as a string
        birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d').date()  # Convert string to date object
        gender = request.form['gender']
        blood_group = request.form['blood_group']
        address = request.form['address']
        postcode = request.form['postcode']

        user_id = session.get('user_id')  # Get the user ID from the session

        new_child = UserProfile(
            user_id=user_id,
            child_name=child_name,
            parents_name=parents_name,
            contact_number=contact_number,
            birthdate=birthdate,
            gender=gender,
            blood_group=blood_group,
            address=address,
            postcode=postcode
        )

        db.session.add(new_child)
        db.session.commit()

        return redirect(url_for('user_home'))

    return render_template('addchildinfo.html')


@app.route('/edit_profile/<int:profile_id>', methods=['GET', 'POST'])
def edit_profile(profile_id):
    profile = UserProfile.query.get_or_404(profile_id)

    if request.method == 'POST':
        profile.child_name = request.form['child_name']
        profile.parents_name = request.form['parents_name']
        profile.contact_number = request.form['contact_number']
        profile.birthdate = datetime.strptime(request.form['birthdate'], '%Y-%m-%d').date()
        profile.gender = request.form['gender']
        profile.blood_group = request.form['blood_group']
        profile.address = request.form['address']
        profile.postcode = request.form['postcode']

        db.session.commit()

        return redirect(url_for('user_home'))

    if request.method == 'GET':
        action = request.args.get('action', '')  # Get the action parameter from the URL
        if action == 'delete':
            db.session.delete(profile)
            db.session.commit()
            flash("Child profile deleted successfully.", 'success')
            return redirect(url_for('user_home'))

    return render_template('edit_profile.html', profile=profile)


from datetime import datetime


@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        child_name = request.form['child_name']
        contact_number = request.form['contact_number']
        birthdate = datetime.strptime(request.form['birthdate'], '%Y-%m-%d').date()  # Convert to Python date object
        gender = request.form['gender']
        appointment_date = datetime.strptime(request.form['appointment_date'], '%Y-%m-%dT%H:%M').replace(tzinfo=None)
        hospital_id = int(request.form['hospital'])  # Assuming the hospital field name is 'hospital' in the HTML form
        user_id = session.get('user_id')

        # Create a new BookAppointment object
        appointment = BookAppointment(
            user_id=user_id,
            hospital_id=hospital_id,
            child_name=child_name,
            contact_number=contact_number,
            birthdate=birthdate,
            gender=gender,
            appointment_date=appointment_date,
        )

        # Add the appointment to the database
        db.session.add(appointment)
        db.session.commit()

        flash('Appointment booked successfully!', 'success')
        return redirect('/user-home')

    else:
        # Retrieve the user_id from the session
        user_id = session.get('user_id')

        # Retrieve the user from the database
        user = User.query.get(user_id)

        # Retrieve the list of registered hospitals from the database
        hospitals = Hospital.query.all()

        return render_template('book_appointmnet.html', user=user, hospitals=hospitals)


from flask import send_file


@app.route('/user_reports', methods=['GET', 'POST'])
def user_reports():
    user_id = session.get('user_id')  # Replace with the way you retrieve user ID from the session

    user_reports = Report.query.filter_by(user_id=user_id).all()
    return render_template('reportdownload.html', user_reports=user_reports)


from flask import Response

@app.route('/download_user_report/<int:report_id>', methods=['GET', 'POST'])
def download_user_report(report_id):
    user_id = session.get('user_id')  # Replace with the way you retrieve user ID from the session

    report = Report.query.filter_by(id=report_id, user_id=user_id).first()
    if not report:
        flash('Report not found or you do not have access to it.', 'error')
        return redirect(url_for('user_reports'))

    response = Response(report.report_pdf, content_type='application/pdf')
    response.headers['Content-Disposition'] = f'attachment; filename=report.pdf'

    return response


from flask import session


@app.route('/appo', methods=['GET', 'POST'])
def appo():
    user_id = session.get('user_id')
    user_appointments = BookAppointment.query.filter_by(user_id=user_id,status='Approved').all()
    return render_template('viewappo.html', appointments=user_appointments)


@app.route('/reject', methods=['GET', 'POST'])
def reject():
    user_id = session.get('user_id')
    rejected_appointments = BookAppointment.query.filter_by(user_id=user_id, status='Rejected').all()
    return render_template('rejectappo.html', appointments=rejected_appointments)


@app.route('/admindash', methods=['GET', 'POST'])
def admindash():
    admin_id = session.get('admin_id')
    if admin_id:
        users = User.query.all()
        return render_template('admindash.html', users=users)
    else:
        return "User not logged in"


@app.route('/reghospitals', methods=['GET', 'POST'])
def reghospitals():
    admin_id = session.get('admin_id')
    if admin_id:
        users = Hospital.query.all()
        return render_template('reghospitals.html', users=users)
    else:
        return "User not logged in"


@app.route('/Confirmappo', methods=['GET', 'POST'])
def Confirmappo():
    appointments = BookAppointment.query.all()
    return render_template('confirmappo.html', appointments=appointments)


@app.route('/approvedappo')
def approvedappo():
    approved_appointments = BookAppointment.query.filter_by(status='Approved').all()
    return render_template('approvedappo.html', appointments=approved_appointments)


@app.route('/approve/<int:appointment_id>')
def approve_appointment(appointment_id):
    appointment = BookAppointment.query.get(appointment_id)
    if appointment:
        appointment.status = "Approved"
        db.session.commit()
        flash(f"Appointment for {appointment.child_name} has been approved.", "success")
    return redirect('/hospital')

@app.route('/reject/<int:appointment_id>')
def reject_appointment(appointment_id):
    appointment = BookAppointment.query.get(appointment_id)
    if appointment:
        appointment.status = "Rejected"
        db.session.commit()
        flash(f"Appointment for {appointment.child_name} has been rejected.", "danger")
    return redirect('/hospital')


from flask import flash, redirect, render_template, url_for

@app.route('/uploadreport', methods=['GET', 'POST'])
def upload_report():
    if request.method == 'POST':
        file = request.files['file']
        user_name = request.form['user_name']  # Get the provided username from the hospital

        user = User.query.filter_by(username=user_name).first()
        if not user:
            flash('User not found!', 'error')
            return redirect(url_for('upload_report'))

        user_id = user.id
        hospital_id = session.get('hospital_id')  # Assuming the hospital is logged in

        pdf_data = file.read()  # Read the uploaded PDF file as bytes

        report = Report(user_id=user_id, hospital_id=hospital_id, report_pdf=pdf_data)
        db.session.add(report)
        db.session.commit()

        flash('Report uploaded successfully!', 'success')
        return redirect(url_for('upload_report'))

    return render_template('reportupload.html')



@app.route('/hospital', methods=['GET', 'POST'])
def hospital():
    hospital_id = session.get('hospital_id')  # Assuming you store hospital_id in the session
    appointments = BookAppointment.query.filter(
        BookAppointment.hospital_id == hospital_id,
        BookAppointment.status == 'pending'
    ).all()
    return render_template('hospitallogin.html', appointments=appointments)


@app.route('/setdate', methods=['GET', 'POST'])
def setdate():
    hospital_id = session.get('hospital_id')  # Assuming you store hospital_id in the session
    statuses_to_include = ['Approved', 'Vaccination-Started', 'Vaccination-Completed', 'Report-Uploaded']
    appointments = BookAppointment.query.filter(
        BookAppointment.hospital_id == hospital_id,
        BookAppointment.status.in_(statuses_to_include)
    ).all()
    return render_template('setdate.html', appointments=appointments)


@app.route('/update_status/<int:appointment_id>/<status>', methods=['GET', 'POST'])
def update_status(appointment_id, status):
    appointment = BookAppointment.query.get(appointment_id)
    if appointment:
        appointment.status = status
        db.session.commit()
        flash('Appointment status updated successfully!', 'success')
    else:
        flash('Appointment not found!', 'error')

    return redirect(url_for('setdate'))


@app.route('/display_confirmed_data')
def display_confirmed_data():
    hospital_id = session['hospital_id']
    confirmed_records = BookAppointment.query.filter_by(hospital_id=hospital_id, status='Approved').all()
    return render_template('hospitalappo.html', approved_records=confirmed_records)


@app.route('/displaydata')
def displaydata():
    user_id = session.get('user_id')  # Replace 'user_id' with the key you use to store the user ID in the session

    statuses_to_include = ['Approved', 'Vaccination-Started', 'Vaccination-Completed', 'Report-Uploaded']
    approved_records = BookAppointment.query.filter(
        BookAppointment.user_id == user_id,
        BookAppointment.status.in_(statuses_to_include)
    ).all()

    return render_template('dateofappo.html', approved_records=approved_records)


if __name__ == '__main__':

    app.run()
