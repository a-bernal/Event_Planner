from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.event import Event
from flask_app.models.rsvp import RSVP

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('login_and_registration.html')

@app.route('/register',methods=['POST'])
def register():

    if not User.validate_registration(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id

    return redirect('/dashboard')


@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email","login") # passing category_filter since we have to separate forms in one single html file
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login") # passing category_filter since we have to separate forms in one single html file
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')

    user_id = session['user_id']
    user = User.get_by_id({'id': user_id})
    events = Event.get_all()
    
    for event in events:
        event.rsvps_count = RSVP.get_rsvps_count_for_event(event.id)  # Get the RSVP count for each event

    return render_template('dashboard.html', user=user, events=events)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')