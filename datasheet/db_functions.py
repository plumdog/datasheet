def get_all_tables(con_str):
    special_tables = ['user', 'alembic_version']

    table_names = [{'name': r[0]} for r in run_sql('SHOW TABLES', con_str)
                   if r[0] not in special_tables]
    return table_names


def get_table_obj(con_str, table_name):
    from sqlalchemy import Table, MetaData
    meta = MetaData()
    tab = Table(table_name, meta, autoload=True, autoload_with=engine(con_str))
    return tab

def engine(connection_str):
    from sqlalchemy import create_engine
    
    return create_engine(connection_str)


def run_sql(sql, connection_str, as_text=True):
    if as_text:
        from sqlalchemy.sql import text
        sql = text(sql)

    conn = engine(connection_str).connect()
    out = conn.execute(sql)
    return out
