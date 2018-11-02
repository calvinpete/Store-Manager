import os


class Config(object):
    """Parent configuration class"""
    SECRET_KEY = os.getenv('SECRET')
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """Configurations for Development"""
    DEBUG = True
    DATABASE_URL = os.getenv('DATABASE_URL')


class TestingConfig(Config):
    """Configurations for Testing"""
    TESTING = True
    DEBUG = True
    DATABASE_URL = "postgresql://calvin:310892@127.0.0.1:5432/storemanagertestdb"


class ProductionConfig(Config):
    """Configurations for Production"""
    pass


app_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}
