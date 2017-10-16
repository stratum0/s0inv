import os

from flask import Flask, redirect, request, send_from_directory
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy

import inventory_labels
import models
import security

NAMESPACE = 'inv'

app = Flask(__name__)

app.config['SECRET_KEY'] = '123456790'
app.config['DATABASE_FILE'] = 's0inv.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

admin = Admin(app, name='s0inv', template_mode='bootstrap3', url='/'+NAMESPACE)
security.init(app, db, admin)
models.init(app, db, admin)

def build_sample_db():
    db.drop_all()
    db.create_all()

app_dir = os.path.realpath(os.path.dirname(__file__))
database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
if not os.path.exists(database_path):
    build_sample_db()


@app.route("/")
def app_index():
    return redirect('/'+NAMESPACE+'/')

@app.route("/<int:item_id>")
def app_item(item_id):
    return redirect('/'+NAMESPACE+'/item/details?id='+str(item_id))

@app.route("/label")
def app_label():
    ids = request.args.get('ids', None)
    if ids:
        filename = inventory_labels.create_pdf(db, ids.split(','))
        return send_from_directory('tmp', filename)
    else:
        return "missing parameter: ids"

app.run()
