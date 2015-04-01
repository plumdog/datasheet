from flask_table import Col, DateCol, DatetimeCol
from .forms import (StringField, DSDateField as DateField,
                    DSDateTimeField as DateTimeField, IntegerField)

def str_data_factory(name):
    return data_types[name.lower()]


def data_factory(val=None, sql_type=None):
    if sql_type.startswith('INTEGER'):
        return IntegerData(val)
    elif sql_type == 'DATE':
        return DateData(val)
    elif sql_type == 'DATETIME':
        return DatetimeData(val)
    else:
        return StringData(val)


class DataType(object):
    col = Col
    field = StringField
    val = None

    def __init__(self, val):
        self.val = val

    @classmethod
    def sql_init(cls, name):
        return cls.sql % ('`' + name + '`')


class IntegerData(DataType):
    field = IntegerField
    sql = '%s INT'


class StringData(DataType):
    sql = '%s VARCHAR(255)'


class DateData(DataType):
    col = DateCol
    field = DateField
    sql = '%s DATE'


class DatetimeData(DataType):
    col = DatetimeCol
    field = DateTimeField
    sql = '%s DATETIME'


data_types = {'integer': IntegerData,
              'string': StringData,
              'date': DateData,
              'datetime': DatetimeData}
