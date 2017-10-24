from flask_security.forms import RegisterForm, LoginForm, Required, Form, NextFormMixin
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from flask import request, current_app
from app import models, db
from flask_security.utils import verify_and_update_password
from flask_security.confirmable import requires_confirmation

class ExtendedRegisterForm(RegisterForm):
    username = StringField('Username', [Required()])

class LoginForm(Form, NextFormMixin):

    username = StringField('Username',
                        validators=[Required(message='EMAIL_NOT_PROVIDED')])
    password = PasswordField('Password',
                             validators=[Required()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Log In")

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        if not self.next.data:
            self.next.data = request.args.get('next', '')
        self.remember.default = True
        if current_app.extensions['security'].recoverable and \
                not self.password.description:
            html = Markup(u'<a href="{url}">{message}</a>'.format(
                url=url_for_security("forgot_password"),
                message=get_message("FORGOT_PASSWORD")[0],
            ))
            self.password.description = html

    def validate(self):
        if not super(LoginForm, self).validate():
            return False

        # self.user = _datastore.get_user(self.username.data)
        self.user = models.User.query.filter(models.User.username == self.username.data).first()

        if self.user is None:
            self.username.errors.append(get_message('USER_DOES_NOT_EXIST')[0])
            # Reduce timing variation between existing and non-existung users
            hash_password(self.password.data)
            return False
        if not self.user.password:
            self.password.errors.append(get_message('PASSWORD_NOT_SET')[0])
            # Reduce timing variation between existing and non-existung users
            hash_password(self.password.data)
            return False
        if not verify_and_update_password(self.password.data, self.user):
            self.password.errors.append(get_message('INVALID_PASSWORD')[0])
            return False
        if requires_confirmation(self.user):
            self.username.errors.append(get_message('CONFIRMATION_REQUIRED')[0])
            return False
        if not self.user.is_active:
            self.username.errors.append(get_message('DISABLED_ACCOUNT')[0])
            return False
        return True
