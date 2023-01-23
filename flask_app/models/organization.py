from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Organization():
    db_name = "DevOnDeck_schema"
    def __init__(self, data):
        self.org_name = data['org_name']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.address = data['address']
        self.city = data['city']
        self.state = data['state']
        self.password = data['password']
        self.org_id = data['org_id']
        self.pos_id = data['pos_id']
        
    @classmethod
    def createOrganization(cls, data):
        query = "INSERT INTO organizations (org_name, first_name, last_name, email, address, city, state, password) VALUES(%(org_name)s, %(first_name)s, %(last_name)s, %(email)s, %(address)s, %(city)s, %(state)s, %(password)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def getOrgEmail(cls):
        query = "SELECT email FROM organizations;"
        result = connectToMySQL(cls.db_name).query_db(query)
        return result
    
    @classmethod
    def get_org_by_email(cls, data):
        query = "SELECT * FROM organizations WHERE email = %(email)s"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if len(result) < 1:
            return False
        return result[0]
    
    @classmethod
    def get_org_by_id(cls, data):
        query = "SELECT * FROM organizations WHERE id = %(org_id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result == False:
            return False
        return result[0]
    
    @classmethod
    def add_OrgProfile_pic(cls, data):
        query = "UPDATE organizations SET profile_pic = %(file_path)s WHERE id = %(org_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def create_positions(cls, data):
        query = "INSERT INTO positions (name, description, skill_1, skill_2, skill_3, skill_4, skill_5, frame_1, frame_2, frame_3, frame_4, frame_5, organization_id) VALUES (%(name)s, %(description)s, %(skill_1)s, %(skill_2)s, %(skill_3)s, %(skill_4)s, %(skill_5)s, %(frame_1)s, %(frame_2)s, %(frame_3)s,%(frame_4)s, %(frame_5)s, %(org_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_positions(cls, data):
        query = "SELECT * FROM positions WHERE organization_id = %(org_id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        positions = []
        for row in result:
            positions.append(row)
        return positions
    
    @classmethod
    def get_all_positions(cls):
        query = "SELECT * FROM positions ORDER BY created_at DESC;"
        result = connectToMySQL(cls.db_name).query_db(query)
        positions = []
        for row in result:
            positions.append(row)
        return positions
    
    @classmethod
    def get_pos_by_id(cls, data):
        query = "SELECT * FROM positions WHERE id = %(pos_id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result == False:
            return False
        return result[0]
    
    @classmethod
    def get_all_org(cls):
        query = "SELECT * FROM organizations;"
        result = connectToMySQL(cls.db_name).query_db(query)
        organisations = []
        for row in result:
            organisations.append(row)
        return organisations
    
    @classmethod
    def update_status(cls, data):
        query = "UPDATE applications SET status = %(status)s WHERE developer_id = %(dev_id)s and position_id = %(pos_id)s and organization_id = %(org_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def create_communications(cls, data):
        query = "INSERT INTO communications (developer_id, organization_id) VALUES (%(dev_id)s, %(org_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_communications(cls, data):
        query = "SELECT * FROM communications WHERE developer_id = %(dev_id)s AND organization_id = %(org_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def send_message(cls, data):
        query = "INSERT INTO messages (communication_id, sender, receiver, message) VALUES (%(communication_id)s, %(sender)s, %(receiver)s, %(message)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_messages(cls, data):
        query = "SELECT * FROM messages WHERE communication_id = %(communication_id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        messages = []
        if result:
            for row in result:
                messages.append(row)
        return messages
    
    @classmethod
    def get_user(cls, data):
        query = "SELECT * FROM developers WHERE id = %(dev_id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result == False:
            return False
        return result[0]

    @classmethod
    def get_user_communications(cls, data):
        query = "SELECT * FROM communications WHERE developer_id = %(dev_id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        communications = []
        if result != False:
            for row in result:
                communications.append(row)
        return communications