CSRF_ENABLED = True
SECRET_KEY = 'Glavnoe - eto funk v dushe, rebyata'

import os
basedir = os.path.abspath(os.path.dirname(__file__) + '/')
db_dir = os.path.abspath(os.path.join(basedir, 'app.db'))


if 'DATABASE_URL' in os.environ:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
else:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_dir
SQLALCHEMY_TRACK_MODIFICATIONS = False