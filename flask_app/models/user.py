from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User():
    db_name = "DevOnDeck_schema"
    def __init__(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.passord = data['password']
        self.address = data['address']
        self.city = data['city']
        self.state = data['state']
        self.user_id = data['user_id']
        self.file_path = data['file_path']
        self.skill_id = data['skill_id']

    @classmethod
    def create_dev(cls, data):
        query = "INSERT INTO developers (first_name, last_name, email, password, address, city, state) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(address)s, %(city)s, %(state)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def getUserEmail(cls):
        query = "SELECT email FROM developers;"
        result = connectToMySQL(cls.db_name).query_db(query)
        return result
    
    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM developers WHERE email = %(email)s"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if len(result) < 1:
            return False
        return result[0]
    
    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM developers WHERE id = %(dev_id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result == False:
            return False
        return result[0]
    
    @classmethod
    def add_profile_pic(cls, data):
        query = "UPDATE developers SET profile_pic = %(file_path)s WHERE id = %(dev_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_all_frameworks(cls):
        query = "SELECT * FROM frameworks"
        result = connectToMySQL(cls.db_name).query_db(query)
        frameworks = []
        for row in result:
            frameworks.append(row)
        return frameworks

    @classmethod
    def get_all_skills(cls):
        query = "SELECT * FROM skills"
        result = connectToMySQL(cls.db_name).query_db(query)
        skills = []
        for row in result:
            skills.append(row)
        return skills
    
    @classmethod
    def add_skill(cls, data):
        query = "INSERT INTO skills_of_developers(skill_id, developer_id) VALUES (%(skill_id)s, %(dev_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def add_frame(cls, data):
        query = "INSERT INTO frameworks_of_developers(framework_id, developer_id) VALUES (%(frame_id)s, %(dev_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_dev_skills(cls, data):
        query = "SELECT skills.id, skills.skill, skills.icon FROM skills LEFT JOIN skills_of_developers ON skills_of_developers.skill_id = skills.id WHERE skills_of_developers.developer_id = %(dev_id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        skills = []
        for row in result:
            skills.append(row)
        return skills
    
    @classmethod
    def get_dev_frameworks(cls, data):
        query = "SELECT frameworks.id, frameworks.framework, frameworks.icon FROM frameworks LEFT JOIN frameworks_of_developers ON frameworks_of_developers.framework_id = frameworks.id WHERE frameworks_of_developers.developer_id = %(dev_id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        frameworks = []
        for row in result:
            frameworks.append(row)
        return frameworks
    
    @classmethod
    def update_user(cls, data):
        query = "UPDATE developers SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, password = %(password)s WHERE id = %(dev_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_all_devs(cls):
        query = "SELECT * FROM developers;"
        result = connectToMySQL(cls.db_name).query_db(query)
        all_devs = []
        for row in result:
            all_devs.append(row)
        return all_devs
    
    @classmethod
    def get_skills(cls):
        query = "SELECT skills.id, skills_of_developers.developer_id, skills.skill, skills.icon FROM skills LEFT JOIN skills_of_developers ON skills_of_developers.skill_id = skills.id;"
        result = connectToMySQL(cls.db_name).query_db(query)
        skills = []
        for row in result:
            skills.append(row)
        return skills
    
    @classmethod
    def get_frameworks(cls):
        query = "SELECT frameworks.id, frameworks_of_developers.developer_id, frameworks.framework, frameworks.icon FROM frameworks LEFT JOIN frameworks_of_developers ON frameworks_of_developers.framework_id = frameworks.id;"
        result = connectToMySQL(cls.db_name).query_db(query)
        frameworks = []
        for row in result:
            frameworks.append(row)
        return frameworks
    
    @classmethod
    def apply(cls, data):
        query = "INSERT INTO applications (position_id, developer_id, organization_id) VALUES(%(pos_id)s, %(dev_id)s, %(org_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_pos_applied(cls, data):
        query = "SELECT applications.position_id, applications.status FROM applications LEFT JOIN developers on applications.developer_id = developers.id WHERE applications.developer_id = %(dev_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        applied_pos = []
        for row in results:
            applied_pos.append(row)
        return applied_pos

    @classmethod
    def get_all_pos_applied(cls, data):
        query = "SELECT * FROM applications WHERE organization_id = %(org_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        # applied_pos = []
        # for row in results:
        #     applied_pos.append(row)
        return results

    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM developers;"
        return connectToMySQL(cls.db_name).query_db(query)