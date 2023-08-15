from flask_app import app
from flask import render_template, redirect, request, session, send_from_directory, flash
from flask_app.models.event import Event
from flask_app.models.user import User
from flask_app.models.rsvp import RSVP


@app.route('/events/new')
def create_event():
    if 'user_id' not in session:
        return redirect('/dasboard')

    return render_template('new_event.html')

@app.route('/events/new/process', methods=['POST'])
def process_event():
    if 'user_id' not in session:
        return redirect('/dasboard')
    if not Event.validate_event(request.form):
        return redirect('/events/new')
    

    data = {
        'user_id': session['user_id'],
        'event_name': request.form['event_name'],
        'description': request.form['description'],
        'location': request.form['location'],
        'date_time': request.form['date_time'],
    }

    Event.save(data)
    return redirect('/dashboard')


@app.route('/events/<int:event_id>', methods=['GET', 'POST'])
def view_event(event_id):
    if 'user_id' not in session:
        return redirect('/logout')

    user_id = session['user_id']
    event = Event.get_by_id({'id': event_id})
    user = User.get_by_id({'id': user_id})
    rsvps_count = RSVP.get_rsvps_count_for_event(event_id)  # Get the RSVP count for the event

    if request.method == 'POST':
        if 'rsvp' in request.form:
            rsvp_data = {
                'user_id': user_id,
                'event_id': event_id
            }
            existing_rsvp = RSVP.get_by_user_event(rsvp_data)
            if existing_rsvp:
                flash('You have already RSVPed to this event.', 'info')
            else:
                RSVP.save(rsvp_data)
                flash('RSVP successful!', 'success')

    return render_template('view_event.html', event=event, user=user, rsvps_count=rsvps_count)


@app.route('/events/delete/<int:id>')
def delete_event(id):
    if 'user_id' not in session:
        return redirect('/logout')
    
    RSVP.delete_by_event_id({'event_id': id})  # Delete associated RSVPs
    Event.delete({'id': id})  # Now you can safely delete the event
    return redirect('/dashboard')

