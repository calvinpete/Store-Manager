class Config(object):
    """Parent configuration class"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = "VeryHardThoughtKey"


class DevelopmentConfig(Config):
    """Configurations for Development"""
    ENV = "development"
    DEBUG = True
    DATABASE_URL = "postgresql://postgres:hs@127.0.0.1:5432/storemanager"


class TestingConfig(Config):
    """Configurations for Testing"""
    ENV = "testing"
    TESTING = True
    DEBUG = True
    DATABASE_URL = "postgresql://postgres:hs@127.0.0.1:5432/storemanagertestdb"


class ProductionConfig(Config):
    """Configurations for Production"""
    ENV = "production"
    DEBUG = False
    DATABASE_URL = "postgreasql://qibiumajgxukme:8cc471c6ed5a6586e9750db34d6d7cbc2fdf06c07d4028c8c62710030cb470a4" \
                   "@ec2-75-101-153-56.compute-1.amazonaws.com:5432/de9iiq47q0aub0"


app_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}
