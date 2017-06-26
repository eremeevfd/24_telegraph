import os


CSRF_ENABLED = True
SECRET_KEY = 'Glavnoe - eto funk v dushe, rebyata'

basedir = os.path.abspath(os.path.dirname(__file__) + '/')
db_dir = os.path.abspath(os.path.join(basedir, 'app.db'))


SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + db_dir
SQLALCHEMY_TRACK_MODIFICATIONS = False