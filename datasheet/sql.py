def create(table_name, cols=[]):
    cols_sql = ', '.join(_cols_sql(cols))
    if cols_sql:
        cols_sql += ', '

    sql = ('CREATE TABLE {table_name} ('
           'id INTEGER NOT NULL AUTO_INCREMENT, '
           '{cols}'
           'PRIMARY KEY (id));')

    return sql.format(table_name=table_name, cols=cols_sql)


def add_cols(table_name, cols=[]):
    if not cols:
        raise ValueError('must give at leat one column')

    cols_sql = ', '.join('ADD COLUMN ' + s for s in _cols_sql(cols))
    return 'ALTER TABLE {table_name} {cols}'.format(
        table_name=table_name, cols=cols_sql)


def _cols_sql(cols):
    col_sqls = []
    for name, col in cols:
        col_sqls.append(col.sql_init(name))
    return col_sqls
