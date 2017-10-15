from flask import Flask, redirect, request, send_from_directory
from app import app, inventory_labels,db
from flask_security import Security, login_required, login_user, logout_user, current_user


@app.route("/")
@login_required
def app_index():
    return redirect("/admin")

@app.route("/<int:item_id>")
@login_required
def app_item(item_id):
    return redirect('/'+NAMESPACE+'/item/details?id='+str(item_id))

@app.route("/label")
@login_required
def app_label():
    ids = request.args.get('ids', None)
    if ids:
        filename = inventory_labels.create_pdf(db, ids.split(','))
        return send_from_directory('../tmp', filename)
    else:
        return "missing parameter: ids"
