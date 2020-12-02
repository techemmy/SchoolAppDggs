import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY') or "b'G\xfb\x12[\xad\x89\xe5Wt\xf4\xf7\xc1\nV|\x19"
    MAIL_SERVER = os.getenv('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = os.getenv('MAIL_PORT', 465)
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'true').lower() in \
                   ['true', 'on', '1']
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TESTING_DATABASE_URL') or \
        'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
