class Config:
    SECRET_KEY = 'your-secret-key'

    # Replace with your XAMPP MySQL credentials
    DB_USER = 'root'
    DB_PASSWORD = ''  # No password by default in XAMPP
    DB_NAME = 'rewear'
    DB_HOST = 'localhost'

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
