import datetime
from app.api.v1.database import DatabaseConnection


db = DatabaseConnection()


class Account:
    """This class holds the logic for managing accounts"""

    def __init__(self, *args):
        self.name = args[0]
        self.email_address = args[1]
        self.password = args[2]
        self.account_type = args[3]
        self.created_on = datetime.datetime.utcnow()
        self.last_modified = datetime.datetime.utcnow()

    def check_user(self):
        """This checks if the user already has an account"""
        if db.select_one('users', 'email_address', self.email_address) is not None:
            return True

    def register(self):
        """This creates an account for a user"""
        db.insert_user(self.name, self.email_address, self.password, self.account_type, self.created_on,
                       self.last_modified)
        user = db.select_one('users', 'email_address', self.email_address)  # selects a specific row of the users table
        return user[1]  # picks the value in the 1st column from that row

    @staticmethod
    def check_admin(email_address):
        """This checks if user has admin rights"""
        user = db.select_one('users', 'email_address', email_address)  # selects a specific row of the users table
        return user[4]  # picks the value in 4th column of of that row

    @staticmethod
    def get_user_email_address(email_address):
        """This fetches the email_address if it exists"""
        user = db.select_one('users', 'email_address', email_address)  # selects a specific row of the users table
        if user is None:
            return None
        return user[2]  # picks the value in the 2nd column of that row

    @staticmethod
    def get_user_name(email_address):
        """This fetches the user's name"""
        user = db.select_one('users', 'email_address', email_address)  # selects a specific row of the users table
        return user[1]  # picks the value in the 1st column of that row

    @staticmethod
    def get_user_id(email_address):
        """This fetches the user's name"""
        user = db.select_one('users', 'email_address', email_address)  # selects a specific row of the users table
        return user[0]  # picks the value in the 1st column of that row

    # def promote_user(self, user_id):
    #     """
    #     This gives admin rights to a user
    #     :param user_id:
    #     :return:
    #     """
    #     for user in self.accounts:
    #         if user_id == user["user_id"]:
    #             user["account_type"] = True
    #             return user
