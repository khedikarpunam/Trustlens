import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'trust-lens-super-secret-key-2024-xk9z')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database', 'trust_lens.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024   # 16 MB
    DATA_FOLDER = os.path.join(basedir, 'data')
    ALLOWED_EXTENSIONS = {'pdf', 'txt'}
