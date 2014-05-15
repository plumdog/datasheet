from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import Required


class LoginForm(Form):
    username = StringField('Username', [Required()])
    password = PasswordField('Password', [Required()])


def form_factory(cols):
    class F(Form):
        pass

    for name, c in cols:
        setattr(F, name, c.field(name.title()))

    return F
