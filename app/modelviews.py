from flask_admin.contrib.sqla import ModelView
from flask_admin.model.template import LinkRowAction
from flask_admin.actions import action
from flask_admin import BaseView, expose
from flask_security import current_user
from app import admin, models, db

class ProjectView(ModelView):
    column_display_pk = True
    form_columns = ['name', 'wikipage', 'logourl']
    def is_accessible(self):
        if current_user.is_authenticated:
            return True
        else:
            return False

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
    def is_accessible(self):
        if current_user.is_authenticated:
            return True
        else:
            return False

class DetailView(BaseView):
    @expose('/')
    def index(self):
        return self.render('details.html')
    def is_accessible(self):
        if current_user.is_authenticated:
            return True
        else:
            return False

class UserView(ModelView):
    can_create = False
    can_edit = False
    can_delete = False
    column_exclude_list = ['password','confirmed_at','active', ]
    # column_searchable_list = ['name', 'email']
    def is_accessible(self):
        if current_user.is_authenticated:
            return True
        else:
            return False


def __init__():
    admin.add_view(ItemView(models.Item, db.session))
    admin.add_view(ProjectView(models.Project, db.session))
    admin.add_view(UserView(models.User, db.session))
