from flask_app.config.mysqlconnection import connectToMySQL
import pprint
from flask import flash

db = "class_hobbies"

class Hobby:
    def __init__(self,data):
        self.id=  data['id']
        self.exp_level = data['exp_level']
        self.activity = data['activity']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at'] 
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO hobbies (activity,exp_level,user_id) VALUES (%(activity)s, %(exp_level)s, %(user_id)s)" 
        return connectToMySQL(db).query_db(query,data)

    @staticmethod
    def hobby_validator(hobby):
        is_valid = True

        if len(hobby['activity']) < 2:
            flash('Your hobby needs to be at least 2 characters long')
            is_valid = False

        if hobby['exp_level'] == 'newb' or hobby['exp_level'] == 'experienced' or hobby['exp_level'] == 'pro':
            pass
        else:
            flash('expereince level should be one of the dropdown options')
            is_valid = False

        return is_valid
