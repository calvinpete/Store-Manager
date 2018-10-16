import re


class Account:
    """This class holds the logic for managing accounts"""

    def __init__(self):
        self.accounts = []  # A data structure to hold admin and user accounts

    def check_user(self, username, email_address, password, phone_number):
        """
        This checks if the user already has an account
        :param username:
        :param email_address:
        :param password:
        :param phone_number
        :return:
        """
        user = {
            "username": username,
            "email_address": email_address,
            "password": password,
            "phone_number": phone_number
        }
        if user in self.accounts:
            return True

    def register(self, name, company_id, phone_number, email_address, username, password, admin=True):
        """
        This creates an account for a user
        :param admin:
        :param name:
        :param company_id:
        :param phone_number:
        :param email_address:
        :param username:
        :param password:
        :return:
        """
        user = {
            "name": name,
            "company_id": company_id,
            "phone_number": phone_number,
            "email_address": email_address,
            "username": username,
            "password": password,
            "admin": admin
        }
        self.accounts.append(user)
        return self.accounts

    def get_user(self, username):
        """
        This fetches the username if it exists
        :param username:
        :return:
        """
        for account in self.accounts:
            # checks if the user is registered
            if username == account["username"]:
                return account["username"]

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

    @staticmethod
    def validate_email_address(email_address):
        """
        This checks for validity of the email address
        :param email_address:
        :return:
        """
        email = re.compile("(^[a-zA-Z0-9_-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]$)")
        match = email.match(email_address)
        if match:
            return True
        else:
            return False
