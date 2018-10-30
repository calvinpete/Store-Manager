import re
from app.api.v1.database import DatabaseConnection


db = DatabaseConnection()


class UserValidator:
    """This holds methods for handling attribute validation and input validations"""
    def __init__(self, email_address, password):
        self.email_address = email_address
        self.password = password

    def check_password(self):
        """This checks if the password exists"""
        if db.select_one('users', 'password', self.password) is not None:
            return True

    def validate_email_address(self):
        """This checks for validity of the email address"""
        email = re.compile("(^[a-zA-Z0-9_-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        match = email.match(self.email_address)
        if match:
            return True
        else:
            return False

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
    def check_string_input(**kwargs):
        """
        This checks if the parameters are not strings
        :param kwargs:
        :return:
        """
        for (k, v) in kwargs.items():
            if isinstance(v, int) or isinstance(v, float) or isinstance(v, list):
                return True

    @staticmethod
    def check_integer_input(**kwargs):
        """
        This checks if the parameters are not integers
        :param kwargs:
        :return:
        """
        for (k, v) in kwargs.items():
            if isinstance(v, str) or isinstance(v, float) or isinstance(v, list):
                return True

    class ProductValidator:
        """This holds methods for handling attribute validation and input validations"""
        pass

    class SaleRecordValidator:
        pass
