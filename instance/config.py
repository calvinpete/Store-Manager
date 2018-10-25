class Config(object):
    """Parent configuration class"""
    SECRET_KEY = "VeryHardThoughtKey"
    DEBUG = False


class DevelopmentConfig(Config):
    """Configurations for Development"""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing"""
    TESTING = True
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production"""
    pass


app_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}
