class Config(object):
    """Parent configuration class"""
    SECRET_KEY = "VeryHardThoughtKey"
    DEBUG = False


class DevelopmentConfig(Config):
    """Configurations for Development"""
    DEBUG = True
    DATABASE_URL = "postgresql://calvin:310892@127.0.0.1:5432/storemanager"


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
