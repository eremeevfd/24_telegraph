CSRF_ENABLED = True
SECRET_KEY = 'Glavnoe - eto funk v dushe, rebyata'

import os
basedir = os.path.abspath(os.path.dirname(__file__) + '/')
db_dir = os.path.abspath(os.path.join(basedir, 'app.db'))

# SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_dir
# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False