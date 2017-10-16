from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
NAMESPACE = 'inv'

app = Flask(__name__)

app.config['SECRET_KEY'] = '123456790'
app.config['DATABASE_FILE'] = 's0inv.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
# Please use your own salt for productive use!
app.config['SECURITY_PASSWORD_SALT'] = "eph4OoGh Oochiel4"

db = SQLAlchemy(app)
from flask_admin import Admin
admin = Admin(app, name='s0inv', template_mode='bootstrap3', url='/'+NAMESPACE)

from app import models,views, modelviews
# Setup Flask-Security
from flask_security import Security, SQLAlchemyUserDatastore, current_user
user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore)
modelviews.__init__()

def build_sample_db():
    db.drop_all()
    db.create_all()

app_dir = os.path.realpath(os.path.dirname(__file__))
database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
if not os.path.exists(database_path):
    build_sample_db()
