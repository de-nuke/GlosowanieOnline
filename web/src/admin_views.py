from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm
from flask.ext import admin, login
from app import db
from models import USER_HASHED_FIELDS
import sys
import hashlib

class SecureFormAdminView(ModelView):
    form_base_class = SecureForm
    column_exclude_list = ['num_of_votes']
    form_excluded_columns = ('vote', 'votes_set', 'has_voted', 'num_of_votes')
    extra_js = ['/src/static/js/readonly.js']

    @property
    def column_formatters(self):
        result = {}
        for hf in USER_HASHED_FIELDS:
            result[hf] = lambda v, c, m, p: '[HASHED] ' + str(getattr(m, hf))[:20]+'...'
        return result

    def is_accessible(self):
        return login.current_user.is_authenticated



    def after_model_change(self, form, model, is_created):
        if model.__class__.__name__ is 'User':
            if is_created:
                for hf in USER_HASHED_FIELDS:
                    print(hf)
                    sys.stdout.flush()
                    setattr(model, hf, hashlib.sha256(getattr(model, hf).encode("utf-8")).hexdigest())
                db.session.commit()





class VoteAdminView(SecureFormAdminView):
    can_edit = False
    can_create = False
    can_delete = False

    def is_accessible(self):
        return login.current_user.is_authenticated