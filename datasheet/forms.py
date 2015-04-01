from flask.ext.wtf import Form
from wtforms import (StringField, PasswordField, TextAreaField, SelectField,
                     DateField, IntegerField, DateTimeField)
from wtforms.validators import Required




class DSDateField(DateField):
    def __init__(self, *args, **kwargs):
        kwargs['format'] = kwargs.get('format', '%d/%m/%Y')
        kwargs['description'] = kwargs.get('description', 'dd/mm/yyyy')
        DateField.__init__(self, *args, **kwargs)


class DSDateTimeField(DateField):
    def __init__(self, *args, **kwargs):
        kwargs['format'] = kwargs.get('format', '%d/%m/%Y %H:%M')
        kwargs['description'] = kwargs.get('description', 'dd/mm/yyyy hh:mm')
        DateTimeField.__init__(self, *args, **kwargs)


class LoginForm(Form):
    username = StringField('Username', [Required()])
    password = PasswordField('Password', [Required()])


class TableForm(Form):
    name = StringField('Name', [Required()])


class ColumnForm(Form):
    name = StringField('Name', [Required()])
    data_type = SelectField('Data Type')

    def __init__(self, *args, **kwargs):
        from .data_types import data_types
        self.data_types.choices = [(d, d) for d in data_types]

def form_factory(cols):
    class F(Form):
        pass

    for name, c in cols:
        setattr(F, name, c.field(name.title()))

    return F
