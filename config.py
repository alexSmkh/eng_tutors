import os


base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        f'sqlite:///{os.path.join(base_dir, "app.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

