from flask_table import Col, DateCol, DatetimeCol

def data_factory(val=None, sql_type=None):
    if sql_type.startswith('INTEGER'):
        return IntegerData(val)
    elif sql_type == 'DATE':
        return DateData(val)
    elif sql_type == 'DATETIME':
        return DatetimeData(val)
    #sql_type.startswith('VARCHAR'):
    else:
        return StringData(val)

class DataType(object):
    col = Col
    val = None

    def __init__(self, val):
        self.val = val

class IntegerData(DataType):
    pass

class StringData(DataType):
    pass

class DateData(DataType):
    col = DateCol

class DatetimeData(DataType):
    col = DatetimeCol
