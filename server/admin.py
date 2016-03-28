from flask import url_for, request
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.login import current_user
from flask_admin import Admin

from server.application import app
from server.persistence.models import db, SocialProfile
from server.persistence.models import User, Device, Measurement
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

admin = Admin(app, name="hc-admin", template_mode="bootstrap3")


class MyModelView(ModelView):
    can_view_details = True

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('admin'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))

    def is_action_allowed(self, name):
        """
            Override this method to allow or disallow actions based
            on some condition.

            The default implementation only checks if the particular action
            is not in `action_disallowed_list`.
        """
        return name not in self.action_disallowed_list


class UserView(MyModelView):
    column_searchable_list = [User.id, User.email]


class DeviceView(MyModelView):
    column_searchable_list = [Device.id, Device.uuid, Device.ip_addr]


class MeasurementView(MyModelView):
    column_searchable_list = [Measurement.id, Measurement.timestamp]


class SocialProfileView(MyModelView):
    column_searchable_list = [SocialProfile.social_id,
                              SocialProfile.provider_name,
                              SocialProfile.nickname]

admin.add_view(UserView(User, db.session))
admin.add_view(DeviceView(Device, db.session))
admin.add_view(MeasurementView(Measurement, db.session))
