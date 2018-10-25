import re


class Account:
    """This class holds the logic for managing accounts"""

    def __init__(self):
        self.accounts = []  # A data structure to hold admin and user accounts

    def check_user(self, email_address):
        """
        This checks if the user already has an account
        :param email_address:
        :return:
        """
        for account in self.accounts:
            # checks if the user is registered
            if email_address == account["email_address"]:
                return True

    def register(self, name, email_address, password, admin=False):
        """
        This creates an account for a user
        :param admin:
        :param name:
        :param email_address:
        :param password:
        :return:
        """
        user_id = len(self.accounts) + 1
        user = {
            "name": name,
            "email_address": email_address,
            "user_id": user_id,
            "password": password,
            "admin": admin
        }
        self.accounts.append(user)
        return self.accounts

    @staticmethod
    def check_input_validity(**kwargs):
        """
        This checks if the parameters are empty
        :param kwargs:
        :return:
        """
        for (k, v) in kwargs.items():
            if len(v) == 0 or v.isspace():
                return True

    @staticmethod
    def check_input_type(**kwargs):
        """
        This checks if the parameters are not strings
        :param kwargs:
        :return:
        """
        for (k, v) in kwargs.items():
            if isinstance(v, int) or isinstance(v, float) or isinstance(v, list):
                return True

    def get_user(self, email_address):
        """
        This fetches the email_address if it exists
        :param email_address:
        :return:
        """
        for account in self.accounts:
            # checks if the user is registered
            if email_address == account["email_address"]:
                return account["user_id"]

    def get_user_name(self, user_id):
        """
        This fetches the user's name
        :param user_id:
        :return:
        """
        for attendant in self.accounts:
            if user_id == attendant["user_id"]:
                return attendant["name"]

    def check_admin(self, user_id):
        """
        This checks if user has admin rights
        :param user_id:
        :return:
        """
        for user in self.accounts:
            if user_id == user["user_id"]:
                return user["admin"]

    def check_password(self, password):
        """
        This checks if the password exists
        :param password:
        :return:
        """
        for account in self.accounts:
            # checks if the user has entered his/her password
            if password == account["password"]:
                return True

    def promote_user(self, user_id):
        """
        This gives admin rights to a user
        :param user_id:
        :return:
        """
        for user in self.accounts:
            if user_id == user["user_id"]:
                user["admin"] = True
                return user

    @staticmethod
    def validate_email_address(email_address):
        """
        This checks for validity of the email address
        :param email_address:
        :return:
        """
        email = re.compile("(^[a-zA-Z0-9_-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        match = email.match(email_address)
        if match:
            return True
        else:
            return False


staff = Account()
