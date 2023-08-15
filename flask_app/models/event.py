from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

db = "event_planner"
class Event:
    def __init__(self, data):
        self.id = data['id']
        self.event_name = data['event_name']
        self.description = data['description']
        self.location = data['location']
        self.date_time = data['date_time']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None

    @classmethod
    def save(cls, data):
        query = "INSERT INTO events (event_name,description,location,date_time,user_id) VALUES (%(event_name)s,%(description)s,%(location)s,%(date_time)s,%(user_id)s);"
        return connectToMySQL(db).query_db(query,data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM events JOIN users on events.user_id = users.id;"
        results = connectToMySQL(db).query_db(query)
        events = []
        for row in results:
            event = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            event.creator = user.User(user_data)
            events.append(event)
        return events

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM events JOIN users on events.user_id = users.id WHERE events.id = %(id)s;"
        result = connectToMySQL(db).query_db(query,data)
        if not result:
            return False

        result = result[0]
        this_event = cls(result)
        user_data = {
                "id": result['users.id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "email": result['email'],
                "password": "",
                "created_at": result['users.created_at'],
                "updated_at": result['users.updated_at']
        }
        this_event.creator = user.User(user_data)
        return this_event
    

    @classmethod
    def update(cls,data):
        query = """
                UPDATE events
                SET event_name = %(event_name)s,
                description = %(description)s,
                location = %(location)s ,
                date_time = %(date_time)s,
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query,data)
    
    @classmethod
    def delete(cls,data):
        query = """
                DELETE FROM events
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query,data)
    
    @staticmethod
    def validate_event(event):
        is_valid = True

        if len(event['event_name']) < 3:
            flash("Name of event must be at least 3 characters long.")
            is_valid = False
        if len(event['description']) < 5:
            flash("Description of event must be at least 5 characters long.")
            is_valid = False
        if len(event['location']) < 5:
            flash("Location of event must be at least 5 characters long.")
        if event['date_time'] == '':
            flash("Please input a valid date.")
            is_valid = False


        return is_valid
    

    @classmethod
    def get_all_with_rsvps_count(cls):
        query = """
            SELECT e.id AS event_id, e.event_name, e.description, e.location, e.date_time, e.user_id,
                u.id AS user_id, u.first_name, u.last_name,
                COUNT(r.id) AS rsvps_count
            FROM events AS e
            JOIN users AS u ON e.user_id = u.id
            LEFT JOIN rsvp AS r ON e.id = r.event_id
            GROUP BY e.id;
        """
        results = connectToMySQL(db).query_db(query)
        events = []
        for row in results:
            event_data = {
                'id': row['event_id'],
                'event_name': row['event_name'],
                'description': row['description'],
                'location': row['location'],
                'date_time': row['date_time'],
                'user_id': row['user_id'],
                'rsvps_count': row['rsvps_count']  # Add rsvps_count to event_data
            }
            event = cls(event_data)
            event.creator = user.User(row)  # You can create a User object here
            events.append(event)
        return events