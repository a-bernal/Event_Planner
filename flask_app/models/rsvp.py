from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

db = "event_planner"

class RSVP:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.event_id = data['event_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO rsvp (user_id, event_id) VALUES (%(user_id)s, %(event_id)s);"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_by_user_event(cls, data):
        query = "SELECT * FROM rsvp WHERE user_id = %(user_id)s AND event_id = %(event_id)s;"
        results = connectToMySQL(db).query_db(query, data)
        if not results:
            return None
        return cls(results[0])

    @classmethod
    def remove(cls, data):
        query = "DELETE FROM rsvp WHERE user_id = %(user_id)s AND event_id = %(event_id)s;"
        return connectToMySQL(db).query_db(query, data)


    @classmethod
    def get_rsvps_count_for_event(cls, event_id):
        query = "SELECT COUNT(*) AS rsvp_count FROM rsvp WHERE event_id = %(event_id)s;"
        data = {
            'event_id': event_id
        }
        result = connectToMySQL(db).query_db(query, data)
        return result[0]['rsvp_count']
    
    @classmethod
    def delete_by_event_id(cls, data):
        query = "DELETE FROM rsvp WHERE event_id = %(event_id)s;"
        return connectToMySQL(db).query_db(query, data)