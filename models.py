from datetime import datetime

from flask import redirect
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.model.template import LinkRowAction
from flask_admin.actions import action

import inventory_labels
#from security import AuthenticatedModelView

def init(app, db, admin):
    class Project(db.Model):
        name = db.Column(db.String(100), primary_key=True)
        wikipage = db.Column(db.String(100))
        logourl = db.Column(db.String(256))

        def __str__(self):
            return self.name

    class ProjectView(ModelView):
        column_display_pk = True
        form_columns = ['name', 'wikipage', 'logourl']

    class Item(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        manufacturer = db.Column(db.String(100))
        product = db.Column(db.String(100))
        serial = db.Column(db.String(100))
        project_name = db.Column(db.String(100), db.ForeignKey('project.name'))
        project = db.relationship('Project', backref='project')
        notes = db.Column(db.Text)
        location = db.Column(db.String(1024))
        user = db.Column(db.String(1024))
        responsible = db.Column(db.String(1024))
        changes = db.relationship('Change', backref='item')

        def __str__(self):
            return "[{}] {} {}".format(self.id, self.manufacturer, self.product)

    inventory_labels.Item = Item
    inventory_labels.Project = Project


    class ItemView(ModelView):
        column_display_pk = True
        form_columns = ['manufacturer', 'product', 'serial', 'location', 'user', 'responsible', 'notes', 'project']
        can_view_details = True
        details_template = 'details.html'
        column_searchable_list = ('manufacturer', 'product', 'serial')
        #column_filters = ('project',)
        column_extra_row_actions = [LinkRowAction('glyphicon glyphicon-tag', '/label?ids={row_id}')]

        def on_model_change(self, form, model, is_created):
            if not is_created:
                changed_cols = [col for col in self.form_columns \
                       if getattr(form, col).data != getattr(form, col).object_data]
                for col in changed_cols:
                    c = Change()
                    c.user = 'Kasa'
                    c.field = col
                    c.item_id = model.id
                    c.new_value = str(getattr(form, col).data)
                    c.datetime = datetime.now().replace(microsecond=0)
                    db.session.add(c)
                    db.session.commit()

        @action('get labels', 'get Labels', None)
        def get_labels(self, ids):
            return redirect('/label?ids='+','.join(ids))

    class Change(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user = db.Column(db.String(30))
        field = db.Column(db.String(256))
        item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
        new_value = db.Column(db.Text)
        datetime = db.Column(db.DateTime)

        def __str__(self):
            return "{}: {} changed {} to '{}' on {}".format(self.datetime, self.user, self.field, self.new_value, str(self.item))

    class DetailView(BaseView):
        @expose('/')
        def index(self):
            return self.render('details.html')

    admin.add_view(ItemView(Item, db.session))
    admin.add_view(ProjectView(Project, db.session))

