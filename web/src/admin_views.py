from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm


class SecureFormAdminView(ModelView):
    form_base_class = SecureForm
    form_excluded_columns = ('vote', 'votes_set', 'has_voted', 'num_of_votes')


class VoteAdminView(SecureFormAdminView):
    can_edit = False
    can_create = False
    can_delete = False