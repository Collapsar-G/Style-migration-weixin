class Config:
    # database
    HOSTNAME = '39.105.76.87'
    PORT = 3266
    USERNAME = 'xcx_collapsar_on'
    PASSWORD = '8iS2HCtLkTK8FjG3'
    DATABASE = 'xcx_collapsar_on'

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'asdfghjkl'


class DevelopmentConfig(Config):
    """开发者环境配置"""
    DEBUG = True
    SERVER_NAME = '127.0.0.1:3268'


class ProductionConfig(Config):
    """实际生产环境配置"""
    SERVER_NAME = '0.0.0.0:3268'


config_map = {
    'dev': DevelopmentConfig,
    'pro': ProductionConfig
}
