import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'eBL0S*wmc2mg?.&;R-7=Z@J+fI)4=QQYu`:}qMA#e>3<R9"[VQ<>%b!1?J!jwD,'
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    TOKEN_EXPIRATION = 600
    MAX_PAGE_SIZE = 100
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/bucketlist'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/bucketlist_prod'


class StagingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/bucketlist_stage'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/bucketlist_test'


configuration = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig,
    staging=StagingConfig
)
