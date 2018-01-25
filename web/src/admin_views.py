from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm
from flask.ext import admin, login

class SecureFormAdminView(ModelView):
    form_base_class = SecureForm
    form_excluded_columns = ('vote', 'votes_set', 'has_voted', 'num_of_votes')

    def is_accessible(self):
        return login.current_user.is_authenticated


class VoteAdminView(SecureFormAdminView):
    can_edit = False
    can_create = False
    can_delete = False

    def is_accessible(self):
        return login.current_user.is_authenticated